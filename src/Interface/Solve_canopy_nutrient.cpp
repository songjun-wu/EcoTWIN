/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_canopy_nutrient.cpp
  * Created  on: 02.12.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_canopy_nutrient(Control &ctrl, Atmosphere &atm){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
   

    // Mixing canopy storage with precipitation input
    if (ctrl.opt_carbon_sim==1){  // Carbon
      Solve_canopy_transport(atm, *_doc_I, *_doc_rain, *_doc_pond, true); // erich_flag = true
    }
    if (ctrl.opt_nitrogen_sim==1){  // Nitrogen
      Solve_canopy_transport(atm, *_no3_I, *_no3_rain, *_no3_pond, true); // erich_flag = true
      _tmp->equals(*_no3_rain);
      _tmp->multiply_by_double(0.5);  // Assumption: DOC concentration in rainwater is half of NO3 concentration
      Solve_canopy_transport(atm, *_don_I, *_tmp, *_don_pond, true); // erich_flag = true
    }
    
    

    // Enrichment due to evaporation?
    //for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        // Enrichment due to canopy evaporation (disabled)
        //if (_I->val[j] > roundoffERR and _Ei->val[j] > roundoffERR){
        //    _no3_I->val[j] = _no3_I->val[j] * (_I->val[j] + _Ei->val[j]) / _I->val[j];
        //}
    //}

    return EXIT_SUCCESS;
}
