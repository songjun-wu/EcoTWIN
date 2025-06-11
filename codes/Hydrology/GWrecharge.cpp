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

    // Percolation from vadose to GW storage
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double vadose = _vadose->val[j];
        double perc_vadose = 0;

        if (vadose > roundoffERR){
            perc_vadose = vadose * par._perc_vadose_coeff->val[j];
            vadose -= perc_vadose;
            _GW->val[j] += perc_vadose;           
        }

        _vadose->val[j] = vadose;
        _Perc_vadose->val[j] = perc_vadose;


    }  
    return EXIT_SUCCESS;
}


int Basin::GWrecharge_2(Control &ctrl, Param &par) {

    // Percolation from vadose to GW storage
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double vadose = _vadose->val[j];
        double perc_vadose = 0;

        if (vadose > roundoffERR){
            perc_vadose = vadose * par._perc_vadose_coeff->val[j] * (_theta3->val[j] / _thetaS3->val[j]);
            perc_vadose = min(perc_vadose, vadose);
            vadose -= perc_vadose;
            _GW->val[j] += perc_vadose;           
        }

        _vadose->val[j] = vadose;
        _Perc_vadose->val[j] = perc_vadose;

    }
    return EXIT_SUCCESS;
}

