/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_soil_profile_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 01.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Mixing_soil_profile_tracking(Control &ctrl, Atmosphere &atm, Param &par){

    /* 
    ### Soil layer 1:
    (_thate1_old)
    + infiltration          (need to mix)
    - percolation1
    - Esoil
    - Transp1           
    (_thate1)
    + reinfiltration
    - repercolation1    

    ### Soil layer 2:
    (_thata2_old)
    + percolation1          (need to mix)
    - percolation2
    - Transp2           
    (_theta2)
    + repercolation1
    - repercolation2    

    ### Soil layer 3:
    (_theta3_old)           
    + percolation2          (need to mix)
    - percolation3
    + Capillary flow        (need to mix)
    - Transp3
    (_theta3)          
    + repercolation2
    - repercolation3
    */

    
    // Isotope tracking
    if (ctrl.opt_tracking_isotope==1) {
        // Mixing layer 1-3
        Solve_soil_transport(par, *_d18o_pond, *_d18o_layer1, *_d18o_layer2, *_d18o_layer3, *_d18o_vadose, *_d18o_chanS, *_tmp, *_tmp, false, ctrl.opt_drainage, false);  // false1: no enrichment due to evaportranspiration; false2: no Fickian diffusion
        // Fractionation due to soil evaporation (only for layer 1 but happens after percolation)
        _tmp->equals(*_theta1_old);
        _tmp->multiply(*_depth1);
        _tmp->plus(*_infilt);
        _tmp->minus(*_Perc1);
        _tmp->minus(*_Tr1);
        _tmp->minus(*_Es);
        Fractionation(atm, par, *_Es, *_tmp, *_d18o_layer1, *_d18o_layer1, *_tmp, 1);  // issoil = 1; todo
    }

    // Cumulative age tracking
    if (ctrl.opt_tracking_age==1) {
        // Mixing layer 1-3
        Solve_soil_transport(par, *_age_pond, *_age_layer1, *_age_layer2, *_age_layer3, *_age_vadose, *_age_chanS, *_tmp, *_tmp, false, ctrl.opt_drainage, false);  // false1: no enrichment due to evaportranspiration; false2: no Fickian diffusion
    }


    // Transient age tracking
    if (ctrl.opt_tracking_trans_age==1) {
        
        // Mixing layer 1
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            // Mix infiltration with top layer storage
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _trans_age_layer1->val[j], _infilt->val[j], 0.0);
        }
        
        // Mixing layer 2
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta2_old->val[j] * _depth2->val[j], _trans_age_layer2->val[j], _Perc1->val[j], 0.0);
        }


        // Mixing layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _trans_age_layer3->val[j], _Perc2->val[j], 0.0);
        }

        // Mixing capillary flow with layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j] + _Perc2->val[j] - _Perc3->val[j], _trans_age_layer3->val[j], _capillary_flow->val[j], 0.0);
        }

    }



    return EXIT_SUCCESS;
}
