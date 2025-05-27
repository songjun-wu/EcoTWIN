/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_canopy_nitrogen.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_canopy_nitrogen(Control &ctrl, Atmosphere &atm){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
    

    // Mixing canopy storage with precipitation input
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // The Nitrate concentration in rainfall is defined as a constant value of 2.0
        Mixing_full(_I_old->val[j], _no3_I->val[j], atm._P->val[j], 2.0);
        _no3_pond->val[j] = _no3_I->val[j]; // Align the composition in ponding water with that in throughfall

        // Enrichment due to canopy evaporation (disabled)
        //if (_I->val[j] > roundoffERR and _Ei->val[j] > roundoffERR){
        //    _no3_I->val[j] = _no3_I->val[j] * (_I->val[j] + _Ei->val[j]) / _I->val[j];
        //}
    }

    return EXIT_SUCCESS;
}
