/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Nitrogen_addition.cpp
  * Created  on: 30.02.2025
  * Modified on: 01.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Sort_nitrogen_addition(Control &ctrl, Param &par){

    double fertN_add_layer1_IN, fertN_add_layer1_fast_NP, fertN_add_layer2_IN, fertN_add_layer2_fast_NP;  // fertilisation and manure N addition to layer 1 and 2 [mgN/L*m = gN/m2]
    int idx;
    double fert_add_tmp;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    if (par.sort_nitrogen_addition_OK == 0){

        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            _fertN_add_layer1_IN.push_back(vector<double> ());
            _fertN_add_layer1_fast_NP.push_back(vector<double> ());
            _fertN_add_layer2_IN.push_back(vector<double> ());
            _fertN_add_layer2_fast_NP.push_back(vector<double> ());

            for (unsigned int day_of_year = 0; day_of_year < 366; day_of_year++) {
                fertN_add_layer1_IN = fertN_add_layer1_fast_NP = fertN_add_layer2_IN = fertN_add_layer2_fast_NP = 0;

                       
                // Fertilization addition to IN and fast_NP pools
                if (ctrl.opt_fert_input==1 and is_crop[idx] == 1){  // Input from raster map
                    fert_add_tmp = 1.0;  // Will be scaled for each grid in module <Nitrogen_addition>
                    if (day_of_year >= fert_day[idx] and day_of_year< (fert_day[idx] + fert_period[idx])){
                        fertN_add_layer1_IN     += fert_add_tmp * (1 - fert_down[idx]) * DT / fert_period[idx] * fert_IN[idx];         // * p_cell 
                        fertN_add_layer1_fast_NP  += fert_add_tmp * (1 - fert_down[idx]) * DT / fert_period[idx] * (1 - fert_IN[idx]);   // * p_cell
                        fertN_add_layer2_IN     += fert_add_tmp *      fert_down[idx]  * DT / fert_period[idx] * fert_IN[idx];         // * p_cell 
                        fertN_add_layer2_fast_NP  += fert_add_tmp *      fert_down[idx]  * DT / fert_period[idx] * (1 - fert_IN[idx]);   // * p_cell
                    }
                } else {  // Input from table (Crop_info.ini)
                    if (fert_add[idx] > 0){
                        fert_add_tmp = fert_add[idx];
                        if (day_of_year >= fert_day[idx] and day_of_year< (fert_day[idx] + fert_period[idx])){
                            fertN_add_layer1_IN     += fert_add_tmp * (1 - fert_down[idx]) * DT / fert_period[idx] * fert_IN[idx];         // * p_cell 
                            fertN_add_layer1_fast_NP  += fert_add_tmp * (1 - fert_down[idx]) * DT / fert_period[idx] * (1 - fert_IN[idx]);   // * p_cell
                            fertN_add_layer2_IN     += fert_add_tmp *      fert_down[idx]  * DT / fert_period[idx] * fert_IN[idx];         // * p_cell 
                            fertN_add_layer2_fast_NP  += fert_add_tmp *      fert_down[idx]  * DT / fert_period[idx] * (1 - fert_IN[idx]);   // * p_cell
                        }
                    }
                }


                // Manure application to IN and fast_NP pools
                if (ctrl.opt_fert_input==1 and is_crop[idx] == 1){}  // Fert and mannure imported from map, assigned to zero here

                if (manure_add[idx] > 0){
                    if (day_of_year >= manure_day[idx] and day_of_year< (manure_day[idx] + manure_period[idx])){
                        fertN_add_layer1_IN     += manure_add[idx] * (1 - manure_down[idx]) * DT / manure_period[idx] * manure_IN[idx];         // * p_cell 
                        fertN_add_layer1_fast_NP  += manure_add[idx] * (1 - manure_down[idx]) * DT / manure_period[idx] * (1 - manure_IN[idx]);   // * p_cell 
                        fertN_add_layer2_IN     += manure_add[idx] *      manure_down[idx]  * DT / manure_period[idx] * manure_IN[idx];         // * p_cell
                        fertN_add_layer2_fast_NP  += manure_add[idx] *      manure_down[idx]  * DT / manure_period[idx] * (1 - manure_IN[idx]);   // * p_cell
                    }
                }

                // Local to global
                _fertN_add_layer1_IN[i].push_back(fertN_add_layer1_IN);
                _fertN_add_layer1_fast_NP[i].push_back(fertN_add_layer1_fast_NP);
                _fertN_add_layer2_IN[i].push_back(fertN_add_layer2_IN);
                _fertN_add_layer2_fast_NP[i].push_back(fertN_add_layer2_fast_NP);
            }
        }
        par.sort_nitrogen_addition_OK = 1;
    }
    return EXIT_SUCCESS;
}


int Basin::Nitrogen_addition(Control &ctrl, Param &par){

    double p_cell;  // The proportion of each land use type in the grid cell [decimal]
    double fertN_add_layer1_IN, fertN_add_layer1_fast_NP, fertN_add_layer2_IN, fertN_add_layer2_fast_NP;  // fertilisation and manure N addition to layer 1 and 2 [mgN/L*m = gN/m2]
    double ST1, ST2;  // Soil storage in layer 1 and 2 [m]
    int idx;

    double day_of_year = ctrl.day_of_year;;  // Day of year

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        ST1 = _theta1->val[j] * _depth1->val[j];
        ST2 = _theta2->val[j] * _depth2->val[j];

        
        fertN_add_layer1_IN = fertN_add_layer1_fast_NP = fertN_add_layer2_IN = fertN_add_layer2_fast_NP = 0;
        
        // Calcualte the nitrogen addition to IN, fast_NP, and humus_NP N pools in layer 1 and 2
        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            p_cell = par.param_category->val[idx][j];
            
            if (p_cell > 0){
                // IN and fast_NP
                if (ctrl.opt_fert_input==1 and is_crop[idx] == 1){  // Fertilizer is determined by raster inputs
                    fertN_add_layer1_IN += _fertN_add_layer1_IN[i][day_of_year-1] * p_cell * _N_fertilization->val[j];
                    fertN_add_layer1_fast_NP += _fertN_add_layer1_fast_NP[i][day_of_year-1] * p_cell * _N_fertilization->val[j];
                    fertN_add_layer2_IN += _fertN_add_layer2_IN[i][day_of_year-1] * p_cell * _N_fertilization->val[j];
                    fertN_add_layer2_fast_NP += _fertN_add_layer2_fast_NP[i][day_of_year-1] * p_cell * _N_fertilization->val[j];
                } else { // Fertilizer is determined by table inputs (Crop_info.ini)
                    fertN_add_layer1_IN += _fertN_add_layer1_IN[i][day_of_year-1] * p_cell;
                    fertN_add_layer1_fast_NP += _fertN_add_layer1_fast_NP[i][day_of_year-1] * p_cell;
                    fertN_add_layer2_IN += _fertN_add_layer2_IN[i][day_of_year-1] * p_cell;
                    fertN_add_layer2_fast_NP += _fertN_add_layer2_fast_NP[i][day_of_year-1] * p_cell;
                
                }
            }
        }

       
        // Nitrogen addition to layer 1
        if (ST1 > 0){
            _no3_layer1->val[j] = (ST1 * _no3_layer1->val[j] + fertN_add_layer1_IN) / ST1;
        } else {
            _fast_NP1_nonwood->val[j] += fertN_add_layer1_IN;
        }
        _fast_NP1_nonwood->val[j]  += fertN_add_layer1_fast_NP;

        // Nitrogen addition to layer 2
        if (ST2 > 0){
            _no3_layer2->val[j] = (ST2 * _no3_layer2->val[j] + fertN_add_layer2_IN) / ST2;
        } else {
            _fast_NP1_nonwood->val[j] += fertN_add_layer2_IN;
        }
        _fast_NP1_nonwood->val[j]  += fertN_add_layer2_fast_NP;  // The fast pool addtion will only be added to the nonwood pool in layer 1


        // Only counts the Nitrogen addition to IN and fast_NP pools
        _nitrogen_add->val[j] += fertN_add_layer1_IN + fertN_add_layer2_IN + fertN_add_layer1_fast_NP + fertN_add_layer2_fast_NP;
        //_nitrogen_add->val[j] = fertN_add_layer1_IN + fertN_add_layer2_IN;

    }
    return EXIT_SUCCESS;
}