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
    + irrigation_from_river
    + irrigation_from_GW
    (pond)
    - Infiltration      
    + ovf_in            
    - Reinfiltration
    - ovf_out
    - ovf_toChn           
    */

    double irrigation_amount, irrigation_conc;

    // Isotopes
    if (ctrl.opt_tracking_isotope==1) {
        // Mixing snow and irrigation
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mixing snow with throughfall if temperature is below snow rain threshold
            if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
                Mixing_full(_snow_old->val[j], _d18o_snow->val[j], _snowacc->val[j], _d18o_pond->val[j]);
            } else{  // Else throughfall mixes with snow melt
                Mixing_full(_Th->val[j], _d18o_pond->val[j], _snowmelt->val[j], _d18o_snow->val[j]);
            }

            // Mixing with irrigation
            irrigation_amount = _irrigation_from_river->val[j] + _irrigation_from_GW->val[j];
            if (irrigation_amount > roundoffERR){
                irrigation_conc = (_irrigation_from_river->val[j] * _d18o_chanS->val[j] + _irrigation_from_GW->val[j] * _d18o_GW->val[j]) / irrigation_amount;
                Mixing_full(_pond->val[j], _d18o_pond->val[j], irrigation_amount, irrigation_conc);
            }
        }
    }


    // Ages
    if (ctrl.opt_tracking_age==1) {
        // Mixing snow and irrigation
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mixing snow with throughfall if temperature is below snow rain threshold
            if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
                Mixing_full(_snow_old->val[j], _age_snow->val[j], _snowacc->val[j], _age_pond->val[j]);
            } else{  // Else throughfall mixes with snow melt
                Mixing_full(_Th->val[j], _age_pond->val[j], _snowmelt->val[j], _age_snow->val[j]);
            }

            // Mixing with irrigation
            irrigation_amount = _irrigation_from_river->val[j] + _irrigation_from_GW->val[j];
            if (irrigation_amount > roundoffERR){
                irrigation_conc = (_irrigation_from_river->val[j] * _age_chanS->val[j] + _irrigation_from_GW->val[j] * _age_GW->val[j]) / irrigation_amount;
                Mixing_full(_pond->val[j], _age_pond->val[j], irrigation_amount, irrigation_conc);
            }
        }
    }

    return EXIT_SUCCESS;
}
