#include "Basin.h"

int Basin::Sort_nitrogen_addition(Control &ctrl, Param &par){

    double IN_add_layer1, IN_add_layer2;  // IN addition to layer 1 and 2 [mgN/L*m = gN/m2]
    int idx;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    if (par.sort_nitrogen_addition_OK == 0){
        
        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            _nitrogen_addition_layer1.push_back(vector<double> ());
            _nitrogen_addition_layer2.push_back(vector<double> ());
            for (unsigned int day_of_year = 0; day_of_year < 366; day_of_year++) {
                IN_add_layer1 = IN_add_layer2 = 0;
            
            
                
                // Fertilization
                if (fert_add[idx] > 0){
                    if (day_of_year >= fert_day[idx] and day_of_year< (fert_day[idx] + fert_period[idx])){
                        IN_add_layer1 += fert_add[idx] * (1 - fert_down[idx]) * DT / fert_period[idx];  // * p_cell 
                        IN_add_layer2 += fert_add[idx] *      fert_down[idx]  * DT / fert_period[idx]; // * p_cell
                    }
                }
                
                // Manure application
                if (manure_add[idx] > 0){
                    if (day_of_year >= manure_day[idx] and day_of_year< (manure_day[idx] + manure_period[idx])){
                        IN_add_layer1 += manure_add[idx] * (1 - manure_down[idx]) * DT / manure_period[idx];  // * p_cell 
                        IN_add_layer2 += manure_add[idx] *      manure_down[idx]  * DT / manure_period[idx];  // * p_cell 
                    }
                }

                // Plant residue addtion
                if (residue_add[idx] > 0){
                    if (day_of_year >= residue_day[idx] and day_of_year< (residue_day[idx] + residue_period[idx])){
                        IN_add_layer1 += residue_add[idx] * (1 - residue_down[idx]) * DT / residue_period[idx];  // * p_cell 
                        IN_add_layer2 += residue_add[idx] *      residue_down[idx]  * DT / residue_period[idx];  // * p_cell 
                    }
                }

                // Local to global
                _nitrogen_addition_layer1[i].push_back(IN_add_layer1);
                _nitrogen_addition_layer2[i].push_back(IN_add_layer2);
            }
        }
        par.sort_nitrogen_addition_OK = 1;
    }
    return EXIT_SUCCESS;
}


int Basin::Nitrogen_addition(Control &ctrl, Param &par){

    double p_cell;  // The proportion of each land use type in the grid cell [decimal]
    double IN_add_layer1, IN_add_layer2;  // IN addition to soil layer 1 and 2 [mgN/L*m = gN/m2]
    double ST1, ST2;  // Soil storage in layer 1 and 2 [m]
    int idx;

    double day_of_year = ctrl.day_of_year;;  // Day of year
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        ST1 = _theta1->val[j] * _depth1->val[j];
        ST2 = _theta2->val[j] * _depth2->val[j];

        
        IN_add_layer1 = IN_add_layer2 = 0;

        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            p_cell = par.param_category->val[idx][j];

            if (p_cell > 0){
                IN_add_layer1 += _nitrogen_addition_layer1[i][day_of_year-1] * p_cell;
                IN_add_layer2 += _nitrogen_addition_layer2[i][day_of_year-1] * p_cell;            
            }
        }

        // Update Nitrate concentration
        _nitrogen_add->val[j] = IN_add_layer1 + IN_add_layer2;
        _no3_layer1->val[j] = (ST1 * _no3_layer1->val[j] + IN_add_layer1) / ST1;
        _no3_layer2->val[j] = (ST2 * _no3_layer2->val[j] + IN_add_layer2) / ST2;

    }
    return EXIT_SUCCESS;
}