#include "Basin.h"


int Basin::Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm) {

    //Solve_canopy_fluxes(ctrl, par, atm);

    Snow_acc_melt(ctrl, par, atm);

    //Routing_ovf(ctrl, par);

    return EXIT_SUCCESS;
}