#include "Basin.h"

int Basin::Solve_routing_nitrogen(Control &ctrl, Param &par){

    /* Update the storages for routing flux mixing
    ### Ponding water:
    + Th                (mixed)
    + snowmelt          (mixed)            
    - Infiltration      
    (_pond_old)
    + ovf_in            (need to mix)  
    - Reinfiltration
    - ovf_out
    - ovf_toChn           
    (_pond = 0)

    ### Soil layer 1:
    + infiltration      (mixed)
    - percolation1
    - Esoil
    - Transp1           
    (_theta1_old)
    + reinfiltration    (need to mix)
    - repercolation1    
    (_thata1)

    ### Soil layer 2:
    + percolation1      (mixed)
    - percolation2
    - Transp2           
    (_theta2_old)
    + repercolation1    (need to mix)
    - repercolation2    
    (_theta2)

    ### Soil layer 3:
    + percolation2      (mixed)
    - percolation3
    - Transp3     
    (_thata3_old)      
    + repercolation2    (need to mix)
    - repercolation3
    + interflow_in      (need to mix)   
    - interflow_out
    - interflow_toChn   
    (_theta3)

    ### GW:
    + percolation3      (mixed)
    (_GW_old)
    + repercolation3    (need to mix)
    + rerepercolation3  (need to mix)
    + GWf_in            (need to mix)
    - GWf_out
    - GWf_toChn         
    (_GW)

    ### chanS:
    (_chanS_old)
    + _Qupstream        (need to mix)
    + _ovf_toChn        (need to mix)
    +  _interf_toChn    (need to mix)
    + _GWf_toChn        (need to mix)
    - _Q
    (_chanS)
    */

    int from_j;
    int lat_ok;
    double no3_in_all_acc, q_in_all;
    double m3s_to_m = ctrl.Simul_tstep/(ctrl._dx*ctrl._dx);
    double rPerc2, rPerc3;

    _no3_ovf_in_acc->reset();
    _no3_interf_in_acc->reset();
    _no3_GWf_in_acc->reset();
    _no3_Qupstream_acc->reset();

    // ********* Mixing reinfiltration and percolation ********
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        from_j = _sortedGrid.to_cell[j];
        lat_ok = _sortedGrid.lat_ok[j];

        if (ctrl.opt_reinfil == 1){
            rPerc2 = _rPerc2->val[j];
            rPerc3 = _rPerc3->val[j];
        } else {
            rPerc2 = rPerc3 = 0;
        }

        // Ponding water mixing with overland flow
        Mixing_full(_pond_old->val[j], _no3_pond->val[j], _ovf_in->val[j], _no3_ovf_in_acc->val[j] / _ovf_in->val[j]);
        
        if (lat_ok == 1){  // Add 18O in overland outflow to the overland inflow of downstream cell
            _no3_ovf_in_acc->val[from_j] += _no3_pond->val[j] * _ovf_out->val[j];
        }


        // Re-infiltration and re-percolation
        if (ctrl.opt_reinfil == 1){ 
            // Re-infiltration mixing with layer 1
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _no3_layer1->val[j], _rinfilt->val[j], _no3_pond->val[j]);
            // Re-percolation mixing with layer 2
            Mixing_full(_theta2_old->val[j] * _depth2->val[j], _no3_layer2->val[j], _rPerc1->val[j], _no3_layer1->val[j]);
            // Re-percolation mixing with layer 3
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _no3_layer3->val[j], rPerc2, _no3_layer2->val[j]);
            // GW mixing with repercolation from layer 3
            Mixing_full(_GW_old->val[j], _no3_GW->val[j], rPerc3, _no3_layer3->val[j]);

            
        }

        
        // Interflow mixing with lateral inflow
        if (ctrl.opt_reinfil == 1){ 
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j] + rPerc2 - rPerc3, _no3_layer3->val[j], _interf_in->val[j], _no3_interf_in_acc->val[j] / _interf_in->val[j]);
            Mixing_full(_GW_old->val[j] + rPerc3, _no3_GW->val[j], _rrPerc3->val[j], _no3_layer3->val[j]); // GW mixed with repercolation due to excess interflow
        } else {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _no3_layer3->val[j], _interf_in->val[j], _no3_interf_in_acc->val[j] / _interf_in->val[j]);
            Mixing_full(_GW_old->val[j], _no3_GW->val[j], _rrPerc3->val[j], _no3_layer3->val[j]); // GW mixed with repercolation due to excess interflow
        }
        if (lat_ok == 1){  // Add 18O in interflow outflow to the inferflow inflow of downstream cell
            _no3_interf_in_acc->val[from_j] += _no3_layer3->val[j] * _interf_out->val[j];
        }

        
        // GW flow mixing with lateral inflow
        Mixing_full(_GW_old->val[j] + rPerc3 + _rrPerc3->val[j], _no3_GW->val[j], _GWf_in->val[j], _no3_GWf_in_acc->val[j] / _GWf_in->val[j]);
        if (lat_ok == 1){  // Add 18O in GW outflow to the GW inflow of downstream cell
            _no3_GWf_in_acc->val[from_j] += _no3_GW->val[j] * _GWf_out->val[j];
        }
        

        // Channel storage mixing (with upstream inflow)
        if (_chnwidth->val[j] > roundoffERR){
            
                            // Upstream inflow              Overland flow to channel                  Interflow to channel                           GW flow to channel
            no3_in_all_acc = _no3_Qupstream_acc->val[j] + _no3_pond->val[j] * _ovf_toChn->val[j] + _no3_layer3->val[j] * _interf_toChn->val[j] + _no3_GW->val[j] * _GWf_toChn->val[j]; 
            q_in_all = _Qupstream->val[j] * m3s_to_m + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j];

            Mixing_full(_chanS_old->val[j], _no3_chanS->val[j], q_in_all, no3_in_all_acc / q_in_all);

            if (lat_ok == 1){  // Add 18O in discharge to inflow of the downstream channel storage
                _no3_Qupstream_acc->val[from_j] += _no3_chanS->val[j] * _Q->val[j] * m3s_to_m;   
            }
        }

    }





    return EXIT_SUCCESS;
}
