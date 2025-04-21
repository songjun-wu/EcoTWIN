#include "Basin.h"


int Basin::Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm) {
    
    Solve_canopy(ctrl, par, atm);

    Solve_surface(ctrl, par, atm);
    
    Solve_soil_profile(ctrl, par, atm);

    Routing(ctrl, par);
    
    //Check_mass_balance(ctrl, par, atm);

    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1 or ctrl.opt_nitrogen_sim==1){
        Store_states();  // Store all water storages for mixing
    }



    return EXIT_SUCCESS;
}