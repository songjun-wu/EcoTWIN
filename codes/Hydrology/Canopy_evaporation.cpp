#include "Basin.h"

/*
Canopy evaporation modules
*/


int Basin::Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double max_canopy_storage = 0;
    double canopy_storage = 0;
    double Ei = 0;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Parameters
        double alpha = par._alpha->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = _LAI->val[j];
        double canopy_storage = _I->val[j]; // Canopy storage


        if (canopy_storage > 0) {
            max_canopy_storage = LAI * alpha;
            Ei = _PE->val[j] * pow(canopy_storage / max_canopy_storage, 2/3);
            Ei = min(Ei, canopy_storage);
            canopy_storage -= Ei;
        } else{
            Ei = 0;
        }

        _Ei->val[j] = Ei;
        _I->val[j] = canopy_storage;
        _PE->val[j] -= Ei;

    }

    return EXIT_SUCCESS;
}







