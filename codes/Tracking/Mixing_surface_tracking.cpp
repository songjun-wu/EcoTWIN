#include "Basin.h"

int Basin::Mixing_surface_tracking(Control &ctrl, Atmosphere &atm, Param &par){

    /*
    ### Snow
    (_snow_old)
    + snowacc
    - snowmelt
    (_snow)

    ### Ponding water:
    (_pond_old = 0.0)
    + Th
    + snowmelt
    (pond)
    - Infiltration      
    + ovf_in            
    - Reinfiltration
    - ovf_out
    - ovf_toChn           
    */

    // Isotopes
    if (ctrl.opt_tracking_isotope==1) {
        // Mixing snow accumulation or snow melt
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mixing snow with throughfall if temperature is below snow rain threshold
            if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
                Mixing_full(_snow_old->val[j], _d18o_snow->val[j], _snowacc->val[j], _d18o_pond->val[j]);
            } else{  // Else throughfall mixes with snow melt
                Mixing_full(_Th->val[j], _d18o_pond->val[j], _snowmelt->val[j], _d18o_snow->val[j]);
            }
            
        }
    }


    // Ages
    if (ctrl.opt_tracking_age==1) {
        // Mixing snow accumulation or snow melt
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mixing snow with throughfall if temperature is below snow rain threshold
            if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
                Mixing_full(_snow_old->val[j], _age_snow->val[j], _snowacc->val[j], _age_pond->val[j]);
            } else{  // Else throughfall mixes with snow melt
                Mixing_full(_Th->val[j], _age_pond->val[j], _snowmelt->val[j], _age_snow->val[j]);
            }
            
        }
    }

    return EXIT_SUCCESS;
}
