/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_soil_profile.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm){
    

    // Infiltration
    if (ctrl.opt_infil == 1){
        Infiltration_1(ctrl, par);
    }


    // Percolation (and drainage if activated)
    if (ctrl.opt_percolation == 1){
        Percolation_1(ctrl, par);
        Capillary_flow(ctrl, par);
        GWrecharge_1(ctrl, par);
    } else if (ctrl.opt_percolation == 2){
        Percolation_2(ctrl, par);
        Capillary_flow(ctrl, par);
        GWrecharge_2(ctrl, par);
    } else if (ctrl.opt_percolation == 3){
        Percolation_3(ctrl, par);
        Capillary_flow(ctrl, par);
        GWrecharge_2(ctrl, par);  // todo
    }

    

    // Evapotranspiratioin
    if (ctrl.opt_evap==1){
        Seperate_PET(par, atm);
        Evapotranspiration_1(ctrl, par, atm);
    } else if (ctrl.opt_evap==2){
        //Seperate_PET(par, atm);
        Evapotranspiration_2(ctrl, par, atm);
    }

    
    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_soil_profile_tracking(ctrl, atm, par);  // d18o change due to canopy mixing and evaporation
        Mixing_vadose_tracking(ctrl, atm);  // Vadose storage mixing
        Mixing_GW_tracking(ctrl, atm);  // GW storage mixing
    }

    // Carbon and nitrogen
    if (ctrl.opt_carbon_sim==1 or ctrl.opt_nitrogen_sim==1){
        Solve_soil_profile_nutrient(ctrl, atm, par);
        Solve_vadose_nutrient(ctrl, atm);
        Solve_GW_nutrient(ctrl, atm);
    }




    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1 or ctrl.opt_nitrogen_sim==1){
        // Store all water storages for routing mixing
        // States update happens after soil mixing
        // Do not activate when checking the hydrological mass balance
        Store_states();  
        
    }
    
   
    return EXIT_SUCCESS;
}
