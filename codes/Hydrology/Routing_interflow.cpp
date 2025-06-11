/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Routing_interflow.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Routing_interflow_1(Control &ctrl, Param &par){

    int from_j;
    double interflow_to_go = 0;
    double interflow_toChn = 0;
    double interflow_toTrestrial;

    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double dtdx = ctrl.Simul_tstep / dx;
    double alpha = 0;
    double interflow_in;
    double chnlength;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


        chnlength = _chnlength->val[j];
        interflow_in = _interf_in->val[j];
        interflow_to_go = 0; // Available water for interflow
        interflow_toTrestrial = 0;   // Output of interflow to downstream cell
        interflow_toChn = 0;   // Output of interflow to stream
    
        from_j = _sortedGrid.to_cell[j];
       
        // Available interflow = interflow from upstream + excess water above field capacity
        // Should interflow_in be included here, or after stream recharge?
        
        interflow_to_go = interflow_in + _vadose->val[j];
               
        if (interflow_to_go > roundoffERR)  {
            
            // Interflow to channel
            if (chnlength > 0){  // If there is channel in this grid cell
                interflow_toChn = interflow_to_go * par._Ks_vadose->val[j] * (1 - exp(-1 * par._interfExp->val[j] * interflow_to_go)) * par._lat_to_Chn_vadose->val[j];  // [m2/s]
                interflow_toChn *= dtdx; // Store interflow to channel in [m]
                interflow_toChn *= (chnlength/dx); // Adjusted with channel length; [m]
                interflow_toChn = min(interflow_toChn, interflow_to_go);  // Cannot exceed water to go
                interflow_to_go -=  interflow_toChn;    // [m]
            }
            
            // Interflow to downstream grid
            // Linear approximation of Kinematic wave approach
            // Assumption: Q = head * alpha
            alpha = par._Ks_vadose->val[j] * sin(atan(_slope->val[j]));  // [m/s]
            interflow_toTrestrial = interflow_to_go / (1 + alpha * dtdx) * alpha; // qx+1 = hx+1[m] * alpha; [m2/s]
            interflow_toTrestrial *= dtdx; // Store qx+1 in m
            interflow_toTrestrial = min(interflow_toTrestrial, interflow_to_go);  // Cannot exceed water to go [m]
            interflow_to_go -= interflow_toTrestrial; // [m]

            // Remaining water stays in vadose storage
            _vadose->val[j] = interflow_to_go;
      
            // Route water to next grid cell
            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _interf_in->val[from_j] += interflow_toTrestrial;
            }          
        }
        
        // Update global variables
        _interf_toChn->val[j] = interflow_toChn;  // Interflow to channel; [m]
        _interf_out->val[j] = interflow_toTrestrial;  // Interflow to downstream territrial cell [m]

    }
    return EXIT_SUCCESS;
}