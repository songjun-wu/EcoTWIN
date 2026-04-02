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
        ET_weight = par._ET_weight->val[j];  // ET weight

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

    double soil_evap; // Soil evaporation [m per timestep]
    double Tr1; // Transpiration in layer 1 [m per timestep]
    double Tr2; // Transpiration in layer 2 [m per timestep]
    double Tr3; // Transpiration in layer 3 [m per timestep]
    double transp; // Transpiration [m per timestep]
    double depth1, depth2, depth3;
    double theta1, theta2, theta3;
    double ST1, ST2, ST3;
    double thetaS1;
    double FC1, FC2, FC3;
    double WP1, WP2, WP3;
    double evaporation_weight_by_depth; // Soil evaporation only happens in first 10 cm of soil
    // Radiation seperation
    double SCF_veg;  // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972)
    double Rnet_veg;  // Radiation for vegetation [W/m2]
    double Rnet_soil;  // Radiation for soil [W/m2]
    // === Saturated vapor pressure ===
    double Ta;  // Air temperature in degree Celsius
    double Ea_s;  // Saturated vapor pressure in atmosphere [Pa]
    // === Conductance ===
    // Water limitation factor averaged from three layers
    double water_limitation_factor;
    double ga; // Aerodynamic conductance [m/s]
    // Soil surface resistance from Sellers, P. J., et al. (1996)
    // https://doi.org/10.1175/1520-0442(1996)009<0676:ARLSPF>2.0.CO;2
    double rs_soil;
    double gs;
    double gc;  // Canopy conductance [m/s]


    // Parameters of Penman-Monteith equation
    double VPD;  // Vapour pressure deficit [Pa]
    double PM_delta; // Slope of saturated vapor pressure curve at air temperature [Pa/K]
    double PM_pho;  // Air density [kg/m3]
    double PM_cp;  // Specific heat capacity of air at constant pressure [J kg-1 K-1]
    double PM_lambda;  // Latent heat of vaporization of water [J kg-1]
    double PM_gamma;  // Psychrometric constant (Approximate value for standard pressure) [Pa K-1]

    //double minimum_theta = 1e-3;

    double DT = ctrl.Simul_tstep;  // Timestep length in seconds
    
    double f_rock;  // Fraction of rock in the grid cell [0, 1]

    



    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
       
        // Parameters
        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j]; // The lower boundary is included for calibration
        evaporation_weight_by_depth = depth1 > 0.1 ? 0.1/depth1 : 1.0;  // Soil evaporation only happens in first 10 cm of soil

        // Stages and fluxes
        theta1 = _theta1->val[j]; // Soil moisture in layer 1 [-]
        theta2 = _theta2->val[j]; // Soil moisture in layer 2 [-]
        theta3 = _theta3->val[j]; // Soil moisture in layer 3 [-]
        ST1 = theta1 * depth1; // Soil storage in layer 1 [m]
        ST2 = theta2 * depth2; // Soil storage in layer 2 [m]
        ST3 = theta3 * depth3; // Soil storage in layer 3 [m]
        thetaS1 = _thetaS1->val[j];
        WP1 = _thetaWP1->val[j];
        WP2 = _thetaWP2->val[j];
        WP3 = _thetaWP3->val[j];
        FC1 = _thetaFC1->val[j];
        FC2 = _thetaFC2->val[j];
        FC3 = _thetaFC3->val[j];

        // Initialization
        soil_evap = 0;
        Tr1 = 0;
        Tr2 = 0;
        Tr3 = 0;




        // ======= Penman-Monteith equation for transpiration and soil evaporation calculation =======
        // Radiation seperation
        SCF_veg = 1 - exp(par._rE->val[j] * _LAI->val[j]);  // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972)
        Rnet_veg = atm._Rnet->val[j] * SCF_veg;  // Radiation for vegetation [W/m2]
        Rnet_soil = atm._Rnet->val[j] - Rnet_veg;  // Radiation for soil [W/m2]

        // === Saturated vapor pressure ===
        Ta = atm._Ta->val[j];  // Air temperature in degree Celsius
        Ea_s = 611 * exp((17.3 * Ta)/(Ta + 237.3));  // Saturated vapor pressure in atmosphere [Pa]
        // === Conductance ===
        // Water limitation factor averaged from three layers
        water_limitation_factor =\  
        _froot_layer1->val[j] * (theta1 - WP1) / (FC1 - WP1) + 
        _froot_layer2->val[j] * (theta2 - WP2) / (FC2 - WP2) + 
        _froot_layer3->val[j] * (theta3 - WP3) / (FC3 - WP3);
        water_limitation_factor = min(max(0.0, water_limitation_factor), 1.0); 
        ga = 0.02 * 2.0; // Aerodynamic conductance [m/s]
        // Soil surface resistance from Sellers, P. J., et al. (1996)
        // https://doi.org/10.1175/1520-0442(1996)009<0676:ARLSPF>2.0.CO;2
        rs_soil = (1 / ga) + exp(8.2 - 4.255 * theta1/thetaS1);
        gs = 1 / rs_soil;
        gc = _canopy_conductance->val[j];  // Canopy conductance [m/s]



        


        // === Parameters of Penman-Monteith equation ===
        VPD = max(0.05, Ea_s * (1 - atm._RH->val[j]));  // Vapour pressure deficit [Pa]
        PM_delta = 4098 * Ea_s / ((Ta + 237.3)*(Ta + 237.3)) ; // Slope of saturated vapor pressure curve at air temperature [Pa/K]
        PM_pho = 1.2;  // Air density [kg/m3]
        PM_cp = 1005;  // Specific heat capacity of air at constant pressure [J kg-1 K-1]
        PM_lambda = 2.45e6;  // Latent heat of vaporization of water [J kg-1]
        PM_gamma = 65;  // Psychrometric constant (Approximate value for standard pressure) [Pa K-1]

        // === Penman-Monteith implementation ===
        transp = (PM_delta * Rnet_veg + PM_pho * PM_cp * VPD * ga) / (PM_lambda * (PM_delta + PM_gamma * (1 + ga/gc)));  // Transpiration [kg m-2 s-1]
        soil_evap = (PM_delta * Rnet_soil + PM_pho * PM_cp * VPD * ga) / (PM_lambda * (PM_delta + PM_gamma * (1 + ga/gs)));  // Soil evaporation [kg m-2 s-1]
        // Evaporation and Transpiration should be adjusted by par._ET_weight->val[j] due to potential underestimation of daily simulaton compared to integral of hourly simulaton
        // Set par._ET_weight->val[j] to 1 for subdaily simulation
        transp *= par._ET_weight->val[j] * DT / 1000;  // Unit transformation from kg m-2 s-1 to m per timestep
        soil_evap *= evaporation_weight_by_depth * par._ET_weight->val[j] * DT / 1000;  // Evaporation only happens in first 10 cm of soil; Unit transformation from kg m-2 s-1 to m per timestep
        transp = transp < 0 ? 0 : transp;
        soil_evap = soil_evap < 0 ? 0 : soil_evap;
        f_rock = par.param_category->val[ctrl.rock_category][j];
        soil_evap *= (1- f_rock * 0.5);  // Assumption: rock has 50% evaporation capacity

        
  
        // Transpiration in layer 1
        Tr1 = min(transp * _froot_layer1->val[j], ST1 - WP1*depth1);
        ST1 -= Tr1;
        // Soil evaporation in layer 1
        soil_evap = min(soil_evap, ST1 - WP1*depth1);
        ST1 -= soil_evap;

        // Transpiration in layer 2
        Tr2 = min(transp * _froot_layer2->val[j], ST2 - WP2*depth2);
        ST2 -= Tr2;
        
        // Transpiration in layer 3
        Tr3 = min(transp * _froot_layer3->val[j], ST3 - WP3*depth3);
        ST3 -= Tr3;

        // Update global variables
        _theta1->val[j] = ST1 / depth1;
        _theta2->val[j] = ST2 / depth2;
        _theta3->val[j] = ST3 / depth3;
        _Es->val[j] = soil_evap;
        _Tr1->val[j] = Tr1;
        _Tr2->val[j] = Tr2;
        _Tr3->val[j] = Tr3;
        _Tr->val[j] = Tr1 + Tr2 + Tr3;


       
        // Debug todo
        //if (j==1127) cout<<0.1/depth1<<"  "<<_Tr->val[j] <<"  "<<_Es->val[j]<<"  "<<_theta1->val[j]<<"  "<< water_limitation_factor<<"  "<<_canopy_conductance->val[j] << endl;
        /*
        if (j==1127) {
            cout << "_canopy_conductance->val[j] : "<< _canopy_conductance->val[j] << endl;
            cout << " Rnet_veg : "<< Rnet_veg << endl;
            cout << " Rnet_soil : "<< Rnet_soil << endl;
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