/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_soil_profile_nitrogen.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_soil_profile_nutrient(Control &ctrl, Atmosphere &atm, Param &par){

    /* 
    ### Soil layer 1:
    (_thate1_old)
    + infiltration          (need to mix)
    - percolation1
    - Esoil
    - Transp1           
    (_thate1)
    + reinfiltration
    - repercolation1    


    ### Soil layer 2:
    (_thata2_old)
    + percolation1          (need to mix)
    - percolation2
    - Transp2           
    (_theta2)
    + repercolation1
    - repercolation2    

    ### Soil layer 3:
    (_theta3_old)           
    + percolation2          (need to mix)
    - percolation3
    - Transp3
    (_theta3)          
    + repercolation2
    - repercolation3
    + interflow_in      
    - interflow_out
    - interflow_toChn   
    */

    
    
    
    
    // ======= Mixing through layer 1-3 =======
    // flag1: enrichment due to evaportranspiration
    // flag2: drainage
    // flag3: Fickian diffusion
    // flag4: Whether solute is stable water isotope
    if (ctrl.opt_carbon_sim==1){
      Solve_soil_transport(par, *_doc_pond, *_doc_layer1, *_doc_layer2, *_doc_layer3, *_doc_vadose, *_doc_chanS, *_leaching_mass_doc, *_drainage_mass_doc, true, ctrl.opt_drainage, true, false);  
    }
    
    if (ctrl.opt_nitrogen_sim==1){
      Solve_soil_transport(par, *_no3_pond, *_no3_layer1, *_no3_layer2, *_no3_layer3, *_no3_vadose, *_no3_chanS, *_leaching_mass_no3, *_drainage_mass_no3, true, ctrl.opt_drainage, true, false);
    }


    // ======= Carbon/nitrogen biogeochemical processes =======
    if (ctrl.opt_carbon_sim==1 or ctrl.opt_nitrogen_sim==1){
      Carbon_addition(ctrl, par);      
      Carbon_transformation(ctrl, atm, par);
      Carbon_management(ctrl, par);
    }


    // ======= Nitrogen biogeochemical processes =======
    /* Nitrogen addtion */
    Sort_nitrogen_addition(ctrl, par);
    Nitrogen_addition(ctrl, par);
    Soil_denitrification(ctrl, atm, par);  // Denitrification
   

    return EXIT_SUCCESS;
}
