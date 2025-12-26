/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_surface_transport.cpp
  * Created  on: 27.11.2025
  * Modified on: 27.11.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_surface_transport(Control &ctrl, Atmosphere &atm, Param &par,
                                   svector &sv_conc_I, svector &sv_conc_snow, svector &sv_conc_pond, svector &sv_conc_chanS, svector &sv_conc_GW,
                                   bool enrich_flag){

    /*
    ### Snow
    (_snow_old)
    + snowacc
    - snowmelt
    (_snow)

    ### Ponding water:
    (_pond_old = 0.0)
    + Th
    + snowmelt
    + irrigation_from_river
    + irrigation_from_GW
    (pond)
    - Infiltration      
    + ovf_in            
    - Reinfiltration
    - ovf_out
    - ovf_toChn           
    */
    
    double irrigation_amount, irrigation_conc;

    // Mixing snow and irrigation
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        
        // Mixing snow with throughfall if temperature is below snow rain threshold
        if (atm._Ta->val[j] < par._snow_rain_thre->val[j]){
            Mixing_full(_snow_old->val[j], sv_conc_snow.val[j], _snowacc->val[j], sv_conc_pond.val[j]);
        } else{  // Else throughfall mixes with snow melt
            sv_conc_pond.val[j] = sv_conc_I.val[j]; // Align the composition in ponding water with that in throughfall
            //mix throughfall with snow melt
            Mixing_full(_Th->val[j], sv_conc_pond.val[j], _snowmelt->val[j], sv_conc_snow.val[j]);
        }

        // Mixing with irrigation
        irrigation_amount = _irrigation_from_river->val[j] + _irrigation_from_GW->val[j];
        if (irrigation_amount > roundoffERR){
            irrigation_conc = (_irrigation_from_river->val[j] * sv_conc_chanS.val[j] + _irrigation_from_GW->val[j] * sv_conc_GW.val[j]) / irrigation_amount;
            Mixing_full(_pond->val[j], sv_conc_pond.val[j], irrigation_amount, irrigation_conc);
        }
        
    }

    return EXIT_SUCCESS;
}

