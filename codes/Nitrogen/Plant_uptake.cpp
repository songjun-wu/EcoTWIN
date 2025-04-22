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
                        uptake_help = up1[idx] - up2[idx] * exp( -up3[idx] * (day_of_year - plant_day[idx]));
                        uptake_IN = (up1[idx] * up2[idx] * up3[idx] * uptake_help) / (up2[idx] + uptake_help) / (up2[idx] + uptake_help);
                    }
                }

                _potential_uptake_layer1[i].push_back(uptake_IN * upper_uptake[idx]); //* p_cell * root_fraction_1
                _potential_uptake_layer2[i].push_back(uptake_IN * upper_uptake[idx]);   // * p_cell * (1 - root_fraction_1)
                _potential_uptake_layer3[i].push_back(uptake_IN * (1 - upper_uptake[idx])); // * p_cell 

            }
        }
        par.sort_plant_uptake_OK = 1;
    }
    return EXIT_SUCCESS;
}



int Basin::Plant_uptake(Control &ctrl, Param &par){

    double p_cell;  // The proportion of each land use type in the grid cell [decimal]
    double ST1, ST2;  // Soil storage in layer 1 and 2 [m]
    double root_fraction_1;  // root_fraction_1 / (root_fraction_1 + root_fraction_2); [decimal]
    double puptake_layer1, puptake_layer2, puptake_layer3;  // Potentail uptake in layer 1-3 [gN/m2]
    int idx;

    double day_of_year = ctrl.day_of_year;;  // Day of year
    //double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        puptake_layer1 = puptake_layer2 = puptake_layer3 = 0;
        root_fraction_1 = _p_perc1->val[j] / (_p_perc1->val[j] + _p_perc2->val[j]);

        for (int i = 0; i < num_landuse; i++) {
            idx = landuse_idx[i];
            p_cell = par.param_category->val[idx][j];
            if (p_cell <= 0) {
                continue;
            }
            
            if (day_of_year >= plant_day[idx] and day_of_year < harvest_day[idx]) {
                puptake_layer1 += _potential_uptake_layer1[i][day_of_year-1] * p_cell * root_fraction_1;
                puptake_layer2 += _potential_uptake_layer2[i][day_of_year-1] * p_cell * (1 - root_fraction_1);
                puptake_layer3 += _potential_uptake_layer3[i][day_of_year-1] * p_cell; 
            }

            

        }
    }
    return EXIT_SUCCESS;
}