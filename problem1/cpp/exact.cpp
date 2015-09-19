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
  int maxChange = 99; //max change of english pound
  int numDoms = 5; //num of denomaitions need to design
  float bestScore = FLT_MAX; //store the current best score
  vector<int> bestDenoms; //store the best score's corresponding denomaitions
  int numTry = 7; //number of possible values to hold at each level

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

    vector<int> changeArray(maxChange, 0); //create array of each change amount. each value is the num of exact change of that amount
    vector<int> exchangeArray(maxChange, 0); //create array of each change amount. each value is the num of exhange of that amount

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

    for(int idx=0; idx<changeArray.size(); idx++) {
      int testAmount;
      int exceedAmount;
      int amount = idx + 1;
      int minExchange = changeArray[idx];
      for (int idx_denom=0; idx_denom<denoms.size(); idx_denom++){
        eachDenom = denoms[idx_denom];
        if (amount % eachDenom == 0) {
          testAmount = (amount/eachDenom) * eachDenom;
        } else {
          testAmount = (int(amount/eachDenom)+1) * eachDenom;
        }

        if (testAmount < maxChange) {
          exceedAmount = testAmount;
        } else {
          continue;
        }
        minExchange = min(minExchange, changeArray[exceedAmount-1] + changeArray[exceedAmount-amount-1]);
        exchangeArray[idx] = minExchange;
      }
    }

    printV(changeArray);
    printV(exchangeArray);

    cout<< changeArray[42]<<endl;
    cout<< exchangeArray[42]<<endl;

    // make panality for multiple of 5 and then add up the score
    for(int idx=0; idx<changeArray.size(); idx++) {
      if ((idx + 1) % 5 == 0) {
        changeArray[idx] = changeArray[idx] * N;
      }
      finalScore += changeArray[idx];
    }
    return finalScore;
  }

  //check given element x is existed in the vetor
  bool isContained(vector<int> inputV, int x) {
    if(std::find(inputV.begin(), inputV.end(), x) != inputV.end()) {
      return true;
    } else {
      return false;
    }
  }

  //later can be used to sort list of pair
  template<typename P> struct Cmp {
    bool operator()(const P &p1, const P &p2){
      if(p1.first < p2.first) return true;
      return false;
    }
  };

  //given the denoms vector and current score, try different next coin that will yield better score, and return the top numTry
  vector<pair <float, int>> getTheTopTries(vector<int> denoms, float currScore) {
    vector<pair<float, int>> rankList;
    for (int idx_denom=1; idx_denom<maxChange/2; idx_denom++) {
      int testDenom = idx_denom + 1;
      if (isContained(bestDenoms, testDenom) || isContained(denoms, testDenom)) {
        continue;
      }
      vector<int> testDenoms = denoms;
      testDenoms.push_back(testDenom);
      float testValue = getScoreWithGivenDenominations(testDenoms);

      if (testValue < currScore){
        rankList.push_back(make_pair(testValue, testDenom));
      }
    }
    sort(rankList.begin(), rankList.end(), Cmp<pair<float, int>>()); //sort the vector of pair

    vector<pair<float, int>>::const_iterator first = rankList.begin(); //to get the top sublist
    vector<pair<float, int>>::const_iterator last = rankList.begin() + numTry;
    vector<pair<float, int>> topRankList(first, last);
    return topRankList;
  }

  // minimize the score. recurssively trying all possibilities
  pair <float, vector<int>> findOptimalDenoms(vector<int> denoms) {
    int currScore = getScoreWithGivenDenominations(denoms); //current score of current demonination list
    if (denoms.size() < numDoms) { //current denoms is less than numDoms, keep trring
      vector<pair<float, int>> rankList = getTheTopTries(denoms, currScore);
      for (int idx=1; idx<rankList.size(); idx++){ //each elem in rankList potentionaly will be better solution
        // int testScore = rankList[idx].first;
        int testDenom = rankList[idx].second;
        vector<int> testDenoms = denoms;
        testDenoms.push_back(testDenom); //add new possible
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

  // vector<int> myV(1,1); // denominations should most have 1
  vector<int> myV { 1, 5, 10, 25, 50 }; // denominations should most have 1

  cout<< sol.getScoreWithGivenDenominations(myV)<<endl; //just testing the score correctness, diven only 1 denomination

  // pair<float, vector<int>> result = sol.findOptimalDenoms(myV); //start to guess the actual denominations
  // cout<<"bestScore: "<<result.first<<endl;
  // sol.printV(result.second);

  // cout<<"recalculate the socre"<<endl; //just to confirm
  // cout<< sol.getScoreWithGivenDenominations(result.second)<<endl;

}
















