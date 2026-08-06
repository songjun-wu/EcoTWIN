/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_root_fraction.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

/*
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
*/


double Basin::Temp_factor(double T){
    //return pow(2, (T - 25.0) / 10.0);;  // Q10 temperature dependence function with Q10 = 2
    return 47.9 / (1.0 + exp(106.0 / (T + 18.3)));
}


/*
double Basin::Moist_factor(const double db_theta, const double db_thetaWP, const double db_thetaS, const double db_depth){

    //double fct_thetaS = 0.6;
    //double fct_theta_up = 0.12;
    //double fct_theta_low = 0.08;
    //double fct_theta_pow = 1.0;
    //double db_depth in m;
    
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
*/



double Basin::Moist_factor(const double db_theta, const double db_thetaWP, const double db_thetaFC, const double db_thetaS, const double db_depth){

    double fct_theta;
    double theta_optimal = 0.8 * db_thetaFC;

    if (db_theta >= theta_optimal) {
        fct_theta = (db_thetaS - db_theta) / (db_thetaS - theta_optimal);
    } else {
        fct_theta = (db_theta - 0.0) / (theta_optimal - 0.0);
    } 

    fct_theta = max(0.0, min(fct_theta, 1.0));

    return fct_theta;
}
