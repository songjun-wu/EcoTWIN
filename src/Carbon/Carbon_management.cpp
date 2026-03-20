/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Redistribution and modification are allowed under proper acknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_management.cpp
  * Created  on: 15.03.2026
  * Modified on: 15.03.2026
***************************************************************/


#include "Basin.h"

int Basin::Carbon_management(Control &ctrl, Param &par){


  double plant_green_CP, plant_wood_CP, plant_reserve_CP;  // Vegetation pools [gC/m2]
  int idx_last_land_use;  // Index of last land use category
  double N_biological_fixiation;  // Biological nitrogen fixation [gN/m2]


  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    
    plant_green_CP = _plant_green_CP->val[j];
    plant_wood_CP = _plant_wood_CP->val[j];
    plant_reserve_CP = _plant_reserve_CP->val[j];

    // Harvest and Herbivory loss: loss from plant_green_CP due to harvest and herbivory [gC/m2]
    // Herbivory loss
    plant_green_CP *= (1 - par._herbivory_uptake_coeff->val[j]);
    plant_reserve_CP *= (1 - par._herbivory_uptake_coeff->val[j]);

    // Crop harvest loss
    idx_last_land_use = ctrl.num_category - 1;
    if (ctrl.day_of_year==harvest_day[idx_last_land_use]){
      plant_green_CP *= (1 - par._harvest_coeff->val[j]);
      plant_reserve_CP *= (1 - par._harvest_coeff->val[j]);
    }

    // Update vegetation carbon pools    
    _plant_green_CP->val[j] = plant_green_CP;
    _plant_wood_CP->val[j] = plant_wood_CP;
    _plant_reserve_CP->val[j] = plant_reserve_CP;


    if (ctrl.opt_nitrogen_sim==1){
      // Biological nitrogen fixation based on NPP
      N_biological_fixiation = max(0.0, 0.7 * (1 - exp(-0.003 * _NPP->val[j])) * 14 / 12);
      _no3_layer1->val[j] += N_biological_fixiation * _froot_layer1->val[j] / (_theta1->val[j] * _depth1->val[j]);
      _no3_layer2->val[j] += N_biological_fixiation * _froot_layer2->val[j] / (_theta2->val[j] * _depth2->val[j]);
      _no3_layer3->val[j] += N_biological_fixiation * _froot_layer3->val[j] / (_theta3->val[j] * par._depth3->val[j]);
    }

  }  // end for (unsigned int j = 0; j < _sortedGrid.row.size(); j++)

    return EXIT_SUCCESS;
}

