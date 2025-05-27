/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Atmosphere.h
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




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
  svector *_climzones; // climate zones should corresponds to the number of columns for climate inputs

  /* Climate */
  svector *_P;  // Precipitation [m]
  ifstream if__P;  // Precipitation [m]
  svector *_Ta;  // Air temperature [degree C]
  ifstream if__Ta;  // Air temperature [degree C]
  svector *_RH;  // Relative humidity [decimal]
  ifstream if__RH;  // Relative humidity [decimal]
  svector *_PET;  // Potential evapotranspiration [m]
  ifstream if__PET;  // Potential evapotranspiration [m]
  svector *_airpressure;  // Air pressure [Pa]
  ifstream if__airpressure;  // Air pressure [Pa]
  svector *_Rnet;  // Net radiation [W/m2]
  ifstream if__Rnet;  // Net radiation [W/m2]
  svector *_windspeed;  // Wind speed at 2 m [m/s]
  ifstream if__windspeed;  // Wind speed at 2 m [m/s]
  svector *_d18o_P;  // d18O in precipitation [‰]
  ifstream if__d18o_P;  // d18O in precipitation [‰]
  /* end of Climate */


  
  Atmosphere(Control &ctrl);  // constrcuctor of Basin
  //dtor
  ~Atmosphere();  // destrcuctor of Atmos
  int dtor(Control &ctrl);

  // Climate inputs
  int open_climate(Control &ctrl);
  int read_climate(Control &ctrl);
  int open_climate_maps(string fname, ifstream &ifHandle);
  int read_climate_maps(ifstream &ifHandle, svector &climateMap);

  int init_climate(Control &ctrl);
  int update_climate(Control &ctrl);
  int init_climate_maps(string fname, ifstream &ifHandle);
  int update_climate_maps(ifstream &ifHandle, svector &climateMap);

};

#endif