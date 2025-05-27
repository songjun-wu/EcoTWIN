/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Seperate_PET.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




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







