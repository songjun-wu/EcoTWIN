/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ReGWrecharge.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"



int Basin::ReGWrecharge_1(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose) {

    double perc_vadose = 0;
    double vadose = db_vadose;

    if (vadose > roundoffERR){
      perc_vadose = vadose * par._perc_vadose_coeff->val[j];
      vadose -= perc_vadose;
      db_GW += perc_vadose;           
    }

    db_vadose = vadose;
    db_rPerc_vadose = perc_vadose;     

    return EXIT_SUCCESS;
}



int Basin::ReGWrecharge_2(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose) {

    double perc_vadose = 0;
    double vadose = db_vadose;

    if (vadose > roundoffERR){
      perc_vadose = vadose * par._perc_vadose_coeff->val[j] * (_theta3->val[j] / _thetaS3->val[j]);
      perc_vadose = min(perc_vadose, vadose);
      vadose -= perc_vadose;
      db_GW += perc_vadose;           
    }

    db_vadose = vadose;
    db_rPerc_vadose = perc_vadose;     

    return EXIT_SUCCESS;
}

