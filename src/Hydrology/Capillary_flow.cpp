/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Capillary_flow.cpp
  * Created  on: 16.02.2026
  * Modified on: 16.02.2026
***************************************************************/


#include "Basin.h"



int Basin::Capillary_flow(Control &ctrl, Param &par) {

    double theta3;  // Soil moisture content of layer 3 [m3/m3]
    double thetaFC3;  // Field capacity of layer 3 [m3/m3]
    double depth3;  // Depth of layer 3 [m]
    double vadose;  // Vadose storage [m]
    double capillary_flow;  // Capillary flow [m]
    double deficit;  // Deficit in layer 3 [m]
    double perc_optimal_theta;  // The specific threshold between field capacity and saturated content for percolation [0-1]

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        theta3 = _theta3->val[j];
        perc_optimal_theta = par._perc_optimal_theta->val[j];  // The specific threshold between field capacity and saturated content for percolation [0-1]
        thetaFC3 = _thetaS3->val[j] * perc_optimal_theta + _thetaFC3->val[j] * (1 - perc_optimal_theta);
        //thetaFC3 = _thetaFC3->val[j];
        depth3 = par._depth3->val[j];
        vadose = _vadose->val[j];
        capillary_flow = 0;
        deficit = 0;

        


        deficit = (thetaFC3 - theta3) * depth3;
        if (deficit > roundoffERR and vadose > roundoffERR){
            capillary_flow = min(vadose * par._capillary_flow_rate->val[j], deficit);
            vadose -= capillary_flow;
            theta3 += capillary_flow / depth3;
        } else {
            capillary_flow = 0;
        }

        // Update global variables
        _capillary_flow->val[j] = capillary_flow;
        _vadose->val[j] = vadose;
        _theta3->val[j] = theta3;
        
    }
    return EXIT_SUCCESS;
}