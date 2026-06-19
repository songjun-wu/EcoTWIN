/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Parameter_correction.cpp
  * Created  on: 06.04.2026
  * Modified on: 06.04.2026
***************************************************************/


#include "Basin.h"

int Basin::Parameter_correction(Control &ctrl, Param &par){



  // Drainage intensity needs to be corrected by reference drainage density
  if (ctrl.opt_drainage==1){
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      par._drainage_intensity->val[j] = min(1.0, par._drainage_intensity->val[j]*_reference_drainage_density->val[j]);
    }
  }

  if (ctrl.opt_carbon_sim==1){
    // Maximum carbon content in wood pool needs to be corrected by spatial maps of forest biomass (in gC/m2)
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      par._plant_wood_CP_max->val[j] *= _plant_wood_CP_forest_max->val[j];
      par._decomposition_weight_humus_pool->val[j] *= _humus_decomposition_spatial_weights->val[j];  // Correction of decomposition rates of humus pool based on the spatial pattern of soil carbon storage [-]
    }
  }



  par.sort_parameter_correction_OK = 1;
  
  return EXIT_SUCCESS;
}