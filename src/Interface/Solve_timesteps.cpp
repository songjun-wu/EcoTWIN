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
    //int j = _sortedGrid.row.size()-1;
    //int j = 1;  // todo; 858 forest, 1127 cropland, 3367 Alpine
    //cout <<endl<<ctrl.year << "-"<<ctrl.month<<"-"<<ctrl.day<<"     ";  // todo
    //for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) { // todo
      //if (_sortedGrid.row[j] == 1 and _sortedGrid.col[j] == 11) cout << j<<"  "; // todo
    //}



    Initialisation_each_timestep(ctrl, par);
    Solve_canopy(ctrl, par, atm);
    Solve_surface(ctrl, par, atm);
    Solve_soil_profile(ctrl, par, atm);
    Solve_routing(ctrl, par);
    Solve_channel(ctrl, par, atm);



    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1 or ctrl.opt_carbon_sim==1 or ctrl.opt_nitrogen_sim==1){
        Store_states();  // Store all water storages for mixing
    }

    Statistic_summary(ctrl, par);



    
    return EXIT_SUCCESS;
}