/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_canopy_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"

int Basin::Mixing_canopy_tracking(Control &ctrl, Atmosphere &atm){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
    
    if (ctrl.opt_tracking_isotope==1) {
        // Mixing canopy storage with precipitation input
        
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_I_old->val[j], _d18o_I->val[j], atm._P->val[j], atm._d18o_P->val[j]);
            _d18o_pond->val[j] = _d18o_I->val[j]; // Align the composition in ponding water with that in throughfall
        }
        
        // Fractionation due to canopy evaporation (Disabled)
        // Fractionation(atm, *_Ei, *_I, *_d18o_I, *_d18o_I, *_tmp, 0);  // issoil = 0
    }

    

    if (ctrl.opt_tracking_age==1){
        // Mixing canopy storage with precipitation input
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_I_old->val[j], _age_I->val[j], atm._P->val[j], 0.0);
            _age_pond->val[j] = _age_I->val[j]; // Align the composition in ponding water with that in throughfall
        }
    }

    return EXIT_SUCCESS;
}
