/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Statistic_summary.cpp
  * Created  on: 23.12.2025
  * Modified on: 23.12.2025
***************************************************************/


#include "Basin.h"


int Basin::Statistic_summary(Control &ctrl, Param &par) {
    
    // Summary hydrological statistics
    Hydrology_summary();

    // Summary carbon statistics
    if (ctrl.opt_carbon_sim==1){
      Carbon_summary(ctrl, par);
    }

    // Summary nitrogen statistics
    if (ctrl.opt_nitrogen_sim==1){
      Nitrogen_summary(ctrl, par);
    }


    return EXIT_SUCCESS;
}