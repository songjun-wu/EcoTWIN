/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Canopy_evaporation.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

/*
Canopy evaporation modules
*/


int Basin::Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double max_canopy_storage;  // Maximum canopy storage
    double canopy_storage;  // Canopy storage
    double Ei; // Canopy evaporation
    double PET; // Potential ET

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Stages and fluxes
        canopy_storage = _I->val[j]; // Canopy storage
        PET = atm._PET->val[j];  // Potential ET

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







