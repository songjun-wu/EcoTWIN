/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2026   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* read_time_series.cpp
  * Created  on: 30.09.2026
  * Modified on: 30.09.2026
***************************************************************/


#include "Atmosphere.h"

int Atmosphere::open_climate_time_series(Control &ctrl){
  if (ctrl.opt_carbon_sim == 1){
    open_climate_TS(ctrl.path_ClimateFolder + ctrl.fn__atmCO2_db, if__atmCO2_db);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate_time_series(Control &ctrl){
  if (ctrl.opt_carbon_sim == 1){
    read_climate_TS(if__atmCO2_db, _atmCO2_db);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::open_climate_TS(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file not found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate_TS(ifstream &ifHandle, double &climateValue){
  double value;
  ifHandle.read((char *)&value, sizeof(double));
  climateValue = value;
  return EXIT_SUCCESS;
}