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
  static vector<int> bestDenoms; //store the best score's corresponding denomaitions
  int numTry = 3; //number of possible values to hold at each level

public:
  Solution(float x): N(x) {} // constructor definition.

  void printArray(vector<int> inputArray) {
    //nothing special. just print int vector with ideal format
    for (int i=0; i<inputArray.size(); i++) {
      cout<<inputArray[i]<< " ";
    }
    cout<<endl;
  }

  float getScoreWithGivenDenominations(vector<int> Denoms) {
    //input denomination list, then calculate changeArray, and then return the score
    if (Denoms.empty()) {
      return 0;
    }

    vector<int> changeArray(maxChange, 0); //create array of each change amount. each value is the num of exhange of that amount
    int changeAmount; //each of the change amout that neet to get the number of coins
    int bestExactChange; //minimized number of coins of each changeAmount
    int eachDenom; //each denomination(or coin) in the given Denoms vector
    int amountDiff; //definition: changeAmount-eachDenom
    int finalScore = 0; //the sum number of changeArray, with panality(N) considered
    printArray(changeArray);

    //get changeArray with given denoms vector
    for(int idx=0; idx<changeArray.size(); idx++) {
      changeAmount = idx + 1;
      bestExactChange = INT_MAX;
      if (changeAmount == 1) {
        changeArray[idx] = 1;
      }
      else {
        for (int idx_denom=0; idx_denom<Denoms.size(); idx_denom++) {
          // always need to add up one coin. dynamic programmingly check previous results and find the best one
          eachDenom = Denoms[idx_denom];
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
    printArray(changeArray);

    for(int idx=0; idx<changeArray.size(); idx++) {
      if ((idx + 1) % 5 == 0) {
        changeArray[idx] = changeArray[idx] * N;
      }
    }
    printArray(changeArray);

    return 1;
  }

};



int main(int argc, char *argv[]){
  if (argc != 2) {
    cout<< "Usage: " << argv[0] << " N" <<endl;
    return 1;
  }
	Solution sol(atof(argv[1]));
  vector<int> myV(1,1);
  sol.getScoreWithGivenDenominations(myV);


}
















