#include "Basin.h"

int Basin::Mixing_canopy_tracking(Control &ctrl, Atmosphere &atm){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
    
    if (ctrl.opt_tracking_isotope==1) {
        // Mixing canopy storage with precipitation input
        
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_I_old->val[j], _d18o_I->val[j], atm._P->val[j], atm._d18o_P->val[j]);
            _d18o_pond->val[j] = _d18o_I->val[j]; // Align the composition in ponding water with that in throughfall
        }
        
        // Fractionation due to canopy evaporation (Disabled)
        // Fractionation(atm, *_Ei, *_I, *_d18o_I, *_d18o_I, *_tmp, 0);  // issoil = 0
    }

    

    if (ctrl.opt_tracking_age==1){
        // Mixing canopy storage with precipitation input
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_I_old->val[j], _age_I->val[j], atm._P->val[j], 0.0);
            _age_pond->val[j] = _age_I->val[j]; // Align the composition in ponding water with that in throughfall
        }
    }

    return EXIT_SUCCESS;
}
