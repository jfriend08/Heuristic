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

struct patientInfo {
  int xloc,yloc,rescuetime;
  patientInfo(int myxloc, int myyloc, int myrescuetime): xloc(myxloc), yloc(myyloc), rescuetime(myrescuetime){}
} ;
//later can be used to sort list of pair
template<typename P> struct Cmp {
  bool operator()(const P &p1, const P &p2){
    if(p1.first < p2.first) return true;
    return false;
  }
};

template<typename P> struct CmpSecond {
  bool operator()(const P &p1, const P &p2){
    if(p1.second < p2.second) return true;
    return false;
  }
};

class Solution {

};
class kMeans {
  private:
    vector<patientInfo> allPatients;
    int numCluster;
    vector<pair<int, int> > cent_points;
  public:
    kMeans(vector<patientInfo> inputAllPatients, int intputNumCluster): allPatients(inputAllPatients), numCluster(intputNumCluster) {}

    pair<int, int> findClosestIdxAndDist(patientInfo patient) {
      int cloestIdx;
      int cloestedDist = INT_MAX;

      for (int cp_idx=0; cp_idx<cent_points.size(); cp_idx++) {
        // float sqSum = pow(patient.xloc-cent_points[cp_idx].first,2) + pow(patient.yloc-cent_points[cp_idx].second,2);
        // float dist = sqrt(sqSum);
        int dist = abs(patient.xloc-cent_points[cp_idx].first) + abs(patient.yloc-cent_points[cp_idx].second);
        if (dist<cloestedDist) {
          cloestedDist = dist;
          cloestIdx = cp_idx;
        }
      }
      return make_pair(cloestIdx, cloestedDist);
    }
    void printPairs(vector<pair<int, int> > pairs) {
      for(int i=0; i<pairs.size(); i++) {
        printf("[%d, %d] ", pairs[i].first, pairs[i].second);
      }
      printf("\n");

    }
    void updateCentPoints(vector<vector<patientInfo> > &Groups) {
      // for each group
      for(int i=0; i<Groups.size(); i++){
        // for each points in group
        int totalX=0, totalY=0;
        int thisGroupSize = Groups[i].size();
        for (int member=0; member<thisGroupSize; member++) {
          totalX += Groups[i][member].xloc;
          totalY += Groups[i][member].yloc;
        }
        printf("totalX: %d, totalY: %d, thisGroupSize: %d\n", totalX, totalY, thisGroupSize);
        cent_points[i].first = totalX/thisGroupSize;
        cent_points[i].second = totalY/thisGroupSize;
        // make_pair(totalX/thisGroupSize, totalY/thisGroupSize);
      }
    }

    vector<pair<int,pair<int, int> > > findHospitalLocations() {
      map<int, bool> seen;
      float totalCloestDist_cur=0, totalCloestDist_prev = FLT_MAX;
      vector<vector<patientInfo> > finalGroups(numCluster);

      //cent_points init: randomly pick up cent_points from data
      while(cent_points.size() < numCluster){
        int init_cent_idx = rand() % allPatients.size();
        if (!seen[init_cent_idx]) {
          seen[init_cent_idx] = true;
          cent_points.push_back(make_pair(allPatients[init_cent_idx].xloc, allPatients[init_cent_idx].yloc));
        }
      }
      while( fabs(totalCloestDist_cur-totalCloestDist_prev)/totalCloestDist_prev > 0.01 ){
        printf("------------------------------\n");
        totalCloestDist_prev = totalCloestDist_cur==0 ? INT_MAX:totalCloestDist_cur;
        totalCloestDist_cur = 0;
        vector<vector<patientInfo> > Groups(numCluster);
        for(int eachPoint_idx = 0; eachPoint_idx<allPatients.size(); eachPoint_idx++){
          int cloestedDist = INT_MAX;
          pair<int, long int> idx_dist = findClosestIdxAndDist(allPatients[eachPoint_idx]);
          Groups[idx_dist.first].push_back(allPatients[eachPoint_idx]);
          // cout<<"idx_dist.second: "<<idx_dist.second<<endl;
          totalCloestDist_cur += idx_dist.second;
        }

        for(int i=0; i<Groups.size(); i++) {
          printf("Group %d: %lu size\n", i, Groups[i].size());
        }

        printf("totalCloestDist_prev: %f\n", totalCloestDist_prev);
        printf("totalCloestDist_cur: %f\n", totalCloestDist_cur);
        cout<<float(fabs(totalCloestDist_cur-totalCloestDist_prev)/totalCloestDist_prev)<<endl;

        printf("cent_points before:\n");
        printPairs(cent_points);
        updateCentPoints(Groups);
        printf("cent_points after:\n");
        printPairs(cent_points);
        finalGroups = Groups;
      }

      vector<pair<int,pair<int, int> > > superResult;
      for (int i=0; i<finalGroups.size(); i++) {
        // vector of pairs. first val in each pair is the #patients in that group, and the second val is the hospotial location
        superResult.push_back(make_pair(finalGroups[i].size(), cent_points[i]));
      }

      sort(superResult.begin(), superResult.end(), Cmp<pair<int,pair<int, int> > >()); //sort the vector of pair
      return superResult;

      // printf("cent_points updateCentPointsByLife:\n");
      // updateCentPointsByLife(finalGroups);
      // printPairs(cent_points);

    }
};

class Point_class {
private:
  int locX, locY, rescuetime;
  bool isHospital;
public:
  Point_class(int mylocX, int mylocY, bool myisHospital): locX(mylocX), locY(mylocY), isHospital(myisHospital) {}
  Point_class(int mylocX, int mylocY, int myrescuetime, bool myisHospital): locX(mylocX), locY(mylocY), rescuetime(myrescuetime), isHospital(myisHospital) {}
  bool getIsHospital() { return isHospital;}
  int getX() {return locX;}
  int getY() {return locY;}

};

class Schedule {
private:
  vector<vector<int> > distanceMap;
public:
  int findCurrentTime(vector<Point_class> cur_Ambulance) {
    if (cur_Ambulance.size() == 1) {
      return 0;
    } else {
      return -1;
    }
  }
  // vector<patientInfo> findAvailableChoices(vector<patientInfo> allPatients, int timeNow, vector<vector<int> > Hospotials) {

  // }
  vector<patientInfo> findPatientOnRoute(vector<Point_class> cur_Ambulance, vector<patientInfo> allPatients, vector<vector<int> > Hospotials) {
    vector<patientInfo> myPatients;
    int timeNow = findCurrentTime(cur_Ambulance);
    int curX = cur_Ambulance[cur_Ambulance.size()-1].getX();
    int curY = cur_Ambulance[cur_Ambulance.size()-1].getY();
    while(myPatients.size()< 4) {
      // vector<patientInfo> patientChoices = findAvailableChoices(allPatients, timeNow, Hospotials);
    }
    myPatients.push_back(allPatients[0]);


    return myPatients;

  }
  void distMapInit(int size) {
    distanceMap.resize(size);
    for (int i = 0; i < size; ++i){
      distanceMap[i].resize(size);
    }
    for (int i=0; i<size; i++) {
      for (int j=0; j<size; j++) {
        if (i==j){
          distanceMap[i][j] = 0;
        } else {
          distanceMap[i][j] = -1;
        }
      }
    }
  }
  void ambulanceScheduling(vector<vector<Point_class> > &Ambulances, vector<patientInfo> &allPatients, vector<vector<int> > Hospotials) {
    distMapInit(allPatients.size()+Hospotials.size());

    for(int dim=0; dim<allPatients.size()+Hospotials.size(); dim++) {
      distanceMap[dim][dim] = 0;
    }

    for(int ambu_idx=0; ambu_idx<Ambulances.size(); ambu_idx++) {
      vector<Point_class> cur_Ambulance = Ambulances[ambu_idx];
      vector<patientInfo> patientToPickUp = findPatientOnRoute(cur_Ambulance, allPatients, Hospotials);
    }
    cout<< allPatients.size()<<endl;


  }

};






int main(int argc, char *argv[]){
  char separator;
  int num_Patients = 50, num_Hospital = 5, num_Ambulance, count = 0;
  string tmp_string;
  int xloc,yloc,rescuetime;

  vector<pair<int,int> > hospotials_tmp;
  vector<vector<int> > Hospotials(num_Hospital);
  vector<vector<Point_class> > Ambulances;
  vector<patientInfo> allPatients;

  cin.ignore(100000, '(');
  cin >> tmp_string;

  while (count < num_Patients) {
    cin >> xloc >> separator >> yloc >> separator >> rescuetime;
    printf("%d\t%d\t%d\n", xloc, yloc, rescuetime);
    patientInfo myPatient(xloc, yloc, rescuetime);
    allPatients.push_back(myPatient);
    count++;
  }

  cin >> tmp_string;
  count = 0;
  while (count < num_Hospital) {
    cin >> num_Ambulance;
    hospotials_tmp.push_back(make_pair(count, num_Ambulance));
    count++;
  }

  sort(hospotials_tmp.begin(), hospotials_tmp.end(), CmpSecond<pair<int,int > >()); //sort the vector of pair

  //get KMeans and know how many point in each of the point
  kMeans myKMean(allPatients, num_Hospital);
  vector<pair<int,pair<int, int> > > groupSize_centerPorint = myKMean.findHospitalLocations();
  for(int i=0; i<groupSize_centerPorint.size(); i++) {
    printf("group:%d\tnumPatients:%d\tlocation:[%d,%d]\n", i, groupSize_centerPorint[i].first, groupSize_centerPorint[i].second.first, groupSize_centerPorint[i].second.second);
  }

  //
  for(int i=0; i<hospotials_tmp.size(); i++) {
    int hospital_idx = hospotials_tmp[i].first;
    int num_Ambulance = hospotials_tmp[i].second;
    int hospital_locX= groupSize_centerPorint[i].second.first;
    int hospital_locY= groupSize_centerPorint[i].second.second;
    printf("hospotial idx:%d\tnumAmbulance:%d\tlocation:[%d,%d]\n", hospital_idx, num_Ambulance, hospital_locX, hospital_locY);

    vector<int> myHospitalInfo;
    //locX, locY, num_Ambulance
    myHospitalInfo.push_back(hospital_locX); myHospitalInfo.push_back(hospital_locY); myHospitalInfo.push_back(num_Ambulance);
    Hospotials[hospital_idx] = myHospitalInfo;
  }

  int ambulance_idx = 0;
  for(int i=0; i<Hospotials.size(); i++) {
    printf("Hospital:%d|%d,%d,%d|", i, Hospotials[i][0], Hospotials[i][1], Hospotials[i][2]);
    for(int numAmbulance=0; numAmbulance<Hospotials[i][2]; numAmbulance++) {

      Point_class myPoint(Hospotials[i][0], Hospotials[i][1], true); //init a point
      vector<Point_class> tmp_AmbulancePath; //init a path vector for this ambulance
      tmp_AmbulancePath.push_back(myPoint);
      Ambulances.push_back(tmp_AmbulancePath); //push path vector or Ambulances

      if (numAmbulance==Hospotials[i][2]-1) {
        printf("%d\n", ambulance_idx);
      } else {
        printf("%d,", ambulance_idx);
      }
      ambulance_idx++;
    }
  }

  Schedule scheduleClass;
  scheduleClass.ambulanceScheduling(Ambulances, allPatients, Hospotials);

  for (int i=0; i<Ambulances.size(); i++) {
    int ambulance_idx = i+1;
    vector<Point_class> ambulance_path = Ambulances[i];
    for(int eachPoint_idx=0; eachPoint_idx<ambulance_path.size(); eachPoint_idx++) {
      Point_class thisPoint = ambulance_path[eachPoint_idx];
      if ( (eachPoint_idx==0) | (thisPoint.getIsHospital()) ){
        printf("Ambulance:%d|%d,%d\n", ambulance_idx, thisPoint.getX(), thisPoint.getY());
      }
    }
  }



}
















