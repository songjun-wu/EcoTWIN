/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_summary.cpp
  * Created  on: 17.12.2025
  * Modified on: 17.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Carbon_summary(Control &ctrl, Param &par){

    // Summary carbon pools
    if (ctrl.opt_summary_statistics==1){
      for (int j = 0; j < _sortedGrid.row.size(); j++){
        _plant_C->val[j] = _plant_green_CP->val[j] + _plant_reserve_CP->val[j] + _plant_wood_CP->val[j];  // Total vegetation carbon [gC/m2]  
      }
    }

    return EXIT_SUCCESS;
}
