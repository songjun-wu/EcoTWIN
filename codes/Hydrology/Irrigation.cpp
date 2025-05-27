#include "Basin.h"

int Basin::Irrigation(Control &ctrl, Param &par){

    double available_water_storage, plant_water_demand, irrigation_deficit, acc_irrigation_deficit;
    double irrigation_from_river, irrigation_from_GW;
    int idx;
    double p_cell;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // Initilisation
        irrigation_from_river = 0;
        irrigation_from_GW = 0;
        acc_irrigation_deficit = 0;

        if (par._irrigation_coeff->val[j] <= roundoffERR){
            _irrigation_from_river->val[j] = 0;
            _irrigation_from_GW->val[j] = 0;
            continue;
        }

        // Calculate the water deficit
        for (int i = 0; i < num_landuse; i++) {
            
            idx = landuse_idx[i];
            p_cell = par.param_category->val[idx][j];  // Area proportion of each land use type

            // Check if there is water demand for irrigation
            if (ctrl.day_of_year < plant_day[idx] or ctrl.day_of_year > harvest_day[idx]) continue;
            if (irrigation_thres[idx] <= roundoffERR or p_cell <= roundoffERR) continue;
       
            // Determine if irrigation is needed based on the water stress from the first two layers
            plant_water_demand = ((_thetaFC1->val[j]-_thetaWP1->val[j])*_depth1->val[j] + (_thetaFC2->val[j]-_thetaWP2->val[j])*_depth2->val[j]) * irrigation_thres[idx];
            available_water_storage = (_theta1->val[j]-_thetaWP1->val[j])*_depth1->val[j] + (_theta2->val[j]-_thetaWP2->val[j])*_depth2->val[j];
            irrigation_deficit = (plant_water_demand - available_water_storage) * p_cell * par._irrigation_coeff->val[j];  // Deficit scaled by an irrigation coefficient

            if (irrigation_deficit > roundoffERR){
                acc_irrigation_deficit  += irrigation_deficit;
            }
        }

        // Irrigation if needed
        if (acc_irrigation_deficit > 0){
            if (_chnwidth->val[j] > 0){  // If it is a channel grid
                irrigation_from_river = min(acc_irrigation_deficit, _chanS->val[j] * 0.5);
                acc_irrigation_deficit -=  irrigation_from_river;
                _chanS->val[j] -= irrigation_from_river;
            } 

            // Otherwise extract from GW
            if (acc_irrigation_deficit > roundoffERR){
                irrigation_from_GW = min(acc_irrigation_deficit, _GW->val[j]);
                _GW->val[j] -= irrigation_from_GW;
            }

        }

        // Save irrigation outputs
        _irrigation_from_river->val[j] = irrigation_from_river;
        _irrigation_from_GW->val[j] = irrigation_from_GW;
        _pond->val[j] += (irrigation_from_river + irrigation_from_GW);
    }

    return EXIT_SUCCESS;
}