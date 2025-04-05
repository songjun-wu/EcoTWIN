#include "Basin.h"

/*
Canopy intercpetion modules
Interception_1: Maximum canopy stoages are directly specified by LAI * alpha
Interception_2: Maximum canopy stoages are additionally corrected by rE (Landarf et al., 2024)
*/

int Basin::Solve_canopy(Control &ctrl, Param &par, Atmosphere &atm) {

    if (ctrl.opt_intecept == 1){
        Interception_1(ctrl, par, atm);
    } else if (ctrl.opt_intecept == 2){
        Interception_2(ctrl, par, atm);
    }

    return EXIT_SUCCESS;
}


int Basin::Interception_1(Control &ctrl, Param &par, Atmosphere &atm) {

    double Th; // Throughfall

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Parameters
        double alpha = par._alpha->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = atm._LAI->val[j];
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

    double Th; // Throughfall

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        // Parameters
        double alpha = par._alpha->val[j];
        double rE = par._rE->val[j];

        // Stages and fluxes
        double precip = atm._P->val[j];
        double LAI = atm._LAI->val[j];
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




