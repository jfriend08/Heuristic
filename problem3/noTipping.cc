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
#include <iostream>

using namespace std;

#define PORT "8013"  // the port users will be connecting to

#define BACKLOG 1   // how many pending connections queue will hold

void sigchld_handler(int s) {
  // waitpid() might overwrite errno, so we save and restore it:
  int saved_errno = errno;

  while(waitpid(-1, NULL, WNOHANG) > 0);

  errno = saved_errno;
}


// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa) {
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


class NoTippingPlayer {
private:
  int count;
  bool amFirstPlayer;
public:
  NoTippingPlayer(){
    count = 0;
  }
  void setFirstPlayer(){amFirstPlayer=true;}
  string letMeThink() {
    string result;
    if(count==0) {
      result = "-1 15";
    } else {
      result = "-5 1";
    }
    // cout<<"result: "<<result<<" count:"<<count<<endl;
    count++;
    return result;
  }
};

int main(void) {
  NoTippingPlayer player;
  while(1) {
    string s1, s2;
    int position, weight;
    bool iHaveDecide = false;

    cin >> s1 >> position >> weight >> s2;

    if (s1.empty()){
      continue;
    }
    // printf("s1:%s, position:%d, weight:%d\n", s1.c_str(), position, weight);
    string result = player.letMeThink();
    printf("%s\n",result.c_str());
    // cout<<result<<endl;
    // printf("%s",result.c_str());
    // while(!iHaveDecide){
    //   if (weight==0) {
    //     player.setFirstPlayer();
    //   }
    //   string result = player.letMeThink();
    //   printf("%s",result.c_str());
    //   if (!result.empty()) {
    //     // iHaveDecide = true;
    //   }
    // }


  }
  return 0;
}