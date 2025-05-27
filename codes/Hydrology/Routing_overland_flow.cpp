/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Routing_overland_flow.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"

int Basin::Routing_ovf_1(Control &ctrl, Param &par){

    int from_j;
    double dx = ctrl._dx;
    double proportion_ovf_toChn;
    double ovf_to_go = 0;
    double chnlength, chnwidth;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        chnwidth = _chnwidth->val[j];
        chnlength = _chnlength->val[j];
        from_j = _sortedGrid.to_cell[j];

        ovf_to_go = _ovf_in->val[j] + _pond->val[j];  // Available surface water = ponding water + overland inflow from upstream cells
        
        // Reinfiltration if activated
        if (ctrl.opt_reinfil==1 and ovf_to_go>roundoffERR){
            if (ctrl.opt_infil == 1){ // Reinfiltration
                Reinfiltration_1(ctrl,par, j, _rinfilt->val[j], _theta1->val[j], ovf_to_go);
            }

            if (ctrl.opt_percolation == 1){ // Repercolation and Re GW recharge
                Repercolation_1(ctrl, par, j, _theta1->val[j], _theta2->val[j], _theta3->val[j],  _rPerc1->val[j], _rPerc2->val[j]);
                ReGWrecharge_1(ctrl, par, j, _theta3->val[j], _GW->val[j], _rPerc3->val[j]);
            } else if (ctrl.opt_percolation == 2){
                Repercolation_2(ctrl, par, j, _theta1->val[j], _theta2->val[j], _theta3->val[j],  _rPerc1->val[j], _rPerc2->val[j]);
                ReGWrecharge_2(ctrl, par, j, _theta3->val[j], _GW->val[j], _rPerc3->val[j]);
            } else if (ctrl.opt_percolation == 3){
                Repercolation_3(ctrl, par, j, _theta1->val[j], _theta2->val[j], _theta3->val[j],  _rPerc1->val[j], _rPerc2->val[j]);
                ReGWrecharge_2(ctrl, par, j, _theta3->val[j], _GW->val[j], _rPerc3->val[j]);  // todo
            }

        }
        

        if (chnwidth > 0){  // If there is channel in this grid cell
            proportion_ovf_toChn = min(par._pOvf_toChn->val[j] * chnlength / dx , 1.0);  // The proportion of overland flow that routes into river              
            _ovf_toChn->val[j] = ovf_to_go * proportion_ovf_toChn; // [m]
            ovf_to_go -= _ovf_toChn->val[j];
        }

        // Terrestrial grid cell
        _ovf_out->val[j] = ovf_to_go;  // To downstream terrestrial cell
        if (_sortedGrid.lat_ok[j] == 1){  // If there is a downstream cell
            _ovf_in->val[from_j] += ovf_to_go; // [m]
        }
        _pond->val[j] = 0;  // All ponding water has routed to downstream cell

             
        }        
    
    return EXIT_SUCCESS;
}