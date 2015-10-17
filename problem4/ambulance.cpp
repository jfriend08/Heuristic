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

class Solution {

};
class kMeans {
  private:
    vector<patientInfo> allPatients;
    int numCluster;
    vector<pair<float, float> > cent_points;
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
    void printPairs(vector<pair<float, float> > pairs) {
      for(int i=0; i<pairs.size(); i++) {
        printf("[%f, %f] ", pairs[i].first, pairs[i].second);
      }
      printf("\n");

    }
    void updateCentPoints(vector<vector<patientInfo> > &Groups) {
      // for each group
      for(int i=0; i<Groups.size(); i++){
        // for each points in group
        float totalX=0, totalY=0;
        float thisGroupSize = Groups[i].size();
        for (int member=0; member<thisGroupSize; member++) {
          totalX += Groups[i][member].xloc;
          totalY += Groups[i][member].yloc;
        }
        printf("totalX: %f, totalY: %f, thisGroupSize: %f\n", totalX, totalY, thisGroupSize);
        cent_points[i].first = totalX/thisGroupSize;
        cent_points[i].second = totalY/thisGroupSize;
        // make_pair(totalX/thisGroupSize, totalY/thisGroupSize);
      }
    }

    void findHospitalLocations() {
      map<int, bool> seen;
      float totalCloestDist_cur=0, totalCloestDist_prev=FLT_MAX;

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
      }
    }

};



int main(int argc, char *argv[]){
  vector<int> ambulance;
  vector<patientInfo> allPatients;

  char separator;
  int num_Patients = 50, num_Hospital = 5, num_Ambulance, count = 0;
  string tmp_string;
  int xloc,yloc,rescuetime;

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
    ambulance.push_back(num_Ambulance);
    count++;
  }

  kMeans myKMean(allPatients, num_Hospital);
  myKMean.findHospitalLocations();
}
















