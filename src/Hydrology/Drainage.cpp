/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Drainage.cpp
  * Created  on: 22.12.2025
  * Modified on: 22.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Drainage(Control &ctrl, Param &par){

    double depth1, depth2, depth3;  // Soil layer dpeth [m]
    double theta1, theta2, theta3;  // Soil moisture [m3/m3]
    double thetaFC1, thetaFC2, thetaFC3;  // Field capacity [m3/m3]

    double drainage_depth;  // Drainage depth [m]
    double relative_drainage_depth;  // Drainage depth relative to the bottom of soil layer [0-1]
    double relative_grounwater_table;  // Groundwater table relative to the bottom of soil layer [0-1]
    double drainage1, drainage2, drainage3;  // Drainage amount for each soil layer [m]
    double drainage_cumulative;  // Cumulative drainage amount [m]

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        if (_drainage_depth->val[j] < roundoffERR) continue;
        

        drainage_depth = _drainage_depth->val[j];
        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j];
        theta1 = _theta1->val[j];
        theta2 = _theta2->val[j];
        theta3 = _theta3->val[j];
        thetaFC1 = _thetaFC1->val[j];
        thetaFC2 = _thetaFC2->val[j];
        thetaFC3 = _thetaFC3->val[j];
        drainage1 = 0.0;
        drainage2 = 0.0;
        drainage3 = 0.0;
        drainage_cumulative = 0.0;

        // Soil layer 1
        relative_drainage_depth =  max(0.0, (depth1 - drainage_depth) / depth1);  
        relative_grounwater_table = theta1 > thetaFC1 ? (theta1 - thetaFC1) / (_thetaS1->val[j] - thetaFC1) : 0.0;
        if (relative_grounwater_table > relative_drainage_depth) {
            drainage1 = (relative_grounwater_table - relative_drainage_depth) * (theta1 - thetaFC1) * depth1 * par._drainage_intensity->val[j];
            _drainage_from_layer1->val[j] = drainage1;
            _theta1->val[j] = (theta1 * depth1 - drainage1) / depth1;
        }


        

        // Soil layer 2
        relative_drainage_depth =  max(0.0, (depth2 - (drainage_depth - depth1)) / depth2);
        if (relative_drainage_depth < 1.0) {
            relative_grounwater_table = theta2 > thetaFC2 ? (theta2 - thetaFC2) / (_thetaS2->val[j] - thetaFC2) : 0.0;
            if (relative_grounwater_table > relative_drainage_depth) {
                drainage2 = (relative_grounwater_table - relative_drainage_depth) * (theta2 - thetaFC2) * depth2 * par._drainage_intensity->val[j];
                _drainage_from_layer2->val[j] = drainage2;
                _theta2->val[j] = (theta2 * depth2 - drainage2) / depth2;
            }
        }  // End of relative_drainage_depth > 0.0 (soil layer 2)



        
        // Soil layer 3
        relative_drainage_depth =  max(0.0, (depth3 - (drainage_depth - depth1 - depth2)) / depth3);
        if (relative_drainage_depth < 1.0) {
            relative_grounwater_table = theta3 > thetaFC3 ? (theta3 - thetaFC3) / (_thetaS3->val[j] - thetaFC3) : 0.0;
            if (relative_grounwater_table > relative_drainage_depth) {
                drainage3 = (relative_grounwater_table - relative_drainage_depth) * (theta3 - thetaFC3) * depth3 * par._drainage_intensity->val[j];
                _drainage_from_layer3->val[j] = drainage3;
                _theta3->val[j] = (theta3 * depth3 - drainage3) / depth3;
            }
        }  // End of relative_drainage_depth > 0.0 (soil layer 3)


        // Update drainage
        _drainage_from_soil->val[j] = drainage1 + drainage2 + drainage3;
    }
    return EXIT_SUCCESS;
}