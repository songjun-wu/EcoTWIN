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
    double fct_Ts, fct_theta1, fct_theta2, fct_theta3, fct_size, fct_depth_layer1, fct_depth_layer2, fct_depth_layer3, fdepth_decay_Exp; // factors for soil decomposition
    double C_from_humus, C_2_humus, C_2_humus_nonwood, C_2_humus_wood;
    double frac_soluble_CP_to_doc;

    // Factor of wood litter size for soil carbon decomposition (identical in all grid cells and all soil layers)
    fct_size = min(1.0, pow((1.0 + -1.71*WoodLitterSize + 0.86*pow(WoodLitterSize, 2)),-0.306));  // Factor of wood litter size for soil carbon decomposition

    // Varaibles for nitrogen simulation
    double NC_ratio_fast_pool_nonwood;
    double available_N;

    // Variables for DOC pool decomposition
    double ref_decomp_rate_doc;  // Reference decomposition rate of DOC pool [day-1]
    double delta_doc_layer1, delta_doc_layer2, delta_doc_layer3;
    double delta_no3_layer1, delta_no3_layer2, delta_no3_layer3;

    double C_trans_ratio_fast_2_humus, C_respiration_ratio_acid, C_respiration_ratio_soluble, C_respiration_ratio_ethanol, C_respiration_ratio_nonsoluble;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


      depth1 = _depth1->val[j];
      depth2 = _depth2->val[j];
      depth3 = par._depth3->val[j];
      theta1 = _theta1->val[j];
      theta2 = _theta2->val[j];
      theta3 = _theta3->val[j];
      fdepth_decay_Exp = par._fdepth_decay_Exp->val[j];

      // Factors of soil temperature; identical over whole soil profile
      fct_Ts = Temp_factor(Get_soil_temperature(atm._Ta->val[j], _LAI->val[j]), par._transformation_exp_base->val[j]);
      // Factors of soil depth; decay exponentially with depth
      fct_depth_layer1 =  exp(-fdepth_decay_Exp * depth1/2);
      fct_depth_layer2 =  exp(-fdepth_decay_Exp * (depth1+depth2/2));
      fct_depth_layer3 =  exp(-fdepth_decay_Exp * (depth1+depth2+depth3/2));

      // Sort out transformation ratios and respiration ratios
      C_trans_ratio_fast_2_humus = par._C_trans_ratio_fast_2_humus->val[j];
      C_respiration_ratio_acid = C_to_go_acid - C_trans_ratio_fast_2_humus;
      C_respiration_ratio_soluble = C_to_go_soluble - C_trans_ratio_fast_2_humus;
      C_respiration_ratio_ethanol = C_to_go_ethanol - C_trans_ratio_fast_2_humus;
      C_respiration_ratio_nonsoluble = C_to_go_nonsoluble - C_trans_ratio_fast_2_humus;

      
      /* ========================= Layer 1 ========================= */
      // Initialisation for layer 1
      double total_CP1_nonwood = _acid_CP1_nonwood->val[j] + _ethanol_CP1_nonwood->val[j] + _soluble_CP1_nonwood->val[j] + _nonsoluble_CP1_nonwood->val[j];
      fct_theta1 = Moist_factor(theta1, _thetaWP1->val[j], _thetaFC1->val[j], _thetaS1->val[j], depth1);
      
      

      // =============== Layer 1 (wood pool)  ===============
      available_N = _no3_layer1->val[j] * theta1 * depth1;
      Carbon_transformation_process_fast_pool(ctrl, atm, par, j,
                                    _acid_CP1_wood->val[j], _ethanol_CP1_wood->val[j], _soluble_CP1_wood->val[j], _nonsoluble_CP1_wood->val[j], _humus_CP1->val[j],
                                    _soil_respiration_C->val[j], C_2_humus_wood,
                                    available_N, _minerl_soil->val[j],
                                    fct_Ts, fct_theta1, fct_size, fct_depth_layer1, par._NC_ratio_fast_pool_wood->val[j],
                                    C_trans_ratio_fast_2_humus, C_respiration_ratio_acid, C_respiration_ratio_soluble, C_respiration_ratio_ethanol, C_respiration_ratio_nonsoluble);
      Carbon_transformation_process_humus_pool(ctrl, atm, par, j,
                                    _humus_CP1->val[j],
                                    _soil_respiration_C->val[j], C_from_humus,
                                    available_N, _minerl_soil->val[j], 
                                    fct_Ts, fct_theta1, fct_size, fct_depth_layer1);
    

      /* =============== Layer 1 (non-wood pool)  =============== */
      NC_ratio_fast_pool_nonwood = (total_CP1_nonwood > roundoffERR) ? _fast_NP1_nonwood->val[j] / total_CP1_nonwood : 1e3;  // Maximum NC ratio is 1e3
      Carbon_transformation_process_fast_pool(ctrl, atm, par, j,
                                    _acid_CP1_nonwood->val[j], _ethanol_CP1_nonwood->val[j], _soluble_CP1_nonwood->val[j], _nonsoluble_CP1_nonwood->val[j], _humus_CP1->val[j],
                                    _soil_respiration_C->val[j], C_2_humus_nonwood,
                                    available_N, _minerl_soil->val[j],
                                    fct_Ts, fct_theta1, 1.0, fct_depth_layer1, NC_ratio_fast_pool_nonwood,
                                    C_trans_ratio_fast_2_humus, C_respiration_ratio_acid, C_respiration_ratio_soluble, C_respiration_ratio_ethanol, C_respiration_ratio_nonsoluble);

      C_2_humus = C_2_humus_wood + C_2_humus_nonwood;
      _soil_decomposition_C->val[j] += C_from_humus - C_2_humus;

      // Update global nitrogen varaibles
      if (ctrl.opt_nitrogen_sim==1){
        _no3_layer1->val[j] = available_N / (theta1 * depth1);
      }

      


      /* ========================= Layer 2 ========================= */
      // Initialisation for layer 2
      fct_theta2 = Moist_factor(theta2, _thetaWP2->val[j], _thetaFC2->val[j], _thetaS2->val[j], depth2);
      // =============== Layer 2 (wood pool)  ===============
      available_N = _no3_layer2->val[j] * theta2 * depth2;
      Carbon_transformation_process_fast_pool(ctrl, atm, par, j,
                                    _acid_CP2_wood->val[j], _ethanol_CP2_wood->val[j], _soluble_CP2_wood->val[j], _nonsoluble_CP2_wood->val[j], _humus_CP2->val[j],
                                    _soil_respiration_C->val[j], C_2_humus,
                                    available_N, _minerl_soil->val[j],
                                    fct_Ts, fct_theta2, fct_size, fct_depth_layer2, par._NC_ratio_fast_pool_wood->val[j],
                                    C_trans_ratio_fast_2_humus, C_respiration_ratio_acid, C_respiration_ratio_soluble, C_respiration_ratio_ethanol, C_respiration_ratio_nonsoluble);
      Carbon_transformation_process_humus_pool(ctrl, atm, par, j,
                                    _humus_CP2->val[j],
                                    _soil_respiration_C->val[j], C_from_humus,
                                    available_N, _minerl_soil->val[j], 
                                    fct_Ts, fct_theta2, fct_size, fct_depth_layer2);
      _soil_decomposition_C->val[j] += C_from_humus - C_2_humus;
      // Update global nitrogen varaibles
      if (ctrl.opt_nitrogen_sim==1){
        _no3_layer2->val[j] = available_N / (theta2 * depth2);
      }


      /* ========================= Layer 3 ========================= */
      // Initialisation for layer 3
      fct_theta3 = Moist_factor(theta3, _thetaWP3->val[j], _thetaFC3->val[j], _thetaS3->val[j], depth3);
      
      // =============== Layer 3 (wood pool)  ===============
      available_N = _no3_layer3->val[j] * theta3 * depth3;
      Carbon_transformation_process_fast_pool(ctrl, atm, par, j,
                                    _acid_CP3_wood->val[j], _ethanol_CP3_wood->val[j], _soluble_CP3_wood->val[j], _nonsoluble_CP3_wood->val[j], _humus_CP3->val[j],
                                    _soil_respiration_C->val[j], C_2_humus,
                                    available_N, _minerl_soil->val[j],
                                    fct_Ts, fct_theta3, fct_size, fct_depth_layer3, par._NC_ratio_fast_pool_wood->val[j],
                                    C_trans_ratio_fast_2_humus, C_respiration_ratio_acid, C_respiration_ratio_soluble, C_respiration_ratio_ethanol, C_respiration_ratio_nonsoluble);
      Carbon_transformation_process_humus_pool(ctrl, atm, par, j,
                                    _humus_CP3->val[j],
                                    _soil_respiration_C->val[j], C_from_humus,
                                    available_N, _minerl_soil->val[j], 
                                    fct_Ts, fct_theta3, fct_size, fct_depth_layer3);
      _soil_decomposition_C->val[j] += C_from_humus - C_2_humus;
      // Update global nitrogen varaibles
      if (ctrl.opt_nitrogen_sim==1){
        _no3_layer3->val[j] = available_N / (theta3 * depth3);
      }


      // Dissolved organic carbon
      frac_soluble_CP_to_doc = Calculate_fraction_soluble_CP_to_DOC(_theta1->val[j]*depth1, _Perc1->val[j], par._ref_frac_soluble_to_doc->val[j]);
      _doc_layer1->val[j] += (_soluble_CP1_nonwood->val[j] + _soluble_CP1_wood->val[j]) * frac_soluble_CP_to_doc / (theta1 * depth1);
      _soluble_CP1_nonwood->val[j] *= (1 - frac_soluble_CP_to_doc);
      _soluble_CP1_wood->val[j] *= (1 - frac_soluble_CP_to_doc);

      frac_soluble_CP_to_doc = Calculate_fraction_soluble_CP_to_DOC(_theta2->val[j]*depth2, _Perc2->val[j], par._ref_frac_soluble_to_doc->val[j]);
      _doc_layer2->val[j] += _soluble_CP2_wood->val[j] * frac_soluble_CP_to_doc / (theta2 * depth2);
      _soluble_CP2_wood->val[j] *= (1 - frac_soluble_CP_to_doc);


      frac_soluble_CP_to_doc = Calculate_fraction_soluble_CP_to_DOC(_theta3->val[j]*depth3, _Perc3->val[j], par._ref_frac_soluble_to_doc->val[j]);
      _doc_layer3->val[j] += _soluble_CP3_wood->val[j] * frac_soluble_CP_to_doc / (theta3 * depth3);
      _soluble_CP3_wood->val[j] *= (1 - frac_soluble_CP_to_doc);

      // Decomposition of DOC pool
      ref_decomp_rate_doc = par._ref_decomp_rate_doc->val[j];
      delta_doc_layer1 = _doc_layer1->val[j] * ref_decomp_rate_doc * fct_Ts * fct_depth_layer1;
      delta_doc_layer2 = _doc_layer2->val[j] * ref_decomp_rate_doc * fct_Ts * fct_depth_layer2;
      delta_doc_layer3 = _doc_layer3->val[j] * ref_decomp_rate_doc * fct_Ts * fct_depth_layer3;
      _doc_layer1->val[j] -= delta_doc_layer1;
      _doc_layer2->val[j] -= delta_doc_layer2;
      _doc_layer3->val[j] -= delta_doc_layer3;

      if (ctrl.opt_nitrogen_sim==1){
        // The accompani organic nitrogen is mineralised and goes to DIN pool
        // Note that in EcoTWIN DOC only comes from dissolution of soluble DOC pool; therefore the CN ratio of DOC pool is identical to the CN ratio of fast pool
        delta_no3_layer1 = delta_doc_layer1 * (par._NC_ratio_fast_pool_wood->val[j] + NC_ratio_fast_pool_nonwood) / 2;
        delta_no3_layer2 = delta_doc_layer2 * par._NC_ratio_fast_pool_wood->val[j];
        delta_no3_layer3 = delta_doc_layer3 * par._NC_ratio_fast_pool_wood->val[j];
        _no3_layer1->val[j] += delta_no3_layer1;
        _no3_layer2->val[j] += delta_no3_layer2;
        _no3_layer3->val[j] += delta_no3_layer3;
        // Update total mineralization amount
        _minerl_soil->val[j] += delta_no3_layer1*theta1*depth1 + delta_no3_layer2*theta2*depth2 + delta_no3_layer3*theta3*depth3; 
      }



      // DOC composition is also considered as a part of soil respiration
      _soil_respiration_C->val[j] += delta_doc_layer1 * theta1 * depth1 + delta_doc_layer2 * theta2 * depth2 + delta_doc_layer3 * theta3 * depth3;




      
      // Update global nitrogen varaibles
      if (ctrl.opt_nitrogen_sim==1){
        // Transfromation does not change the NC ratio in nonwood pool
        _fast_NP1_nonwood->val[j] = NC_ratio_fast_pool_nonwood * (_acid_CP1_nonwood->val[j]+_ethanol_CP1_nonwood->val[j]+_soluble_CP1_nonwood->val[j]+_nonsoluble_CP1_nonwood->val[j]);
      }

    }  // End of grid loop

    return EXIT_SUCCESS;
}


double Basin::Calculate_fraction_soluble_CP_to_DOC(double soil_storage, double percolation, double ref_frac_soluble_to_doc){

  double min_residence_time = 1;
  double max_residence_time = 3000;
  double fct_residence_time;
  double residence_time;


  if (percolation < roundoffERR) {
    fct_residence_time = 1.0;
  } else {
    residence_time = soil_storage / percolation;

    

    if (residence_time < min_residence_time){
      fct_residence_time = 0.0;
    } else if (residence_time > max_residence_time){
      fct_residence_time = 1.0;
    } else {
      fct_residence_time = (residence_time - min_residence_time) / (max_residence_time - min_residence_time);
    }


    fct_residence_time = 0.2 + 0.8*fct_residence_time;

  }

  return ref_frac_soluble_to_doc * fct_residence_time;
}


int Basin::Carbon_transformation_process_humus_pool(  Control &ctrl, Atmosphere &atm, Param &par, int j,
                                          double &db_humus_CP,
                                          double &db_soil_respiration_C, double &db_C_from_humus,
                                          double &db_available_N, double &db_minerl_soil,
                                          double db_fct_Ts, double db_fct_theta, double db_fct_size, double fct_depth){

  double humus_CP = db_humus_CP;
  double C_from_humus;
  double minerl_soil;

  C_from_humus = humus_CP * (min(1.0, ref_decomp_rate_humus * par._decomposition_weight_humus_pool->val[j] * db_fct_Ts * db_fct_theta * fct_depth)); // Decomposition of humus is not limited by wood and litter size, as well as nutrients
  db_humus_CP -= C_from_humus;
  db_C_from_humus = C_from_humus;
  db_soil_respiration_C += C_from_humus;
  
  if (ctrl.opt_nitrogen_sim) {
  minerl_soil = C_from_humus * _humus_NC_ratio->val[j];
  // Respiration releases excess nitrogen to mineral nitrogen pool
  db_minerl_soil += minerl_soil;
  // Update available nitrogen pool
  db_available_N += minerl_soil;  
  }

  return EXIT_SUCCESS;
}



int Basin::Carbon_transformation_process_fast_pool(  Control &ctrl, Atmosphere &atm, Param &par, int j,
                                          double &db_acid_CP, double &db_ethanol_CP, double &db_soluble_CP, double &db_nonsoluble_CP, double &db_humus_CP,
                                          double &db_soil_respiration_C, double &db_C_2_humus,
                                          double &db_available_N, double &db_minerl_soil,
                                          double db_fct_Ts, double db_fct_theta, double db_fct_size, double fct_depth, double db_NC_ratio_fast,
                                          double db_C_trans_ratio_fast_2_humus, double db_C_respiration_ratio_acid, double db_C_respiration_ratio_soluble, double db_C_respiration_ratio_ethanol, double db_C_respiration_ratio_nonsoluble){

      double soluble_CP = db_soluble_CP;
      double acid_CP = db_acid_CP;      
      double ethanol_CP = db_ethanol_CP;
      double nonsoluble_CP = db_nonsoluble_CP;
      double humus_CP = db_humus_CP;
      double required_N;  // 
      double fct_N_limitation = 1.0;

      double C_from_acid, C_from_ethanol, C_from_nonsoluble, C_from_soluble;
      double C_2_acid, C_2_soluble, C_2_ethanol, C_2_nonsoluble, C_2_humus;
      double respiration_from_acid, respiration_from_soluble, respiration_from_ethanol, respiration_from_nonsoluble;

      double minerl_soil;  // Mineralization (nitrogen balance of DIN pool)


      // Potential decomposition without nitrogen limitation
      C_from_acid = acid_CP * (min(1.0, ref_decomp_rate_acid * par._decomposition_weight_fast_pool->val[j] * db_fct_Ts * db_fct_theta * db_fct_size * fct_depth));
      C_from_ethanol = ethanol_CP * (min(1.0, ref_decomp_rate_ethanol * par._decomposition_weight_fast_pool->val[j] * db_fct_Ts * db_fct_theta * db_fct_size * fct_depth));
      C_from_nonsoluble = nonsoluble_CP * (min(1.0, ref_decomp_rate_nonsoluble * par._decomposition_weight_fast_pool->val[j] * db_fct_Ts * db_fct_theta * db_fct_size * fct_depth));
      C_from_soluble = soluble_CP * (min(1.0, ref_decomp_rate_soluble * par._decomposition_weight_fast_pool->val[j] * db_fct_Ts * db_fct_theta * fct_depth)); // Decomposition of DOC is not limited by wood and litter size
      C_2_humus =(C_from_acid + C_from_ethanol + C_from_soluble + C_from_nonsoluble) * db_C_trans_ratio_fast_2_humus;

      /* =============== Nitrogen simulation =============== */
      // For carbon: transformation contrainted by nitrogen availability: building humus and transformation between soluble and other litter pools may consume nitrogen from mineral nitrogen pool (DIN) 
      // For nitrogen: transformations lead to nitrogen absortion or release
      if (ctrl.opt_nitrogen_sim) {
        // NC ratio between litter pools are identifcal
        // BUt NC ratio differs between litter pools and humus pools, litter pools and DOC pool
        respiration_from_acid = C_from_acid * db_C_respiration_ratio_acid;
        respiration_from_soluble = C_from_soluble * db_C_respiration_ratio_soluble;
        respiration_from_ethanol = C_from_ethanol * db_C_respiration_ratio_ethanol;
        respiration_from_nonsoluble = C_from_nonsoluble * db_C_respiration_ratio_nonsoluble;

        
       
        

        // Assumption: transformation does not change the NC ratio in targeted pool;
        // This is realised by absorbing or releasing nitrogen from/to mineral nitrogen pool (DIN)
        required_N =  -1 * (respiration_from_acid+respiration_from_ethanol+respiration_from_soluble+respiration_from_nonsoluble) * db_NC_ratio_fast +  // Respiration only generates CO2, thus leading to nitrogen excess
                       1 * C_2_humus * (_humus_NC_ratio->val[j] - db_NC_ratio_fast);    // Inbalance due to different NC ratios between fast and humus pools (fast pools to humus pool)

                       
        if ((required_N > db_available_N) && (required_N > roundoffERR)) {
          fct_N_limitation = db_available_N / required_N;
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
        minerl_soil = -1 * required_N * fct_N_limitation;  // Decomposition uptake might be negative under low humus generation yet intense soil resporation
        db_minerl_soil += minerl_soil;
        // Update available nitrogen pool
        db_available_N += minerl_soil;
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
      C_2_humus = (C_from_acid + C_from_ethanol + C_from_nonsoluble + C_from_soluble) * db_C_trans_ratio_fast_2_humus;

      // Soil respiration and soil decomposition
      db_soil_respiration_C += C_from_acid * db_C_respiration_ratio_acid + \
                          C_from_soluble * db_C_respiration_ratio_soluble + \
                          C_from_ethanol * db_C_respiration_ratio_ethanol + \
                          C_from_nonsoluble * db_C_respiration_ratio_nonsoluble;
      db_C_2_humus = C_2_humus;
      // Allocation carbon to pools
      db_acid_CP = acid_CP - C_from_acid + C_2_acid;
      db_ethanol_CP = ethanol_CP - C_from_ethanol + C_2_ethanol;
      db_soluble_CP = soluble_CP - C_from_soluble + C_2_soluble;
      db_nonsoluble_CP = nonsoluble_CP - C_from_nonsoluble + C_2_nonsoluble;
      db_humus_CP = humus_CP + C_2_humus;

      


      return EXIT_SUCCESS;
}