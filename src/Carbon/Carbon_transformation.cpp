/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_transformation.cpp
  * Created  on: 22.11.2025
  * Modified on: 26.11.2025
***************************************************************/


#include "Basin.h"

int Basin::Carbon_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double depth1, depth2, depth3;
    double theta1, theta2, theta3;
    double soluble_CP1_cumu, humus_CP1_cumu, acid_CP1_wood_nonwood_ratio;
    double acid_CP, ethanol_CP, nonsoluble_CP, soluble_CP, humus_CP;
    double respiration_from_acid, respiration_from_soluble, respiration_from_ethanol, respiration_from_nonsoluble, respiration_from_humus;  // Soil respiration from each pool
    double soil_respiration_C;  // Total soil respiration in carbon (gC/m2)
    double soil_decomposition_C;  // Total soil decomposition in carbon (gC/m2)

    double fct_Ts, fct_theta, fct_size, fct_N_limitation; // transformation factors
    double C_from_acid, C_from_ethanol, C_from_nonsoluble, C_from_soluble, C_from_humus; // Decomposition of carbon pools
    double C_2_acid, C_2_ethanol, C_2_nonsoluble, C_2_soluble, C_2_humus; // Gains of carbon pools

    fct_size = min(1.0, pow((1.0 + -1.71*WoodLitterSize + 0.86*pow(WoodLitterSize, 2)),-0.306));  // Factor of wood litter size for soil carbon decomposition

    // Varaibles for nitrogen simulation
    double NC_ratio_soluble, NC_ratio_fast, C_fast_2_humus, C_soluble_2_fast, C_soluble_2_humus;
    double N_balance_fast, N_balance_DON, required_N, available_N;
    double mineralisation_soil;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

      depth1 = _depth1->val[j];
      depth2 = _depth2->val[j];
      depth3 = par._depth3->val[j];
      theta1 = _theta1->val[j];
      theta2 = _theta2->val[j];
      theta3 = _theta3->val[j];
      // Factors of soil temperature; identical over whole soil profile
      fct_Ts = Temp_factor(Get_soil_temperature(atm._Ta->val[j], _LAI->val[j]));
      // Initialisation
      soluble_CP1_cumu = 0;
      humus_CP1_cumu = 0;
      soil_respiration_C = 0;
      soil_decomposition_C = 0;
           
      
      // ============== Layer 1 ==============
      double total_acid_CP1 = _acid_CP1_wood->val[j] + _acid_CP1_nonwood->val[j];
      acid_CP1_wood_nonwood_ratio = (total_acid_CP1 > roundoffERR) ? _acid_CP1_wood->val[j] / total_acid_CP1 : 0.5;
          
      fct_theta = Moist_factor(theta1, _thetaWP1->val[j], _thetaS1->val[j], depth1);
      
      /* ==================================================== */
      /* =============== Layer 1 (wood pool)  =============== */
      soluble_CP = _doc_layer1->val[j] * theta1 * depth1 * acid_CP1_wood_nonwood_ratio;
      humus_CP = _humus_CP1->val[j] * acid_CP1_wood_nonwood_ratio;
      acid_CP = _acid_CP1_wood->val[j];      
      ethanol_CP = _ethanol_CP1_wood->val[j];
      nonsoluble_CP = _nonsoluble_CP1_wood->val[j];

      
      // Potential decomposition without nitrogen limitation
      C_from_acid = acid_CP * (min(1.0, ref_decomp_rate_acid * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size));
      C_from_ethanol = ethanol_CP * (min(1.0, ref_decomp_rate_ethanol * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size));
      C_from_nonsoluble = nonsoluble_CP * (min(1.0, ref_decomp_rate_nonsoluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size));
      C_from_soluble = soluble_CP * (min(1.0, ref_decomp_rate_soluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta)); // Decomposition of DOC is not limited by wood and litter size
      C_from_humus = humus_CP * (min(1.0, ref_decomp_rate_humus * par._decomposition_weight_humus_pool->val[j] * fct_Ts * fct_theta)); // Decomposition of humus is not limited by wood and litter size, as well as nutrients

      /* =============== Nitrogen simulation =============== */
      // For carbon: transformation contrainted by nitrogen availability: building humus and transformation between soluble and other litter pools may consume nitrogen from mineral nitrogen pool (DIN) 
      // For nitrogen: transformations lead to nitrogen absortion or release
      if (ctrl.opt_nitrogen_sim) {
        // NC ratio between litter pools are identifcal
        // BUt NC ratio differs between litter pools and humus pools, litter pools and DOC pool
        respiration_from_acid = C_from_acid * C_respiration_ratio_acid;
        respiration_from_soluble = C_from_soluble * C_respiration_ratio_soluble;
        respiration_from_ethanol = C_from_ethanol * C_respiration_ratio_ethanol;
        respiration_from_nonsoluble = C_from_nonsoluble * C_respiration_ratio_nonsoluble;
        C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                          C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                          C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

        NC_ratio_soluble = (_doc_layer1->val[j] > roundoffERR) ? _don_layer1->val[j] / _doc_layer1->val[j] : 1e3;  // Maximum NC ratio is 1e3 
        NC_ratio_fast = par._NC_ratio_fast_pool_wood->val[j];  // The NC ratio of wood litter pools is consistent in all layers

        C_fast_2_humus =(C_from_acid + C_from_ethanol + C_from_nonsoluble) * C_trans_ratio_all_2_humus;
        C_soluble_2_fast = C_from_soluble * (C_trans_ratio_soluble_2_acid + C_trans_ratio_soluble_2_ethanol + C_trans_ratio_soluble_2_nonsoluble);
        C_soluble_2_humus = C_from_soluble * C_trans_ratio_all_2_humus;

        // Assumption: transformation does not change the NC ratio in targeted pool;
        // This is realised by absorbing or releasing nitrogen from/to mineral nitrogen pool (DIN)
        N_balance_fast = (respiration_from_acid+respiration_from_ethanol+respiration_from_nonsoluble) * NC_ratio_fast +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_2_soluble * (NC_ratio_fast - NC_ratio_soluble) +    // Inbalance due to different NC ratios between soluble and fast pools (fast pools to DON pool)
                                C_fast_2_humus * (NC_ratio_fast - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between fast and humus pools (fast pools to humus pool)

        N_balance_DON =  respiration_from_soluble * NC_ratio_soluble +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_soluble_2_fast * (NC_ratio_soluble - NC_ratio_fast) +  // Inbalance due to different NC ratios between soluble and fast pools (DON pool to fast pools)
                                C_soluble_2_humus * (NC_ratio_soluble - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between soluble and humus pools (DON pool to humus pool)
        // Required nitrogen for decomposition from DIN pool [gN/m2];
        // We also need to consider the nitrogen excess from respiration of humus pool
        required_N = - (N_balance_fast + N_balance_DON + C_from_humus*par._NC_ratio_humus_pool->val[j]);
        // Available nitrogen in DIN pool [gN/m2]
        available_N = _no3_layer1->val[j] * theta1 * depth1;

        
        if ((required_N > available_N) && (required_N > roundoffERR)) {
          fct_N_limitation = available_N / required_N;
        }  else {
          fct_N_limitation = 1.0;
        }


        // Update decomposition rates under nitrogen limitation
        C_from_acid = C_from_acid * fct_N_limitation;
        C_from_ethanol = C_from_ethanol * fct_N_limitation;
        C_from_nonsoluble = C_from_nonsoluble * fct_N_limitation;
        C_from_soluble = C_from_soluble * fct_N_limitation;
        // Here we only need to update dissolved inorganic nitrogen pool;
        // Because we assume that transformation does not change the NC ratio in targeted pool;
        mineralisation_soil = - required_N * fct_N_limitation;  // Decomposition uptake might be negative under low humus generation yet intense soil resporation
        _minerl_soil->val[j] += mineralisation_soil;
        _no3_layer1->val[j] = (available_N + mineralisation_soil) / (theta1 * depth1);
      }  // End of nitrogen simulation

      // Transformation
      C_2_acid        = C_from_ethanol      * C_trans_ratio_ethanol_2_acid + \
                        C_from_soluble      * C_trans_ratio_soluble_2_acid + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_acid;

      C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

      C_2_ethanol     = C_from_acid         * C_trans_ratio_acid_2_ethanol + \
                        C_from_soluble      * C_trans_ratio_soluble_2_ethanol + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_ethanol;

      C_2_nonsoluble  = C_from_acid         * C_trans_ratio_acid_2_nonsoluble  + \
                        C_from_soluble      * C_trans_ratio_soluble_2_nonsoluble  + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_nonsoluble ;
      C_2_humus = (C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble) * C_trans_ratio_all_2_humus;

      // Soil respiration and soil decomposition
      soil_respiration_C += C_from_acid * C_respiration_ratio_acid + \
                          C_from_soluble * C_respiration_ratio_soluble + \
                          C_from_ethanol * C_respiration_ratio_ethanol + \
                          C_from_nonsoluble * C_respiration_ratio_nonsoluble + \
                          C_from_humus;
      soil_decomposition_C += C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble + C_from_humus;
      // Allocation carbon to pools
      _acid_CP1_wood->val[j] = acid_CP - C_from_acid + C_2_acid;
      _ethanol_CP1_wood->val[j]  = ethanol_CP - C_from_ethanol + C_2_ethanol;
      _nonsoluble_CP1_wood->val[j] = nonsoluble_CP - C_from_nonsoluble + C_2_nonsoluble;
      soluble_CP1_cumu += soluble_CP - C_from_soluble + C_2_soluble;  // Sum over wood and nonwood pool in layer 1
      humus_CP1_cumu += humus_CP - C_from_humus + C_2_humus;  // Sum over wood and nonwood pool in layer 1

      


      
      /* ======================================================= */
      /* =============== Layer 1 (nonwood pool)  =============== */
      soluble_CP = _doc_layer1->val[j] * theta1 * depth1 * (1.0 - acid_CP1_wood_nonwood_ratio);
      humus_CP = _humus_CP1->val[j] * (1.0 - acid_CP1_wood_nonwood_ratio);
      acid_CP = _acid_CP1_nonwood->val[j];      
      ethanol_CP = _ethanol_CP1_nonwood->val[j];
      nonsoluble_CP = _nonsoluble_CP1_nonwood->val[j];
      // Decomposition
      C_from_acid = acid_CP * min(1.0, ref_decomp_rate_acid * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * 1.0 );  // Non-wood pools has minimal litter size of 1.0
      C_from_ethanol = ethanol_CP * min(1.0, ref_decomp_rate_ethanol * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * 1.0 );  // Non-wood pools has minimal litter size of 1.0
      C_from_nonsoluble = nonsoluble_CP * min(1.0, ref_decomp_rate_nonsoluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * 1.0 );  // Non-wood pools has minimal litter size of 1.0
      C_from_soluble = soluble_CP * min(1.0, ref_decomp_rate_soluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta ); // Decomposition of DOC is not limited by wood and litter size
      C_from_humus = humus_CP * min(1.0, ref_decomp_rate_humus * par._decomposition_weight_humus_pool->val[j] * fct_Ts * fct_theta ); // Decomposition of humus is not limited by wood and litter size, as well as nutrients

      /* =============== Nitrogen simulation =============== */
      // For carbon: transformation contrainted by nitrogen availability: building humus and transformation between soluble and other litter pools may consume nitrogen from mineral nitrogen pool (DIN) 
      // For nitrogen: transformations lead to nitrogen absortion or release
      if (ctrl.opt_nitrogen_sim) {

        // NC ratio between litter pools are identifcal
        // BUt NC ratio differs between litter pools and humus pools, litter pools and DOC pool
        respiration_from_acid = C_from_acid * C_respiration_ratio_acid;
        respiration_from_soluble = C_from_soluble * C_respiration_ratio_soluble;
        respiration_from_ethanol = C_from_ethanol * C_respiration_ratio_ethanol;
        respiration_from_nonsoluble = C_from_nonsoluble * C_respiration_ratio_nonsoluble;
        C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                          C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                          C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

        NC_ratio_soluble = (_doc_layer1->val[j] > roundoffERR) ? _don_layer1->val[j] / _doc_layer1->val[j] : 1e3;  // Maximum NC ratio is 1e3 
        NC_ratio_fast = ((acid_CP + ethanol_CP + nonsoluble_CP) > roundoffERR) ? _fast_NP1_nonwood->val[j] / (acid_CP + ethanol_CP + nonsoluble_CP) : 1e3;  // Maximum NC ratio is 1e3 

        C_fast_2_humus =(C_from_acid + C_from_ethanol + C_from_nonsoluble) * C_trans_ratio_all_2_humus;
        C_soluble_2_fast = C_from_soluble * (C_trans_ratio_soluble_2_acid + C_trans_ratio_soluble_2_ethanol + C_trans_ratio_soluble_2_nonsoluble);
        C_soluble_2_humus = C_from_soluble * C_trans_ratio_all_2_humus;

        // Assumption: transformation does not change the NC ratio in targeted pool;
        // This is realised by absorbing or releasing nitrogen from/to mineral nitrogen pool (DIN)
        N_balance_fast = (respiration_from_acid+respiration_from_ethanol+respiration_from_nonsoluble) * NC_ratio_fast +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_2_soluble * (NC_ratio_fast - NC_ratio_soluble) +    // Inbalance due to different NC ratios between soluble and fast pools
                                C_fast_2_humus * (NC_ratio_fast - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between fast and humus pools

        N_balance_DON =  respiration_from_soluble * NC_ratio_soluble +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_soluble_2_fast * (NC_ratio_soluble - NC_ratio_fast) +  // Inbalance due to different NC ratios between soluble and fast pools
                                C_soluble_2_humus * (NC_ratio_soluble - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between soluble and humus pools

        // Required nitrogen for decomposition from DIN pool [gN/m2];
        // We also need to consider the nitrogen excess from respiration of humus pool
        required_N = - (N_balance_fast + N_balance_DON + C_from_humus*par._NC_ratio_humus_pool->val[j]);
        // Available nitrogen in DIN pool [gN/m2]
        available_N = _no3_layer1->val[j] * theta1 * depth1;

        if ((required_N > available_N) && (required_N > roundoffERR)) {
          fct_N_limitation = available_N / required_N;
        }  else {
          fct_N_limitation = 1.0;
        }
        // Update decomposition rates under nitrogen limitation
        C_from_acid = C_from_acid * fct_N_limitation;
        C_from_ethanol = C_from_ethanol * fct_N_limitation;
        C_from_nonsoluble = C_from_nonsoluble * fct_N_limitation;
        C_from_soluble = C_from_soluble * fct_N_limitation;
        // Here we only need to update dissolved inorganic nitrogen pool;
        // Because we assume that transformation does not change the NC ratio in targeted pool;
        mineralisation_soil = - required_N * fct_N_limitation;  // Decomposition uptake might be negative under low humus generation yet intense soil resporation
        _minerl_soil->val[j] += mineralisation_soil;
        _no3_layer1->val[j] = (available_N + mineralisation_soil) / (theta1 * depth1);
      }  // End of nitrogen simulation

      // Transformation
      C_2_acid        = C_from_ethanol      * C_trans_ratio_ethanol_2_acid + \
                        C_from_soluble      * C_trans_ratio_soluble_2_acid + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_acid;

      C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

      C_2_ethanol     = C_from_acid         * C_trans_ratio_acid_2_ethanol + \
                        C_from_soluble      * C_trans_ratio_soluble_2_ethanol + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_ethanol;

      C_2_nonsoluble  = C_from_acid         * C_trans_ratio_acid_2_nonsoluble  + \
                        C_from_soluble      * C_trans_ratio_soluble_2_nonsoluble  + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_nonsoluble ;
      C_2_humus = (C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble) * C_trans_ratio_all_2_humus;

      // Soil respiration and soil decomposition
      soil_respiration_C += C_from_acid * C_respiration_ratio_acid + \
                          C_from_soluble * C_respiration_ratio_soluble + \
                          C_from_ethanol * C_respiration_ratio_ethanol + \
                          C_from_nonsoluble * C_respiration_ratio_nonsoluble + \
                          C_from_humus;
      soil_decomposition_C += C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble + C_from_humus;
      // Allocation carbon to pools
      _acid_CP1_nonwood->val[j] = acid_CP - C_from_acid + C_2_acid;
      _ethanol_CP1_nonwood->val[j]  = ethanol_CP - C_from_ethanol + C_2_ethanol;
      _nonsoluble_CP1_nonwood->val[j] = nonsoluble_CP - C_from_nonsoluble + C_2_nonsoluble;
      soluble_CP1_cumu += soluble_CP - C_from_soluble + C_2_soluble;  // Sum over wood and nonwood pool in layer 1
      humus_CP1_cumu += humus_CP - C_from_humus + C_2_humus;  // Sum over wood and nonwood pool in layer 1
      // Marge soluble and humus pool from wood and nonwood pools in layer 1
      _doc_layer1->val[j] = theta1>roundoffERR ? soluble_CP1_cumu / theta1 / depth1 : 0.0;
      _humus_CP1->val[j] = humus_CP1_cumu;

      // Update nitrogen pools
      if (ctrl.opt_nitrogen_sim) {
        // Based on the assumption that transformation does not change the NC ratio in targeted pool;
        _fast_NP1_nonwood->val[j] = (_acid_CP1_nonwood->val[j]+_ethanol_CP1_nonwood->val[j]+_nonsoluble_CP1_nonwood->val[j]) * NC_ratio_fast;
        _don_layer1->val[j] = _doc_layer1->val[j] * NC_ratio_soluble;

      }
      




      // ============== Layer 2 ==============
      fct_theta = Moist_factor(theta2, _thetaWP2->val[j], _thetaS2->val[j], depth2);
      fct_N_limitation = 1.0;
      soluble_CP = _doc_layer2->val[j] * theta2 * depth2;
      humus_CP = _humus_CP2->val[j];
      acid_CP = _acid_CP2_wood->val[j];      
      ethanol_CP = _ethanol_CP2_wood->val[j];
      nonsoluble_CP = _nonsoluble_CP2_wood->val[j];
      // Potential decomposition without nitrogen limitation
      C_from_acid = acid_CP * min(1.0, ref_decomp_rate_acid * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_ethanol = ethanol_CP * min(1.0, ref_decomp_rate_ethanol * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_nonsoluble = nonsoluble_CP * min(1.0, ref_decomp_rate_nonsoluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_soluble = soluble_CP * min(1.0, ref_decomp_rate_soluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta); // Decomposition of DOC is not limited by wood and litter size
      C_from_humus = humus_CP * min(1.0, ref_decomp_rate_humus * par._decomposition_weight_humus_pool->val[j] * fct_Ts * fct_theta); // Decomposition of humus is not limited by wood and litter size, as well as nutrients

      /* =============== Nitrogen simulation =============== */
      // For carbon: transformation contrainted by nitrogen availability: building humus and transformation between soluble and other litter pools may consume nitrogen from mineral nitrogen pool (DIN) 
      // For nitrogen: transformations lead to nitrogen absortion or release
      if (ctrl.opt_nitrogen_sim) {
        // NC ratio between litter pools are identifcal
        // BUt NC ratio differs between litter pools and humus pools, litter pools and DOC pool
        respiration_from_acid = C_from_acid * C_respiration_ratio_acid;
        respiration_from_soluble = C_from_soluble * C_respiration_ratio_soluble;
        respiration_from_ethanol = C_from_ethanol * C_respiration_ratio_ethanol;
        respiration_from_nonsoluble = C_from_nonsoluble * C_respiration_ratio_nonsoluble;
        C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                          C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                          C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

        NC_ratio_soluble = (_doc_layer2->val[j] > roundoffERR) ? _don_layer2->val[j] / _doc_layer2->val[j] : 1e3;  // Maximum NC ratio is 1e3 
        NC_ratio_fast = par._NC_ratio_fast_pool_wood->val[j];

        C_fast_2_humus =(C_from_acid + C_from_ethanol + C_from_nonsoluble) * C_trans_ratio_all_2_humus;
        C_soluble_2_fast = C_from_soluble * (C_trans_ratio_soluble_2_acid + C_trans_ratio_soluble_2_ethanol + C_trans_ratio_soluble_2_nonsoluble);
        C_soluble_2_humus = C_from_soluble * C_trans_ratio_all_2_humus;

        // Assumption: transformation does not change the NC ratio in targeted pool;
        // This is realised by absorbing or releasing nitrogen from/to mineral nitrogen pool (DIN)
        N_balance_fast = (respiration_from_acid+respiration_from_ethanol+respiration_from_nonsoluble) * NC_ratio_fast +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_2_soluble * (NC_ratio_fast - NC_ratio_soluble) +    // Inbalance due to different NC ratios between soluble and fast pools
                                C_fast_2_humus * (NC_ratio_fast - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between fast and humus pools

        N_balance_DON =  respiration_from_soluble * NC_ratio_soluble +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_soluble_2_fast * (NC_ratio_soluble - NC_ratio_fast) +  // Inbalance due to different NC ratios between soluble and fast pools
                                C_soluble_2_humus * (NC_ratio_soluble - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between soluble and humus pools

        // Required nitrogen for decomposition from DIN pool [gN/m2];
        // We also need to consider the nitrogen excess from respiration of humus pool
        required_N = - (N_balance_fast + N_balance_DON + C_from_humus*par._NC_ratio_humus_pool->val[j]);
        // Available nitrogen in DIN pool [gN/m2]
        available_N = _no3_layer2->val[j] * theta2 * depth2;

        if ((required_N > available_N) && (required_N > roundoffERR)) {
          fct_N_limitation = available_N / required_N;
        }  else {
          fct_N_limitation = 1.0;
        }
        // Update decomposition rates under nitrogen limitation
        C_from_acid = C_from_acid * fct_N_limitation;
        C_from_ethanol = C_from_ethanol * fct_N_limitation;
        C_from_nonsoluble = C_from_nonsoluble * fct_N_limitation;
        C_from_soluble = C_from_soluble * fct_N_limitation;
        // Here we only need to update dissolved inorganic nitrogen pool;
        // Because we assume that transformation does not change the NC ratio in targeted pool;
        mineralisation_soil = - required_N * fct_N_limitation;  // Decomposition uptake might be negative under low humus generation yet intense soil resporation
        _minerl_soil->val[j] += mineralisation_soil;
        _no3_layer2->val[j] = (available_N + mineralisation_soil) / (theta2 * depth2);
      }  // End of nitrogen simulation

      // Transformation
      C_2_acid        = C_from_ethanol      * C_trans_ratio_ethanol_2_acid + \
                        C_from_soluble      * C_trans_ratio_soluble_2_acid + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_acid;

      C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

      C_2_ethanol     = C_from_acid         * C_trans_ratio_acid_2_ethanol + \
                        C_from_soluble      * C_trans_ratio_soluble_2_ethanol + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_ethanol;

      C_2_nonsoluble  = C_from_acid         * C_trans_ratio_acid_2_nonsoluble  + \
                        C_from_soluble      * C_trans_ratio_soluble_2_nonsoluble  + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_nonsoluble ;
      C_2_humus = (C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble) * C_trans_ratio_all_2_humus;

      // Soil respiration and soil decomposition
      soil_respiration_C += C_from_acid * C_respiration_ratio_acid + \
                          C_from_soluble * C_respiration_ratio_soluble + \
                          C_from_ethanol * C_respiration_ratio_ethanol + \
                          C_from_nonsoluble * C_respiration_ratio_nonsoluble + \
                          C_from_humus;
      soil_decomposition_C += C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble + C_from_humus;
      // Allocation carbon to pools
      _acid_CP2_wood->val[j] = acid_CP - C_from_acid + C_2_acid;
      _ethanol_CP2_wood->val[j]  = ethanol_CP - C_from_ethanol + C_2_ethanol;
      _nonsoluble_CP2_wood->val[j] = nonsoluble_CP - C_from_nonsoluble + C_2_nonsoluble;
      _doc_layer2->val[j] = theta2 > roundoffERR ? (soluble_CP - C_from_soluble + C_2_soluble) / theta2 / depth2 : 0.0;
      _humus_CP2->val[j] = humus_CP - C_from_humus + C_2_humus;

      // Update nitrogen pools
      if (ctrl.opt_nitrogen_sim) {
        // Based on the assumption that transformation does not change the NC ratio in targeted pool;
        _don_layer2->val[j] = _doc_layer2->val[j] * NC_ratio_soluble;
      }





      // ============== Layer 3 ==============
      fct_theta = Moist_factor(theta3, _thetaWP3->val[j], _thetaS3->val[j], depth3);
      fct_N_limitation = 1.0;
      soluble_CP = _doc_layer3->val[j] * theta3 * depth3;
      humus_CP = _humus_CP3->val[j];
      acid_CP = _acid_CP3_wood->val[j];      
      ethanol_CP = _ethanol_CP3_wood->val[j];
      nonsoluble_CP = _nonsoluble_CP3_wood->val[j];
      // Decomposition
      C_from_acid = acid_CP * min(1.0, ref_decomp_rate_acid * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_ethanol = ethanol_CP * min(1.0, ref_decomp_rate_ethanol * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_nonsoluble = nonsoluble_CP * min(1.0, ref_decomp_rate_nonsoluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta * fct_size);
      C_from_soluble = soluble_CP * min(1.0, ref_decomp_rate_soluble * par._decomposition_weight_fast_pool->val[j] * fct_Ts * fct_theta); // Decomposition of DOC is not limited by wood and litter size
      C_from_humus = humus_CP * min(1.0, ref_decomp_rate_humus * par._decomposition_weight_humus_pool->val[j] * fct_Ts * fct_theta); // Decomposition of humus is not limited by wood and litter size, as well as nutrients

      /* =============== Nitrogen simulation =============== */
      // For carbon: transformation contrainted by nitrogen availability: building humus and transformation between soluble and other litter pools may consume nitrogen from mineral nitrogen pool (DIN) 
      // For nitrogen: transformations lead to nitrogen absortion or release
      if (ctrl.opt_nitrogen_sim) {
        // NC ratio between litter pools are identifcal
        // BUt NC ratio differs between litter pools and humus pools, litter pools and DOC pool
        respiration_from_acid = C_from_acid * C_respiration_ratio_acid;
        respiration_from_soluble = C_from_soluble * C_respiration_ratio_soluble;
        respiration_from_ethanol = C_from_ethanol * C_respiration_ratio_ethanol;
        respiration_from_nonsoluble = C_from_nonsoluble * C_respiration_ratio_nonsoluble;
        C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                          C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                          C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

        NC_ratio_soluble = (_doc_layer3->val[j] > roundoffERR) ? _don_layer3->val[j] / _doc_layer3->val[j] : 1e3;  // Maximum NC ratio is 1e3 
        NC_ratio_fast = par._NC_ratio_fast_pool_wood->val[j];

        C_fast_2_humus =(C_from_acid + C_from_ethanol + C_from_nonsoluble) * C_trans_ratio_all_2_humus;
        C_soluble_2_fast = C_from_soluble * (C_trans_ratio_soluble_2_acid + C_trans_ratio_soluble_2_ethanol + C_trans_ratio_soluble_2_nonsoluble);
        C_soluble_2_humus = C_from_soluble * C_trans_ratio_all_2_humus;

        // Assumption: transformation does not change the NC ratio in targeted pool;
        // This is realised by absorbing or releasing nitrogen from/to mineral nitrogen pool (DIN)
        N_balance_fast = (respiration_from_acid+respiration_from_ethanol+respiration_from_nonsoluble) * NC_ratio_fast +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_2_soluble * (NC_ratio_fast - NC_ratio_soluble) +    // Inbalance due to different NC ratios between soluble and fast pools
                                C_fast_2_humus * (NC_ratio_fast - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between fast and humus pools

        N_balance_DON =  respiration_from_soluble * NC_ratio_soluble +  // Respiration only generates CO2, thus leading to nitrogen excess
                                C_soluble_2_fast * (NC_ratio_soluble - NC_ratio_fast) +  // Inbalance due to different NC ratios between soluble and fast pools
                                C_soluble_2_humus * (NC_ratio_soluble - par._NC_ratio_humus_pool->val[j]);    // Inbalance due to different NC ratios between soluble and humus pools

        // Required nitrogen for decomposition from DIN pool [gN/m2];
        // We also need to consider the nitrogen excess from respiration of humus pool
        required_N = - (N_balance_fast + N_balance_DON + C_from_humus*par._NC_ratio_humus_pool->val[j]);
        // Available nitrogen in DIN pool [gN/m2]
        available_N = _no3_layer3->val[j] * theta3 * depth3;

        if ((required_N > available_N) && (required_N > roundoffERR)) {
          fct_N_limitation = available_N / required_N;
        }  else {
          fct_N_limitation = 1.0;
        }
        // Update decomposition rates under nitrogen limitation
        C_from_acid = C_from_acid * fct_N_limitation;
        C_from_ethanol = C_from_ethanol * fct_N_limitation;
        C_from_nonsoluble = C_from_nonsoluble * fct_N_limitation;
        C_from_soluble = C_from_soluble * fct_N_limitation;
        // Here we only need to update dissolved inorganic nitrogen pool;
        // Because we assume that transformation does not change the NC ratio in targeted pool;
        mineralisation_soil = - required_N * fct_N_limitation;  // Decomposition uptake might be negative under low humus generation yet intense soil resporation
        _minerl_soil->val[j] += mineralisation_soil;
        _no3_layer3->val[j] = (available_N + mineralisation_soil) / (theta3 * depth3);

      }  // End of nitrogen simulation

      // Transformation
      C_2_acid        = C_from_ethanol      * C_trans_ratio_ethanol_2_acid + \
                        C_from_soluble      * C_trans_ratio_soluble_2_acid + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_acid;

      C_2_soluble     = C_from_acid         * C_trans_ratio_acid_2_soluble + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_soluble + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_soluble;

      C_2_ethanol     = C_from_acid         * C_trans_ratio_acid_2_ethanol + \
                        C_from_soluble      * C_trans_ratio_soluble_2_ethanol + \
                        C_from_nonsoluble   * C_trans_ratio_nonsoluble_2_ethanol;

      C_2_nonsoluble  = C_from_acid         * C_trans_ratio_acid_2_nonsoluble  + \
                        C_from_soluble      * C_trans_ratio_soluble_2_nonsoluble  + \
                        C_from_ethanol      * C_trans_ratio_ethanol_2_nonsoluble ;
      C_2_humus = (C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble) * C_trans_ratio_all_2_humus;

      // Soil respiration and soil decomposition
      soil_respiration_C += C_from_acid * C_respiration_ratio_acid + \
                          C_from_soluble * C_respiration_ratio_soluble + \
                          C_from_ethanol * C_respiration_ratio_ethanol + \
                          C_from_nonsoluble * C_respiration_ratio_nonsoluble + \
                          C_from_humus;
      soil_decomposition_C += C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble + C_from_humus;
      // Allocation carbon to pools
      _acid_CP3_wood->val[j] = acid_CP - C_from_acid + C_2_acid;
      _ethanol_CP3_wood->val[j]  = ethanol_CP - C_from_ethanol + C_2_ethanol;
      _nonsoluble_CP3_wood->val[j] = nonsoluble_CP - C_from_nonsoluble + C_2_nonsoluble;
      _doc_layer3->val[j] = theta3 > roundoffERR ? (soluble_CP - C_from_soluble + C_2_soluble) / theta3 / depth3 : 0.0;
      _humus_CP3->val[j] = humus_CP - C_from_humus + C_2_humus;



      // Update soil respiration and soil decomposition from all soil layers
      _soil_respiration_C->val[j] = soil_respiration_C;
      _soil_decomposition_C->val[j] = soil_decomposition_C;
      }

    return EXIT_SUCCESS;
}