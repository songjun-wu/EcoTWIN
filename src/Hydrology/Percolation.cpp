/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Percolation.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"



int Basin::Percolation_1(Control &ctrl, Param &par) {

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double theta1 = _theta1->val[j];
        double theta2 = _theta2->val[j];
        double theta3 = _theta3->val[j];

        double thetaFC1 = _thetaFC1->val[j];
        double thetaFC2 = _thetaFC2->val[j];
        double thetaFC3 = _thetaFC3->val[j];

        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j];

        double perc1 = 0;
        double perc2 = 0;
        double perc3 = 0;

        // Drainage variables
        double drainage_depth =  _drainage_depth->val[j];;  // Drainage depth [m]
        double relative_drainage_depth;  // Drainage depth relative to the bottom of soil layer [0-1]
        double relative_grounwater_table;  // Groundwater table relative to the bottom of soil layer [0-1]
        double drainage1, drainage2, drainage3;  // Drainage amount for each soil layer [m]

        drainage1 = 0.0;
        drainage2 = 0.0;
        drainage3 = 0.0;
        

        // Drainage from soil layer 1
        if (ctrl.opt_drainage == 1 and drainage_depth > roundoffERR) {
            // Initialize drainage variables
            drainage1 = 0.0;
            drainage2 = 0.0;
            drainage3 = 0.0;

            // Drainage from layer 1 if activated
            relative_drainage_depth =  max(0.0, (depth1 - drainage_depth) / depth1);  
            relative_grounwater_table = theta1 > thetaFC1 ? (theta1 - thetaFC1) / (_thetaS1->val[j] - thetaFC1) : 0.0;
            if (relative_grounwater_table > relative_drainage_depth) {
                drainage1 = (relative_grounwater_table - relative_drainage_depth) * (theta1 - thetaFC1) * depth1 * par._drainage_intensity->val[j];
                theta1 = (theta1 * depth1 - drainage1) / depth1;
            }
        }  // End of drainage from soil layer 1

        // Percolation from layer 1 to layer 2
        if (theta1 > thetaFC1) {
            perc1 = (theta1 - thetaFC1) * depth1 * _p_perc1->val[j];
            theta1 -= perc1 / depth1;
            theta2 += perc1 / depth2;
        }


        // Drainage from soil layer 2
        if (ctrl.opt_drainage == 1 and drainage_depth > roundoffERR) {
            relative_drainage_depth =  max(0.0, (depth2 - (drainage_depth - depth1)) / depth2);
            if (relative_drainage_depth < 1.0) {
                relative_grounwater_table = theta2 > thetaFC2 ? (theta2 - thetaFC2) / (_thetaS2->val[j] - thetaFC2) : 0.0;
                if (relative_grounwater_table > relative_drainage_depth) {
                    drainage2 = (relative_grounwater_table - relative_drainage_depth) * (theta2 - thetaFC2) * depth2 * par._drainage_intensity->val[j];
                    theta2 = (theta2 * depth2 - drainage2) / depth2;
                }
            }
        } // End of drainage from soil layer 2

        // Percolation from layer 2 to layer3
        if (theta2 > thetaFC2){
            perc2 = (theta2 - thetaFC2) * depth2 * _p_perc2->val[j];
            theta2 -= perc2 / depth2;
            theta3 += perc2 / depth3;
        }  // End of percolation from layer 2 to layer 3


        // Drainage from soil layer 3
        if (ctrl.opt_drainage == 1 and drainage_depth > roundoffERR) {
            relative_drainage_depth =  max(0.0, (depth3 - (drainage_depth - depth1 - depth2)) / depth3);
            if (relative_drainage_depth < 1.0) {
                relative_grounwater_table = theta3 > thetaFC3 ? (theta3 - thetaFC3) / (_thetaS3->val[j] - thetaFC3) : 0.0;
                if (relative_grounwater_table > relative_drainage_depth) {
                    drainage3 = (relative_grounwater_table - relative_drainage_depth) * (theta3 - thetaFC3) * depth3 * par._drainage_intensity->val[j];
                    theta3 = (theta3 * depth3 - drainage3) / depth3;
                }
            }
        } // End of drainage from soil layer 3

        // Percolation from layer 3 to vadose storage
        if (theta3 > thetaFC3){
            perc3 = (theta3 - thetaFC3) * depth3 * _p_perc3->val[j];
            theta3 -= perc3 / depth3;
            _vadose->val[j] += perc3;
        }  // End of percolation from layer 3 to vadose storage

        // Local to global
        _theta1->val[j] = theta1;
        _theta2->val[j] = theta2;
        _theta3->val[j] = theta3;
        _Perc1->val[j] = perc1;
        _Perc2->val[j] = perc2;
        _Perc3->val[j] = perc3;
        if (ctrl.opt_drainage == 1) {
            _drainage_from_layer1->val[j] = drainage1;
            _drainage_from_layer2->val[j] = drainage2;
            _drainage_from_layer3->val[j] = drainage3;
            _drainage_from_soil->val[j] = drainage1 + drainage2 + drainage3;
        }   
    }
    return EXIT_SUCCESS;
}

int Basin::Percolation_2(Control &ctrl, Param &par) {
   
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double theta1 = _theta1->val[j];
        double theta2 = _theta2->val[j];
        double theta3 = _theta3->val[j];

        double thetaS1 = _thetaS1->val[j];
        double thetaS2 = _thetaS2->val[j];
        double thetaS3 = _thetaS3->val[j];

        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j];

        double perc1 = 0;
        double perc2 = 0;
        double perc3 = 0;
        double perc_in = 0;
        double delta_theta = 0;
        
        // Percolation from layer 1
        // Only happens when saturation is met, because infiltration has been added to layer 1
        if (theta1 > thetaS1){

            perc1 = (theta1 - thetaS1) * depth1;  // Percolation to layer 2
            theta1 = thetaS1;
            perc_in = perc1;
        
            // Percolation from layer 2
            // if saturation is not met then fill the deficit, otherwise all water pass to next layer
            if (theta2 < thetaS2){ 
                delta_theta = perc_in * (1 - exp(par._percExp->val[j] * log(max(theta2/thetaS2, 1e-6)))) / depth2;
                double available_space = (thetaS2 - theta2) * depth2;
                if (delta_theta * depth2 > available_space) {
                    delta_theta = available_space / depth2;
                    perc_in -= available_space;
                } else {
                    perc_in -= delta_theta * depth2;
                }
                theta2 += delta_theta;
            }
            perc2 = perc_in;  // Percolation to next layer

            // Percolation from layer 3 to vadose storage
            // if saturation is not met then fill the deficit, otherwise all water pass to next layer
            if (theta3 < thetaS3){ 
                delta_theta = perc_in * (1 - exp(par._percExp->val[j] * log(max(theta3/thetaS3, 1e-6)))) / depth3;
                double available_space = (thetaS3 - theta3) * depth3;
                if (delta_theta * depth3 > available_space) {
                    delta_theta = available_space / depth3;
                    perc_in -= available_space;
                } else {
                    perc_in -= delta_theta * depth3;
                }
                theta3 += delta_theta;
            }
            perc3 = perc_in;  // Percolation to next layer

            // Water percolates to vadose storage
            _vadose->val[j] += perc_in;
        }

        // Local to global
        _theta1->val[j] = theta1;
        _theta2->val[j] = theta2;
        _theta3->val[j] = theta3;
        _Perc1->val[j] = perc1;
        _Perc2->val[j] = perc2;
        _Perc3->val[j] = perc3;
      
    }
    return EXIT_SUCCESS;
}


int Basin::Percolation_3(Control &ctrl, Param &par) {

     for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double theta1 = _theta1->val[j];
        double theta2 = _theta2->val[j];
        double theta3 = _theta3->val[j];
        // All water above field capacity will be routed? Or threshold should be saturated content?
        double thetaS1 = _thetaFC1->val[j];
        double thetaS2 = _thetaFC2->val[j];
        double thetaS3 = _thetaFC3->val[j];

        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j];

        double perc1 = 0;
        double perc2 = 0;
        double perc3 = 0;
        
        // Percolation from layer 1
        // TODO: if saturation is not met then fill the deficit, otherwise all water pass to next layer
        if (theta1 > thetaS1){
            perc1 = (theta1 - thetaS1) * depth1;  // Percolation to next layer
            theta1 = thetaS1;
            theta2 += perc1 / depth2;
        }

        if (theta2 > thetaS2){
            perc2 = (theta2 - thetaS2) * depth2;  // Percolation to next layer
            theta2 = thetaS2;
            theta3 += perc2 / depth3;
        }

        if (theta3 > thetaS3){
            perc3 = (theta3 - thetaS3) * depth3;  // Percolation to next layer
            theta3 = thetaS3;
            _vadose->val[j] += perc3;
        }

        // Local to global
        _theta1->val[j] = theta1;
        _theta2->val[j] = theta2;
        _theta3->val[j] = theta3;
        _Perc1->val[j] = perc1;
        _Perc2->val[j] = perc2;
        _Perc3->val[j] = perc3;
 
    }
    return EXIT_SUCCESS;
}