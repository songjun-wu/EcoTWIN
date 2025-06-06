/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Plant_uptake.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Sort_plant_uptake(Control &ctrl, Param &par){

    double uptake_help, uptake_IN;
    vector<double> potential_uptake_IN_layer1, potential_uptake_IN_layer2, potential_uptake_IN_layer3;
    int idx;

    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps
    if (par.sort_plant_uptake_OK==0) {

        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            _potential_uptake_layer1.push_back(vector<double> ());
            _potential_uptake_layer2.push_back(vector<double> ());
            _potential_uptake_layer3.push_back(vector<double> ());
        
            for (unsigned int day_of_year = 0; day_of_year < 366; day_of_year++) {

                if (plant_day[idx] <= harvest_day[idx]){
                    if (day_of_year >= plant_day[idx] and day_of_year < harvest_day[idx]){
                        uptake_help = (up1[idx] - up2[idx]) * exp( -up3[idx] * (day_of_year - plant_day[idx]));
                        uptake_IN = (up1[idx] * up2[idx] * up3[idx] * uptake_help) / (up2[idx] + uptake_help) / (up2[idx] + uptake_help);
                    }else {
                        uptake_IN = 0.0;
                    }
                } 

                _potential_uptake_layer1[i].push_back(uptake_IN * upper_uptake[idx]); // * p_cell * root_fraction_1
                _potential_uptake_layer2[i].push_back(uptake_IN * upper_uptake[idx]);   // * p_cell * (1 - root_fraction_1)
                _potential_uptake_layer3[i].push_back(uptake_IN * (1 - upper_uptake[idx])); // * p_cell 
                
            }
        }
        par.sort_plant_uptake_OK = 1;
    }
    return EXIT_SUCCESS;
}



int Basin::Plant_uptake(Control &ctrl, Param &par, Atmosphere &atm){

    double p_cell;  // The proportion of each land use type in the grid cell [decimal]
    double root_fraction_1;  // root_fraction_1 / (root_fraction_1 + root_fraction_2); [decimal]
    double theta1, theta2, theta3;  // Soil moisture content in layer 1-3 [decimal]
    double dissIN1, dissIN2, dissIN3;  // IN storage in layer 1-3 [gN/m2]
    double potential_plant_uptake1, potential_plant_uptake2, potential_plant_uptake3;  // Potentail uptake in layer 1-3 [gN/m2]
    double plant_uptake1, plant_uptake2, plant_uptake3;  // Actual plant uptake in layer 1-3 [gN/m2]
    double temp_fct_uptake;  // The temperature function of vegetation uptake 
    double max_uptake;  // Maximum plant uptake [gN/m2]
    int idx;

    double day_of_year = ctrl.day_of_year;;  // Day of year
    //double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


        potential_plant_uptake1 = potential_plant_uptake2 = potential_plant_uptake3 = 0;
        
        root_fraction_1 = _p_perc1->val[j] / (_p_perc1->val[j] + _p_perc2->val[j]);

        // Get potential uptake
        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            p_cell = par.param_category->val[idx][j];
            if (p_cell <= 0) {
                continue;
            }
            if (day_of_year >= plant_day[idx] and day_of_year < harvest_day[idx]) {
                potential_plant_uptake1 += _potential_uptake_layer1[i][day_of_year-1] * p_cell * root_fraction_1;           // [gN/m2]
                potential_plant_uptake2 += _potential_uptake_layer2[i][day_of_year-1] * p_cell * (1 - root_fraction_1);     // [gN/m2]
                potential_plant_uptake3 += _potential_uptake_layer3[i][day_of_year-1] * p_cell;                             // [gN/m2]
            }            
        }
        // Correction based on temperature 
        temp_fct_uptake = min((atm._Ta->val[j] - 5) / 20, 1.0);
        temp_fct_uptake = max(0.0, temp_fct_uptake);
        potential_plant_uptake1 *= temp_fct_uptake;
        potential_plant_uptake2 *= temp_fct_uptake;
        potential_plant_uptake3 *= temp_fct_uptake;

        plant_uptake1 = plant_uptake2 = plant_uptake3 = 0;
        theta1 = _theta1->val[j];
        theta2 = _theta2->val[j];
        theta3 = _theta3->val[j];
        dissIN1 = theta1 * _depth1->val[j] * _no3_layer1->val[j];
        dissIN2 = theta2 * _depth2->val[j] * _no3_layer2->val[j];
        dissIN3 = theta3 * par._depth3->val[j] * _no3_layer3->val[j];
        
        // Calculate actual uptake
        // Layer1
        if (theta1 > _thetaWP1->val[j]){
            if (dissIN1 > roundoffERR and potential_plant_uptake1 > roundoffERR){
                max_uptake = dissIN1 * (theta1 - _thetaWP1->val[j]) / theta1;
                plant_uptake1 = min(potential_plant_uptake1, max_uptake);
                _no3_layer1->val[j] = (dissIN1 - plant_uptake1) / (theta1 * _depth1->val[j]);
            }
        }

        // Layer 2
        if (theta2 > _thetaWP2->val[j]){
            if (dissIN2 > roundoffERR and potential_plant_uptake2 > roundoffERR){
                max_uptake = dissIN2 * (theta2 - _thetaWP2->val[j]) / theta2;
                plant_uptake2 = min(potential_plant_uptake2, max_uptake);
                _no3_layer2->val[j] = (dissIN2 - plant_uptake2) / (theta2 * _depth2->val[j]);
            }
        }
        
        // Layer 3
        if (theta3 > _thetaWP3->val[j]){
            if (dissIN3 > roundoffERR and potential_plant_uptake3 > roundoffERR){
                max_uptake = dissIN3 * (theta3 - _thetaWP3->val[j]) / theta3;
                plant_uptake3 = min(potential_plant_uptake3, max_uptake);
                _no3_layer3->val[j] = (dissIN3 - plant_uptake3) / (theta3 * par._depth3->val[j]);
            }
        }
    
        // Aggregate plant uptake in three layers; NO3 concentration has been updated
        _plant_uptake->val[j] = plant_uptake1 + plant_uptake2 + plant_uptake3;
    }
    return EXIT_SUCCESS;
}