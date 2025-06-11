/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_routing_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Mixing_routing_tracking(Control &ctrl, Param &par){

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
    (_theta3)

    ### Vadose zone:
    + percolation3      (mixed)
    - percolation_vadose
    (_vadose_old)
    + repercolation3    (need to mix)
    - repercolation_vadose
    + interflow_in      (need to mix)   
    - interflow_out
    - interflow_toChn
    (_vadose)

    ### GW:
    - irrigation_from_GW
    + percolation3      (mixed)
    (_GW_old)
    + repercolation_vadose (need to mix)
    + GWf_in            (need to mix)
    - GWf_out
    - GWf_toChn         
    (_GW)

    ### chanS:
    - irrigation_from_river
    (_chanS_old)
    + _Qupstream        (need to mix)
    + _ovf_toChn        (need to mix)
    +  _interf_toChn    (need to mix)
    + _GWf_toChn        (need to mix)
    - _Q
    - _Echan
    (_chanS)
    */



    // Isotopes
    if (ctrl.opt_tracking_isotope==1) {

        int from_j;
        int lat_ok;
        double d18o_in_all_acc, q_in_all;
        double m3s_to_m = ctrl.Simul_tstep/(ctrl._dx*ctrl._dx);
        double rPerc2, rPerc3, rPerc_vadose;
        double influx, cinflux;

        _flux_ovf_in_acc->reset();
        _flux_interf_in_acc->reset();
        _flux_GWf_in_acc->reset();
        _flux_Qupstream_acc->reset();

        // ********* Mixing reinfiltration and percolation ********
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            from_j = _sortedGrid.to_cell[j];
            lat_ok = _sortedGrid.lat_ok[j];

            if (ctrl.opt_reinfil == 1){
                rPerc2 = _rPerc2->val[j];
                rPerc3 = _rPerc3->val[j];
                rPerc_vadose = _rPerc_vadose->val[j];
            } else {
                rPerc2 = rPerc3 = rPerc_vadose = 0;
            }


            // Ponding water mixing with overland flow
            Mixing_full(_pond_old->val[j], _d18o_pond->val[j], _ovf_in->val[j], _flux_ovf_in_acc->val[j] / _ovf_in->val[j]);

            if (lat_ok == 1){  // Add 18O in overland outflow to the overland inflow of downstream cell
                _flux_ovf_in_acc->val[from_j] += _d18o_pond->val[j] * _ovf_out->val[j];
            }


            // Re-infiltration and re-percolation
            if (ctrl.opt_reinfil == 1){ 
                // Re-infiltration mixing with layer 1
                Mixing_full(_theta1_old->val[j] * _depth1->val[j], _d18o_layer1->val[j], _rinfilt->val[j], _d18o_pond->val[j]);
                // Re-percolation mixing with layer 2
                Mixing_full(_theta2_old->val[j] * _depth2->val[j], _d18o_layer2->val[j], _rPerc1->val[j], _d18o_layer1->val[j]);
                // Re-percolation mixing with layer 3
                Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _d18o_layer3->val[j], rPerc2, _d18o_layer2->val[j]);
                // Vadose mixing with repercolation from layer 3
                Mixing_full(_vadose_old->val[j], _d18o_vadose->val[j], rPerc3, _d18o_layer3->val[j]); 
                // GW mixing with repercolation from vadose
                if (ctrl.opt_baseflow_mixing == 0) Mixing_full(_GW_old->val[j], _d18o_GW->val[j], rPerc_vadose, _d18o_vadose->val[j]);
            }

            
            // Interflow mixing with lateral inflow
            if(_interf_in->val[j] > roundoffERR) {
                Mixing_full(_vadose_old->val[j] + rPerc3 - rPerc_vadose, _d18o_vadose->val[j], _interf_in->val[j], _flux_interf_in_acc->val[j] / _interf_in->val[j]);
            }
            if (lat_ok == 1){  // Add 18O in interflow outflow to the inferflow inflow of downstream cell
                _flux_interf_in_acc->val[from_j] += _d18o_vadose->val[j] * _interf_out->val[j];
            }

            // GW mixing with lateral inflow
            if (ctrl.opt_baseflow_mixing == 0){  // Still use full mixing
                if (_GWf_in->val[j] > roundoffERR) {
                    Mixing_full(_GW_old->val[j] + rPerc_vadose, _d18o_GW->val[j], _GWf_in->val[j], _flux_GWf_in_acc->val[j] / _GWf_in->val[j]);
                }
            } else if (ctrl.opt_baseflow_mixing == 1){  // Baseflow mixing strategy
                influx = _GWf_in->val[j] + _Perc_vadose->val[j] + rPerc_vadose;
                if (influx > roundoffERR) {
                    cinflux = (_flux_GWf_in_acc->val[j] + (_Perc_vadose->val[j]+rPerc_vadose)*_d18o_vadose->val[j]) / influx;
                    Mixing_baseflow(_GW_old->val[j], _d18o_GW->val[j], influx, cinflux, _GWf_out->val[j]);
                }
            }

            if (lat_ok == 1){  // Add 18O in GW outflow to the GW inflow of downstream cell
                _flux_GWf_in_acc->val[from_j] += _d18o_GW->val[j] * _GWf_out->val[j];
            }


            // Channel storage mixing (with upstream inflow)
            if (_chnwidth->val[j] > roundoffERR){
                
                                // Upstream inflow              Overland flow to channel                  Interflow to channel                           GW flow to channel
                d18o_in_all_acc = _flux_Qupstream_acc->val[j] + _d18o_pond->val[j] * _ovf_toChn->val[j] + _d18o_vadose->val[j] * _interf_toChn->val[j] + _d18o_GW->val[j] * _GWf_toChn->val[j]; 
                q_in_all = _Qupstream->val[j] * m3s_to_m + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j];

                Mixing_full(_chanS_old->val[j], _d18o_chanS->val[j], q_in_all, d18o_in_all_acc / q_in_all);

                if (lat_ok == 1){  // Add 18O in discharge to inflow of the downstream channel storage
                    _flux_Qupstream_acc->val[from_j] += _d18o_chanS->val[j] * _Q->val[j] * m3s_to_m;
                }

            }
        }

    }







    // Age
    if (ctrl.opt_tracking_age==1) {

        int from_j;
        int lat_ok;
        double age_in_all_acc, q_in_all;
        double m3s_to_m = ctrl.Simul_tstep/(ctrl._dx*ctrl._dx);
        double rPerc2, rPerc3, rPerc_vadose;
        double influx, cinflux;

        _flux_ovf_in_acc->reset();
        _flux_interf_in_acc->reset();
        _flux_GWf_in_acc->reset();
        _flux_Qupstream_acc->reset();

        // ********* Mixing reinfiltration and percolation ********
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            from_j = _sortedGrid.to_cell[j];
            lat_ok = _sortedGrid.lat_ok[j];

            if (ctrl.opt_reinfil == 1){
                rPerc2 = _rPerc2->val[j];
                rPerc3 = _rPerc3->val[j];
                rPerc_vadose = _rPerc_vadose->val[j];
            } else {
                rPerc2 = rPerc3 = rPerc_vadose = 0;
            }


            // Ponding water mixing with overland flow
            Mixing_full(_pond_old->val[j], _age_pond->val[j], _ovf_in->val[j], _flux_ovf_in_acc->val[j] / _ovf_in->val[j]);

            if (lat_ok == 1){  // Add age in overland outflow to the overland inflow of downstream cell
                _flux_ovf_in_acc->val[from_j] += _age_pond->val[j] * _ovf_out->val[j];
            }


            // Re-infiltration and re-percolation
            if (ctrl.opt_reinfil == 1){ 
                // Re-infiltration mixing with layer 1
                Mixing_full(_theta1_old->val[j] * _depth1->val[j], _age_layer1->val[j], _rinfilt->val[j], _age_pond->val[j]);
                // Re-percolation mixing with layer 2
                Mixing_full(_theta2_old->val[j] * _depth2->val[j], _age_layer2->val[j], _rPerc1->val[j], _age_layer1->val[j]);
                // Re-percolation mixing with layer 3
                Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _age_layer3->val[j], rPerc2, _age_layer2->val[j]);
                // Vadose mixing with repercolation from layer 3
                Mixing_full(_vadose_old->val[j], _age_vadose->val[j], rPerc3, _age_layer3->val[j]);
                // GW mixing with repercolation from vadose zone
                if (ctrl.opt_baseflow_mixing == 0) Mixing_full(_GW_old->val[j], _age_GW->val[j], rPerc_vadose, _age_vadose->val[j]);
            }

            
            // Interflow mixing with lateral inflow
            if(_interf_in->val[j] > roundoffERR) {
                Mixing_full(_vadose_old->val[j] + rPerc3 - rPerc_vadose, _age_vadose->val[j], _interf_in->val[j], _flux_interf_in_acc->val[j] / _interf_in->val[j]);
            }
                if (lat_ok == 1){  // Add 18O in interflow outflow to the inferflow inflow of downstream cell
                _flux_interf_in_acc->val[from_j] += _age_vadose->val[j] * _interf_out->val[j];
            }

            // GW mixing with lateral inflow
            if (ctrl.opt_baseflow_mixing == 0){  // Still use full mixing
                if (_GWf_in->val[j] > roundoffERR) {
                    Mixing_full(_GW_old->val[j] + rPerc_vadose, _age_GW->val[j], _GWf_in->val[j], _flux_GWf_in_acc->val[j] / _GWf_in->val[j]);
                }
            } else if (ctrl.opt_baseflow_mixing == 1){  // Baseflow mixing strategy
                influx = _GWf_in->val[j] + _Perc_vadose->val[j] + rPerc_vadose;
                if (influx > roundoffERR) {
                    cinflux = (_flux_GWf_in_acc->val[j] + (_Perc_vadose->val[j]+rPerc_vadose)*_age_vadose->val[j]) / influx;
                    Mixing_baseflow(_GW_old->val[j], _age_GW->val[j], influx, cinflux, _GWf_out->val[j]);
                }
            }
            if (lat_ok == 1){  // Add 18O in GW outflow to the GW inflow of downstream cell
                _flux_GWf_in_acc->val[from_j] += _age_GW->val[j] * _GWf_out->val[j];
            }


            // Channel storage mixing (with upstream inflow)
            if (_chnwidth->val[j] > roundoffERR){
                
                                // Upstream inflow              Overland flow to channel                  Interflow to channel                           GW flow to channel
                age_in_all_acc = _flux_Qupstream_acc->val[j] + _age_pond->val[j] * _ovf_toChn->val[j] + _age_vadose->val[j] * _interf_toChn->val[j] + _age_GW->val[j] * _GWf_toChn->val[j]; 
                q_in_all = _Qupstream->val[j] * m3s_to_m + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j];

                Mixing_full(_chanS_old->val[j], _age_chanS->val[j], q_in_all, age_in_all_acc / q_in_all);

                if (lat_ok == 1){  // Add 18O in discharge to inflow of the downstream channel storage
                    _flux_Qupstream_acc->val[from_j] += _age_chanS->val[j] * _Q->val[j] * m3s_to_m;
                }

            }
        }

    }

    return EXIT_SUCCESS;
}
