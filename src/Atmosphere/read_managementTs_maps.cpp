/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* read_managementTs_maps.cpp
  * Created  on: 22.12.2025
  * Modified on: 22.12.2025
***************************************************************/


#include "Basin.h"

int Basin::open_managementTs(Control &ctrl){
  if (ctrl.opt_drainage == 1){
    open_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn__drainage_depth, if__drainage_depth);
  }
  return EXIT_SUCCESS;
}

int Basin::read_managementTs(Control &ctrl){
  if (ctrl.opt_drainage == 1){
    read_groundTs_maps(if__drainage_depth, *_drainage_depth);
  }
  return EXIT_SUCCESS;
}

int Basin::init_managementTs(Control &ctrl){
  if (ctrl.opt_drainage == 1){
    init_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn__drainage_depth, if__drainage_depth);
  }
  return EXIT_SUCCESS;
}

int Basin::update_managementTs(Control &ctrl, Param &par){
  if (ctrl.opt_drainage == 1){
    update_groundTs_maps(if__drainage_depth, par, *_drainage_depth);
  }
  return EXIT_SUCCESS;
}

// End of file