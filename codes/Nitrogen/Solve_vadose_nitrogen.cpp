/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_vadose_nitrogen.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_vadose_nitrogen(Control &ctrl, Atmosphere &atm){
    /*
    ### vadose:
        (_vadose_old)
        + percolation3      (need to mix)
        - percolation_vadose
        (_vadose)
        + repercolation3
        - repercolation_vadose   
        + interf_in
        - interf_out
        - interf_toChn                            
    */

    
    // Mixing vadose storage with percolation from layer 3
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        Mixing_full(_vadose_old->val[j], _no3_vadose->val[j], _Perc3->val[j], _no3_layer3->val[j]);
    }

    return EXIT_SUCCESS;
}
