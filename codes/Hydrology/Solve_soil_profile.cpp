#include "Basin.h"

int Basin::Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm){
   
    // Hydraulic proporties
    if (par.param_category->sort_PTF == 0){
        // Estimate saturated hydraulic conductivity, field capacity, and wilting point
        Soil_proporty(ctrl, par);
        par.param_category->sort_PTF = 1;
    }
    // Root fraction
    if (ctrl.opt_evap == 1 or ctrl.opt_nitrogen_sim==1){
        Sort_root_fraction(ctrl, par);
    }
    // Travel time of percolation
    if (ctrl.opt_percolation == 1){
        Sort_percolation_travel_time(ctrl, par);
    }

    
    // Infiltration
    if (ctrl.opt_infil == 1){
        Infiltration_1(ctrl, par);
    }

    

    // Percolation
    if (ctrl.opt_percolation == 1){
        Percolation_1(ctrl, par);
        GWrecharge_1(ctrl, par);
    } else if (ctrl.opt_percolation == 2){
        Percolation_2(ctrl, par);
        GWrecharge_2(ctrl, par);
    } else if (ctrl.opt_percolation == 3){
        Percolation_3(ctrl, par);
        GWrecharge_2(ctrl, par);  // todo
    }

    
    // Evapotranspiratioin
    if (ctrl.opt_evap==1){
        Seperate_PET(par, atm);
        Evapotranspiration_1(ctrl, par, atm);
    }

    
    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_soil_profile_tracking(ctrl, atm, par);  // d18o change due to canopy mixing and evaporation
        Mixing_GW_tracking(ctrl, atm);  // // GW storage mixing
    }

    if (ctrl.opt_nitrogen_sim==1){
        Solve_soil_profile_nitrogen(ctrl, atm, par);
        Solve_GW_nitrogen(ctrl, atm);
    }




    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1 or ctrl.opt_nitrogen_sim==1){
        // Store all water storages for routing mixing
        // States update happens after soil mixing
        // Do not activate when checking the hydrological mass balance
        Store_states();  
        
    }
    
   
    return EXIT_SUCCESS;
}
