/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Interception.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

/*
Canopy intercpetion modules
Interception_1: Maximum canopy stoages are directly specified by LAI * alpha
Interception_2: Maximum canopy stoages are additionally corrected by rE (Landarf et al., 2024)
*/


int Basin::Interception_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double Th = 0; // Throughfall



    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Parameters
        double alpha = par._alpha->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = _LAI->val[j];
        double C = _I->val[j]; // Canopy storage
       
        double max_canopy_storage = alpha * LAI; // Maximum canopy storage

        Th = (C + precip) <= max_canopy_storage ? 0.0 : (C + precip - max_canopy_storage);
        Th = min<double>(Th, C + precip);

        // Update canopy storage
        _I->val[j] += (precip - Th);
        _Th->val[j] = Th;   
    }

    
    return EXIT_SUCCESS;
}

int Basin::Interception_2(Control &ctrl, Param &par, Atmosphere &atm) {

    double Th = 0; // Throughfall

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        // Parameters
        double alpha = par._alpha->val[j];
        double rE = par._rE->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = _LAI->val[j];
        double C = _I->val[j]; // Canopy storage
        double SCF = 1 - exp(rE * LAI); // surface cover fraction, rExtinct = -0.463 Rutter (1972), now included for calibration

        // Maximum canopy storage after correction
        double max_canopy_storage = alpha * LAI;
        max_canopy_storage = max<double>(0, max_canopy_storage * (1 - (1 / (1 + (SCF *precip/max_canopy_storage)))));

        Th = C + precip <= max_canopy_storage ? 0.0 : (C + precip - max_canopy_storage);
        Th = min<double>(Th, C + precip);

        // Update canopy storage
        _I->val[j] += (precip - Th);
        _Th->val[j] = Th;
    }

    return EXIT_SUCCESS;
}






