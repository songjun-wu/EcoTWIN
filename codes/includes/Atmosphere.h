#ifndef Atmosphere_H_
#define Atmosphere_H_

#include "Param.h"

#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Atmosphere {

  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  sortedGrid _sortedGrid;
  int _nzones;
  /* end of Properties */
  
  public:
  grid *_climzones; // climate zones should corresponds to the number of columns for climate inputs

  /* Climate */
  grid *_P;  // Precipitation [m]
  ifstream if__P;  // Precipitation [m]
  grid *_Ta;  // Air temperature [degree C]
  ifstream if__Ta;  // Air temperature [degree C]
  grid *_Tmin;  // Minimum air temperature [degree C]
  ifstream if__Tmin;  // Minimum air temperature [degree C]
  grid *_Tmax;  // Maximum air temperature [degree C]
  ifstream if__Tmax;  // Maximum air temperature [degree C]
  grid *_RH;  // Relative humidity [decimal]
  ifstream if__RH;  // Relative humidity [decimal]
  grid *_LAI;  // Leaf area index [decimal]
  ifstream if__LAI;  // Leaf area index [decimal]
  /* end of Climate */


  
  Atmosphere(Control &ctrl);  // constrcuctor of Basin
  //dtor
  ~Atmosphere();  // destrcuctor of Basin

  int open_climate(Control &ctrl);
  int read_climate(Control &ctrl);
  int open_climate_maps(string fname, ifstream &ifHandle);
  int read_climate_maps(ifstream &ifHandle, grid &climateMap);

  int init_climate(Control &ctrl);
  int update_climate(Control &ctrl);
  int init_climate_maps(string fname, ifstream &ifHandle);
  int update_climate_maps(ifstream &ifHandle, grid &climateMap);

};

#endif