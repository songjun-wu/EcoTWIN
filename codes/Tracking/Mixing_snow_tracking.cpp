#include "Basin.h"

int Basin::Mixing_snow_tracking(Control &ctrl, Atmosphere &atm, Param &par){

    if (ctrl.opt_tracking_isotope==1) {
        
        // Mixing snow pack
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mixing snow with throughfall if temperature is below snow rain threshold
            if (atm._Ta < par._snow_rain_thre){
                Mixing_full(_snow_old->val[j], _d18o_snow->val[j], _Th->val[j], _d18o_I->val[j]);
            } else{  // Else throughfall mixes with snow melt
                Mixing_full(_Th->val[j], _d18o_pond->val[j], _snowmelt->val[j], _d18o_snow->val[j]);
            }

            
        }



    }
    return EXIT_SUCCESS;
}
