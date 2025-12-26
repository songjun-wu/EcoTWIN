/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_root_fraction.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Sort_root_fraction(Control &ctrl, Param &par) {

    // Calculate the root fraction
    if (par.sort_root_fraction_OK == 0){
        
        double root_tmp_layer1, root_tmp_layer12, root_tmp_layer123;
        double root1, root2, root3, root_total;
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            double froot_coeff = par._froot_coeff->val[j];
            double depth1 = _depth1->val[j];
            double depth2 = _depth2->val[j];
            double depth3 = par._depth3->val[j]; // The lower boundary is included for calibration 

            root_tmp_layer1   = (1 - pow(froot_coeff, depth1 * 100)); // m to cm
            root_tmp_layer12  = (1 - pow(froot_coeff, (depth1 + depth2) * 100));
            root_tmp_layer123 = (1 - pow(froot_coeff, (depth1 + depth2 + depth3) * 100));

            root1 = root_tmp_layer123;
            root2 = root_tmp_layer123 - root_tmp_layer1;
            root3 = root_tmp_layer123 - root_tmp_layer12;
            root_total = root1 + root2 + root3;

            // Turn root density to fraction
            _froot_layer1->val[j] = root1 / root_total;  
            _froot_layer2->val[j] = root2 / root_total;
            _froot_layer3->val[j] = root3 / root_total;
            
        }
        par.sort_root_fraction_OK = 1;

    }

    return EXIT_SUCCESS;
}