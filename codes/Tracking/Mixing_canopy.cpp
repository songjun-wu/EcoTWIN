#include "Basin.h"

int Basin::Mixing_canopy(Control &ctrl, Atmosphere &atm){
    
    if (ctrl.opt_tracking_isotope==1) {

        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_I_old->val[j], _d18o_I->val[j], atm._P->val[j], atm._d18o_P->val[j]);
        }

        // Fractionation due to canopy evaporation
        Fractionation(atm, *_Ei, *_I, *_d18o_I, *_d18o_I, *_tmp, 0);  // issoil = 0
    }

    return EXIT_SUCCESS;
}
