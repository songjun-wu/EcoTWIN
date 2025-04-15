#include "Basin.h"

/*
Canopy evaporation modules
*/


int Basin::Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double max_canopy_storage = 0;
    double canopy_storage = 0;
    double Ei = 0;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Stages and fluxes
        double canopy_storage = _I->val[j]; // Canopy storage
        double PET = atm._PET->val[j];  // Potential ET

        if (canopy_storage > 0) {
            max_canopy_storage = _LAI->val[j] * par._alpha->val[j];
            Ei = PET * pow(canopy_storage / max_canopy_storage, 2/3);
            Ei = min(Ei, canopy_storage);
            Ei = min(Ei, PET);
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







