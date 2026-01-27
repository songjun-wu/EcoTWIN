/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Redistribution and modification are allowed under proper acknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_addition.cpp
  * Created  on: 22.11.2025
  * Modified on: 23.11.2025
***************************************************************/


#include "Basin.h"

int Basin::Carbon_addition(Control &ctrl, Param &par){

    double ratio_green_2_leaf = 4.0;  // Ratio of vegetation green pool to leaf carbon pool  
    
    double depth1, depth2, depth3;  // Depth of each layer [m]
    double froot_layer1, froot_layer2, froot_layer3;  // Root fraction in each layer [-]
    double soluble_CP1, soluble_CP2, soluble_CP3;  // Soluble carbon pools in each layer [gC/m2]

    double plant_green_CP, plant_wood_CP, plant_reserve_CP;  // Vegetation pools [gC/m2]
    double plant_green_CP_max, plant_reserve_CP_max; // Maximum carbon content of vegetation pools [gC/m2] (plant_wood_CP_max is a parameter)
    double plant_green_CP_pot, plant_wood_CP_pot, plant_reserve_CP_pot;  // potential vegetation pools for priliminary estiamtion of NPP distribution [gC/m2]
    double excess_C;  // Carbon exceeding the maximum content of vegetation pools

    // From NPP to vegetations
    double NPP; // Net primary production
    double NPP_2_green, NPP_2_wood, NPP_2_reserve, NPP_2_root_exudates, NPP_from_green_to_reserve; // NPP addition to vegetation pools
    
    // From vegetation to litter
    double leaf_shedding;  // The shedding fraction of leaf [-]
    double C_green_2_litter_nonwood, C_plant_reserve_CP_2_litter_nonwood, C_wood_2_litter_wood; // Carbon fluxes from vegetation to green/wood litter pools

    // From litter to soil carbon pools
    double litter_nonwood, litter_wood;   // Litter pools
    double C_wood_to_acid_wood, C_wood_to_ethanol, C_wood_to_nonsoluble, C_wood_to_soluble, C_wood_to_humus; // Carbon fluxes from wood litter pools to wood carbon pools

    
    // Variables for nitrogen simulation
    double mineral_N_layer1, mineral_N_layer2, mineral_N_layer3;  // Mineral N pools in each layer [gN/m2]
    double potential_N_for_plant_growth;  // Potential nitrogen uptake by vegetation for plant growth in all layers [gN/m2]
    double potential_N_for_plant_growth_layer1, potential_N_for_plant_growth_layer2, potential_N_for_plant_growth_layer3; // Potential nitrogen uptake by vegetation for plant growth in each layer [gN/m2]
    double actual_N_for_plant_growth; // Actual nitrogen uptake by vegetation for plant growth in all layers [gN/m2]
    double plant_uptake; // Plant uptake in each layer [gN/m2]
    double fct_N_limitation;  // Limitation of vegetation growth of green and wood pools based on N availability; plant_reserve_CP pool is not affected; Set to 1 if nitrogen simulation is not enabled is not activated


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


      depth1 = _depth1->val[j];
      depth2 = _depth2->val[j];
      depth3 = par._depth3->val[j];
      
      plant_green_CP = _plant_green_CP->val[j];
      plant_wood_CP = _plant_wood_CP->val[j];
      plant_reserve_CP = _plant_reserve_CP->val[j];

      plant_green_CP_max = ratio_green_2_leaf * _LAI->val[j] / par._C_in_LeafArea->val[j];  // The maximum carbon content in green pool [gC/m2]
      plant_reserve_CP_max = par._plant_reserve_CP_max->val[j] / par._C_in_LeafArea->val[j];  // The maximum carbon content in plant_reserve_CP pool [gC/m2]
      soluble_CP1 = _doc_layer1->val[j] * _theta1->val[j] * depth1;
      soluble_CP2 = _doc_layer2->val[j] * _theta2->val[j] * depth2;
      soluble_CP3 = _doc_layer3->val[j] * _theta3->val[j] * depth3;

      froot_layer1 = _froot_layer1->val[j];  // Root fraction in layer 1 [-]
      froot_layer2 = _froot_layer2->val[j];  // Root fraction in layer 2 [-]
      froot_layer3 = _froot_layer3->val[j];  // Root fraction in layer 3 [-]

      fct_N_limitation = 1.0;  // Limitation of vegetation growth of green and wood pools based on N availability; plant_reserve_CP pool is not affected; Set to 1 if nitrogen simulation is not enabled is not activated



      /* ================================================================================================= */
      /* ======= Distribute vegetation pools to litter pools (leaf sheding, wood, and plant_reserve_CP tau) ======= */
      /* ================================================================================================= */
      // Leaf sheding: from vegetation green pool to non-woody litter pool
      // TODO: Autumn sheding needs to be added
      leaf_shedding = max(_LAI->val[j] * par._LAI_shed_coef->val[j], _LAI_old->val[j] - _LAI->val[j]);  // Normal shedding or due to plant mortality
      C_green_2_litter_nonwood = min(ratio_green_2_leaf * leaf_shedding / par._C_in_LeafArea->val[j], plant_green_CP); 
      plant_green_CP -= C_green_2_litter_nonwood;
      // The green carbon pool cannot exceed the LAI-scaled maximum (ratio_green_2_leaf * _LAI->val[j] / par._C_in_LeafArea->val[j])
      excess_C = plant_green_CP - plant_green_CP_max;
      if (excess_C > 0) {
        C_green_2_litter_nonwood += excess_C;
        plant_green_CP -= excess_C;
      }

      // TODO: HARVEST?
      // TODO: Herbivory loss from plant_green_CP & green_NP? Not considered at the moment

      // Wood sheding: from vegetation wood pool to wood litter pool
      C_wood_2_litter_wood = plant_wood_CP / par._tau_wood_C->val[j];
      plant_wood_CP -= C_wood_2_litter_wood;

      // Depletion of plant_reserve_CP pool: from plant_reserve_CP pool to green litter pool
      C_plant_reserve_CP_2_litter_nonwood = plant_reserve_CP / 365;  // _tau_plant_reserve_CP_C = 365 days; depletion of plant_reserve_CP pool
      plant_reserve_CP -= C_plant_reserve_CP_2_litter_nonwood;
      

      /* ================================================== */
      /* ======= Distribute NPP to vegetation pools ======= */
      /* ================================================== */
      NPP = _NPP->val[j];
      plant_green_CP_pot = plant_green_CP;
      plant_wood_CP_pot = plant_wood_CP; 
      plant_reserve_CP_pot = plant_reserve_CP;

      NPP_2_green = 0;
      NPP_2_wood = 0;
      NPP_2_reserve = 0;
      NPP_2_root_exudates = 0;

      if (NPP <= 0){  // Negetive NPP
        NPP_2_reserve = max(NPP, - plant_reserve_CP);
        NPP -= NPP_2_reserve;
        NPP_2_green = max(NPP, - plant_green_CP);
        NPP -= NPP_2_green;
        NPP_2_wood = max(NPP, - plant_wood_CP);
        NPP -= NPP_2_wood;

      } else {
        // Positive NPP: Potential growth of vegetation pools
        NPP_2_wood =  NPP *  par._frac_NPP_to_wood->val[j];
        NPP_2_green = NPP *  par._frac_NPP_to_green->val[j];
        NPP_2_reserve = NPP * (1 - par._frac_NPP_to_green->val[j] - par._frac_NPP_to_wood->val[j]);
        
        // Growth of wood pool. Excess wood addtion is transfered to green pool
        plant_wood_CP_pot += NPP_2_wood;
        excess_C = plant_wood_CP_pot - par._plant_wood_CP_max->val[j];
        if (excess_C > 0){
          //plant_wood_CP_pot = par._plant_wood_CP_max->val[j];
          NPP_2_wood -= excess_C;
          NPP_2_green += excess_C;
        }

        // Growth of plant_reserve_CP pool. Excess plant_reserve_CP addtion is transfered to green pool too
        plant_reserve_CP_pot += NPP_2_reserve;
        excess_C = plant_reserve_CP_pot - plant_reserve_CP_max;
        if (excess_C > 0){
          //plant_reserve_CP_pot = par._plant_reserve_CP_max->val[j];
          NPP_2_reserve -= excess_C;
          NPP_2_green += excess_C;
        }

        // Growth of green pool. Excess green addtion will fill the plant_reserve_CP pool (if there is any deficit)
        plant_green_CP_pot += NPP_2_green;
        excess_C = plant_green_CP_pot - plant_green_CP_max;
        if (excess_C > 0){
          plant_green_CP_pot = plant_green_CP_max;
          NPP_2_green -= excess_C;
          if (plant_reserve_CP_pot < plant_reserve_CP_max){
            NPP_from_green_to_reserve = min(excess_C, plant_reserve_CP_max - plant_reserve_CP_pot);
            NPP_2_reserve += NPP_from_green_to_reserve;
            excess_C -= NPP_from_green_to_reserve;
          }
          NPP_2_root_exudates = excess_C;  // The remaining carbon excess goes into root_exudates, then added to green pool
        }
              
        
      }  // End if NPP > 0



      /* ================================================== */
      /* ======= Nitrogen simulation ======= */
      /* ======= For carbon: Nitrogen limitation of vegetation growth ======= */
      /* ======= For nitrogen: mineral N uptake to sustain vegetation growth ======= */
      /* ================================================== */
      if (ctrl.opt_nitrogen_sim){
        potential_N_for_plant_growth = (NPP_2_green)*par._NC_ratio_plant_green->val[j] + NPP_2_wood*par._NC_ratio_plant_wood->val[j];
        if (potential_N_for_plant_growth > roundoffERR) {
          // Actual growth of vegetation pools with N limitation
          // Get mineral N pools in each layer
          mineral_N_layer1 = _no3_layer1->val[j] * _theta1->val[j] * depth1;
          mineral_N_layer2 = _no3_layer2->val[j] * _theta2->val[j] * depth2;
          mineral_N_layer3 = _no3_layer3->val[j] * _theta3->val[j] * depth3;

          // Get potential nitrogen uptake in each layer based on root distribution
          potential_N_for_plant_growth_layer1 = potential_N_for_plant_growth * froot_layer1;
          potential_N_for_plant_growth_layer2 = potential_N_for_plant_growth * froot_layer2;
          potential_N_for_plant_growth_layer3 = potential_N_for_plant_growth * froot_layer3;

          actual_N_for_plant_growth = 0.0;  // Cumulative nitrogen uptake by vegetation for plant growth in all layers
          // Plant nitrogen uptake in each layer
          if (mineral_N_layer1 > roundoffERR) {
            plant_uptake = min(potential_N_for_plant_growth_layer1, mineral_N_layer1);
            actual_N_for_plant_growth += plant_uptake;
            mineral_N_layer1 -= plant_uptake;
          }
          if (mineral_N_layer2 > roundoffERR) {
            plant_uptake = min(potential_N_for_plant_growth_layer2, mineral_N_layer2);
            actual_N_for_plant_growth += plant_uptake;
            mineral_N_layer2 -= plant_uptake;
          }
          if (mineral_N_layer3 > roundoffERR) {
            plant_uptake = min(potential_N_for_plant_growth_layer3, mineral_N_layer3);
            actual_N_for_plant_growth += plant_uptake;
            mineral_N_layer3 -= plant_uptake;
          }
          
          // fct_N_limitation is calculated as the ratio between actual and potential nitrogen uptake
          fct_N_limitation = actual_N_for_plant_growth / potential_N_for_plant_growth;  // Limitation of vegetation growth of green and wood pools based on N availability

          // Update global variables
          _no3_layer1->val[j] = mineral_N_layer1 / (_theta1->val[j] * depth1);
          _no3_layer2->val[j] = mineral_N_layer2 / (_theta2->val[j] * depth2);
          _no3_layer3->val[j] = mineral_N_layer3 / (_theta3->val[j] * depth3);
          _plant_uptake->val[j] = actual_N_for_plant_growth;  // Update plant uptake [gN/m2]          
      } else {
        fct_N_limitation = 1.0;  // vegetation growth is little thus not limited by N availability
      }
    }  // end if (ctrl.opt_nitrogen_sim)


    /* ======= Update carbon variables ======= */
    plant_green_CP += NPP_2_green * fct_N_limitation;  
    plant_wood_CP += NPP_2_wood * fct_N_limitation;
    plant_reserve_CP += NPP_2_reserve;
    //NPP_2_root_exudates *= 1; // Root exudates is not limited by N availability, as it contains only nitrogen-free sugar
    
    _plant_green_CP->val[j] = plant_green_CP;
    _plant_wood_CP->val[j] = plant_wood_CP;
    _plant_reserve_CP->val[j] = plant_reserve_CP;
    _NPP->val[j] = NPP_2_green + NPP_2_wood + NPP_2_reserve + NPP_2_root_exudates;

    
 
    /* ============================================================= */
    /* ======= Distribute carbon fluxes to soil litter pools ======= */
    /* ============================================================= */
    // From non-woody litter to non-woody pools (only exists in top soil layer)
    litter_nonwood = C_green_2_litter_nonwood + C_plant_reserve_CP_2_litter_nonwood + NPP_2_root_exudates;  // Nonwood litter contains addition from vegetation green pool, plant_reserve_CP pool, and root exudates from excess NPP
    _acid_CP1_nonwood->val[j] += litter_nonwood * par._frac_litter_to_acid_nonwood->val[j];
    _ethanol_CP1_nonwood->val[j] += litter_nonwood * par._frac_litter_to_ethanol_nonwood->val[j];
    _nonsoluble_CP1_nonwood->val[j] += litter_nonwood * par._frac_litter_to_nonsoluble_nonwood->val[j];
    soluble_CP1 += litter_nonwood * par._frac_litter_to_soluble_nonwood->val[j];
    _humus_CP1->val[j] += litter_nonwood * (1 - 
                                            par._frac_litter_to_soluble_nonwood->val[j] - 
                                            par._frac_litter_to_acid_nonwood->val[j] - 
                                            par._frac_litter_to_ethanol_nonwood->val[j] - 
                                            par._frac_litter_to_nonsoluble_nonwood->val[j]);
    

    // From woody litter to woody pools (vertically distributed along the roots)
    // Distribute wood litter pool to different soil carbon pools
    litter_wood = C_wood_2_litter_wood;  // Wood litter cotains addition from vegetation woody pool and root exudates
    C_wood_to_acid_wood = C_wood_2_litter_wood * par._frac_litter_to_acid_wood->val[j];
    C_wood_to_ethanol = C_wood_2_litter_wood * par._frac_litter_to_ethanol_wood->val[j];
    C_wood_to_nonsoluble = C_wood_2_litter_wood * par._frac_litter_to_nonsoluble_wood->val[j];
    C_wood_to_soluble = C_wood_2_litter_wood * par._frac_litter_to_soluble_wood->val[j];
    C_wood_to_humus = C_wood_2_litter_wood * (1 - 
                                            par._frac_litter_to_soluble_wood->val[j] - 
                                            par._frac_litter_to_acid_wood->val[j] - 
                                            par._frac_litter_to_ethanol_wood->val[j] - 
                                            par._frac_litter_to_nonsoluble_wood->val[j]);
          
    // Assign soil carbon addition vertically along root distribution
    // Layer 1
    _acid_CP1_wood->val[j] += C_wood_to_acid_wood * froot_layer1;
    _ethanol_CP1_wood->val[j] += C_wood_to_ethanol * froot_layer1;
    _nonsoluble_CP1_wood->val[j] += C_wood_to_nonsoluble * froot_layer1;
    soluble_CP1 += C_wood_to_soluble * froot_layer1;
    _humus_CP1->val[j] += C_wood_to_humus * froot_layer1;
    // Layer 2
    _acid_CP2_wood->val[j] += C_wood_to_acid_wood * froot_layer2;
    _ethanol_CP2_wood->val[j] += C_wood_to_ethanol * froot_layer2;
    _nonsoluble_CP2_wood->val[j] += C_wood_to_nonsoluble * froot_layer2;
    soluble_CP2 += C_wood_to_soluble * froot_layer2;
    _humus_CP2->val[j] += C_wood_to_humus * froot_layer2;
    // Layer 3
    _acid_CP3_wood->val[j] += C_wood_to_acid_wood * froot_layer3;
    _ethanol_CP3_wood->val[j] += C_wood_to_ethanol * froot_layer3;
    _nonsoluble_CP3_wood->val[j] += C_wood_to_nonsoluble * froot_layer3;
    soluble_CP3 += C_wood_to_soluble * froot_layer3;
    _humus_CP3->val[j] += C_wood_to_humus * froot_layer3;

    /* ======= Update carbon variables ======= */
    _doc_layer1->val[j] = soluble_CP1 / (_theta1->val[j] * depth1);
    _doc_layer2->val[j] = soluble_CP2 / (_theta2->val[j] * depth2);
    _doc_layer3->val[j] = soluble_CP3 / (_theta3->val[j] * depth3);
    
    /* =============== Nitrogen simulation =============== */
    /* ======= For nitrogen: nitrogen addtion from vegetation to litter pools ======= */
    /* ================================================== */
    if (ctrl.opt_nitrogen_sim){
      // Nitrogen carbon ratio is constant in acid, ethanol, and nonsoluble wood litter pools, thus nitrogen addition does not need explicit calculation
      // Nitrogen carbon ratio is varaible in non-wood pools in the first layer and DON pool across all layers
      
      double soluble_DON_NP1 = _don_layer1->val[j] * _theta1->val[j] * depth1;
      double soluble_DON_NP2 = _don_layer2->val[j] * _theta2->val[j] * depth2;
      double soluble_DON_NP3 = _don_layer3->val[j] * _theta3->val[j] * depth3;
      double soluble_DIN_NP1 = _no3_layer1->val[j] * _theta1->val[j] * depth1;
      double soluble_DIN_NP2 = _no3_layer2->val[j] * _theta2->val[j] * depth2;
      double soluble_DIN_NP3 = _no3_layer3->val[j] * _theta3->val[j] * depth3;

      double C_wood_2_litter_wood_each_layer;

      double mineralisation_soil = 0.0; // Cumulative mineralisation of plant N to dissovled inorganic pools in soil
      double mineralisation_soil_each_layer = 0.0; // Mineralisation of plant N to dissovled inorganic pools in each layer

      // Non-wood pools in the first layer
      // From green pool to litter pools
      _fast_NP1_nonwood->val[j] += (C_green_2_litter_nonwood) * (1 - par._frac_litter_to_soluble_nonwood->val[j]) * par._NC_ratio_fast_pool_nonwood->val[j];  // Only green pool contains ntrogen (reserve pool is nitrogen free)
      soluble_DON_NP1 += (C_green_2_litter_nonwood) * par._frac_litter_to_soluble_nonwood->val[j] * par._NC_ratio_fast_pool_nonwood->val[j];
      mineralisation_soil_each_layer = (C_green_2_litter_nonwood) * (par._NC_ratio_plant_green->val[j] - par._NC_ratio_fast_pool_nonwood->val[j]);
      soluble_DIN_NP1 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;
     
      // Wood pools in the first layer
      // No need to update fast_NP1_wood because all wood pools have consistent NC ratio as par._NC_ratio_fast_pool_wood->val[j]; so we only need to track fast carbon pools
      C_wood_2_litter_wood_each_layer = C_wood_2_litter_wood * froot_layer1;
      soluble_DON_NP1 += C_wood_2_litter_wood_each_layer * par._frac_litter_to_soluble_wood->val[j] * par._NC_ratio_fast_pool_wood->val[j];
      mineralisation_soil_each_layer = C_wood_2_litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_fast_pool_wood->val[j]);
      soluble_DIN_NP1 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;
      
      // Wood pools in the second layer
      // No need to update fast_NP1_wood because all wood pools have consistent NC ratio as par._NC_ratio_fast_pool_wood->val[j]; so we only need to track fast carbon pools
      C_wood_2_litter_wood_each_layer = C_wood_2_litter_wood * froot_layer2;
      soluble_DON_NP2 += C_wood_2_litter_wood_each_layer * par._frac_litter_to_soluble_wood->val[j] * par._NC_ratio_fast_pool_wood->val[j];
      mineralisation_soil_each_layer = C_wood_2_litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_fast_pool_wood->val[j]);
      soluble_DIN_NP2 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;

      // Wood pools in the third layer
      // No need to update fast_NP1_wood because all wood pools have consistent NC ratio as par._NC_ratio_fast_pool_wood->val[j]; so we only need to track fast carbon pools
      C_wood_2_litter_wood_each_layer = C_wood_2_litter_wood * froot_layer3;
      soluble_DON_NP3 += C_wood_2_litter_wood_each_layer * par._frac_litter_to_soluble_wood->val[j] * par._NC_ratio_fast_pool_wood->val[j];
      mineralisation_soil_each_layer = C_wood_2_litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_fast_pool_wood->val[j]);
      soluble_DIN_NP3 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;
      
      // Update DON and DIN concentrations
      _don_layer1->val[j] = soluble_DON_NP1 / (_theta1->val[j] * depth1);
      _don_layer2->val[j] = soluble_DON_NP2 / (_theta2->val[j] * depth2);
      _don_layer3->val[j] = soluble_DON_NP3 / (_theta3->val[j] * depth3);
      _no3_layer1->val[j] = soluble_DIN_NP1 / (_theta1->val[j] * depth1);
      _no3_layer2->val[j] = soluble_DIN_NP2 / (_theta2->val[j] * depth2);
      _no3_layer3->val[j] = soluble_DIN_NP3 / (_theta3->val[j] * depth3);
      _minerl_soil->val[j] += mineralisation_soil;
      
    }   // end if (ctrl.opt_nitrogen_sim)

  }  // end for (unsigned int j = 0; j < _sortedGrid.row.size(); j++)

    return EXIT_SUCCESS;
}

