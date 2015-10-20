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
  int patientIdx,xloc,yloc,rescuetime;
  patientInfo(int myPatientIdx, int myxloc, int myyloc, int myrescuetime): patientIdx(myPatientIdx), xloc(myxloc), yloc(myyloc), rescuetime(myrescuetime){}
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
        // printf("[%d, %d] ", pairs[i].first, pairs[i].second);
      }
      // printf("\n");

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
        // printf("totalX: %d, totalY: %d, thisGroupSize: %d\n", totalX, totalY, thisGroupSize);
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
        // printf("------------------------------\n");
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
          // printf("Group %d: %lu size\n", i, Groups[i].size());
        }

        // printf("totalCloestDist_prev: %f\n", totalCloestDist_prev);
        // printf("totalCloestDist_cur: %f\n", totalCloestDist_cur);
        // cout<<float(fabs(totalCloestDist_cur-totalCloestDist_prev)/totalCloestDist_prev)<<endl;

        // printf("cent_points before:\n");
        // printPairs(cent_points);
        updateCentPoints(Groups);
        // printf("cent_points after:\n");
        // printPairs(cent_points);
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
  int patient_idx, locX, locY, rescuetime;
  bool isHospital;
public:
  //for hospital
  Point_class(int mylocX, int mylocY, bool myisHospital): locX(mylocX), locY(mylocY), isHospital(myisHospital) {}
  //for patient
  Point_class(int myPatientIdx, int mylocX, int mylocY, int myrescuetime, bool myisHospital): patient_idx(myPatientIdx), locX(mylocX), locY(mylocY), rescuetime(myrescuetime), isHospital(myisHospital) {}
  bool getIsHospital() { return isHospital;}
  int getPatientIdex() {return patient_idx;}
  int getX() {return locX;}
  int getY() {return locY;}
  int getRescutime() {return rescuetime;}
  void updateRescuetime(int mytime) {rescuetime = mytime;}

};

class Schedule {
private:
  map< pair<pair<int, int>, pair<int, int> >, int > distanceMap;
  map< int, pair<pair<int, int>, pair<int, int> > > pheromone;
public:
  int findCurrentTime(vector<Point_class> cur_Ambulance) {
    int totalTime=0, numH=0, numP=0;
    if (cur_Ambulance.size() == 1) { return 0; } //has no patient yet
    for (int i=0; i<cur_Ambulance.size()-1; i++) {
      pair<int, int> thisLoc = make_pair(cur_Ambulance[i].getX(), cur_Ambulance[i].getY());
      pair<int, int> nextLoc = make_pair(cur_Ambulance[i+1].getX(), cur_Ambulance[i+1].getY());
      totalTime += getDist(thisLoc, nextLoc);
    }
    for (int i=0; i<cur_Ambulance.size(); i++) {
      if (cur_Ambulance[i].getIsHospital()) { numH++;}
      else {numP++;}
    }
    totalTime += numH-1 + numP;
    return totalTime;
  }
  int getDist(pair<int, int> thisLoc, pair<int, int> thatLoc) {
    int dist;
    if (distanceMap.find(make_pair(thisLoc, thatLoc)) != distanceMap.end()) {
      dist = distanceMap[make_pair(thisLoc, thatLoc)];
    } else {
      dist = abs(thisLoc.first- thatLoc.first)+abs(thisLoc.second-thatLoc.second);
      distanceMap[make_pair(thisLoc, thatLoc)] = dist;
      distanceMap[make_pair(thatLoc, thisLoc)] = dist;
    }
    return dist;
  }
  vector<vector<int> > initPheMap(){
    vector<vector<int> > pheromoneMap(600, vector<int>(600));
    for(int i=0; i<pheromoneMap.size(); i++) {
      for(int j=0; j<pheromoneMap[i].size(); j++) {
        pheromoneMap[i][j] = 0;
      }
    }
    return pheromoneMap;
  }
  int getPheromoneAmount(pair<int, int> curLoc, pair<int, int> patientLoc, int timeNow) {
    int totalPheromoneAmount = 0;
    float midPointX = (curLoc.first+patientLoc.first)/2;
    float xDev = abs(curLoc.first-patientLoc.first)/2;
    float midPointY = (curLoc.second+patientLoc.second)/2;
    float yDev = abs(curLoc.second-patientLoc.second)/2;
    // vector<vector<int> > pheromoneMap = initPheMap();
    for (int timePassed=0; timePassed<timeNow; timePassed++) {
      if (pheromone.find(timePassed) != pheromone.end()) {
        pair<pair<int, int>, pair<int, int> > locations = pheromone[timePassed];
        pair<int, int> prevStartLoc = locations.first;
        pair<int, int> prevEndLoc = locations.second;
        int x1 = min(prevStartLoc.first, prevEndLoc.first);
        int x2 = max(prevStartLoc.first, prevEndLoc.first);
        int x3 = min(curLoc.first, patientLoc.first);
        int x4 = max(curLoc.first, patientLoc.first);
        int y1 = min(prevStartLoc.second, prevEndLoc.second);
        int y2 = max(prevStartLoc.second, prevEndLoc.second);
        int y3 = min(curLoc.second, patientLoc.second);
        int y4 = max(curLoc.second, patientLoc.second);
        int x5 = max(x1, x3);
        int y5 = max(y1, y3);
        int x6 = min(x2, x4);
        int y6 = min(y2, y4);

        bool degradedCheck = (x5 >= x6) & (y5 >= y6);
        if (!degradedCheck) {
          int area = (abs(x5-x6)+1)*(abs(y5-y6)+1);
          totalPheromoneAmount -= area*1; //pheromone panelity
        }
      }
    }
    int myDesireArea = (abs(curLoc.first-patientLoc.first)+1)*(abs(curLoc.second-patientLoc.second)+1);
    totalPheromoneAmount += myDesireArea*timeNow*1;
    return totalPheromoneAmount;
  }
  int findAvailableShortestPatient_idx(pair<int, int> curLoc, vector<patientInfo> allPatients, int timeNow, vector<vector<int> > Hospotials, vector<Point_class> cur_Ambulance) {
    int shortestAvailablePatient_idx = -1;
    float bestMinScore=FLT_MAX; //the smaller the better
    int minDistAmbulanceToPatient=INT_MAX;
    for (int p_idx=0; p_idx<allPatients.size(); p_idx++) {
      int dist_A_P, distPatientToCloestHostipal=INT_MAX;
      float minScore;
      pair<int, int> patientLoc = make_pair(allPatients[p_idx].xloc, allPatients[p_idx].yloc);

      Point_class myPoint(allPatients[p_idx].patientIdx, allPatients[p_idx].xloc,allPatients[p_idx].yloc, allPatients[p_idx].rescuetime, false);
      vector<Point_class> testAmbulanceRout = cur_Ambulance;
      testAmbulanceRout.push_back(myPoint);

      dist_A_P = getDist(curLoc, patientLoc);
      int pheromoneAmountToHere = getPheromoneAmount(curLoc, patientLoc, timeNow);
      // minScore = dist_A_P;
      minScore = dist_A_P/log2(sqrt(allPatients[p_idx].rescuetime));
      // minScore = dist_A_P/log10(sqrt(allPatients[p_idx].rescuetime));
      // printf("original minScore:%f\n",minScore);
      minScore = (dist_A_P/log2(sqrt(allPatients[p_idx].rescuetime)))*pow(0.999999,pheromoneAmountToHere);
      // minScore = pow(0.999,pheromoneAmountToHere);
      // printf("pheromone:%d\tdist_A_P:%d\trescuetime:%d\tminScore:%f\n", pheromoneAmountToHere, dist_A_P, allPatients[p_idx].rescuetime, minScore);
      // minScore = 1/log2(pheromoneAmountToHere);

      for (int hop_idx=0; hop_idx<Hospotials.size(); hop_idx++) {
        pair<int, int> hospotialLoc = make_pair(Hospotials[hop_idx][0],Hospotials[hop_idx][1]);
        int dis_P_H = getDist(hospotialLoc, patientLoc);
        if (distPatientToCloestHostipal > dis_P_H) {
          distPatientToCloestHostipal = dis_P_H;
        }
      }
      if (noPatienWouldDie(findCurrentTime(testAmbulanceRout), distPatientToCloestHostipal, testAmbulanceRout) && bestMinScore > minScore) {
      // if (noPatienWouldDie(findCurrentTime(testAmbulanceRout), distPatientToCloestHostipal, testAmbulanceRout) && minDistAmbulanceToPatient > dist_A_P) {
        bestMinScore = minScore;
        // minDistAmbulanceToPatient = dist_A_P;
        shortestAvailablePatient_idx = p_idx;
      }
    }
    return shortestAvailablePatient_idx;

  }
  void updatePheromone(pair<int, int> AmbulanceLoc, pair<int, int> PatientLoction, int timeNow) {
    pheromone[timeNow] = make_pair(AmbulanceLoc, PatientLoction);
  }
  int findPatientOnRoute(vector<Point_class> cur_Ambulance, vector<patientInfo> allPatients, vector<vector<int> > Hospotials) {
    int timeNow = findCurrentTime(cur_Ambulance);
    // cout<<"timeNow: "<<timeNow<<endl;
    int curX = cur_Ambulance[cur_Ambulance.size()-1].getX();
    int curY = cur_Ambulance[cur_Ambulance.size()-1].getY();
    // cout<<"findPatientOnRoute. allPatients.size(): "<< allPatients.size()<<endl;
    int patient_idx = findAvailableShortestPatient_idx(make_pair(curX, curY), allPatients, timeNow, Hospotials, cur_Ambulance);
    if (patient_idx != 1) {
      updatePheromone(make_pair(curX,curY), make_pair(allPatients[patient_idx].xloc, allPatients[patient_idx].yloc), timeNow);
    }
    // printf("my location: [%d,%d]\tShortest Patient Location: [%d,%d,%d]\n", curX, curY, allPatients[patient_idx].xloc, allPatients[patient_idx].yloc, allPatients[patient_idx].rescuetime);
    return patient_idx;
  }

  bool noPatienWouldDie(int timeNow, int dist2H, vector<Point_class> cur_Ambulance) {
    timeNow = findCurrentTime(cur_Ambulance);
    int idxOfPatientOnCar;
    for (idxOfPatientOnCar=cur_Ambulance.size()-1; idxOfPatientOnCar>0; idxOfPatientOnCar--) {
      if(cur_Ambulance[idxOfPatientOnCar].getIsHospital()) {break;}
    }
    idxOfPatientOnCar++;

    for (idxOfPatientOnCar=idxOfPatientOnCar; idxOfPatientOnCar<cur_Ambulance.size(); idxOfPatientOnCar++) {
      if (cur_Ambulance[idxOfPatientOnCar].getRescutime() < timeNow+dist2H+2 ){
        return false;
      }
    }
    return true;
  }

  int findHosptialOfCurrentRout(vector<Point_class> cur_Ambulance, vector<vector<int> > Hospotials) {
    // cout<<"findHosptialOfCurrentRout"<<endl;
    int shortest_dist2H = INT_MAX;
    vector<int> shortest_hospital;
    int shortest_hospital_idx=-1;
    int timeNow = findCurrentTime(cur_Ambulance);
    int curX = cur_Ambulance[cur_Ambulance.size()-1].getX();
    int curY = cur_Ambulance[cur_Ambulance.size()-1].getY();
    pair <int,int> myLoc = make_pair(curX, curY);

    //find the shortest hospital that patient won't die
    for(int i=0; i<Hospotials.size(); i++) {
      pair <int,int> thisHospitalLoc = make_pair(Hospotials[i][0], Hospotials[i][1]);
      int dist2H = getDist(myLoc, thisHospitalLoc);
      // if (!noPatienWouldDie(timeNow, dist2H, cur_Ambulance)) {
      //   cout<<"patient will die if choose this hospital"<<endl;
      // }
      if (noPatienWouldDie(timeNow, dist2H, cur_Ambulance) && shortest_dist2H > dist2H) {
        shortest_dist2H = dist2H;
        shortest_hospital = Hospotials[i];
        shortest_hospital_idx = i;
      }
    }
    // cout<<"shortest_hospital_idx: "<<shortest_hospital_idx<<endl;
    return shortest_hospital_idx;
    // printf("found shortest_hospital: [%d,%d]\n", shortest_hospital[0], shortest_hospital[1]);

    // Point_class myPoint(shortest_hospital[0], shortest_hospital[1], true); //init a point
    // cur_Ambulance.push_back(myPoint);

  }

  void printAmbulance(vector<vector<Point_class> > &Ambulances) {
    for (int i=0; i<Ambulances.size(); i++) {
      int ambulance_idx = i+1;
      vector<Point_class> ambulance_path = Ambulances[i];

      for(int eachPoint_idx=0; eachPoint_idx<ambulance_path.size(); eachPoint_idx++) {
        Point_class thisPoint = ambulance_path[eachPoint_idx];
        if ( (eachPoint_idx!=ambulance_path.size()-1) && (thisPoint.getIsHospital()) ){
          if (ambulance_path[eachPoint_idx+1].getIsHospital()) {
            continue;
          }
          printf("Ambulance:%d|%d,%d|", ambulance_idx, thisPoint.getX(), thisPoint.getY());
        }
        else if (!thisPoint.getIsHospital()) {
          int marching_idx = eachPoint_idx+1;
          while(marching_idx<ambulance_path.size() && !ambulance_path[marching_idx].getIsHospital()) {
            marching_idx++;
          }
          for(int tmpIdx=eachPoint_idx; tmpIdx<marching_idx; tmpIdx++) {
            Point_class thisPoint = ambulance_path[tmpIdx];
            if (tmpIdx<marching_idx-1){
              printf("%d,%d,%d,%d;", thisPoint.getPatientIdex(), thisPoint.getX(), thisPoint.getY(), thisPoint.getRescutime());
            } else {
              printf("%d,%d,%d,%d|", thisPoint.getPatientIdex(), thisPoint.getX(), thisPoint.getY(), thisPoint.getRescutime());
            }
          }
          if (marching_idx<ambulance_path.size()){
            Point_class thisPoint = ambulance_path[marching_idx];
            printf("%d,%d\n", thisPoint.getX(), thisPoint.getY());
            eachPoint_idx = marching_idx-1;
          } else {
            printf("\n");
          }
        }
      }
    }
  }
  void patientTimeToLiveUpdate(vector<Point_class> &cur_Ambulance) {
    int timeNow = findCurrentTime(cur_Ambulance);
    for(int idx=cur_Ambulance.size()-1-1; !cur_Ambulance[idx].getIsHospital(); idx--) {
      cur_Ambulance[idx].updateRescuetime(cur_Ambulance[idx].getRescutime()-timeNow);
    }
  }
  int numOfPatientOnCar(vector<Point_class> cur_Ambulance) {
    int patientCount = 0;
    for(int idx = cur_Ambulance.size()-1; !cur_Ambulance[idx].getIsHospital(); idx--) {
      patientCount++;
    }
    return patientCount;
  }

  void ambulanceScheduling(vector<vector<Point_class> > &Ambulances, vector<patientInfo> &allPatients, vector<vector<int> > Hospotials) {
    int noPatientCanSavedCount = 0;
    while( noPatientCanSavedCount!= Ambulances.size() & allPatients.size()>0) {
      noPatientCanSavedCount = 0;

      for(int ambu_idx=0; ambu_idx<Ambulances.size(); ambu_idx++) {
        // printf("ambulance idex: %d\t", ambu_idx+1);
        vector<Point_class> cur_Ambulance = Ambulances[ambu_idx];
        if (numOfPatientOnCar(cur_Ambulance)==4) {
          //meet max capacity. find cloest hospital
          // printf("Too many patient on car: %lu\n", cur_Ambulance.size());
          int hotel_idx = findHosptialOfCurrentRout(cur_Ambulance, Hospotials);
          Point_class myPoint(Hospotials[hotel_idx][0], Hospotials[hotel_idx][1], true); //init a point
          Ambulances[ambu_idx].push_back(myPoint);
          patientTimeToLiveUpdate(Ambulances[ambu_idx]);
          // printf("after findHosptialOfCurrentRout: %lu\n", cur_Ambulance.size());
          continue;
        }

        int patient_idx = findPatientOnRoute(cur_Ambulance, allPatients, Hospotials);

        if (patient_idx==-1) {
          //no available patient for this ambulance. find cloest hospital
          // printf("Need to return hospital\n");
          noPatientCanSavedCount++;
          int hotel_idx = findHosptialOfCurrentRout(cur_Ambulance, Hospotials);
          Point_class myPoint(Hospotials[hotel_idx][0], Hospotials[hotel_idx][1], true); //init a point
          Ambulances[ambu_idx].push_back(myPoint);
          patientTimeToLiveUpdate(Ambulances[ambu_idx]);
          continue;
        }

        Point_class myPoint(allPatients[patient_idx].patientIdx, allPatients[patient_idx].xloc,allPatients[patient_idx].yloc, allPatients[patient_idx].rescuetime, false);
        Ambulances[ambu_idx].push_back(myPoint);
        allPatients.erase (allPatients.begin()+patient_idx);
      }
      // printAmbulance(Ambulances);
      // printf("----------------------------- %lu Patient Remained  -----------------------------\n", allPatients.size());
    }
  }

};


int main(int argc, char *argv[]){
  char separator;
  int num_Patients = 300, num_Hospital = 5, num_Ambulance, count = 0;
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
    // printf("%d\t%d\t%d\n", xloc, yloc, rescuetime);
    patientInfo myPatient(count+1, xloc, yloc, rescuetime);
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
    // printf("group:%d\tnumPatients:%d\tlocation:[%d,%d]\n", i, groupSize_centerPorint[i].first, groupSize_centerPorint[i].second.first, groupSize_centerPorint[i].second.second);
  }

  //
  for(int i=0; i<hospotials_tmp.size(); i++) {
    int hospital_idx = hospotials_tmp[i].first;
    int num_Ambulance = hospotials_tmp[i].second;
    int hospital_locX= groupSize_centerPorint[i].second.first;
    int hospital_locY= groupSize_centerPorint[i].second.second;
    // printf("hospotial idx:%d\tnumAmbulance:%d\tlocation:[%d,%d]\n", hospital_idx, num_Ambulance, hospital_locX, hospital_locY);

    vector<int> myHospitalInfo;
    //locX, locY, num_Ambulance
    myHospitalInfo.push_back(hospital_locX); myHospitalInfo.push_back(hospital_locY); myHospitalInfo.push_back(num_Ambulance);
    Hospotials[hospital_idx] = myHospitalInfo;
  }

  int ambulance_idx = 0;
  for(int i=0; i<Hospotials.size(); i++) {
    printf("Hospital:%d|%d,%d,%d|", i+1, Hospotials[i][0], Hospotials[i][1], Hospotials[i][2]);
    for(int numAmbulance=0; numAmbulance<Hospotials[i][2]; numAmbulance++) {

      Point_class myPoint(Hospotials[i][0], Hospotials[i][1], true); //init a point
      vector<Point_class> tmp_AmbulancePath; //init a path vector for this ambulance
      tmp_AmbulancePath.push_back(myPoint);
      Ambulances.push_back(tmp_AmbulancePath); //push path vector or Ambulances

      if (numAmbulance==Hospotials[i][2]-1) {
        printf("%d\n", ambulance_idx+1);
      } else {
        printf("%d,", ambulance_idx+1);
      }
      ambulance_idx++;
    }
  }

  Schedule scheduleClass;
  scheduleClass.ambulanceScheduling(Ambulances, allPatients, Hospotials);
  scheduleClass.printAmbulance(Ambulances);
}
















