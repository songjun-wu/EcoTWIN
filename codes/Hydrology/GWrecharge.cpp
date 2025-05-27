/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* GWrecharge.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"



int Basin::GWrecharge_1(Control &ctrl, Param &par) {

    
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double depth3 = par._depth3->val[j];
        double theta3 = _theta3->val[j];
        double perc3 = 0;

        if (theta3 > _thetaFC3->val[j]){
            perc3 = (theta3 - _thetaFC3->val[j]) * depth3 * _p_perc3->val[j] * par._wRecharge->val[j];
            theta3 -= perc3 / depth3;
            _GW->val[j] += perc3;
        }         

        _theta3->val[j] = theta3;
        _Perc3->val[j] = perc3;
    }
    
    return EXIT_SUCCESS;
}

int Basin::GWrecharge_2(Control &ctrl, Param &par) {

    
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double depth3 = par._depth3->val[j];
        double theta3 = _theta3->val[j];
        double perc3 = 0;

        if (theta3 > _thetaFC3->val[j]){
            perc3 = (theta3 - _thetaFC3->val[j]) * depth3 * par._wRecharge->val[j];
            theta3 -= perc3 / depth3;
            _GW->val[j] += perc3;
        }         

        _theta3->val[j] = theta3;
        _Perc3->val[j] = perc3;
    }
    
    return EXIT_SUCCESS;
}
