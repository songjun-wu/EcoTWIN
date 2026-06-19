/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_surface_nutrient.cpp
  * Created  on: 02.12.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_surface_nutrient(Control &ctrl, Atmosphere &atm, Param &par){

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

    if (ctrl.opt_carbon_sim==1){
      Solve_surface_transport(ctrl, atm, par, *_doc_I, *_doc_snow, *_doc_pond, *_doc_chanS, *_doc_GW, true); // enrich_flag = true
    }
    if (ctrl.opt_nitrogen_sim==1){
      Solve_surface_transport(ctrl, atm, par, *_no3_I, *_no3_snow, *_no3_pond, *_no3_chanS, *_no3_GW, true); // enrich_flag = true
      //Solve_surface_transport(ctrl, atm, par, *_don_I, *_don_snow, *_don_pond, *_don_chanS, *_don_GW, true); // enrich_flag = true
    }  
    
    return EXIT_SUCCESS;
}
