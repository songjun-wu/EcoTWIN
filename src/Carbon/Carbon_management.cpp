/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Redistribution and modification are allowed under proper acknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_management.cpp
  * Created  on: 15.03.2026
  * Modified on: 15.03.2026
***************************************************************/


#include "Basin.h"

int Basin::Carbon_management(Control &ctrl, Param &par){


  double plant_green_CP, plant_reserve_CP;  // Vegetation pools [gC/m2]
  double plant_mobile_N;  // Plant mobile nitrogen [gN/m2]
  int idx_last_land_use;  // Index of last land use category


  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    
    plant_green_CP = _plant_green_CP->val[j];
    plant_reserve_CP = _plant_reserve_CP->val[j];
    plant_mobile_N = _plant_mobile_NP->val[j];

    // Harvest and Herbivory loss: loss from plant_green_CP due to harvest and herbivory [gC/m2]
    // === Herbivory loss ===
    plant_green_CP *= (1 - par._herbivory_uptake_coeff->val[j]);
    plant_reserve_CP *= (1 - par._herbivory_uptake_coeff->val[j]);
    plant_mobile_N *= (1 - par._herbivory_uptake_coeff->val[j]);

    // === Crop harvest loss ===
    idx_last_land_use = ctrl.num_category - 1;
    if (ctrl.day_of_year==harvest_day[idx_last_land_use]){
      plant_green_CP *= (1 - par._harvest_coeff->val[j]);
      plant_reserve_CP *= (1 - par._harvest_coeff->val[j]);
      plant_mobile_N *= (1 - par._harvest_coeff->val[j]);
    }

    // Update vegetation carbon pools    
    _plant_green_CP->val[j] = plant_green_CP;
    _plant_reserve_CP->val[j] = plant_reserve_CP;
    _plant_mobile_NP->val[j] = plant_mobile_N;



  }  // end for (unsigned int j = 0; j < _sortedGrid.row.size(); j++)

    return EXIT_SUCCESS;
}

