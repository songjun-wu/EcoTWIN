/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_channel_nitrogen.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_channel_nitrogen(Control &ctrl, Atmosphere &atm, Param &par){

    /* Update the storages for routing flux mixing

    ### chanS:
    - irrigation_from_river
    (_chanS_old)
    + _Qupstream        (need to mix)
    + _ovf_toChn        (need to mix)
    +  _interf_toChn    (need to mix)
    + _GWf_toChn        (need to mix)
    - _Q
    - chanE             (enrichment)
    (_chanS)
    */
    
    // ********* Mixing reinfiltration and percolation ********
    
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
     
        if (_chnlength->val[j] > 0){    // If this is a channel cell 
            if (_Echan->val[j] > roundoffERR){
                if (_chanS->val[j] > roundoffERR){
                    _no3_chanS->val[j] *= (_chanS->val[j] + _Echan->val[j]) / _chanS->val[j];  // Enrichment due to channel evaporation
                } else {
                    _no3_chanS->val[j] = 0.0;
                }   
            }
        }


    }
    
    Instream_transformation(ctrl, atm, par);  // In-stream denitrification





    return EXIT_SUCCESS;
}
