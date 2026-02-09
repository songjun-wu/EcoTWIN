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
    double theta1, theta2, theta3;
    double ST1, ST2, ST3;
    double FC1, FC2, FC3;
    double WP1, WP2, WP3;
    double ET_weight;

    double minimum_theta = 1e-3;

    
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
        // Transpiration
        if (theta1 > FC1){
            froot_coeff_corrcted = _froot_layer1->val[j];
        } else if (theta1 < WP1){
            froot_coeff_corrcted = 0.0;
        } else{
            froot_coeff_corrcted = _froot_layer1->val[j] * (theta1 - WP1) / (FC1 - WP1);      
        }
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr1 = min(PT*froot_coeff_corrcted * ET_weight, ST1 - minimum_theta);
        ST1 -= Tr1;
        PT -= Tr1;
        // Soil evaporation
        Esoil = min(PE*min(ST1/depth1/FC1, 1.0), ST1 - minimum_theta) * ET_weight;
        ST1 -= Esoil;

        
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
        Tr2 = min(PT*froot_coeff_corrcted * ET_weight, ST2 - minimum_theta);
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
        Tr3 = min(PT*froot_coeff_corrcted * ET_weight, ST3 - minimum_theta);
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



int Basin::Evapotranspiration_2(Control &ctrl, Param &par, Atmosphere &atm){


    // Evapotranspiration

    double Esoil; // Soil evaporation in layer 1
    double Tr1; // Transpiration in layer 1
    double Tr2; // Transpiration in layer 2
    double Tr3; // Transpiration in layer 3
    double froot_coeff_corrcted;
    double depth1, depth2, depth3;
    double PE, PT;
    double theta1, theta2, theta3;
    double ST1, ST2, ST3;
    double FC1, FC2, FC3;
    double WP1, WP2, WP3;
    double ET_weight;

    double minimum_theta = 1e-3;

    double DT = ctrl.Simul_tstep;  // Timestep length in seconds


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        Esoil = 0;
        Tr1 = 0;
        Tr2 = 0;
        Tr3 = 0;

        // Parameters
        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j]; // The lower boundary is included for calibration
        ET_weight = par._ET_reduction->val[j];  // ET reduction

        // Stages and fluxes
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



        

        // === Saturated vapor pressure ===
        double Ta = atm._Ta->val[j];  // Air temperature in degree Celsius
        double Ts = Get_soil_temperature(Ta, _LAI->val[j]);  // Soil temperature [Degree C]
        double Ea_s = 611 * exp((17.3 * Ta)/(Ta + 237.3));  // Saturated vapor pressure in atmosphere [Pa]
        double Ec_s = Ea_s;  // Here we assume the saturated vapor pressure in canopy is the same as in atmosphere [Pa]
        double Es_s = 611 * exp((17.3 * Ts)/(Ts + 237.3));  // Saturated vapor pressure in soil [Pa]

        // === Conduntance in atmosphere, canopy and soil ===
        // Water limitation factor averaged from three layers
        double water_limitation_factor =\  
        _froot_layer1->val[j] * (theta1 - WP1) / (FC1 - WP1) + \
        _froot_layer2->val[j] * (theta2 - WP2) / (FC2 - WP2) + \
        _froot_layer3->val[j] * (theta3 - WP3) / (FC3 - WP3);
        water_limitation_factor = min(max(0.0, water_limitation_factor), 1.0);
        // conductance       
        double ga = 0.02 * 2.0; // Aerodynamic conductance [m/s]
        double gs = 1 / (1/ 0.005 + 1000 + 4000 * (1 - water_limitation_factor)); // Soil surface conductance [m/s]; Soil resistance = 1000 + 4000 * (0.3 - water_limitation_factor)
        double gc = 1 / (1/ga + 1/_canopy_conductance->val[j]);  // Canopy conductance [m/s]
        
        // === Relative humidity ===
        // Relative humidity in air
        double rh_a = atm._RH->val[j];  // [-, decimal fraction]
        // Relative humidity at leaf surface
        double rh_c = 1;  // Here we assume the relative humidity at leaf surface is 1.0
        // Relative humidity at the surface from EcH2O-iso; Kuppel et al., (2018).
        double beta = 0.25 * pow(1 - cos(3.14 * theta1 / FC1), 2);
        double rh_s = beta + (1 - beta) * rh_a;  // [-, decimal fraction]

        // === Transpiration and soil evaporation ===
        double SCF_veg = 1 - exp(par._rE->val[j] * _LAI->val[j]);  // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972)
        double transp = gc * (Ec_s * rh_c - Ea_s * rh_a) / (461 * (Ta + 273.15)) / 1000 * DT;  // transpiraton in m/timestep; pho_water = 1000 kg/m3 for unit transformation from kg m2-1 s-1 to m s-1
        double Esoil = gs * (Es_s * rh_s - Ea_s * rh_a) / (461 * (Ta + 273.15)) / 1000 * DT * (1 - SCF_veg);  // soil evaporation in m/timestep; pho_water = 1000 kg/m3 for unit transformation from kg m2-1 s-1 to m s-1
        transp = transp < 0 ? 0 : transp;
        Esoil = Esoil < 0 ? 0 : Esoil;
  
        // Transpiration in layer 1
        Tr1 = min(transp * _froot_layer1->val[j], ST1 - minimum_theta);
        ST1 -= Tr1;
        // Soil evaporation in layer 1
        Esoil = min(Esoil, ST1 - minimum_theta);
        ST1 -= Esoil;

        // Transpiration in layer 2
        Tr2 = min(transp * _froot_layer2->val[j], ST2 - minimum_theta);
        ST2 -= Tr2;
        
        // Transpiration in layer 3
        Tr3 = min(transp * _froot_layer3->val[j], ST3 - minimum_theta);
        ST3 -= Tr3;

        // Update global variables
        _theta1->val[j] = ST1 / depth1;
        _theta2->val[j] = ST2 / depth2;
        _theta3->val[j] = ST3 / depth3;
        _Es->val[j] = Esoil;
        _Tr1->val[j] = Tr1;
        _Tr2->val[j] = Tr2;
        _Tr3->val[j] = Tr3;
        _Tr->val[j] = Tr1 + Tr2 + Tr3;



        
        // Debug todo
        /*
        if (j==1127) {
            cout << "_canopy_conductance->val[j] : "<< _canopy_conductance->val[j] << endl;
            cout << "ga : "<< ga << endl;
            cout << "gc : "<< gc << endl;
            cout << "gs : "<< gs << endl;
            cout << "ea : "<< Ea_s << endl;cout << "ec : "<< Ec_s << endl;
            cout << "ec : "<< Ec_s << endl;
            cout << "es : "<< Es_s << endl;
            cout << "rh_a : "<< rh_a << endl;
            cout << "rh_s : "<< rh_s << endl;
            cout << "ta : "<< Ta << endl;
            cout << "LAI : "<< _LAI->val[j] << endl;
            cout << "SCF_veg : "<< SCF_veg << endl;
            cout << "tranp : "<< transp   * 1000  << endl;
            cout << "Esoil : "<< Esoil   * 1000 << endl;
            cout << "--------------------------------" << endl;
        }
        */    



    

    }

    return EXIT_SUCCESS;
}