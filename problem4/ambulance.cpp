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

class Solution {

};
class kMeans {
  private:
    vector<patientInfo> allPatients;
    int numCluster;
    vector<pair<int, int> > cent_points;
  public:
    kMeans(vector<patientInfo> inputAllPatients, int intputNumCluster): allPatients(inputAllPatients), numCluster(intputNumCluster) {}

    pair<int, float> findClosestIdxAndDist(patientInfo patient) {
      int cloestIdx;
      float cloestedDist = FLT_MAX;

      for (int cp_idx=0; cp_idx<cent_points.size(); cp_idx++) {
        float sqSum = pow(patient.xloc-cent_points[cp_idx].first,2) + pow(patient.yloc-cent_points[cp_idx].second,2);
        float dist = sqrt(sqSum);
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

    void updateCentPointsByLife(vector<vector<patientInfo> > &Groups) {
      // for each group
      for(int i=0; i<Groups.size(); i++){
        // for each points in group
        float totalX=0, totalY=0;
        float thisGroupSize = Groups[i].size();
        int time_lowBound=INT_MAX, time_upBound=INT_MIN;
        float timeInterval;
        for (int member=0; member<thisGroupSize; member++) {
          if(Groups[i][member].rescuetime > time_upBound) {
            time_upBound = Groups[i][member].rescuetime;
          }
          if(Groups[i][member].rescuetime < time_lowBound) {
            time_lowBound = Groups[i][member].rescuetime;
          }
        }

        timeInterval = (time_upBound - time_lowBound);

        for (int member=0; member<thisGroupSize; member++) {
          float weighting = (timeInterval-Groups[i][member].rescuetime)/timeInterval;
          totalX += Groups[i][member].xloc * weighting;
          totalY += Groups[i][member].yloc * weighting;
        }
        cent_points[i].first = totalX/thisGroupSize;
        cent_points[i].second = totalY/thisGroupSize;
        // make_pair(totalX/thisGroupSize, totalY/thisGroupSize);
      }
    }

    vector<pair<int,pair<int, int> > > findHospitalLocations() {
      map<int, bool> seen;
      float totalCloestDist_cur=0, totalCloestDist_prev=FLT_MAX;
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
        totalCloestDist_prev = totalCloestDist_cur;
        totalCloestDist_cur = 0;
        vector<vector<patientInfo> > Groups(numCluster);
        for(int eachPoint_idx = 0; eachPoint_idx<allPatients.size(); eachPoint_idx++){
          int cloestedDist = INT_MAX;
          pair<int, float> idx_dist = findClosestIdxAndDist(allPatients[eachPoint_idx]);
          Groups[idx_dist.first].push_back(allPatients[eachPoint_idx]);
          totalCloestDist_cur += idx_dist.second;
        }

        for(int i=0; i<Groups.size(); i++) {
          printf("Group %d: %lu size\n", i, Groups[i].size());
        }

        printf("totalCloestDist_prev: %f\n", totalCloestDist_prev);
        printf("totalCloestDist_cur: %f\n", totalCloestDist_cur);

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

      sort(superResult.begin(), superResult.end(), Cmp<pair<int,pair<float, float> > >()); //sort the vector of pair
      return superResult;

      // printf("cent_points updateCentPointsByLife:\n");
      // updateCentPointsByLife(finalGroups);
      // printPairs(cent_points);

    }

};



int main(int argc, char *argv[]){
  char separator;
  int num_Patients = 50, num_Hospital = 5, num_Ambulance, count = 0;
  string tmp_string;
  int xloc,yloc,rescuetime;

  vector<pair<int,int> > hospotials_tmp;
  vector<vector<int> > hospotials(num_Hospital);
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

  sort(hospotials_tmp.begin(), hospotials_tmp.end(), Cmp<pair<int,int > >()); //sort the vector of pair

  kMeans myKMean(allPatients, num_Hospital);
  vector<pair<int,pair<int, int> > > groupSize_centerPorint = myKMean.findHospitalLocations();
  for(int i=0; i<groupSize_centerPorint.size(); i++) {
    printf("group:%d\tnumPatients:%d\tlocation:[%d,%d]\n", i, groupSize_centerPorint[i].first, groupSize_centerPorint[i].second.first, groupSize_centerPorint[i].second.second);
  }

  for(int i=0; i<hospotials_tmp.size(); i++) {
    int hospital_idx = hospotials_tmp[i].first;
    int num_Ambulance = hospotials_tmp[i].second;
    int hospital_locX= groupSize_centerPorint[i].second.first;
    int hospital_locY= groupSize_centerPorint[i].second.second;
    printf("hospotial idx:%d\tnumAmbulance:%d\tlocation:[%d,%d]\n", hospital_idx, num_Ambulance, hospital_locX, hospital_locY);

    vector<int> myHospitalInfo;
    myHospitalInfo.push_back(hospital_locX); myHospitalInfo.push_back(hospital_locY); myHospitalInfo.push_back(num_Ambulance);
    hospotials[hospital_idx] = myHospitalInfo;
  }
  int ambulance_idx = 0;
  for(int i=0; i<hospotials.size(); i++) {
    printf("Hospital:%d|%d,%d,%d|", i, hospotials[i][0], hospotials[i][1], hospotials[i][2]);
    for(int numAmbulance=0; numAmbulance<hospotials[i][2]; numAmbulance++) {
      if (numAmbulance==hospotials[i][2]-1) {
        printf("%d\n", ambulance_idx);
      } else {
        printf("%d,", ambulance_idx);
      }
      ambulance_idx++;
    }
  }



}
















