#include "Basin.h"

/*
Canopy intercpetion modules
Interception_1: Maximum canopy stoages are directly specified by LAI * alpha
Interception_2: Maximum canopy stoages are additionally corrected by rE (Landarf et al., 2024)
*/


int Basin::Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double max_canopy_storage;
    double canopy_storage;
    double Ei;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Parameters
        double alpha = par._alpha->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = atm._LAI->val[j];
        double canopy_storage = _I->val[j]; // Canopy storage


        if (canopy_storage > 0) {
            max_canopy_storage = LAI * alpha;
            Ei = atm._PET->val[j] * pow(canopy_storage / max_canopy_storage, 2/3);
            Ei = min(Ei, canopy_storage);
            canopy_storage -= Ei;
        } else{
            Ei = 0;
        }

        _Ei->val[j] = Ei;
        _I->val[j] = canopy_storage;
        atm._PET->val[j] -= Ei;

    }

    return EXIT_SUCCESS;
}







