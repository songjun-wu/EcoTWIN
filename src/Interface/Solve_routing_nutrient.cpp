/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_routing_nutrient.cpp
  * Created  on: 30.02.2025
  * Modified on: 03.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_routing_nutrient(Control &ctrl, Param &par){

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

    if (ctrl.opt_carbon_sim==1){
      Solve_routing_transport(ctrl, par, *_doc_pond, *_doc_layer1, *_doc_layer2, *_doc_layer3, *_doc_vadose, *_doc_GW, *_doc_chanS);
    }
    if (ctrl.opt_nitrogen_sim==1){
      Solve_routing_transport(ctrl, par, *_no3_pond, *_no3_layer1, *_no3_layer2, *_no3_layer3, *_no3_vadose, *_no3_GW, *_no3_chanS);
      //Solve_routing_transport(ctrl, par, *_don_pond, *_don_layer1, *_don_layer2, *_don_layer3, *_don_vadose, *_don_GW, *_don_chanS);
    }
    

    return EXIT_SUCCESS;
}
