/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Evapotranspiration.cpp
  * Created  on: 30.02.2025
  * Modified on: 06.06.2025
***************************************************************/


#include "Basin.h"

/*
Evapotranspiration_1: 
Evapotranspiration calcualted based on PET and a soil water dependent root extraction function.
Citation: Feddes, R., Kowalik, P., Kolinska-Malinka, K., & Zaradny, H. (1976). Simulation of field water uptake by plants using a soil water dependent root extraction function. Journal of Hydrology, 31, 13-26. https://doi.org/10.1016/0022-1694(76)90017-2
*/


int Basin::Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm){

    // Evapotranspiration

    double Esoil; // Soil evaporation in layer 1
    double Tr1; // Transpiration in layer 1
    double Tr2; // Transpiration in layer 2
    double Tr3; // Transpiration in layer 3
    double froot_coeff_corrcted;
    double depth1, depth2, depth3;
    double PE, PT;
    double Throughfall;
    double theta1, theta2, theta3;
    double ST1, ST2, ST3;
    double FC1, FC2, FC3;
    double WP1, WP2, WP3;
    double ET_weight;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        Esoil = 0;
        Tr1 = 0;
        Tr2 = 0;
        Tr3 = 0;

        // Parameters
        froot_coeff_corrcted = 0;
        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j]; // The lower boundary is included for calibration
        ET_weight = par._ET_reduction->val[j];  // ET reduction

        // Stages and fluxes
        PE = _PE->val[j]; // Remaining potential evaporation;
        PT = _PT->val[j]; // Remaining potential transpiration;
        Throughfall = _Th->val[j]; // Throughfall [m]
        theta1 = _theta1->val[j]; // Soil moisture in layer 1 [-]
        theta2 = _theta2->val[j]; // Soil moisture in layer 2 [-]
        theta3 = _theta3->val[j]; // Soil moisture in layer 3 [-]
        ST1 = theta1 * depth1; // Soil storage in layer 1 [m]
        ST2 = theta2 * depth2; // Soil storage in layer 2 [m]
        ST3 = theta3 * depth3; // Soil storage in layer 3 [m]
        WP1 = _thetaWP1->val[j];
        WP2 = _thetaWP2->val[j];
        WP3 = _thetaWP3->val[j];
        FC1 = _thetaFC1->val[j];
        FC2 = _thetaFC2->val[j];
        FC3 = _thetaFC3->val[j];

        // For layer 1
        // Soil evaporation
        Esoil = min(PE*min(theta1/FC1 * ET_weight, 1.0), ST1);
        ST1 -= Esoil;
        // Transpiration
        if (theta1 > FC1){
            froot_coeff_corrcted = _froot_layer1->val[j];
        } else if (theta1 < WP1){
            froot_coeff_corrcted = 0.0;
        } else{
            froot_coeff_corrcted = _froot_layer1->val[j] * (theta1 - WP1) / (FC1 - WP1);      
        }
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr1 = min(PT*froot_coeff_corrcted * ET_weight, ST1);
        ST1 -= Tr1;
        PT -= Tr1;

        // For layer 2
        // Transpiration
        if (theta2 > FC2){
            froot_coeff_corrcted = _froot_layer2->val[j];
        } else if (theta2 < WP2){
            froot_coeff_corrcted = 0.0;
        } else{
            froot_coeff_corrcted = _froot_layer2->val[j] * (theta2 - WP2) / (FC2 - WP2);      
        }
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr2 = min(PT*froot_coeff_corrcted * ET_weight, ST2);
        ST2 -= Tr2;
        PT -= Tr2;

            
        // For layer 3
        // Transpiration
        if (theta3 > FC3){
            froot_coeff_corrcted = _froot_layer3->val[j];
        } else if (theta3 < WP3){
            froot_coeff_corrcted = 0.0;
        } else{
            froot_coeff_corrcted = _froot_layer3->val[j] * (theta3 - WP3) / (FC3 - WP3);      
        }
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr3 = min(PT*froot_coeff_corrcted * ET_weight, ST3);
        ST3 -= Tr3;
        PT -= Tr3;


        _theta1->val[j] = ST1 / depth1;
        _theta2->val[j] = ST2 / depth2;
        _theta3->val[j] = ST3 / depth3;
        _Es->val[j] = Esoil;
        _Tr1->val[j] = Tr1;
        _Tr2->val[j] = Tr2;
        _Tr3->val[j] = Tr3;
        _Tr->val[j] = Tr1 + Tr2 + Tr3;

    }

    return EXIT_SUCCESS;
}