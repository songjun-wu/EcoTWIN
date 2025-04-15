#include "Basin.h"

/*
Seperate PET to PE and PT based on LAI and a rExtinct parameter; Rutter (1972)
*/


int Basin::Seperate_PET(Param &par, Atmosphere &atm) {

    double SCF_veg;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972); Here included for calibration
        SCF_veg = 1 - exp(par._rE->val[j] * _LAI->val[j]);
        _PE->val[j] = atm._PET->val[j] * (1 - SCF_veg);
        _PT->val[j] = atm._PET->val[j] - _PE->val[j];
    }

    return EXIT_SUCCESS;
}







