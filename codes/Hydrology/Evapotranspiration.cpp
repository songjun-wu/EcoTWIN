#include "Basin.h"

/*
Evapotranspiration_1: 
Evapotranspiration calcualted based on PET and a soil water dependent root extraction function.
Citation: Feddes, R., Kowalik, P., Kolinska-Malinka, K., & Zaradny, H. (1976). Simulation of field water uptake by plants using a soil water dependent root extraction function. Journal of Hydrology, 31, 13-26. https://doi.org/10.1016/0022-1694(76)90017-2
*/


int Basin::Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm){

    double Esoil; // Soil evaporation in layer 1
    double AET1; // Evapotranspiration in layer 1
    double Tr1; // Transpiration in layer 1
    double Tr2; // Transpiration in layer 2
    double Tr3; // Transpiration in layer 3

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

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Parameters
        double froot_coeff_corrcted;
        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j]; // The lower boundary is included for calibration

        // Stages and fluxes
        double PET = atm._PET->val[j]; // Remaining potential evapotranspiration;
        double Throughfall = _Th->val[j]; // Throughfall [m]
        double theta1 = _theta1->val[j]; // Soil moisture in layer 1 [-]
        double theta2 = _theta2->val[j]; // Soil moisture in layer 2 [-]
        double theta3 = _theta3->val[j]; // Soil moisture in layer 3 [-]
        double ST1 = theta1 * depth1; // Soil storage in layer 1 [m]
        double ST2 = theta2 * depth2; // Soil storage in layer 2 [m]
        double ST3 = theta3 * depth3; // Soil storage in layer 3 [m]

        double WP1 = _thetaWP1->val[j];
        double WP2 = _thetaWP2->val[j];
        double WP3 = _thetaWP3->val[j];
        double FC1 = _thetaFC1->val[j];
        double FC2 = _thetaFC2->val[j];
        double FC3 = _thetaFC3->val[j];

        // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972); Here included for calibration
        double SCF_veg = 1 - exp(par._rE->val[j] * _LAI->val[j]);  
        
        // For layer 1
        froot_coeff_corrcted = _froot_layer1->val[j] * (theta1 - WP1) / (FC1 - WP1);  
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        AET1 = min(PET*froot_coeff_corrcted, ST1);  // E + T
        Tr1 = AET1 * SCF_veg;
        Esoil = AET1 - Tr1;
        ST1 -= AET1;
        PET -= AET1;

        // For layer 2
        froot_coeff_corrcted = _froot_layer2->val[j] * (theta2 - WP2) / (FC2 - WP2);
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr2 = min(PET*froot_coeff_corrcted, ST2);
        ST2 -= Tr2;
        PET -= Tr2;

        // For layer 3
        froot_coeff_corrcted = _froot_layer3->val[j] * (theta3 - WP3) / (FC3 - WP3);
        froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
        Tr3 = min(PET*froot_coeff_corrcted, ST3);
        ST3 -= Tr3;
        PET -= Tr3;

        _theta1->val[j] = ST1 / depth1;
        _theta2->val[j] = ST2 / depth2;
        _theta3->val[j] = ST3 / depth3;
        _Es->val[j] = Esoil;
        _Tr1->val[j] = Tr1;
        _Tr2->val[j] = Tr2;
        _Tr3->val[j] = Tr3;
        _Tr->val[j] = Tr1 + Tr2 + Tr3;
        atm._PET->val[j] = PET;

    }

    return EXIT_SUCCESS;
}