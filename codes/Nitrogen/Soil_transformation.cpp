/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Soil_transformation.cpp
  * Created  on: 30.02.2025
  * Modified on: 03.06.2025
***************************************************************/




#include "Basin.h"

int Basin::Soil_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double Ts, fct_Ts, fct_theta, fct_conc;
    double theta1, theta2, theta3;
    double minerl1, minerl2, minerl3;
    double degrad1, degrad2, degrad3;
    double dissIN1, dissIN2, dissIN3;

    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        minerl1 = minerl2 = minerl3 = 0; // Soil mineralisation in three layers [mgN/L*m = gN/m2]
        degrad1 = degrad2 = degrad3 = 0; // Soil degradation in three layers [mgN/L*m = gN/m2]
        theta1 = _theta1->val[j];
        theta2 = _theta2->val[j];
        theta3 = _theta3->val[j];
        dissIN1 = theta1 * _depth1->val[j] * _no3_layer1->val[j];
        dissIN2 = theta2 * _depth2->val[j] * _no3_layer2->val[j];
        dissIN3 = theta3 * par._depth3->val[j] * _no3_layer3->val[j];
        Ts = Get_soil_temperature(atm._Ta->val[j], _LAI->val[j]);  // Soil temperature [Degree C]


        // Soil temperature factor [-]
        fct_Ts = Temp_factor(Ts);  

        // Layer 1
        fct_theta = Moist_factor(theta1, _thetaWP1->val[j], _thetaS1->val[j], _depth1->val[j]);
        // Degradation: from humusN pool to fastN pool
        degrad1 = _humusN1->val[j] * min(par._degradation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
        _humusN1->val[j] -= degrad1;
        _fastN1->val[j] += degrad1;
        // Mineralisation: from fastN pool to dissolved IN (only when theta > 0)
        if (theta1 > 0){
            minerl1 = _fastN1->val[j] * min(par._mineralisation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
            _fastN1->val[j] -= minerl1;
            dissIN1 += minerl1;
            _no3_layer1->val[j] = dissIN1 / (theta1 * _depth1->val[j]);
        }
        

        // Layer 2
        fct_theta = Moist_factor(theta2, _thetaWP2->val[j], _thetaS2->val[j], _depth2->val[j]);
        // Degradation: from humusN pool to fastN pool
        degrad2 = _humusN2->val[j] * min(par._degradation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
        _humusN2->val[j] -= degrad2;
        _fastN2->val[j] += degrad2;
        // Mineralisation: from fastN pool to dissolved IN (only when theta > 0)
        if (theta2 > 0){
            minerl2 = _fastN2->val[j] * min(par._mineralisation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
            _fastN2->val[j] -= minerl2;
            dissIN2 += minerl2;
            _no3_layer2->val[j] = dissIN2 / (theta2 * _depth2->val[j]);
        }
        

        // Layer 3
        fct_theta = Moist_factor(theta3, _thetaWP3->val[j], _thetaS3->val[j], par._depth3->val[j]);
        // Degradation: from humusN pool to fastN pool
        degrad3 = _humusN3->val[j] * min(par._degradation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
        _humusN3->val[j] -= degrad3;
        _fastN3->val[j] += degrad3;
        // Mineralisation: from fastN pool to dissolved IN (only when theta > 0)
        if (theta3 > 0){
            minerl3 = _fastN3->val[j] * min(par._mineralisation_soil->val[j] * fct_Ts * fct_theta / DT, 1.0);
            _fastN3->val[j] -= minerl3;
            dissIN3 += minerl3;
            _no3_layer3->val[j] = dissIN3 / (theta3 * par._depth3->val[j]);
        }
        

        // Update global variables
        _degrad_soil->val[j] = degrad1 + degrad2 + degrad3;
        _minerl_soil->val[j] = minerl1 + minerl2 + minerl3;
        
        
        

        
    }

    return EXIT_SUCCESS;
}


