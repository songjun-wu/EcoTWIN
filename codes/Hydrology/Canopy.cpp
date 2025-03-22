#include "Basin.h"

/*
Canopy intercpetion modules
Interception_1: Maximum canopy stoages are directly specified by LAI * alpha
Interception_2: Maximum canopy stoages are additionally corrected by rE (Landarf et al., 2024)
*/

int Basin::Solve_canopy_fluxes(Control &ctrl, Param &par, Atmosphere &atm) {

    int r, c;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];

        if (ctrl.opt_intecept == 1){
        Interception_1(par, atm, r, c);
        } else if (ctrl.opt_intecept == 2){
        Interception_2(par, atm, r, c);
        }
    }
    return EXIT_SUCCESS;
}


int Basin::Interception_1(Param &par, Atmosphere &atm, int r, int c) {

    // Parameters
    double alpha = par._alpha->matrix[r][c];

    // Stages and fluxes
    double precip = atm._P->matrix[r][c];
    double LAI = atm._LAI->matrix[r][c];
    double C = _I->matrix[r][c]; // Canopy storage
    double D; // Throughfall

    double max_canopy_storage = alpha * LAI; // Maximum canopy storage

    D = C + precip <= max_canopy_storage ? 0.0 : (C + precip - max_canopy_storage);
    D = min<double>(D, C + precip);

    // Update canopy storage
    _I->matrix[r][c] += (precip - D);

    return EXIT_SUCCESS;
}

int Basin::Interception_2(Param &par, Atmosphere &atm, int r, int c) {
    // Parameters
    double alpha = par._alpha->matrix[r][c];
    double rE = par._rE->matrix[r][c];

    // Stages and fluxes
    double precip = atm._P->matrix[r][c];
    double LAI = atm._LAI->matrix[r][c];
    double C = _I->matrix[r][c]; // Canopy storage
    double D; // Throughfall
    double SCF = 1 - exp(rE * LAI); // surface cover fraction, rExtinct = -0.463 Rutter (1972), now included for calibration

    // Maximum canopy storage after correction
    double max_canopy_storage = alpha * LAI;
    max_canopy_storage = max<double>(0, max_canopy_storage * (1 - (1 / (1 + (SCF *precip/max_canopy_storage)))));

    D = C + precip <= max_canopy_storage ? 0.0 : (C + precip - max_canopy_storage);
    D = min<double>(D, C + precip);

    // Update canopy storage
    _I->matrix[r][c] += (precip - D);

    return EXIT_SUCCESS;
}




