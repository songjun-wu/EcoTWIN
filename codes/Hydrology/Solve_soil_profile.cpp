#include "Basin.h"

int Basin::Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm){

    if (par.param_category->sort_PTF == 0){
        // Estimate saturated hydraulic conductivity, field capacity, and wilting point
        Soil_proporty(ctrl, par);
        par.param_category->sort_PTF = 1;
    }

    

    if (ctrl.opt_infil == 1){
        Infiltration_1(ctrl, par);
    }


    if (ctrl.opt_percolation == 1){
        Percolation_1(ctrl, par);
    } else if (ctrl.opt_percolation == 2){
        Percolation_2(ctrl, par);
    } else if (ctrl.opt_percolation == 3){
        Percolation_3(ctrl, par);
    }

    if (ctrl.opt_recharge == 1){
        GWrecharge_1(ctrl, par);
    }


    if (ctrl.opt_evap==1){
        Seperate_PET(par, atm);
        Evapotranspiration_1(ctrl, par, atm);
    }
    

    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_soil_profile(ctrl, atm, par);  // d18o change due to canopy mixing and evaporation
    }
   
    return EXIT_SUCCESS;
}
