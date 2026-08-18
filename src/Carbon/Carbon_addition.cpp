/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
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

    
    // From NPP to vegetations
    double NPP; // Net primary production
    double NPP_2_green, NPP_2_wood, NPP_2_reserve, NPP_2_root_exudates, NPP_from_green_to_reserve; // NPP addition to vegetation pools
    double plant_green_CP, plant_wood_CP, plant_reserve_CP;  // Vegetation pools [gC/m2]
    double plant_green_CP_max, plant_reserve_CP_max; // Maximum carbon content of vegetation pools [gC/m2] (plant_wood_CP_max is a parameter)
    double plant_green_CP_pot, plant_wood_CP_pot, plant_reserve_CP_pot;  // potential vegetation pools for priliminary estiamtion of NPP distribution [gC/m2]
    double excess_C;  // Carbon exceeding the maximum content of vegetation pools
    
    // From vegetation to litter
    double leaf_shedding;  // The shedding fraction of leaf [-]
    double C_green_2_litter_nonwood, C_plant_reserve_CP_2_litter_nonwood, C_wood_2_litter_wood; // Carbon fluxes from vegetation to green/wood litter pools
    double litter_nonwood, litter_wood, litter_nonwood_leaf, litter_nonwood_root;  // The amount of non-woody litter pool in leaf and root [gC/m2]
    double dpm_litter_ratio_nonwood;  // The fraction of decomposable plant material litter pool in non-wood plant materials [-]
    double frac_leaf_in_litter;  // The ratio of leaf carbon to root carbon [-]
    double dpm_litter_CP, rpm_litter_CP;  // The amount of decomposable plant material litter pool in non-wood and wood plant materials [gC/m2]
    double dpm_litter_CP1, dpm_litter_CP2, dpm_litter_CP3;  // Decomposable plant material litter carbon pool in each layer [gC/m2]
    double rpm_litter_CP1, rpm_litter_CP2, rpm_litter_CP3;  // Resistant plant material litter carbon pool in each layer [gC/m2]

    
    // Variables for nitrogen simulation
    double mineral_N_layer1, mineral_N_layer2, mineral_N_layer3;  // Mineral N pools in each layer [gN/m2]
    double potential_N_for_plant_growth_layer1, potential_N_for_plant_growth_layer2, potential_N_for_plant_growth_layer3; // Potential nitrogen uptake by vegetation for plant growth in each layer [gN/m2]
    double actual_N_for_plant_growth; // Actual nitrogen uptake by vegetation for plant growth in all layers [gN/m2]
    double fct_N_limitation_green, fct_N_limitation_wood;  // Limitation of vegetation growth of green and wood pools based on N availability; plant_reserve_CP pool is not affected; Set to 1 if nitrogen simulation is not enabled is not activated
    double N_biological_fixiation; // Nitrogen biological fixiation [gN/m2]
    double litter_wood_each_layer;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      


      depth1 = _depth1->val[j];
      depth2 = _depth2->val[j];
      depth3 = par._depth3->val[j];
      
      plant_green_CP = _plant_green_CP->val[j];
      plant_wood_CP = _plant_wood_CP->val[j];
      plant_reserve_CP = _plant_reserve_CP->val[j];

      plant_green_CP_max = ratio_green_2_leaf * _LAI->val[j] / par._C_in_LeafArea->val[j];  // The maximum carbon content in green pool [gC/m2]
      plant_reserve_CP_max = par._plant_reserve_CP_max->val[j] / par._C_in_LeafArea->val[j];  // The maximum carbon content in plant_reserve_CP pool [gC/m2]

      froot_layer1 = _froot_layer1->val[j];  // Root fraction in layer 1 [-]
      froot_layer2 = _froot_layer2->val[j];  // Root fraction in layer 2 [-]
      froot_layer3 = _froot_layer3->val[j];  // Root fraction in layer 3 [-]

      


    
      

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

        /* ================== Nitrogen Simulation ================ */
        if (ctrl.opt_nitrogen_sim){
          // Get and update mineral N pools in each layer
          mineral_N_layer1 = _no3_layer1->val[j] * _theta1->val[j] * depth1;
          mineral_N_layer2 = _no3_layer2->val[j] * _theta2->val[j] * depth2;
          mineral_N_layer3 = _no3_layer3->val[j] * _theta3->val[j] * depth3;

          double Nflux_from_nonwood = -1 * (NPP_2_green + NPP_2_reserve) * par._NC_ratio_plant_green->val[j];
          double Nflux_from_wood = -1 * NPP_2_wood * par._NC_ratio_plant_wood->val[j];
          // Release the nitrogen from non-wood and wood plant materials to soil mineral N pools
          _plant_mobile_NP->val[j] += Nflux_from_nonwood;   // Non-woody fluxes go to plant mobile N pool
          mineral_N_layer1 += Nflux_from_wood * froot_layer1;  // Woody fluxes go to soil mineral N pools
          mineral_N_layer2 += Nflux_from_wood * froot_layer2;
          mineral_N_layer3 += Nflux_from_wood * froot_layer3;

          // Update global variables
          _no3_layer1->val[j] = mineral_N_layer1 / (_theta1->val[j] * depth1);
          _no3_layer2->val[j] = mineral_N_layer2 / (_theta2->val[j] * depth2);
          _no3_layer3->val[j] = mineral_N_layer3 / (_theta3->val[j] * depth3);         
                              
        }



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

        // Growth of plant_reserve_CP pool. Excess plant_reserve_CP addtion is transfered to green pool
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


      /* ========================================================= */
      /* ================== Nitrogen Availability ================ */
      /* ========================================================= */
      if (ctrl.opt_nitrogen_sim){
        // Get and update mineral N pools in each layer
        mineral_N_layer1 = _no3_layer1->val[j] * _theta1->val[j] * depth1;
        mineral_N_layer2 = _no3_layer2->val[j] * _theta2->val[j] * depth2;
        mineral_N_layer3 = _no3_layer3->val[j] * _theta3->val[j] * depth3;

      /* ======= For carbon: Nitrogen limitation of vegetation growth ======= */
      /* ======= For nitrogen: Nitrogen biological fixiation and mineral N uptake to sustain vegetation growth ======= */
        double potential_N_for_nonwood_growth = (NPP_2_green + NPP_2_reserve + NPP_2_root_exudates) * par._NC_ratio_plant_green->val[j];
        double potential_N_for_wood_growth = NPP_2_wood * par._NC_ratio_plant_wood->val[j];
        double plant_uptake_cumulative = 0.0;  // Cumulative nitrogen uptake by vegetation for plant growth in all layers
        double plant_mobile_N = _plant_mobile_NP->val[j];  // Plant mobile N availability [gN/m2]


        // === Nitrogen biological fixiation ===
        N_biological_fixiation = max(0.0, 0.7 * (1 - exp(-0.003 * _NPP->val[j])) * 14 / 12);  // Note that here fixation is proportional to potential NPP; the real NPP is constrained by nitrogen limitation
        mineral_N_layer1 += N_biological_fixiation * _froot_layer1->val[j];
        mineral_N_layer2 += N_biological_fixiation * _froot_layer2->val[j];
        mineral_N_layer3 += N_biological_fixiation * _froot_layer3->val[j];
        _biological_fixiation_N->val[j] = N_biological_fixiation;  // [gN/m2]

        // === Plant uptake ===
        // First sort the use of plant mobile N for green pool growth
        fct_N_limitation_green = 1.0;  // Limitation of vegetation growth of green and wood pools based on N availability; plant_reserve_CP pool is not affected; Set to 1 if nitrogen simulation is not enabled is not activated
        fct_N_limitation_wood = 1.0;
        double green_used_mobile_N = 0.0;
        double green_soil_demand = 0.0;
        if (potential_N_for_nonwood_growth > roundoffERR) {
          if (potential_N_for_nonwood_growth < plant_mobile_N) {
            green_used_mobile_N = potential_N_for_nonwood_growth;
            plant_mobile_N -= potential_N_for_nonwood_growth;
          } else {
            green_used_mobile_N = plant_mobile_N;
            green_soil_demand = potential_N_for_nonwood_growth - plant_mobile_N;
            plant_mobile_N = 0.0;
          }
        }

        // Calculate the total soil demand
        double total_soil_demand = green_soil_demand + potential_N_for_wood_growth;
        double total_mineral_N = mineral_N_layer1 + mineral_N_layer2 + mineral_N_layer3;
        double actual_soil_uptake = 0.0;
        double remaining_frac = 1.0;

        if (total_soil_demand > roundoffERR && total_mineral_N > roundoffERR) {
          actual_soil_uptake = min(total_soil_demand, total_mineral_N);
          remaining_frac = 1.0 - actual_soil_uptake / total_mineral_N;
          mineral_N_layer1 *= remaining_frac;
          mineral_N_layer2 *= remaining_frac;
          mineral_N_layer3 *= remaining_frac;
        } else if (total_mineral_N <= roundoffERR) {
          mineral_N_layer1 = 0.0; 
          mineral_N_layer2 = 0.0; 
          mineral_N_layer3 = 0.0;
        }

        double actual_green_soil_uptake = min(green_soil_demand, actual_soil_uptake);
        double actual_wood_soil_uptake = actual_soil_uptake - actual_green_soil_uptake;

        // Green Limitation
        if (potential_N_for_nonwood_growth > roundoffERR) {
          fct_N_limitation_green = (green_used_mobile_N + actual_green_soil_uptake) / potential_N_for_nonwood_growth;
        } else {
          fct_N_limitation_green = 1.0;
        }
        // Wood Limitation
        if (potential_N_for_wood_growth > roundoffERR) {
          fct_N_limitation_wood = actual_wood_soil_uptake / potential_N_for_wood_growth;
        } else {
          fct_N_limitation_wood = 1.0;
        }


        // Update global variables
        _no3_layer1->val[j] = mineral_N_layer1 / (_theta1->val[j] * depth1);
        _no3_layer2->val[j] = mineral_N_layer2 / (_theta2->val[j] * depth2);
        _no3_layer3->val[j] = mineral_N_layer3 / (_theta3->val[j] * depth3);
        _plant_mobile_NP->val[j] = plant_mobile_N;  // Update plant mobile N availability [gN/m2]
        _plant_uptake_N->val[j] = green_used_mobile_N + actual_soil_uptake;  // Update plant uptake from soil mineral N pools [gN/m2]       

      }  // end if (ctrl.opt_nitrogen_sim)




    /* ======= Update carbon variables ======= */
    // Apply N limitation to NPP for vegetation growth
    NPP_2_green *= fct_N_limitation_green;
    NPP_2_wood *= fct_N_limitation_wood;
    // Reserve and root exudates are theortically nitrogen-free, but here we assume they also share the same C:N ratio for consistency of all sources of non-woody litter pools
    NPP_2_reserve *= fct_N_limitation_green;
    NPP_2_root_exudates *= fct_N_limitation_green;

    // Update vegetation carbon pools
    plant_green_CP += NPP_2_green;  
    plant_wood_CP += NPP_2_wood;
    plant_reserve_CP += NPP_2_reserve;
    _plant_green_CP->val[j] = plant_green_CP;
    _plant_wood_CP->val[j] = plant_wood_CP;
    _plant_reserve_CP->val[j] = plant_reserve_CP;
    // Update actual NPP
    _NPP->val[j] = NPP_2_green + NPP_2_wood + NPP_2_reserve + NPP_2_root_exudates;



    /* ================================================================================================= */
    /* ======= Distribute vegetation pools to litter pools (leaf sheding, wood, and plant_reserve_CP tau) ======= */
    /* ================================================================================================= */
    // Leaf sheding: from vegetation green pool to non-woody litter pool
    // TODO: Autumn sheding needs to be added
    leaf_shedding = max(_LAI->val[j] * par._LAI_shed_coef->val[j], _LAI_old->val[j] - _LAI->val[j]);  // Normal shedding or due to plant mortality
    C_green_2_litter_nonwood = min(ratio_green_2_leaf * leaf_shedding / par._C_in_LeafArea->val[j], 0.1 * plant_green_CP); 
    plant_green_CP -= C_green_2_litter_nonwood;
    // The green carbon pool cannot exceed the LAI-scaled maximum (ratio_green_2_leaf * _LAI->val[j] / par._C_in_LeafArea->val[j])
    excess_C = plant_green_CP - plant_green_CP_max;
    if (excess_C > 0) {
      C_green_2_litter_nonwood += excess_C;
      plant_green_CP -= excess_C;
    }


    // Wood sheding: from vegetation wood pool to wood litter pool
    C_wood_2_litter_wood = plant_wood_CP / par._tau_wood_C->val[j];
    plant_wood_CP -= C_wood_2_litter_wood;

    // Depletion of plant_reserve_CP pool: from plant_reserve_CP pool to green litter pool
    C_plant_reserve_CP_2_litter_nonwood = plant_reserve_CP / 365;  // _tau_plant_reserve_CP_C = 365 days; depletion of plant_reserve_CP pool
    plant_reserve_CP -= C_plant_reserve_CP_2_litter_nonwood;

    // Harvest for crops
    // Generated litter partially goes to harvest pool during harvest period (tile/crop-based)
    double fraction_crop_to_harvest;
    int idx;
    int day_of_year = ctrl.day_of_year;

    fraction_crop_to_harvest = 0.0;
    for (int i = 0; i < num_landuse; i++) {
      idx = landuse_idx[i];
        if (is_crop[idx] == 1){
          if (day_of_year >= harvest_day[idx] and day_of_year < (harvest_day[idx] + harvest_period[idx])){
            fraction_crop_to_harvest += par.param_category->val[idx][j] * harvest_coeff[idx];
          }
      }
    }

    _harvest_C->val[j] = (C_green_2_litter_nonwood + C_plant_reserve_CP_2_litter_nonwood + C_wood_2_litter_wood) * fraction_crop_to_harvest;
    C_green_2_litter_nonwood *= (1 - fraction_crop_to_harvest);
    C_plant_reserve_CP_2_litter_nonwood *= (1 - fraction_crop_to_harvest);
    C_wood_2_litter_wood *= (1 - fraction_crop_to_harvest);

    


    

    /* ======= Update carbon variables ======= */
    _plant_green_CP->val[j] = plant_green_CP;
    _plant_wood_CP->val[j] = plant_wood_CP;
    _plant_reserve_CP->val[j] = plant_reserve_CP;


    /* ======= Distribute carbon fluxes to soil litter pools ======= */

    // Local variables for litter distribution
    dpm_litter_CP1 = _dpm_litter_CP1->val[j];
    dpm_litter_CP2 = _dpm_litter_CP2->val[j];
    dpm_litter_CP3 = _dpm_litter_CP3->val[j];
    rpm_litter_CP1 = _rpm_litter_CP1->val[j];
    rpm_litter_CP2 = _rpm_litter_CP2->val[j];
    rpm_litter_CP3 = _rpm_litter_CP3->val[j];

    // Related parameters for litter distribution
    dpm_litter_ratio_nonwood = par._alpha_litter_distribution_nonwood->val[j] / (1 + par._alpha_litter_distribution_nonwood->val[j]);  // The fraction of decomposable plant material litter pool in non-wood plant materials [-]
    frac_leaf_in_litter = par._frac_leaf_in_litter->val[j];  // The fraction of leaf in non-woody plant materials (compared to fine root) going to decomposable plant material litter pool [-]
    // From non-woody plant materials to litter pools (both dpm and rpm litter pools)
    litter_nonwood = C_green_2_litter_nonwood + C_plant_reserve_CP_2_litter_nonwood + NPP_2_root_exudates;  // Nonwood litter contains addition from vegetation green pool, reserve pool, and root exudates from excess NPP
    litter_nonwood_leaf = C_green_2_litter_nonwood * frac_leaf_in_litter;  // Leaf only goes to the top soil layer
    litter_nonwood_root = C_green_2_litter_nonwood * (1 - frac_leaf_in_litter) + C_plant_reserve_CP_2_litter_nonwood + NPP_2_root_exudates;  // Fine roots, root exudates and reserve pool go to three soil layer based on root distribution
    // Leaf only goes to the top soil layer
    dpm_litter_CP1 += litter_nonwood_leaf * dpm_litter_ratio_nonwood;
    rpm_litter_CP1 += litter_nonwood_leaf * (1 - dpm_litter_ratio_nonwood);
    // Fine roots are assigned based on root distribution
    dpm_litter_CP1 += litter_nonwood_root * froot_layer1 * dpm_litter_ratio_nonwood;
    rpm_litter_CP1 += litter_nonwood_root * froot_layer1 * (1 - dpm_litter_ratio_nonwood);
    dpm_litter_CP2 += litter_nonwood_root * froot_layer2 * dpm_litter_ratio_nonwood;
    rpm_litter_CP2 += litter_nonwood_root * froot_layer2 * (1 - dpm_litter_ratio_nonwood);
    dpm_litter_CP3 += litter_nonwood_root * froot_layer3 * dpm_litter_ratio_nonwood;
    rpm_litter_CP3 += litter_nonwood_root * froot_layer3 * (1 - dpm_litter_ratio_nonwood);

    // From woody plant materials to litter pools (only rpm pools; vertically distributed along the roots)
    litter_wood = C_wood_2_litter_wood;  // Wood litter cotains addition from vegetation woody pool
    rpm_litter_CP1 += litter_wood * froot_layer1;
    rpm_litter_CP2 += litter_wood * froot_layer2;
    rpm_litter_CP3 += litter_wood * froot_layer3;

    // Update litter pools
    _dpm_litter_CP1->val[j] = dpm_litter_CP1;
    _dpm_litter_CP2->val[j] = dpm_litter_CP2;
    _dpm_litter_CP3->val[j] = dpm_litter_CP3;
    _rpm_litter_CP1->val[j] = rpm_litter_CP1;
    _rpm_litter_CP2->val[j] = rpm_litter_CP2;
    _rpm_litter_CP3->val[j] = rpm_litter_CP3;
    _litter_fall_C->val[j] = litter_nonwood + litter_wood;  // Litter fall from vegetation pools to litter pools [gC m2-1 d-1]

    
    
    /* =============== Nitrogen simulation =============== */
    /* ======= For nitrogen: nitrogen addtion from vegetation to litter pools ======= */
    /* ================================================== */
    if (ctrl.opt_nitrogen_sim){
      // Nitrogen carbon ratio is constant in acid, ethanol, soluble, and nonsoluble wood litter pools, thus nitrogen addition does not need explicit calculation
      // Nitrogen carbon ratio is dynamic in four non-wood pools in the first layer, so we need to track fast_NP1_nonwood
      double soluble_DIN_NP1 = _no3_layer1->val[j] * _theta1->val[j] * depth1;
      double soluble_DIN_NP2 = _no3_layer2->val[j] * _theta2->val[j] * depth2;
      double soluble_DIN_NP3 = _no3_layer3->val[j] * _theta3->val[j] * depth3;


      double mineralisation_soil = 0.0; // Cumulative mineralisation of plant N to dissovled inorganic pools in soil
      double mineralisation_soil_each_layer = 0.0; // Mineralisation of plant N to dissovled inorganic pools in each layer

      // Non-wood pools in the first layer
      // Release of minteral N during distribution of non-woody vegetation pool to litter pools
      _plant_mobile_NP->val[j] += litter_nonwood * dpm_litter_ratio_nonwood * (par._NC_ratio_plant_green->val[j] - par._NC_ratio_dpm_litter->val[j]) + 
                                  litter_nonwood * (1 - dpm_litter_ratio_nonwood) * (par._NC_ratio_plant_green->val[j] - par._NC_ratio_rpm_litter->val[j]); // All excess N goes to plant mobile N pool
      
     
      // Wood pools in the first layer
      // No need to update nitrogen pools because all pools have consistent NC ratio as par._NC_ratio_rpm_litter->val[j]
      litter_wood_each_layer = litter_wood * froot_layer1;
      mineralisation_soil_each_layer = litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_rpm_litter->val[j]);  // Excess N goes to soil mobile N pool
      soluble_DIN_NP1 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;
      // Wood pools in the second layer
      // No need to update fast_NP1_wood because all wood pools have consistent NC ratio as par._NC_ratio_rpm_litter->val[j]; so we only need to track fast carbon pools
      litter_wood_each_layer = litter_wood * froot_layer2; 
      mineralisation_soil_each_layer = litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_rpm_litter->val[j]);  // Excess N goes to soil mobile N pool
      soluble_DIN_NP2 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;

      // Wood pools in the third layer
      // No need to update fast_NP1_wood because all wood pools have consistent NC ratio as par._NC_ratio_rpm_litter->val[j]; so we only need to track fast carbon pools
      litter_wood_each_layer = litter_wood * froot_layer3;
      mineralisation_soil_each_layer = litter_wood_each_layer * (par._NC_ratio_plant_wood->val[j] - par._NC_ratio_rpm_litter->val[j]);  // Excess N goes to soil mobile N pool
      soluble_DIN_NP3 += mineralisation_soil_each_layer;
      mineralisation_soil += mineralisation_soil_each_layer;
      
      // Update DON and DIN concentrations
      _no3_layer1->val[j] = soluble_DIN_NP1 / (_theta1->val[j] * depth1);
      _no3_layer2->val[j] = soluble_DIN_NP2 / (_theta2->val[j] * depth2);
      _no3_layer3->val[j] = soluble_DIN_NP3 / (_theta3->val[j] * depth3);
      _soil_minerl_N->val[j] += mineralisation_soil;
      
    }   // end if (ctrl.opt_nitrogen_sim)


  }  // end for (unsigned int j = 0; j < _sortedGrid.row.size(); j++)

    return EXIT_SUCCESS;
}

