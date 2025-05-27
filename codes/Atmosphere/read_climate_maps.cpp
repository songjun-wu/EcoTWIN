/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* read_climate_maps.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Atmosphere.h"

int Atmosphere::open_climate(Control &ctrl){
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  if (ctrl.opt_evap == 1){
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__PET, if__PET);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__airpressure, if__airpressure);
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Rnet, if__Rnet);
  }
  if (ctrl.opt_chanE == 1){
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__windspeed, if__windspeed);
  }
  if (ctrl.opt_tracking_isotope == 1){
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__d18o_P, if__d18o_P);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate(Control &ctrl){
  read_climate_maps(if__P, *_P);
  read_climate_maps(if__Ta, *_Ta);
  read_climate_maps(if__RH, *_RH);
  if (ctrl.opt_evap == 1){
    read_climate_maps(if__PET, *_PET);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    read_climate_maps(if__airpressure, *_airpressure);
    read_climate_maps(if__Rnet, *_Rnet);
  }
  if (ctrl.opt_chanE == 1){
    read_climate_maps(if__windspeed, *_windspeed);
  }
  if (ctrl.opt_tracking_isotope == 1){
    read_climate_maps(if__d18o_P, *_d18o_P);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::open_climate_maps(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file not found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate_maps(ifstream &ifHandle, svector &climateMap){
  double *data=NULL;
  int dim  = _rowNum*_colNum;
  int r, c;

  data = new double[dim];
  ifHandle.read((char *)data, sizeof(double)*dim);

  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    r = _sortedGrid.row[j];
    c = _sortedGrid.col[j];
    climateMap.val[j] = data[r*_colNum + c];
  }

  delete[] data;
  return EXIT_SUCCESS;
}

int Atmosphere::init_climate(Control &ctrl){
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  if (ctrl.opt_evap == 1){
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__PET, if__PET);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__airpressure, if__airpressure);
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Rnet, if__Rnet);
  }
  if (ctrl.opt_chanE == 1){
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__windspeed, if__windspeed);
  }
  if (ctrl.opt_tracking_isotope == 1){
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__d18o_P, if__d18o_P);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::update_climate(Control &ctrl){
  update_climate_maps(if__P, *_P);
  update_climate_maps(if__Ta, *_Ta);
  update_climate_maps(if__RH, *_RH);
  if (ctrl.opt_evap == 1){
    update_climate_maps(if__PET, *_PET);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    update_climate_maps(if__airpressure, *_airpressure);
    update_climate_maps(if__Rnet, *_Rnet);
  }
  if (ctrl.opt_chanE == 1){
    update_climate_maps(if__windspeed, *_windspeed);
  }
  if (ctrl.opt_tracking_isotope == 1){
    update_climate_maps(if__d18o_P, *_d18o_P);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::init_climate_maps(string fname, ifstream &ifHandle){
  int max = 0;
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file now found    :" + fname);
  }
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    if (_climzones->val[j] > max){
      max = _climzones->val[j];
    }
  }

  _nzones = max + 1; // Climate zone starts from 0 after correction

  return EXIT_SUCCESS;
}

int Atmosphere::update_climate_maps(ifstream &ifHandle, svector &climateMap){
  double *data=NULL;
  int zoneID;
  data = new double[_nzones];
  ifHandle.read((char *)data, sizeof(double)*_nzones);  
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

    zoneID = _climzones->val[j];
    climateMap.val[j] = data[zoneID];
    }
  
  delete[] data;
  return EXIT_SUCCESS;
}