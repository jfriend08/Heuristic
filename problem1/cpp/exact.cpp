#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdio.h>
#include <stdlib.h>
#include <limits>
#include <queue>
#include <math.h>
#include <float.h>
#include <algorithm>    // std::min

using namespace std;

class Solution {
private:
  float N; //will be assign. Penalty of multiple of 5
  int maxChange = 239; //max change of english pound
  int numDoms = 7; //num of denomaitions need to design
  float bestScore = FLT_MAX; //store the current best score
  vector<int> bestDenoms; //store the best score's corresponding denomaitions
  int numTry = 3; //number of possible values to hold at each level

public:
  Solution(float x): N(x) {} // constructor definition.

  void printV(vector<int> inputV) {
    //nothing special. just print int vector with ideal format
    for (int i=0; i<inputV.size(); i++) {
      cout<<inputV[i]<< " ";
    }
    cout<<endl;
  }

  float getScoreWithGivenDenominations(vector<int> denoms) {
    //input denomination list, then calculate changeArray, and then return the score
    if (denoms.empty()) {
      return 0;
    }

    vector<int> changeArray(maxChange, 0); //create array of each change amount. each value is the num of exhange of that amount
    int changeAmount; //each of the change amout that neet to get the number of coins
    int bestExactChange; //minimized number of coins of each changeAmount
    int eachDenom; //each denomination(or coin) in the given Denoms vector
    int amountDiff; //definition: changeAmount-eachDenom
    int finalScore = 0; //the sum number of changeArray, with panality(N) considered

    //get changeArray with given denoms vector
    for(int idx=0; idx<changeArray.size(); idx++) {
      changeAmount = idx + 1;
      bestExactChange = INT_MAX;
      if (changeAmount == 1) {
        changeArray[idx] = 1;
      }
      else {
        for (int idx_denom=0; idx_denom<denoms.size(); idx_denom++) {
          // always need to add up one coin. dynamic programmingly check previous results and find the best one
          eachDenom = denoms[idx_denom];
          amountDiff = changeAmount - eachDenom;
          if (amountDiff > 0) {
            bestExactChange = min(bestExactChange, changeArray[amountDiff-1] + 1);
          }
          else if (amountDiff == 0) {
            bestExactChange = 1;
          }
        }
        changeArray[idx] = bestExactChange;
      }
    }
    // make panality for multiple of 5 and then add up the score
    for(int idx=0; idx<changeArray.size(); idx++) {
      if ((idx + 1) % 5 == 0) {
        changeArray[idx] = changeArray[idx] * N;
      }
      finalScore += changeArray[idx];
    }
    return finalScore;
  }

  bool isContained(vector<int> inputV, int x) {
    if(std::find(inputV.begin(), inputV.end(), x) != inputV.end()) {
      return true;
    } else {
      return false;
    }
  }

  template<typename P> struct Cmp {
    bool operator()(const P &p1, const P &p2){
      if(p1.first < p2.first) return true;
      return false;
      }
    };

  vector<pair <float, int>> getTheTopTries(vector<int> denoms, float currScore) {

    vector<pair<float, int>> rankList;

    // cout<<"inside getTheTopTries"<<endl;
    // cout<<"denoms: "<<endl;
    // printV(denoms);
    // cout<<"currScore: "<<currScore<<endl;

    for (int idx_denom=1; idx_denom<maxChange/2; idx_denom++) {
      int testDenom = idx_denom + 1;
      if (isContained(bestDenoms, testDenom) || isContained(denoms, testDenom)) {
        continue;
      }
      vector<int> testDenoms = denoms;
      testDenoms.push_back(testDenom);
      float testValue = getScoreWithGivenDenominations(testDenoms);

      // cout<<"testValue: "<<testValue<<endl;
      // cout<<"testDenoms:"<<endl;
      // printV(testDenoms);

      if (testValue < currScore){
        rankList.push_back(make_pair(testValue, testDenom));
      }
    }
    sort(rankList.begin(), rankList.end(), Cmp<pair<float, int>>());
    vector<pair<float, int>>::const_iterator first = rankList.begin();
    vector<pair<float, int>>::const_iterator last = rankList.begin() + numTry;
    vector<pair<float, int>> topRankList(first, last);
    return topRankList;
  }

  pair <float, vector<int>> findOptimalDenoms(vector<int> denoms) {
    // minimize the score. recurssively trying all possibilities
    int currScore = getScoreWithGivenDenominations(denoms);
    // cout<<"currScore: "<<currScore<<endl;
    if (denoms.size() < numDoms) {
      vector<pair<float, int>> rankList = getTheTopTries(denoms, currScore);

      // cout<<"hello"<<endl;
      // cout<<rankList[0].first<<endl;
      // cout<<rankList[0].second<<endl;

      for (int idx=1; idx<rankList.size(); idx++){
        int testValue = rankList[idx].first;
        int testDenom = rankList[idx].second;
        vector<int> testDenoms = denoms;
        testDenoms.push_back(testDenom);
        findOptimalDenoms(testDenoms);
      }
    } else {
      if (currScore < bestScore) {

        cout<<"current bestScore: "<< bestScore <<endl;
        printV(bestDenoms);

        bestScore = currScore;
        bestDenoms = denoms;
      }
    }
    return make_pair(bestScore,bestDenoms);
  }

};



int main(int argc, char *argv[]){
  if (argc != 2) {
    cout<< "Usage: " << argv[0] << " N" <<endl;
    return 1;
  }
	Solution sol(atof(argv[1])); //init the N value
  vector<int> myV(1,1); // denominations should most have 1
  cout<< sol.getScoreWithGivenDenominations(myV)<<endl;
  pair<float, vector<int>> result = sol.findOptimalDenoms(myV);
  cout<<"bestScore: "<<result.first<<endl;
  sol.printV(result.second);

}
















