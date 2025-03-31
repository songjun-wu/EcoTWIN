#include "Basin.h"


int Basin::Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm) {
    
    Solve_canopy(ctrl, par, atm);

    Solve_snowpack(ctrl, par, atm);

    Solve_soil_profile(ctrl, par, atm);

    Routing(ctrl, par);
    
    //Routing_ovf(ctrl, par);

    return EXIT_SUCCESS;
}