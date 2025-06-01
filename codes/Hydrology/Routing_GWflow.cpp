/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Routing_GWflow.cpp
  * Created  on: 30.02.2025
  * Modified on: 01.06.2025
***************************************************************/




#include "Basin.h"

int Basin::Routing_GWflow_1(Control &ctrl, Param &par){

    int from_j;
    double GWflow_in; // GW inputs from upstream cell
    double GWflow_to_go; // Available water for GWflow
    double GWflow_out;  // Output of GWflow to downstream cell (terrestrial only)
    double GWflow_toChn;  // Output of GWflow to stream
    double GWflow_toTrestrial; // Output of GWflow to downstream cell (terrestrial only)

    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double dtdx = ctrl.Simul_tstep / dx;
    double alpha = 0;
    double Ks3 = 0;
    double chnlength;



    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        chnlength = _chnlength->val[j];
        GWflow_in = _GWf_in->val[j];
        GWflow_toChn = 0;
        GWflow_out = 0;
        GWflow_toTrestrial = 0;
        
    
        from_j = _sortedGrid.to_cell[j];

        // Available GWflowflow = GWflowflow from upstream + GW storage
        // Should GWflow_in be included here, or after stream recharge?
        GWflow_to_go = GWflow_in + _GW->val[j];

              
        if (GWflow_to_go > roundoffERR)  {

            Ks3 = _Ks3->val[j];  // [m/s]
            // GWflow to channel
            if (chnlength > 0){  // If there is channel in this grid cell
                // Here Ks3 is not used because GW routing should be independent from soil proporties
                GWflow_toChn = GWflow_to_go * par._Ks_GW->val[j] * (1 - exp(-1 * par._GWfExp->val[j] * GWflow_to_go)) * par._lat_to_Chn_GW->val[j];  // [m2/s]
                GWflow_toChn *= dtdx; // Store GWflow to channel in [m]
                GWflow_toChn *= (chnlength/dx); // Adjusted with channel length; [m]
                GWflow_toChn = min(GWflow_toChn, GWflow_to_go);  // Cannot exceed water to go
                GWflow_to_go -=  GWflow_toChn;    // [m]
            }

            // GWflow to downstream grid
            // Linear approximation of Kinematic wave approach
            // Assumption: Q = head * alpha
            // Here Ks3 is not used because GW routing should be independent from soil proporties
            alpha = par._Ks_GW->val[j];  // [m/s]
            //alpha = Ks3 * sin(atan(_slope->val[j])) * par._wGWf->val[j];  // [m/s]
            GWflow_toTrestrial = GWflow_to_go / (1 + alpha * dtdx) * alpha; // qx+1 = hx+1[m] * alpha; [m2/s]
            GWflow_toTrestrial *= dtdx; // Store qx+1 in m
            GWflow_toTrestrial = min(GWflow_toTrestrial, GWflow_to_go);  // Cannot exceed water to go
            GWflow_to_go -= GWflow_toTrestrial; // [m]
            GWflow_out += GWflow_toTrestrial;  // [m]

            // Remaining water = GW storage
            _GW->val[j] = GWflow_to_go; // GWflow_to_go = _GW->val[j] + GWflow_in - GWflow_toChn - GWflow_toTrestrial

            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _GWf_in->val[from_j] += GWflow_toTrestrial;
            }
        }
     
        _GWf_toChn->val[j] = GWflow_toChn;  // GWflow to channel; [m]
        _GWf_out->val[j] = GWflow_toTrestrial;  // GWflow sum (to channel and to downstream territrial cell); [m]

    }
    return EXIT_SUCCESS;
}