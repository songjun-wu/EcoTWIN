/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_GW_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 09.06.2025
***************************************************************/


#include "Basin.h"


int Basin::Mixing_GW_tracking(Control &ctrl, Atmosphere &atm){
    /*
    ### GW:
    - irrigation_from_GW
    (_GW_old)
    + percolation_vadose      (need to mix)
    (_GW)
    + repercolation_vadose    
    + GWf_in
    - GWf_out
    - GWf_toChn                         
    */

    // Isotope mixing
    if (ctrl.opt_tracking_isotope==1) {
        if (ctrl.opt_baseflow_mixing == 0){
            // Mixing GW storage with percolation from vadose zone
            for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
                Mixing_full(_GW_old->val[j], _d18o_GW->val[j], _Perc_vadose->val[j], _d18o_vadose->val[j]);
            }
        }
    }

    // Age mixing
    if (ctrl.opt_tracking_age==1) {
        if (ctrl.opt_baseflow_mixing == 0){
            // Mixing GW storage with percolation from vadose zone
            for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
                Mixing_full(_GW_old->val[j], _age_GW->val[j], _Perc_vadose->val[j], _age_vadose->val[j]);
            }
        }
    }

    return EXIT_SUCCESS;
}
