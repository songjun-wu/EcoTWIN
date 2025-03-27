#include "Basin.h"

int Basin::Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm){

    if (par.param_category->sort_soil_profile_OK == 0){
        // Estimate saturated hydraulic conductivity, field capacity, and wilting point
        Soil_proporty(ctrl, par);
        par.param_category->sort_soil_profile_OK = 1;
    }

    
    

    if (ctrl.opt_infil==1){
        Infiltration_1(ctrl, par);
    }
    
    
    if (ctrl.opt_evap==1){
        //Evapotranspiration_1(ctrl, par, atm, j);
    }
        



    return EXIT_SUCCESS;
}
