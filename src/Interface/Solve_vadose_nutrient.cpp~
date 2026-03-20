/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_vadose_nutrient.cpp
  * Created  on: 02.12.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_vadose_nutrient(Control &ctrl, Atmosphere &atm){
    /*
    ### vadose:
        (_vadose_old)
        + preferential_flow (need to mix)
        + percolation3      (need to mix)
        - percolation_vadose
        (_vadose)
        + repercolation3
        - repercolation_vadose   
        + interf_in
        - interf_out
        - interf_toChn                            
    */

    double input_water, input_mass, input_conc;


    
    // Mixing vadose storage with percolation from layer 3
    if (ctrl.opt_carbon_sim==1){
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          input_water = _preferential_flow->val[j] + _Perc3->val[j];
          input_mass = _doc_pond->val[j] * _preferential_flow->val[j] + _doc_layer3->val[j] * _Perc3->val[j];
          input_conc = input_mass / input_water;
          Mixing_full(_vadose_old->val[j], _doc_vadose->val[j], input_water, input_conc);
          _leaching_mass_doc->val[j] = input_mass;  // Summary statistics of leaching mass
      }
    }
    if (ctrl.opt_nitrogen_sim==1){
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          input_water = _preferential_flow->val[j] + _Perc3->val[j];
          input_mass = _no3_pond->val[j] * _preferential_flow->val[j] + _no3_layer3->val[j] * _Perc3->val[j];
          input_conc = input_mass / input_water;
          Mixing_full(_vadose_old->val[j], _no3_vadose->val[j], input_water, input_conc);
          _leaching_mass_no3->val[j] = input_mass;  // Summary statistics of leaching mass
      }
    }  

    return EXIT_SUCCESS;
}
