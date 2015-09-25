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
  int sqSum = 0;
  for (int i=1; i<4; i++){
    sqSum += (orig[i]-dest[i])^2;
  }
  return sqrt(sqSum);
};

void randomSelect(vector<vector<int> > & allCity){
  int city_idx1, city_idx2;
  int numIteration = allCity.size();

  srand (time(NULL)); /* initialize random seed: */

  city_idx1 = rand() % allCity.size();
  allCity.erase (allCity.begin()+city_idx1);

  for (int i = 0; i<numIteration-1; i++) {
    int city_idx2 = rand() % allCity.size();
    cout <<"city_idx1: " << city_idx1 <<endl;
    cout <<"city_idx2: " << city_idx2 <<endl;
    allCity.erase (allCity.begin()+city_idx2);
    city_idx1 = city_idx2;
  }
  cout<<"allCity.size(): " << allCity.size() <<endl;
}

int main(int argc, char **argv) {

  int cityID, x_loc, y_loc, z_loc, count = 0;
  vector<vector<int> > allCity;
  // map <int,int*> cityMap;
  while (count < 1000) {
    cin >> cityID >> x_loc >> y_loc >> z_loc;
    vector<int> tmpV;
    tmpV.push_back(cityID);
    tmpV.push_back(x_loc);
    tmpV.push_back(y_loc);
    tmpV.push_back(z_loc);
    allCity.push_back(tmpV);
    count++;
  }


  cout<<"sqrt: "<< getDistance(allCity[0], allCity[1]) <<endl;
  randomSelect(allCity);
  cout<<"sqrt: "<< getDistance(allCity[0], allCity[1]) <<endl;


  return 0;
}