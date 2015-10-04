#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>

#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <utility>
#include <math.h>
#include <cmath>
#include <string.h>
#include <string>

using namespace std;

#define PORT "8013"  // the port users will be connecting to

#define BACKLOG 1   // how many pending connections queue will hold

const int left_bound = -25;
const int right_bound = 25;
const int minWeight = 1;
const int maxWeight = 15;

void sigchld_handler(int s)
{
  // waitpid() might overwrite errno, so we save and restore it:
  int saved_errno = errno;

  while(waitpid(-1, NULL, WNOHANG) > 0);

  errno = saved_errno;
}


// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
  if (sa->sa_family == AF_INET) {
    return &(((struct sockaddr_in*)sa)->sin_addr);
  }

  return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

// ---------- No tipping game algorithm ----------------
string recvCmd(int fd) {
  string ret("");

  while (ret.find("STATE END") == string::npos) {
    char buff[100];
    if (recv(fd, (void*) buff, 100, 0) == -1) {
      perror("Recv Error\n");
    } else {
      ret.append(buff);
    }
  }
  ret.push_back('\0');

  return ret;
}

struct Weight {
  int position;
  int weight;
  bool mine;

  Weight(int p, int w, bool m): position(p), weight(w), mine(m) {};
  Weight(): position(0), weight(0), mine(false) {};
};

struct MoveOpt {
  int position;
  int weight;
  float prob;

  MoveOpt(int p, int w, float b): position(p), weight(w), prob(b) {};
  MoveOpt(): position(0), weight(0), prob(0.f) {};
};

bool compProb(MoveOpt *a, MoveOpt *b) {
  return a->prob < b->prob;
}

class NoTippingPlayer {
private:
  vector<Weight*> board;
  set<int> availables;
  map<int, set<int> > finalState; //Record the final state that red player is gonna lose
  bool firstPlayer;

  int getIdx(int i) {
    return 25 + i;
  }

  bool isTipping() {
    int left_torq = 0;
    int right_torq = 0;
    for (int p = 0; p < board.size(); p++) {
      left_torq -= (board[p]->position - (-3)) * board[p]->weight;
      right_torq -= (board[p]->position - (-1)) * board[p]->weight;

      left_torq += (board[p]->position - (-3)) * -1*board[p]->weight;
      right_torq += (board[p]->position - (-1)) * -1*board[p]->weight;
    }

    return left_torq > 0 || right_torq < 0;
  }

  string firstPlayerAddWeight() {
    string ret("");

    for (set<int>::reverse_iterator available = availables.rbegin(); available != availables.rend(); available++) {
      for (map<int, set<int> >::iterator state = finalState.begin(); state != finalState.end(); state++) {
        if (board[getIdx(state->first)]->weight)  continue;

        Weight *nowPos = board[getIdx(state->first)];
        for (set<int>::iterator it = state->second.begin(); it != state->second.end(); it++) {
          nowPos->weight = *it;
          if (isTipping()) {
            continue;
          }
        }
      }
    }

    return string("");
  }

  string secondPlayerAddWeight() {
    return string("");
  }

  string addWeight() {
    return firstPlayer ? firstPlayerAddWeight() : secondPlayerAddWeight();
  }

  string firstPlayerRemoveWeight() {
    return string("");
  }

  string secondPlayerRemoveWeight() {
    return string("");
  }

  string removeWeight() {
    return firstPlayer ? firstPlayerRemoveWeight() : secondPlayerRemoveWeight();
  }

public:
  NoTippingPlayer() {
    for (int p = left_bound; p <= right_bound; p++) {
      board.push_back(new Weight(p, 0, false));
    }
    board[getIdx(-4)]->weight = 3;
    firstPlayer = false;

    //Initialize the final states
    for (int p = left_bound; p <= right_bound; p++) {
      set<int> final;
      for (int w = minWeight; w <= maxWeight; w++) {
        int tmp = board[getIdx(p)]->weight;
        board[getIdx(p)]->weight = w;
        if (!isTipping()) {
          final.insert(w);
        }
        board[getIdx(p)]->weight = tmp;
      }
      if (final.size()) {
        finalState[p] = final;
      }
    }

    for (int i = minWeight; i <= maxWeight; availables.insert(i++)) ;
  }

  void setFirstPlayer() {
    firstPlayer = true;
  }

  string nextMove(bool adding, int position, int weight) {
    //Update state

    if (isTipping()) {
      return string("");
    }

    delete board[position];
    board[position] = new Weight(position, weight, false);
    
    return adding ? addWeight() : removeWeight();
  }
};

// ------------ Main ------------------------------------

int main(void)
{
  int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
  struct addrinfo hints, *servinfo, *p;
  struct sockaddr_storage their_addr; // connector's address information
  socklen_t sin_size;
  struct sigaction sa;
  int yes=1;
  char s[INET6_ADDRSTRLEN];
  int rv;

  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE; // use my IP

  if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
    return 1;
  }

  // loop through all the results and bind to the first we can
  for(p = servinfo; p != NULL; p = p->ai_next) {
    if ((sockfd = socket(p->ai_family, p->ai_socktype,
        p->ai_protocol)) == -1) {
      perror("server: socket");
      continue;
    }

    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
        sizeof(int)) == -1) {
      perror("setsockopt");
      exit(1);
    }

    if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
      close(sockfd);
      perror("server: bind");
      continue;
    }

    break;
  }

  freeaddrinfo(servinfo); // all done with this structure

  if (p == NULL)  {
    fprintf(stderr, "server: failed to bind\n");
    exit(1);
  }

  if (listen(sockfd, BACKLOG) == -1) {
    perror("listen");
    exit(1);
  }

  sa.sa_handler = sigchld_handler; // reap all dead processes
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = SA_RESTART;
  if (sigaction(SIGCHLD, &sa, NULL) == -1) {
    perror("sigaction");
    exit(1);
  }

  NoTippingPlayer player;

  printf("server: waiting for connections...\n");

  while(1) {  // main accept() loop
    sin_size = sizeof their_addr;
    new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
    if (new_fd == -1) {
      perror("accept");
      continue;
    }

    inet_ntop(their_addr.ss_family,
      get_in_addr((struct sockaddr *)&their_addr),
      s, sizeof s);
    printf("server: got connection from %s\n", s);

    string buff = recvCmd(new_fd);
    char cmd[10];
    int pos, weight;
    sscanf(buff.c_str(), "%s %d %d", cmd, &pos, &weight);
    //TODO: Entry point to player
    //TODO: set first player or not

    if (!fork()) { // this is the child process
      close(sockfd); // child doesn't need the listener
      if (send(new_fd, "Hello, world!", 13, 0) == -1)
        perror("send");
      close(new_fd);
      exit(0);
    }
    close(new_fd);  // parent doesn't need this
  }

  return 0;
}