#include "Basin.h"

int Basin::Soil_denitrification(Control &ctrl, Atmosphere &atm, Param &par){

    double Ts, fct_Ts, fct_theta, fct_conc;
    double theta1, theta2, theta3;
    double deni1, deni2, deni3;
    double diss_IN1, diss_IN2, diss_IN3;
    double no3_layer1, no3_layer2, no3_layer3;

    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        deni1 = 0; // Soil denitrification in layer1 [kg/ha]
        deni2 = 0; // Soil denitrification in layer2 [kg/ha]
        deni3 = 0; // Soil denitrification in layer3 [kg/ha]
        theta1 = _theta1->val[j];
        theta2 = _theta2->val[j];
        theta3 = _theta3->val[j];
        no3_layer1 = _no3_layer1->val[j];
        no3_layer2 = _no3_layer2->val[j];
        no3_layer3 = _no3_layer3->val[j];
        diss_IN1 = theta1 * _depth1->val[j] * no3_layer1;
        diss_IN2 = theta2 * _depth2->val[j] * no3_layer2;
        diss_IN3 = theta3 * par._depth3->val[j] * no3_layer3;
        Ts = Get_soil_temperature(atm._Ta->val[j], Ts, _LAI->val[j]);  // Soil temperature [Degree C]


        // Soil temperature factor [-]
        fct_Ts = Temp_factor(Ts);  

        // Layer 1
        if (theta1 > 0){
            // Soil moisture factor
            if (theta1 / _thetaS1->val[j] > 0.7){
                fct_theta = pow((theta1 / _thetaS1->val[j] - 0.7) / (1 - 0.7), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer1 * (no3_layer1 + 10);
            // Denitrification
            deni1 = diss_IN1 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc * DT, 1.0);
            no3_layer1 = (diss_IN1 - deni1) / (theta1 * _depth1->val[j]);
        }

        // Layer 2
        if (theta2 > 0){
            // Soil moisture factor
            if (theta2 / _thetaS2->val[j] > 0.7){
                fct_theta = pow((theta2 / _thetaS2->val[j] - 0.7) / (1 - 0.7), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer2 * (no3_layer2 + 10);
            // Denitrification
            deni2 = diss_IN2 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc / DT, 1.0);
            no3_layer2 = (diss_IN2 - deni2) / (theta2 * _depth2->val[j]);
        }

        // Layer 3
        if (theta3 > 0){
            // Soil moisture factor
            if (theta3 / _thetaS3->val[j] > 0.7){
                fct_theta = pow((theta3 / _thetaS3->val[j] - 0.7) / (1 - 0.7), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer3 * (no3_layer3 + 10);
            // Denitrification
            deni3 = diss_IN3 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc / DT, 1.0);
            no3_layer3 = (diss_IN3 - deni3) / (theta3 * par._depth3->val[j]);
        }

        // Update global variables
        _deni_soil->val[j] = deni1 + deni2 + deni3;
        _no3_layer1->val[j] = no3_layer1;
        _no3_layer2->val[j] = no3_layer2;
        _no3_layer3->val[j] = no3_layer3;
        
    }

    return EXIT_SUCCESS;
}



double Basin::Temp_factor(const double db_Ts){

    double Ts = db_Ts;  // Soil temperature [Degree C]
    double f_Ts = pow(2, (Ts - 20.0) / 10.0);  // Temperature factor

    if (Ts < 5.0) f_Ts *= (Ts / 5.0);
    if (Ts < 0.0) f_Ts = 0.0;

    return f_Ts;

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
        fct_theta = 0.6;
    } else if (db_theta < db_thetaWP){
        fct_theta = 0.0;
    } else {
        //fct_theta = min(1.0, (1 - fct_thetaS) * pow((db_thetaS - db_theta) / (fct_theta_up / 100 * db_depth * 1000), fct_theta_pow)  + fct_thetaS);
        //fct_theta = min(fct_theta, pow((db_theta - db_thetaWP) / (fct_theta_low /100 * db_depth * 1000), fct_theta_pow));
        fct_theta = min(1.0, 0.4 * (db_thetaS - db_theta) / (1.2 * db_depth) + 0.6);
        fct_theta = min(fct_theta, (db_theta - db_thetaWP) / (0.8 * db_depth));
    }

    return fct_theta;

}
