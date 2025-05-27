/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* AtmosphereConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


 #include "Atmosphere.h"

 Atmosphere::Atmosphere(Control &ctrl){

  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;

  _sortedGrid = ctrl._sortedGrid;

  /* Climate */
  _P = new svector(_sortedGrid.size);
  _Ta = new svector(_sortedGrid.size);
  _RH = new svector(_sortedGrid.size);
  if (ctrl.opt_evap == 1){
    _PET = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    _airpressure = new svector(_sortedGrid.size);
    _Rnet = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_chanE == 1){
    _windspeed = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_tracking_isotope == 1){
    _d18o_P = new svector(_sortedGrid.size);
  }
  /* end of Climate */


  if (ctrl.opt_climate_input_format == 2) {
    _climzones = new svector(ctrl.path_BasinFolder + ctrl.fn__climzones, _rowNum, _colNum, _sortedGrid);
  }

  // Climate zone starts from 0 after correction (1 in inputs)
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    _climzones->val[j] -= 1;
  }

  
  if (ctrl.opt_climate_input_format == 1){
    open_climate(ctrl);
    read_climate(ctrl);
  } else if  (ctrl.opt_climate_input_format == 2) {
    init_climate(ctrl); // create maps for climate parameters
    update_climate(ctrl); // update maps for climate parameters
  }
  
 }