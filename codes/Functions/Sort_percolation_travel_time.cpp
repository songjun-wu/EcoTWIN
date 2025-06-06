/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_percolation_travel_time.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Sort_percolation_travel_time(Control &ctrl, Param &par) {
    double dt = ctrl.Simul_tstep;
    double travel_time_ratio = 0;   

    if (par.sort_perc_travel_time_OK == 0){
        
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            // The time for excess water to percolate versus hydraulic conductvity
            travel_time_ratio = dt / ((_thetaS1->val[j] - _thetaFC1->val[j]) / _Ks1->val[j]);
            _p_perc1->val[j] = (1 - exp(-1 * travel_time_ratio));

            travel_time_ratio = dt / ((_thetaS2->val[j] - _thetaFC2->val[j]) / _Ks2->val[j]);
            _p_perc2->val[j] = (1 - exp(-1 * travel_time_ratio));

            travel_time_ratio = dt / ((_thetaS3->val[j] - _thetaFC3->val[j]) / _Ks3->val[j]);
            _p_perc3->val[j] = (1 - exp(-1 * travel_time_ratio));
        }
        par.sort_perc_travel_time_OK = 1;

    }
    return EXIT_SUCCESS;
}