/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_canopy_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_canopy_transport(Atmosphere &atm, svector &_sv_conc_I, svector &_sv_conc_P, svector &_sv_conc_pond, bool enrich_flag){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
    
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        Mixing_full(_I_old->val[j], _sv_conc_I.val[j], atm._P->val[j], _sv_conc_P.val[j]);
        _sv_conc_pond.val[j] = _sv_conc_I.val[j]; // Align the composition in ponding water with that in throughfall
    }

    return EXIT_SUCCESS;
}
