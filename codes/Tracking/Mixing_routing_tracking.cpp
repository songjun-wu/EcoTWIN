#include "Basin.h"

int Basin::Mixing_routing_tracking(Control &ctrl, Param &par){


    if (ctrl.opt_tracking_isotope==1) {

        /* Update the storages for routing flux mixing
        ### Ponding water:
        + Th
        - Infiltration      
                            (Updated _pond_old in Solve_soil_profile)
        - Reinfiltration
        + ovf_in
        - ovf_out
        - ovf_toChn           
                            (Updated _pond_old by the end of timestep)

        ### Soil layer 1:
        + infiltration
        - percolation1
        - Esoil
        - Transp1           
                            (Updated _theta1_old in Solve_soil_profile)
        + reinfiltration
        - repercolation1    
                            (Updated _theta1_old by the end of timestep)

        ### Soil layer 2:
        + percolation1
        - percolation2
        - Transp2           
                            (Updated _theta2_old in Solve_soil_profile)
        + repercolation1
        - repercolation2    
                            (Updated _theta2_old by the end of timestep)

        ### Soil layer 3:
        + percolation2
        - percolation3
        - Transp3           
                            (Updated _theta3_old in Solve_soil_profile)
        + repercolation2
        - repercolation3
        + interflow_in
        - interflow_out
        - interflow_toChn   
                            (Updated _theta3_old by the end of timestep)

        ### GW:
        + percolation3      
                            (Updated _GW_old in Solve_soil_profile)
        + repercolation3    
        + GWf_in
        - GWf_out
        - GWf_toChn         
                            (Updated _GW_old by the end of timestep)

        ### chanS:
                            (Updated _chanS_old in Solve_soil_profile)
        + _Qupstream
        + _ovf_toChn
        +  _interf_toChn
        + _GWf_toChn
        - _Q
                            (Updated _chanS_old by the end of timestep)
        */

        int from_j;
        int lat_ok;

        _d18o_ovf_in_acc->reset();
        _d18o_interf_in_acc->reset();
        _d18o_GWf_in_acc->reset();
        _d18o_Qupstream_acc->reset();

        // ********* Mixing reinfiltration and percolation ********
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            from_j = _sortedGrid.to_cell[j];
            lat_ok = _sortedGrid.lat_ok[j];

            // Ponding water mixing with overland flow
            if (_ovf_in->val[j] > 0){  // Mixing ponding water with overland inflow
                Mixing_full(_pond->val[j] - _ovf_in->val[j] + _ovf_out->val[j] + _ovf_toChn->val[j], _d18o_pond->val[j], _ovf_in->val[j], _d18o_ovf_in_acc->val[j] / _ovf_in->val[j]);
            }
            if (lat_ok == 1){  // Add 18O in overland outflow to the overland inflow of downstream cell
                _d18o_ovf_in_acc->val[from_j] += _d18o_pond->val[j] * _ovf_out->val[j];
            }

            // Re-infiltration and re-percolation
            if (ctrl.opt_infil > 0){ 
                // Re-infiltration mixing with layer 1
                Mixing_full(_theta1_old->val[j] * _depth1->val[j], _d18o_layer1->val[j], _rinfilt->val[j], _d18o_pond->val[j]);
                // Re-percolation mixing with layer 2
                Mixing_full(_theta2_old->val[j] * _depth2->val[j], _d18o_layer2->val[j], _rPerc1->val[j], _d18o_layer1->val[j]);
                // Re-percolation mixing with layer 3
                Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _d18o_layer3->val[j], _rPerc2->val[j], _d18o_layer2->val[j]);
                // GW mixing with repercolation from layer 3
                Mixing_full(_GW_old->val[j], _d18o_GW->val[j], _rPerc3->val[j], _d18o_layer3->val[j]);
            }

            // Interflow mixing
            if (_interf_in->val[j] > 0){  // Mixing layer 3 storage with interflow inflow
                Mixing_full(_theta3->val[j] * par._depth3->val[j] - _interf_in->val[j] + _interf_out->val[j] + _interf_toChn->val[j], _d18o_layer3->val[j], _interf_in->val[j], _d18o_interf_in_acc->val[j] / _interf_in->val[j]);
            }
            if (lat_ok == 1){  // Add 18O in interflow outflow to the inferflow inflow of downstream cell
                _d18o_interf_in_acc->val[from_j] += _d18o_layer3->val[j] * _interf_out->val[j];
            }

            // GW flow mixing
            if (_interf_in->val[j] > 0){  // Mixing GW storage with GW inflow
                Mixing_full(_GW->val[j] - _GWf_in->val[j] + _GWf_out->val[j] + _GWf_toChn->val[j], _d18o_GW->val[j], _GWf_in->val[j], _d18o_GWf_in_acc->val[j] / _GWf_in->val[j]);
            }

            if (lat_ok == 1){  // Add 18O in GW outflow to the GW inflow of downstream cell
                _d18o_GWf_in_acc->val[from_j] += _d18o_GW->val[j] * _GWf_out->val[j];
            }


            // Channel storage mixing (with upstream inflow)
            if (_chnwidth->val[j] > roundoffERR){
                double d18o_in_all_acc, q_in_all;
                                // Upstream inflow              Overland flow to channel                  Interflow to channel                           GW flow to channel
                d18o_in_all_acc = _d18o_Qupstream_acc->val[j] + _d18o_pond->val[j] * _ovf_toChn->val[j] + _d18o_layer3->val[j] * _interf_toChn->val[j] + _d18o_GW->val[j] * _GWf_toChn->val[j]; 
                q_in_all = _Qupstream->val[j] + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j];

                if (q_in_all > roundoffERR){
                    Mixing_full(_chanS_old->val[j], _d18o_chanS->val[j], q_in_all, d18o_in_all_acc / q_in_all);
                }

                if (lat_ok == 1){  // Add 18O in discharge to inflow of the downstream channel storage
                    _d18o_Qupstream_acc->val[from_j] += _d18o_chanS->val[j] * _Q->val[j];
                }

            }

        }



    }

    return EXIT_SUCCESS;
}
