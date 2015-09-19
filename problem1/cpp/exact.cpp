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
    for (int i=0; i<inputArray.size(); i++) {
      cout<<inputArray[i]<< " ";
    }
    cout<<endl;
  }

  float getScoreWithGivenDenominations(vector<int> Denoms) {
    if (Denoms.empty()) {
      return 0;
    }
    vector<int> changeArray(maxChange, 0);
    bestExactChange = INT_MAX;


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
















