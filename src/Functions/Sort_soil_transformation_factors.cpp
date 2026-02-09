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

double Basin::Temp_factor(double T){

    double f_T; // Temperature factor [-, decimal]

    if (T > 34.0) T = 34.0 - (T - 34.0); // Maximum temperature for soil respiration is set to 34 degree celcius

    if (T < 0.0) {
        f_T = 0.0;
    } else {
        f_T = pow(2, (T - 20.0) / 10.0);
        if (T < 5.0) f_T *= (T / 5.0);
    }

    return f_T;

}


double Basin::Moist_factor(const double db_theta, const double db_thetaWP, const double db_thetaS, const double db_depth){

    /* 
    double fct_thetaS = 0.6;
    double fct_theta_up = 0.12;
    double fct_theta_low = 0.08;
    double fct_theta_pow = 1.0;
    double db_depth in m;
    */

    double fct_theta;
    if (db_theta >= db_thetaS) {
        fct_theta = 0.0;
    } else if (db_theta < db_thetaWP){
        fct_theta = 0.0;
    } else {
        //fct_theta = min(1.0, (1 - fct_thetaS) * pow((db_thetaS - db_theta) / (fct_theta_up / 100 * db_depth * 1000), fct_theta_pow)  + fct_thetaS);
        //fct_theta = min(fct_theta, pow((db_theta - db_thetaWP) / (fct_theta_low /100 * db_depth * 1000), fct_theta_pow));
        fct_theta = min(1.0, 1.0 * (db_thetaS - db_theta) / (1.2) + 0.0);
        fct_theta = min(fct_theta, (db_theta - db_thetaWP) / (0.8));
    }

    return fct_theta;

}