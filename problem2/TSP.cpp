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
  vector<vector<float> > distanceMap;

public:
  Solution(int x): numCity(x), bestScore(FLT_MAX) {
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
    cout<<"printVV size: " <<myVV.size()<<endl;
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
    long long int sqSum = 0;
    for (int i=1; i<4; i++){
      sqSum += pow(orig[i]-dest[i],2);
    }
    return sqrt(sqSum);
  }

  float getTotalDist(vector<vector<int> > cityOrder) {
    // cout<<"start getTotalDist. All cities are:"<<endl;
    // printVV(cityOrder);
    float curTotalDis = 0.0;
    for(vector<vector<int> >::iterator it = cityOrder.begin(); it != cityOrder.end()-1; it++) {
      vector<int> startCity = *it;
      vector<int> endCity = *(it+1);
      int startCityID = startCity[0];
      int endCityID = endCity[0];
      float dis = distanceMap[startCityID-1][endCityID-1];
      if (dis==0) {
        // cout<<"not calculated"<<endl;
        dis = getDistance(startCity, endCity);
        distanceMap[startCityID-1][endCityID-1] = dis;
        distanceMap[endCityID-1][startCityID-1] = dis;
      }
      // cout<<"curTotalDis: "<<curTotalDis<<" dis: "<<dis<<endl;
      // printDistanceMap();
      curTotalDis += dis;
    }
    return curTotalDis;
  }

  vector<vector<int> > getRandCityOrder(vector<vector<int> > allCity){
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
  vector<vector<int> > swapCities(int city_idx1, int city_idx2, vector<vector<int> > allCity) {
    // given the vector and indixes, return the swaped vector
    vector<int> tmpV = allCity[city_idx1];
    allCity[city_idx1] = allCity[city_idx2];
    allCity[city_idx2] = tmpV;
    return allCity;
  }
  float acceptance_probability(float newDist, float oldDist,float T) {
    // cout<<"newDist: "<<newDist<<" oldDist: "<<oldDist<<endl;
    return exp((oldDist-newDist)/T);
  }
  vector<int> getCoordinateBound(vector<vector<int> > allCity) {
    int x_max=INT_MIN, y_max=INT_MIN, z_max=INT_MIN, x_min=INT_MAX, y_min=INT_MAX, z_min=INT_MAX;
    int x_loc, y_loc, z_loc;
    vector<int> v;
    for (int i=0; i<allCity.size(); i++) {
      x_loc = allCity[i][1];
      y_loc = allCity[i][2];
      z_loc = allCity[i][3];
      if (x_loc > x_max) { x_max = x_loc; }
      if (x_loc < x_min) { x_min = x_loc; }
      if (y_loc > y_max) { y_max = y_loc; }
      if (y_loc < y_min) { y_min = y_loc; }
      if (z_loc > z_max) { z_max = z_loc; }
      if (z_loc < z_min) { z_min = z_loc; }
    }
    v.push_back(x_max); v.push_back(x_min); v.push_back(y_max); v.push_back(y_min); v.push_back(z_max); v.push_back(z_min);
    return v;
  }
  vector<vector<vector<int> > > bucketSort(vector<vector<int> > allCity, int max, int min, int idx, bool reverse) {
    vector<vector<int> > bucket1, bucket2, bucket3, bucket4, bucket5;
    vector<vector<vector<int> > > final;
    int interval = (max - min)/5;
    cout<<"interval: "<<interval<<endl;

    // if (allCity.empty()){
    //   return final;
    // }

    for (int i=0; i<allCity.size(); i++) {
      vector<int> curV = allCity[i];
      if (curV[idx] >= min && curV[idx] < min+interval) { bucket1.push_back(curV); }
      else if (curV[idx] >= min+interval && curV[idx] < min+2*interval) { bucket2.push_back(curV); }
      else if (curV[idx] >= min+2*interval && curV[idx] < min+3*interval) { bucket3.push_back(curV); }
      else if (curV[idx] >= min+3*interval && curV[idx] < min+4*interval) { bucket4.push_back(curV); }
      else { bucket5.push_back(curV); }
    }
    if (reverse) {
      final.push_back(bucket5);
      final.push_back(bucket4);
      final.push_back(bucket3);
      final.push_back(bucket2);
      final.push_back(bucket1);
      // for(int i=0; i<bucket5.size(); i++ ){ final.push_back(bucket5[i]); }
      // for(int i=0; i<bucket4.size(); i++ ){ final.push_back(bucket4[i]); }
      // for(int i=0; i<bucket3.size(); i++ ){ final.push_back(bucket3[i]); }
      // for(int i=0; i<bucket2.size(); i++ ){ final.push_back(bucket2[i]); }
      // for(int i=0; i<bucket1.size(); i++ ){ final.push_back(bucket1[i]); }
    } else {
      final.push_back(bucket1);
      final.push_back(bucket2);
      final.push_back(bucket3);
      final.push_back(bucket4);
      final.push_back(bucket5);
      // for(int i=0; i<bucket1.size(); i++ ){ final.push_back(bucket1[i]); }
      // for(int i=0; i<bucket2.size(); i++ ){ final.push_back(bucket2[i]); }
      // for(int i=0; i<bucket3.size(); i++ ){ final.push_back(bucket3[i]); }
      // for(int i=0; i<bucket4.size(); i++ ){ final.push_back(bucket4[i]); }
      // for(int i=0; i<bucket5.size(); i++ ){ final.push_back(bucket5[i]); }
    }
    return final;
  }
  void findBestRout(vector<vector<int> > allCity, int x_max, int x_min, int y_max, int y_min, int z_max, int z_min){
    srand (time(NULL)); /* initialize random seed: */
    float T = 1, T_min = 0.00001, alpha = 0.9999;
    int count;
    vector<vector<int> > cityOrder;
    vector<vector<vector<int> > > firstSort;
    vector<vector<vector<vector<int> > > > secondSort, thirdSort;
    // vector<vector<vector<vector<vector<int> > > > > thirdSort;

    firstSort = bucketSort(allCity, x_max, x_min, 1, false);

    for (int x=0; x<firstSort.size(); x++) {
      vector<vector<int> > curV = firstSort[x];
      // printVV(curV);
      bool reverse = x%2==0 ? false:true;
      secondSort.push_back(bucketSort(curV, y_max, y_min, 2, reverse));
    }

    for(int x=0; x<secondSort.size(); x++) {
      for(int y=0; y<secondSort[x].size(); y++) {
        // cout<<"x: "<<x<<" y: "<<y<<endl;
        // printVV(secondSort[x][y]);
        // cout<<"------------------------------------"<<endl;
        vector<vector<int> > curV = secondSort[x][y];
        bool reverse = (x+y)%2==0 ? false:true;
        thirdSort.push_back(bucketSort(curV, z_max, z_min, 3, reverse));
      }
    }
    for(int x=0; x<thirdSort.size(); x++) {
      for(int y=0; y<thirdSort[x].size(); y++) {
        // cout<<"Hi x: "<<x<<" y: "<<y<<endl;
        vector<vector<int> > curV = thirdSort[x][y];
        // printVV(curV);
        for (int elm=0; elm<curV.size(); elm++) {
          cityOrder.push_back(curV[elm]);
        }
      }
    }
    // cityOrder = bucketSort(cityOrder, y_max, y_min, 2);
    // cityOrder = bucketSort(cityOrder, z_max, z_min, 3);
    printVV(cityOrder);

    // cityOrder = getRandCityOrder(allCity);
    float bestScore = getTotalDist(cityOrder);

    while(T > T_min) {
      int city_idx1 = rand() % allCity.size();
      int city_idx2 = rand() % allCity.size();
      // cout<<"city_idx1: "<<city_idx1<<endl;
      // cout<<"city_idx2: "<<city_idx2<<endl;

      vector<vector<int> > swapCity = swapCities(city_idx1,city_idx2,cityOrder);
      float swapScore = getTotalDist(swapCity);

      // float ap = acceptance_probability(swapScore, bestScore, T);
      // float curRand = ((double) rand() / (RAND_MAX));
      // cout <<"T: "<<T<<" curRand: "<<curRand<<" ap: "<<ap<<endl;
      // if (ap > curRand){
      //   cout<<"#1"<<endl;
      // } else {
      //   cout<<"#0"<<endl;
      // }

      if (swapScore<bestScore | acceptance_probability(swapScore, bestScore, T) > ((double) rand() / (RAND_MAX))) {
        // cout<<"bestScore updated: "<< bestScore<< "==>"<< swapScore<< endl;
        cityOrder = swapCity;
        bestScore = swapScore;
        // printDistanceMap();
      }
      // cout<<"-----------"<<count<<"-------------"<<endl;
      T = T*alpha;
      count+=1;
    }
    cout<<"Finished. bestScore: "<< bestScore<<endl;
    cout<<"cityOrder: "<<endl;
    // printVV(cityOrder);

  }


};




int main(int argc, char **argv) {
  const int numCity = 1000;
  Solution sol(numCity); //init the numCity

  int cityID, x_loc, y_loc, z_loc, count = 0;
  vector<vector<int> > allCity;
  int x_max=INT_MIN, y_max=INT_MIN, z_max=INT_MIN, x_min=INT_MAX, y_min=INT_MAX, z_min=INT_MAX;
  while (count < numCity) {
    cin >> cityID >> x_loc >> y_loc >> z_loc;
    if (x_loc > x_max) { x_max = x_loc;}
    if (x_loc < x_min) { x_min = x_loc; }
    if (y_loc > y_max) { y_max = y_loc;}
    if (y_loc < y_min) { y_min = y_loc; }
    if (z_loc > z_max) { z_max = z_loc;}
    if (z_loc < z_min) { z_min = z_loc; }
    vector<int> tmpV;
    tmpV.push_back(cityID);
    tmpV.push_back(x_loc);
    tmpV.push_back(y_loc);
    tmpV.push_back(z_loc);
    allCity.push_back(tmpV);
    count++;
  }

  cout<<"x_max: " <<x_max <<" x_min: "<<x_min<<endl;
  cout<<"y_max: " <<y_max <<" y_min: "<<y_min<<endl;
  cout<<"z_max: " <<z_max <<" z_min: "<<z_min<<endl;

  sol.findBestRout(allCity, x_max, x_min, y_max, y_min, z_max, z_min);

  return 0;
}