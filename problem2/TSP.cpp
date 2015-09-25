#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <float.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <algorithm>
#include <limits>
#include <ostream>

using namespace std;


float getDistance(vector<int> orig, vector<int> dest){
  cout<<orig.size()<<endl;
  int sqSum = 0;
  for (int i=0; i<3; i++){
    sqSum += (orig[i]-dest[i])^2;
  }
  cout<<"sqSum: "<<sqSum<<endl;
  return sqrt(sqSum);
};

int main(int argc, char **argv) {

  int cityID, x_loc, y_loc, z_loc, count = 0;
  map<int,vector<int> > cityMap;
  // map <int,int*> cityMap;
  while (count < 1000) {
    cin >> cityID >> x_loc >> y_loc >> z_loc;
    cityMap[cityID].push_back(x_loc);
    cityMap[cityID].push_back(y_loc);
    cityMap[cityID].push_back(z_loc);
    count++;
  }


  cout<< getDistance(cityMap[1], cityMap[2]) <<endl;


  return 0;
}