#include "Basin.h"

/*
Evapotranspiration_1: 
Evapotranspiration calcualted based on PET and a soil water dependent root extraction function.
Citation: Feddes, R., Kowalik, P., Kolinska-Malinka, K., & Zaradny, H. (1976). Simulation of field water uptake by plants using a soil water dependent root extraction function. Journal of Hydrology, 31, 13-26. https://doi.org/10.1016/0022-1694(76)90017-2
*/


int Basin::Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm){

    // Calculate the root fraction
    if (par.param_category->parameterisation_OK == 0){
        double root_tmp_layer1, root_tmp_layer12, root_tmp_layer123;
        double root1, root2, root3, root_total;
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            double froot_coeff = par._froot_coeff->val[j];
            double depth1 = _depth1->val[j];
            double depth2 = _depth2->val[j];
            double depth3 = par._depth3->val[j]; // The lower boundary is included for calibration 

            root_tmp_layer1   = (1 - pow(froot_coeff, depth1 * 100)); // m to mm
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
            par.param_category->parameterisation_OK = 1;
        }
    }

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
        Esoil = min(PE*min(theta1/FC1, 1.0), ST1);
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
        Tr1 = min(PT*froot_coeff_corrcted, ST1);
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
        Tr2 = min(PT*froot_coeff_corrcted, ST2);
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
        Tr3 = min(PT*froot_coeff_corrcted, ST3);
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