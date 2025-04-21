#include "Basin.h"

int Basin::Solve_surface_nitrogen(Control &ctrl, Atmosphere &atm, Param &par){

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

    // Mixing snow accumulation or snow melt
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Mixing snow with throughfall if temperature is below snow rain threshold
        if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
            Mixing_full(_snow_old->val[j], _no3_snow->val[j], _snowacc->val[j], _no3_pond->val[j]);
        } else{  // Else throughfall mixes with snow melt
            _no3_pond->val[j] = _no3_I->val[j]; // Align the composition in ponding water with that in throughfall
            //mix throughfall with snow melt
            Mixing_full(_Th->val[j], _no3_pond->val[j], _snowmelt->val[j], _no3_snow->val[j]);
        }
        
    }

    return EXIT_SUCCESS;
}
