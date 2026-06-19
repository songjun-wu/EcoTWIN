/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ControlConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Control.h"

Control::Control(){

  current_ts = 0;

  basetime = Set_reference_timestep();

  string confilename = "config.ini";

  ReadConfigFile(confilename);
  getAsciiHeader(path_BasinFolder+fn__depth1);

  //sort grids spatially
  _fdir = new grid(path_BasinFolder + fn__fdir, _rowNum, _colNum);
  _chnwidth_grid = new grid(path_BasinFolder + fn__chnwidth, _rowNum, _colNum);
  _sortedGrid = SortGridLDD();
  
  _Gauge_to_Report = new svector(path_BasinFolder + fn__Gauge_to_Report, _rowNum, _colNum, _sortedGrid);
  _Tsmask = sortTSmask();


  // ===== Option correction =====
  // Nitrogen simulation is dependent on carbon simulation
  if (opt_nitrogen_sim==1){
    opt_carbon_sim = 1;
  }
  // Summary statistics
  if (opt_summary_statistics==0){
    if (opt_carbon_sim==1){
      report__plant_C = 0;
      report__soluble_C = 0;
    }
    if (opt_nitrogen_sim==1){
      report__fast_N = 0;
      report__humus_N = 0;
    }
  }

  
}