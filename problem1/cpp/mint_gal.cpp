#include <iostream>
#include <vector>
#include <set>
#include <float.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <algorithm>
#include <limits>

using namespace std;

float exactScore(set<int> denoms, void* obj);
float exchangeScore(set<int> denoms, void* obj);

class Solution {
private:
  int numDoms;
  float bestScore;
  set<int> bestDenoms;
  int numTry;
  float (*getScore)(set<int>, void*);

  template<typename P> struct Cmp {
    bool operator()(const P &p1, const P &p2) {
      return p1.first < p2.first;
    }
  };
public:
  float N; //Assigned value
  int maxVal;
  Solution(float n, int questionNum) : N(n), maxVal(239), numDoms(7), bestScore(FLT_MAX), numTry(7) {
    if (questionNum == 1) {
      getScore = &exactScore;
    } else {
      getScore = &exchangeScore;
    }
  }

  void printSet(set<int> input) {
    set<int>::iterator it;
    for (it = input.begin(); it != input.end(); it++) {
      cout << *it << " ";
    }
  }

  bool isContained(set<int> input, int x) {
    return input.count(x) != 0;
  }

  vector<pair<float, int> > getTheTopTries(set<int> denoms, float currScore) {
    vector<pair<float, int> > rankList;

    for (int i=1; i < maxVal/2; i++) {
      int newDenom = i+1;
      if (isContained(bestDenoms, newDenom) || isContained(denoms, newDenom)) {
        continue;
      }

      set<int> test = denoms;
      test.insert(i);
      float testScore = this->getScore(test, (void*) this);

      if (testScore < currScore) {
        rankList.push_back(make_pair(testScore, newDenom));
      }
    }
    sort(rankList.begin(), rankList.end(), Cmp<pair<float, int> >());
    rankList.resize(numTry);
    return rankList;
  }

  pair<float, set<int> > findOptimalDenoms(set<int> denoms) {
    float currScore = this->getScore(denoms, (void*) this);

    if (denoms.size() < numDoms) {
      vector<pair<float, int> > rankList = getTheTopTries(denoms, currScore);
      for (int idx = 1; idx < rankList.size(); idx++) {
        int testDenom = rankList[idx].second;
        set<int> testDenoms = denoms;
        testDenoms.insert(testDenom);
        findOptimalDenoms(testDenoms);
      }
    } else {
      if (currScore < bestScore) {
        cout << "New best score: " << bestScore << " -> " << currScore << endl;
        cout << "Old Set: "; printSet(bestDenoms);  cout << endl;
        cout << "New Set: "; printSet(denoms); cout << endl << endl;

        bestScore = currScore;
        bestDenoms = denoms;
      }
    }

    return make_pair(bestScore, bestDenoms);
  }
};

float exactScore(set<int> denoms, void* obj) {
  if (!denoms.size()) {
    return 0.f;
  }
  Solution *ptr = (Solution*) obj;
  vector<int> changes(ptr->maxVal, 0);
  int changeAmount; //each of the change amout that neet to get the number of coins
  int bestExactChange; //minimized number of coins of each changeAmount
  int eachDenom; //each denomination(or coin) in the given Denoms vector
  int amountDiff; //definition: changeAmount-eachDenom
  float finalScore = 0; //the sum number of changeArray, with panality(N) considered

  //get changeArray with given denoms vector
  for(int idx=0; idx<changes.size(); idx++) {
    changeAmount = idx + 1;
    bestExactChange = INT_MAX;
    if (changeAmount == 1) {
      changes[idx] = 1;
    } else {
      for (set<int>::iterator it = denoms.begin(); it != denoms.end(); it++) {
        eachDenom = *it;
        amountDiff = changeAmount - eachDenom;
        if (amountDiff > 0) {
          bestExactChange = min(bestExactChange, changes[amountDiff-1] + 1);
        } else if (amountDiff == 0) {
          bestExactChange = 1;
        }
      }
      changes[idx] = bestExactChange;
    }
  }

  for (int idx = 0; idx < changes.size(); idx++) {
    if ((idx + 1) % 5 == 0) {
      finalScore += changes[idx] * ptr->N;
    } else {
      finalScore += changes[idx];
    }
  }

  return finalScore;
}

float exchangeScore(set<int> denoms, void* obj) {
  if (!denoms.size()) {
    return 0.f;
  }
  Solution *ptr = (Solution*) obj;
  vector<int> changes(ptr->maxVal, 0);
  vector<int> exchanges(ptr->maxVal, 0);
  int changeAmount; //each of the change amout that neet to get the number of coins
  int bestExactChange; //minimized number of coins of each changeAmount
  int eachDenom; //each denomination(or coin) in the given Denoms vector
  int amountDiff; //definition: changeAmount-eachDenom
  float finalScore = 0; //the sum number of changeArray, with panality(N) considered

  //get changeArray with given denoms vector
  for(int idx=0; idx<changes.size(); idx++) {
    changeAmount = idx + 1;
    bestExactChange = INT_MAX;
    if (changeAmount == 1) {
      changes[idx] = 1;
    } else {
      for (set<int>::iterator it = denoms.begin(); it != denoms.end(); it++) {
        eachDenom = *it;
        amountDiff = changeAmount - eachDenom;
        if (amountDiff > 0) {
          bestExactChange = min(bestExactChange, changes[amountDiff-1] + 1);
        } else if (amountDiff == 0) {
          bestExactChange = 1;
        }
      }
      changes[idx] = bestExactChange;
    }
  }

  for (int idx = 0; idx < changes.size(); idx++) {
    int exceedAmount;
    int amount = idx + 1;
    int minExchange = changes[idx];

    for (set<int>::iterator it = denoms.begin(); it != denoms.end(); it++) {
      eachDenom = *it;
      if (amount % eachDenom == 0) {
        exceedAmount = (amount/eachDenom) * eachDenom;
      } else {
        exceedAmount = (int(amount/eachDenom)+1) * eachDenom;
      }

      if (exceedAmount < ptr->maxVal && exceedAmount - amount > 0) {
        minExchange = min(minExchange, changes[exceedAmount-1] + changes[exceedAmount-amount-1]);
      } else if (amount == ptr->maxVal) {
        minExchange = min(minExchange, changes[0]);
      } else {
        continue;
      }
    }
    exchanges[idx] = minExchange;
  }

  for (int idx = 0; idx < exchanges.size(); idx++) {
    if ((idx + 1) % 5 == 0) {
      finalScore += exchanges[idx] * ptr->N;
    } else {
      finalScore += exchanges[idx];
    }
  }

  return finalScore;
}

int main(int argc, char **argv) {
  //First args == 1: exact change problem
  //First args == 2: exchange problem
  //Second args: N

  Solution sol(atof(argv[2]), atoi(argv[1]));
  set<int> firstDenoms;
  firstDenoms.insert(1);

  pair<float, set<int> > result = sol.findOptimalDenoms(firstDenoms);
  cout << "Best Score: " << result.first << endl;
  sol.printSet(result.second);

  return 0;
}