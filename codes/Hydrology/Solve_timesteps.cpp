#include "Basin.h"


int Basin::Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm) {

    
    
    Solve_canopy(ctrl, par, atm);

    Solve_snowpack(ctrl, par, atm);

    Solve_soil_profile(ctrl, par, atm);

    Routing(ctrl, par);
    
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Store_states();  // Store all water storages for mixing
    }

    //cout << _sortedGrid.row[71] << " " << _sortedGrid.col[71] << " " << _theta2->val[71] << " " << _thetaS2->val[71] << endl;

    return EXIT_SUCCESS;
}