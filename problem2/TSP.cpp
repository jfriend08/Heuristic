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


class Solution {
private:
  int numCity;
  float bestScore;
  vector<vector<int> > distanceMap;

public:
  Solution(int x): numCity(x) {
    distanceMap.resize(x);
    for (int i = 0; i < x; ++i){
      distanceMap[i].resize(x);
    }
  } // constructor definition.

   // De-Constructor
  ~Solution() { }

  void printV(vector<int> myV) {
    cout<<"[ ";
    for (vector<int>::iterator it = myV.begin(); it != myV.end(); it++) {
      cout << *it << " ";
    }
    cout<<"]"<<endl;
  }
  void printVV(vector<vector<int> > myVV){
    for(vector<vector<int> >::iterator it = myVV.begin(); it != myVV.end(); it++) {
      printV(*it);
    }
  }
  void printDistanceMap(){
    for (int i=0; i<numCity; i++) {
      for (int j=0; j<numCity; j++){
        cout<<distanceMap[i][j]<<" ";
      }
      cout<<endl;
    }
  }

  float getDistance(vector<int> orig, vector<int> dest){
    cout<<"getDistance"<<endl;
    printV(orig);
    printV(dest);
    long long int sqSum = 0;
    for (int i=1; i<4; i++){
      sqSum += pow(orig[i]-dest[i],2);
    }
    return sqrt(sqSum);
  }

  float getTotalDist(vector<vector<int> > cityOrder) {
    cout<<"start getTotalDist. All cities are:"<<endl;
    printVV(cityOrder);
    float curTotalDis = 0.0;
    for(vector<vector<int> >::iterator it = cityOrder.begin(); it != cityOrder.end()-1; it++) {
      vector<int> startCity = *it;
      vector<int> endCity = *(it+1);
      int startCityID = startCity[0];
      int endCityID = endCity[0];
      float dis = distanceMap[startCityID-1][endCityID-1];
      if (dis==0) {
        dis = getDistance(startCity, endCity);
        distanceMap[startCityID-1][endCityID-1] = dis;
        distanceMap[endCityID-1][startCityID-1] = dis;
      }
      cout<<"curTotalDis: "<<curTotalDis<<" dis: "<<dis<<endl;
      printDistanceMap();
      curTotalDis += dis;
    }
    return curTotalDis;
  }

  vector<vector<int> > getRandCityOrder(vector<vector<int> > & allCity){
    int city_idx1, city_idx2;
    int numIteration = allCity.size();
    map <int, bool> haveSeen;
    vector<vector<int> > cityOrder;

    srand (time(NULL)); /* initialize random seed: */
    while (cityOrder.size() < allCity.size()) {
      int city_idx = rand() % allCity.size();
      if (haveSeen[city_idx]) {
        continue;
      } else {
        cityOrder.push_back(allCity[city_idx]);
        haveSeen[city_idx] = true;
      }
    }
    return cityOrder;
  }



};




int main(int argc, char **argv) {
  const int numCity = 4;
  Solution sol(numCity); //init the numCity

  int cityID, x_loc, y_loc, z_loc, count = 0;
  vector<vector<int> > allCity;
  // map <int,int*> cityMap;
  while (count < numCity) {
    cin >> cityID >> x_loc >> y_loc >> z_loc;
    vector<int> tmpV;
    tmpV.push_back(cityID);
    tmpV.push_back(x_loc);
    tmpV.push_back(y_loc);
    tmpV.push_back(z_loc);
    allCity.push_back(tmpV);
    count++;
  }



  // vector<int> randCities = sol.getRandCityOrder(allCity);
  vector<vector<int> > randCity= sol.getRandCityOrder(allCity);
  // sol.printVV(randCity);
  cout<<sol.getTotalDist(randCity)<<endl;
  // sol.getTotalDist(sol.getRandCityOrder(allCity));

  return 0;
}