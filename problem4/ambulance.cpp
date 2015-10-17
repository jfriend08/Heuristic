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
    patientInfo myPatient(xloc, yloc, rescuetime);
    allPatients.push_back(myPatient);
    count++;
  }

  cin >> tmp_string;
  count = 0;
  while (count < num_Hospital) {
    cin >> num_Ambulance;
    printf ("num_Ambulance: %d\n", num_Ambulance);
    ambulance.push_back(num_Ambulance);
    count++;
  }

  for (int i=0; i<allPatients.size(); i++){
    printf ("%d\t%d\t%d\n", allPatients[i].xloc, allPatients[i].yloc, allPatients[i].rescuetime);
  }


}
















