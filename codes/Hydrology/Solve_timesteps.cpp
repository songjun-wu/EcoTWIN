/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_timesteps.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"


int Basin::Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm) {
    
    // For debug
    //int j = 7;  // todo; 6806, 13
    //cout << ctrl.year << "-"<<ctrl.month<<"-"<<ctrl.day<<"     ";  // todo
    //for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) { // todo
    //}

    

    Solve_canopy(ctrl, par, atm);

    Solve_surface(ctrl, par, atm);

    Solve_soil_profile(ctrl, par, atm);

    Routing(ctrl, par);

    Solve_channel(ctrl, par, atm);

    //Check_mass_balance(ctrl, par, atm);

    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1 or ctrl.opt_nitrogen_sim==1){
        Store_states();  // Store all water storages for mixing
    }

    

    return EXIT_SUCCESS;
}