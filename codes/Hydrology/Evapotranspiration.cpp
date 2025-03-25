#include "Basin.h"

/*
Evapotranspiration_1: 
Evapotranspiration calcualted based on PET and a soil water dependent root extraction function.
Citation: Feddes, R., Kowalik, P., Kolinska-Malinka, K., & Zaradny, H. (1976). Simulation of field water uptake by plants using a soil water dependent root extraction function. Journal of Hydrology, 31, 13-26. https://doi.org/10.1016/0022-1694(76)90017-2
*/


int Basin::Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm, int j){

    // Parameters
    double froot_coeff = par._froot_coeff->val[j];
    double froot_coeff_corrcted;
    double depth1 = _depth1->val[j];
    double depth2 = _depth2->val[j];
    double depth3 = par._depth3->val[j]; // The lower boundary is included for calibration

    // Stages and fluxes
    double PET = atm._PET->val[j]; // Remaining potential transpiration;
    double Throughfall = _Th->val[j]; // Throughfall [m]
    double theta1 = _theta1->val[j]; // Soil moisture in layer 1 [-]
    double theta2 = _theta2->val[j]; // Soil moisture in layer 2 [-]
    double theta3 = _theta3->val[j]; // Soil moisture in layer 3 [-]
    double ST1 = theta1 * depth1; // Soil storage in layer 1 [m]
    double ST2 = theta2 * depth2; // Soil storage in layer 2 [m]
    double ST3 = theta3 * depth3; // Soil storage in layer 3 [m]

    double Esoil; // Soil evaporation in layer 1
    double AET1; // Evapotranspiration in layer 1
    double Tr1; // Transpiration in layer 1
    double Tr2; // Transpiration in layer 2
    double Tr3; // Transpiration in layer 3

    double WP1 = 0.1;
    double WP2 = 0.1;
    double WP3 = 0.1;
    double FC1 = 0.6;
    double FC2 = 0.6;
    double FC3 = 0.6;

    // Surface cover fraction of vegetation, rExtinct = -0.463 Rutter (1972); Here included for calibration
    double SCF_veg = 1 - exp(par._rE->val[j] * atm._LAI->val[j]);

    if (par.param_category->parameterisation_OK == 0){
        _froot_soil->val[j] = (1 - pow(froot_coeff, (depth1 + depth2 + depth3) * 100)); // mm to m
        _froot_layer2->val[j] = (1 - pow(froot_coeff, depth1 * 100));
        _froot_layer3->val[j] = (1 - pow(froot_coeff, (depth1 + depth2) * 100));
        par.param_category->parameterisation_OK = 1;
    }
    

    // For layer 1
    froot_coeff_corrcted = _froot_soil->val[j] * (theta1 - WP1) / (FC1 - WP1);  
    froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
    AET1 = min(PET*froot_coeff_corrcted, ST1);  // E + T
    Tr1 = AET1 * SCF_veg;
    Esoil = AET1 - Tr1;
    ST1 -= AET1;
    PET -= AET1;

    

    // For layer 2
    froot_coeff_corrcted = (_froot_soil->val[j] - _froot_layer2->val[j]) * (theta2 - WP2) / (FC2 - WP2);
    froot_coeff_corrcted = min(froot_coeff_corrcted, 1.0);
    Tr2 = min(PET*froot_coeff_corrcted, ST2);
    ST2 -= Tr2;
    PET -= Tr2;

    // For layer 3
    froot_coeff_corrcted = (_froot_soil->val[j] - _froot_layer3->val[j]) * (theta3 - WP3) / (FC3 - WP3);
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


    return EXIT_SUCCESS;
}