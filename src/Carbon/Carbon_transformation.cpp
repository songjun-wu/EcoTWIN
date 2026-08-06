/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
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
    double fct_Ts, fct_theta1, fct_theta2, fct_theta3, fct_depth_layer1, fct_depth_layer2, fct_depth_layer3, fdepth_decay_Exp; // factors for soil decomposition

    // Varaibles for nitrogen simulation
    double ref_decomp_rate_doc;  // Reference decomposition rate of DOC pool [day-1]
    double delta_doc_layer1, delta_doc_layer2, delta_doc_layer3;



    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


      depth1 = _depth1->val[j];
      depth2 = _depth2->val[j];
      depth3 = par._depth3->val[j];
      theta1 = _theta1->val[j];
      theta2 = _theta2->val[j];
      theta3 = _theta3->val[j];
      fdepth_decay_Exp = par._fdepth_decay_Exp->val[j];

      


      // Assign local variables for carbon transformation
      double DIN_pool_layer1 = _no3_layer1->val[j] * theta1 * depth1;
      double DIN_pool_layer2 = _no3_layer2->val[j] * theta2 * depth2;
      double DIN_pool_layer3 = _no3_layer3->val[j] * theta3 * depth3;
      double DOC_pool_layer1 = _doc_layer1->val[j] * theta1 * depth1;
      double DOC_pool_layer2 = _doc_layer2->val[j] * theta2 * depth2;
      double DOC_pool_layer3 = _doc_layer3->val[j] * theta3 * depth3;
      double soluble_CP1 = _soluble_CP1->val[j];
      double soluble_CP2 = _soluble_CP2->val[j];
      double soluble_CP3 = _soluble_CP3->val[j];

      // Calculate environmental factors for carbon decomposition
      // Factors of soil temperature; identical over whole soil profile
      fct_Ts = Temp_factor(Get_soil_temperature(atm._Ta->val[j], _LAI->val[j]));
      // Factors of soil depth; decay exponentially with depth
      fct_depth_layer1 =  exp(-fdepth_decay_Exp * depth1/2);
      fct_depth_layer2 =  exp(-fdepth_decay_Exp * (depth1+depth2/2));
      fct_depth_layer3 =  exp(-fdepth_decay_Exp * (depth1+depth2+depth3/2));
      // Factors of soil moisture
      fct_theta1 = Moist_factor(theta1, _thetaWP1->val[j], _thetaFC1->val[j], _thetaS1->val[j], depth1); // Soil moisture factor for layer 1
      fct_theta2 = Moist_factor(theta2, _thetaWP2->val[j], _thetaFC2->val[j], _thetaS2->val[j], depth2); // Soil moisture factor for layer 2
      fct_theta3 = Moist_factor(theta3, _thetaWP3->val[j], _thetaFC3->val[j], _thetaS3->val[j], depth3); // Soil moisture factor for layer 3

      

      // Carbon decomposition
      // Layer 1
      Carbon_decomposition_process(ctrl, atm, par, j,
                                    _dpm_litter_CP1->val[j], _rpm_litter_CP1->val[j], _bio_CP1->val[j], _humus_CP1->val[j],
                                    soluble_CP1, _soil_decomposition_C->val[j], _co2_emission_C->val[j],
                                    DIN_pool_layer1, _soil_minerl_N->val[j],
                                    fct_Ts, fct_theta1, fct_depth_layer1);
      // Layer 2
      Carbon_decomposition_process(ctrl, atm, par, j,
                                    _dpm_litter_CP2->val[j], _rpm_litter_CP2->val[j], _bio_CP2->val[j], _humus_CP2->val[j],
                                    soluble_CP2, _soil_decomposition_C->val[j], _co2_emission_C->val[j],
                                    DIN_pool_layer2, _soil_minerl_N->val[j],
                                    fct_Ts, fct_theta2, fct_depth_layer2);
      // Layer 3
      Carbon_decomposition_process(ctrl, atm, par, j,
                                    _dpm_litter_CP3->val[j], _rpm_litter_CP3->val[j], _bio_CP3->val[j], _humus_CP3->val[j],
                                    soluble_CP3, _soil_decomposition_C->val[j], _co2_emission_C->val[j],
                                    DIN_pool_layer3, _soil_minerl_N->val[j],
                                    fct_Ts, fct_theta3, fct_depth_layer3);
      
      
      // Mobilisation of bounded DOC to mobile DOC
      // First calculate the groundwater table depth
      double excess_soil_water, groundwater_table, fct_groundwater_depth, DOC_mobilisation, ref_frac_soluble_to_doc;
      excess_soil_water = max(0.0, theta1 - _thetaFC1->val[j]) / (_thetaS1->val[j] - _thetaFC1->val[j]) * depth1 + 
                          max(0.0, theta2 - _thetaFC2->val[j]) / (_thetaS2->val[j] - _thetaFC2->val[j]) * depth2 + 
                          max(0.0, theta3 - _thetaFC3->val[j]) / (_thetaS3->val[j] - _thetaFC3->val[j]) * depth3;
      groundwater_table = _initial_groundwater_table->val[j] - excess_soil_water;   // Groundwater table depth [m]
      if (groundwater_table < roundoffERR) groundwater_table = 0;
      // Calculate the factor of groundwater depth
      fct_groundwater_depth = exp(-par._f_groundwater_depth_decay_exp_base->val[j] * sqrt(groundwater_table));
      // Mobilisation of bounded DOC to mobile DOC
      ref_frac_soluble_to_doc = par._ref_frac_soluble_to_doc->val[j];
      DOC_mobilisation = soluble_CP1 * ref_frac_soluble_to_doc * fct_groundwater_depth;
      DOC_pool_layer1 += DOC_mobilisation;
      soluble_CP1 -= DOC_mobilisation;
      DOC_mobilisation = soluble_CP2 * ref_frac_soluble_to_doc * fct_groundwater_depth;
      DOC_pool_layer2 += DOC_mobilisation;
      soluble_CP2 -= DOC_mobilisation;
      DOC_mobilisation = soluble_CP3 * ref_frac_soluble_to_doc * fct_groundwater_depth;
      DOC_pool_layer3 += DOC_mobilisation;
      soluble_CP3 -= DOC_mobilisation;





      // Decomposition of DOC pool
      
      // Nitrogen has been released to mineral pool during DOC production. Therefore, no nitrogen is released during DOC decomposition
      ref_decomp_rate_doc = par._ref_decomp_rate_doc->val[j];
      delta_doc_layer1 = soluble_CP1 * ref_decomp_rate_doc * fct_depth_layer1;
      delta_doc_layer2 = soluble_CP2 * ref_decomp_rate_doc * fct_depth_layer2;
      delta_doc_layer3 = soluble_CP3 * ref_decomp_rate_doc * fct_depth_layer3;
      soluble_CP1 -= delta_doc_layer1;
      soluble_CP2 -= delta_doc_layer2;
      soluble_CP3 -= delta_doc_layer3;

      // DOC decomposition is also considered as a part of soil respiration
      _co2_emission_C->val[j] += delta_doc_layer1 + delta_doc_layer2 + delta_doc_layer3;
      


      // Update DOC and DIN concentration
      _soluble_CP1->val[j] = soluble_CP1;
      _soluble_CP2->val[j] = soluble_CP2;
      _soluble_CP3->val[j] = soluble_CP3;
      _doc_layer1->val[j] = DOC_pool_layer1 / (theta1 * depth1);
      _doc_layer2->val[j] = DOC_pool_layer2 / (theta2 * depth2);
      _doc_layer3->val[j] = DOC_pool_layer3 / (theta3 * depth3);
      _no3_layer1->val[j] = DIN_pool_layer1 / (theta1 * depth1);
      _no3_layer2->val[j] = DIN_pool_layer2 / (theta2 * depth2);
      _no3_layer3->val[j] = DIN_pool_layer3 / (theta3 * depth3);
  }

  return EXIT_SUCCESS;
}



int Basin::Carbon_decomposition_process( Control &ctrl, Atmosphere &atm, Param &par, int j,
                                            double &db_dpm_litter_CP, double &db_rpm_litter_CP, double &db_bio_CP, double &db_humus_CP,
                                            double &db_DOC_pool, double &db_soil_decomposition_C, double &db_co2_emission,
                                            double &db_DIN_pool, double &db_soil_minerl_N,
                                            double db_fct_Ts, double db_fct_theta, double fct_depth){
                                            
    double decomposition_total, decomposition_from_dpm_litter_CP, decomposition_from_rpm_litter_CP, decomposition_from_bio_CP, decomposition_from_humus_CP;
    double fct_N_limitation = 1.0;
    double frac_DOC_production_from_litter_CP = par._frac_DOC_production_from_litter_CP->val[j];
    double frac_DOC_production_from_soil_CP = par._frac_DOC_production_from_soil_CP->val[j];

    double Cflux_to_DOC_pool;
    double Nflux_litter, Nflux_soil, Nflux_balance;

    double beta = 0.2;  // todo; carbon retention fraction

    double env_factors = db_fct_Ts * db_fct_theta * fct_depth;

    // Calculate the potential decomposition rates of carbon pools
    decomposition_from_dpm_litter_CP = db_dpm_litter_CP * ref_decomp_rate_dpm_litter_CP * env_factors;
    decomposition_from_rpm_litter_CP = db_rpm_litter_CP * ref_decomp_rate_rpm_litter_CP * env_factors;
    decomposition_from_bio_CP = db_bio_CP * ref_decomp_rate_bio_CP * env_factors;
    decomposition_from_humus_CP = db_humus_CP * ref_decomp_rate_humus_CP * env_factors;
    
    
    // ============================ Nitrogen limitation ============================
    if (ctrl.opt_nitrogen_sim){
      // Decomposition from litter pools might be limited by nitrogen availability as CN ratio is higher in plant and litter pools than the soil organic pools
      // Required N for building soil organic carbon from litter pools
      // Here we assume that the accompained N will be mineralised to DIN when organic carbon is respired as CO2 or decomposed into DOC
      //Nflux_litter =  -1 *decomposition_from_dpm_litter_CP * beta * (_NC_ratio_soil_pool->val[j] - par._NC_ratio_dpm_litter->val[j]) +  // N absorption when building soil organic carbon from dpm litter pools
      //                -1 * decomposition_from_rpm_litter_CP * beta * (_NC_ratio_soil_pool->val[j] - par._NC_ratio_rpm_litter->val[j]) +  // N absorption when building soil organic carbon from rpm litter pools
      //                decomposition_from_dpm_litter_CP *  (1 - beta) * par._NC_ratio_dpm_litter->val[j]  + //  N release during respiration of dpm litter pools
      //               decomposition_from_rpm_litter_CP *  (1 - beta) * par._NC_ratio_rpm_litter->val[j]; //  N release during respiration of rpm litter pools
      // The formula can be simplified as:
      Nflux_litter =  decomposition_from_dpm_litter_CP * (par._NC_ratio_dpm_litter->val[j] - beta * _NC_ratio_soil_pool->val[j]) +
                      decomposition_from_rpm_litter_CP * (par._NC_ratio_rpm_litter->val[j] - beta * _NC_ratio_soil_pool->val[j]);
      
      // Released N from soil respiration via CO2 emission and DOC production)
      Nflux_soil =    (decomposition_from_bio_CP + decomposition_from_humus_CP) *  (1 - beta) * _NC_ratio_soil_pool->val[j]; // N release during respiration of soil organic pools
                        
      Nflux_balance = Nflux_litter + Nflux_soil;  // N balance during decomposition (absorption of N by building soil organic carbon / release of N during respiration)
          
      if (db_DIN_pool + Nflux_balance < 0) {
        fct_N_limitation = - (db_DIN_pool + Nflux_soil) / Nflux_litter;
        Nflux_balance = - db_DIN_pool;
      } else {
        fct_N_limitation = 1.0;
      }
      // Update decomposition rates under nitrogen limitation
      decomposition_from_dpm_litter_CP *= fct_N_limitation;
      decomposition_from_rpm_litter_CP *= fct_N_limitation;
      db_soil_minerl_N += Nflux_balance;
      db_DIN_pool += Nflux_balance;

      
    }

    


  
    // Summary the total decomposition
    decomposition_total = decomposition_from_dpm_litter_CP + decomposition_from_rpm_litter_CP + decomposition_from_bio_CP + decomposition_from_humus_CP;


    // Update carbon pools    
    // Litter pools
    db_dpm_litter_CP -= decomposition_from_dpm_litter_CP;
    db_rpm_litter_CP -= decomposition_from_rpm_litter_CP;
    // Soil pools
    db_bio_CP -= decomposition_from_bio_CP - decomposition_total * beta * 0.46;
    db_humus_CP -= decomposition_from_humus_CP - decomposition_total * beta * 0.54;

    // Update carbon fluxes
    // DOC pools and CO2 emission
    Cflux_to_DOC_pool = (decomposition_from_dpm_litter_CP + decomposition_from_rpm_litter_CP) * (1 - beta) * frac_DOC_production_from_litter_CP +
                        (decomposition_from_bio_CP + decomposition_from_humus_CP) * (1 - beta) * frac_DOC_production_from_soil_CP;
    db_DOC_pool += Cflux_to_DOC_pool;
    db_co2_emission += decomposition_total * (1 - beta) - Cflux_to_DOC_pool;
    // Total decomposition
    db_soil_decomposition_C += decomposition_total;


    return EXIT_SUCCESS;

}

