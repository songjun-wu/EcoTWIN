#include "Basin.h"

int Basin::Solve_channel(Control &ctrl, Param &par, Atmosphere &atm){
   
    if (ctrl.opt_chanE == 1){
        Channel_evaporation_1(ctrl, atm, par);
    } else if  (ctrl.opt_chanE == 2){
        Channel_evaporation_2(ctrl, atm, par);
    }

    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_channel_tracking(ctrl, atm, par);
    }

    if (ctrl.opt_nitrogen_sim==1){
        Solve_channel_nitrogen(ctrl, atm, par);
    }
    
   
    return EXIT_SUCCESS;
}
