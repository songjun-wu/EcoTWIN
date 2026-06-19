/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Soil_denitrification.cpp
  * Created  on: 30.02.2025
  * Modified on: 03.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Soil_denitrification(Control &ctrl, Atmosphere &atm, Param &par){

    double depth1, depth2, depth3;
    double Ts, fct_Ts, fct_theta, fct_conc;
    double theta1, theta2, theta3;
    double deni1, deni2, deni3;
    double diss_IN1, diss_IN2, diss_IN3;
    double no3_layer1, no3_layer2, no3_layer3;

    double moisture_function_threshold;
    double fdepth_decay_Exp, fct_depth_layer1, fct_depth_layer2, fct_depth_layer3;

    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        deni1 = 0; // Soil denitrification in layer1 [gN/m2]
        deni2 = 0; // Soil denitrification in layer2 [gN/m2]
        deni3 = 0; // Soil denitrification in layer3 [gN/m2]
        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j];
        theta1 = _theta1->val[j];
        theta2 = _theta2->val[j];
        theta3 = _theta3->val[j];
        no3_layer1 = _no3_layer1->val[j]; // Nitrate concentration in layer 1 [mgN/L]
        no3_layer2 = _no3_layer2->val[j]; // Nitrate concentration in layer 2 [mgN/L]
        no3_layer3 = _no3_layer3->val[j]; // Nitrate concentration in layer 3 [mgN/L]
        diss_IN1 = theta1 * depth1 * no3_layer1; // Dissolved inorganic nitrogen in layer 1 [mgN/L * m = gN/m2]
        diss_IN2 = theta2 * depth2 * no3_layer2; // Dissolved inorganic nitrogen in layer 2 [mgN/L * m = gN/m2]
        diss_IN3 = theta3 * depth3 * no3_layer3; // Dissolved inorganic nitrogen in layer 3 [mgN/L * m = gN/m2]
        Ts = Get_soil_temperature(atm._Ta->val[j], _LAI->val[j]);  // Soil temperature [Degree C]

        moisture_function_threshold = par._deni_soil_moisture_thres->val[j];

        

        // Soil temperature factor [-]
        fct_Ts = Temp_factor(Ts, par._transformation_exp_base->val[j]);  

        // Factors of soil depth; decay exponentially with depth
        fdepth_decay_Exp = par._fdepth_decay_Exp->val[j];
        fct_depth_layer1 =  exp(-fdepth_decay_Exp * depth1/2);
        fct_depth_layer2 =  exp(-fdepth_decay_Exp * (depth1+depth2/2));
        fct_depth_layer3 =  exp(-fdepth_decay_Exp * (depth1+depth2+depth3/2));


        // Layer 1
        if (theta1 > 0){
            // Soil moisture factor
            if (theta1 / _thetaS1->val[j] > moisture_function_threshold){
                fct_theta = pow((theta1 / _thetaS1->val[j] - moisture_function_threshold) / (1 - moisture_function_threshold), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer1 / (no3_layer1 + 1.5);
            // Denitrification
            deni1 = diss_IN1 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc * fct_depth_layer1 * DT, 0.5);
            no3_layer1 = (diss_IN1 - deni1) / (theta1 * _depth1->val[j]);
        }

        // Layer 2
        if (theta2 > 0){
            // Soil moisture factor
            if (theta2 / _thetaS2->val[j] > moisture_function_threshold){
                fct_theta = pow((theta2 / _thetaS2->val[j] - moisture_function_threshold) / (1 - moisture_function_threshold), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer2 / (no3_layer2 + 1.5);
            // Denitrification
            deni2 = diss_IN2 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc * fct_depth_layer2 * DT, 0.5);
            no3_layer2 = (diss_IN2 - deni2) / (theta2 * _depth2->val[j]);
        }

        // Layer 3
        if (theta3 > 0){
            // Soil moisture factor
            if (theta3 / _thetaS3->val[j] > moisture_function_threshold){
                fct_theta = pow((theta3 / _thetaS3->val[j] - moisture_function_threshold) / (1 - moisture_function_threshold), 2.5);
            } else{
                fct_theta = 0;
            }
            // Concentration factor
            fct_conc = no3_layer3 / (no3_layer3 + 1.5);
            // Denitrification
            deni3 = diss_IN3 * min(par._denitrification_soil->val[j] * fct_Ts * fct_theta * fct_conc * fct_depth_layer3 * DT, 0.5);
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
