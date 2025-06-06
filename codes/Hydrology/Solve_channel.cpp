/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_channel.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_channel(Control &ctrl, Param &par, Atmosphere &atm){
   
    if (ctrl.opt_chanE == 1){
        Channel_evaporation_1(ctrl, atm, par);
    } else if  (ctrl.opt_chanE == 2){
        Channel_evaporation_2(ctrl, atm, par);
    }

    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_channel_tracking(ctrl, atm, par);
    }

    if (ctrl.opt_nitrogen_sim==1){
        Solve_channel_nitrogen(ctrl, atm, par);
    }
    
   
    return EXIT_SUCCESS;
}
