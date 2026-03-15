/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Basin.h
  * Created  on: 30.02.2025
  * Modified on: 23.11.2025
***************************************************************/


#ifndef BASIN_H_
#define BASIN_H_

#include "Param.h"
#include "Atmosphere.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Basin {
  /* Properties */
  double roundoffERR;
  int _rowNum, _colNum;
  double _dx, _nodata;
  int num_landuse;        // The number of land use types
  vector<int> landuse_idx;  // The location of each land use type in param.ini or N_addition.ini
  sortedGrid _sortedGrid; 
  /* end of Properties */

  public:
  /* GIS */
  svector *_chnwidth;  // Channel width [m]
  svector *_chndepth;  // Channel depth [m]
  svector *_chnlength;  // Channel length [m]
  svector *_slope;  // Slope [m/m]
  svector *_depth1;  // Depth of soil layer 1 [m]
  svector *_depth2;  // Depth of soil layer 2 [m]
  svector *_sand1;  // Sand content of layer 1 [decimal]
  svector *_clay1;  // Clay content of layer 1 [decimal]
  svector *_organic1;  // Organic content of layer 1 [decimal]
  svector *_bulkdensity1;  // Bulk density of layer 1 [g/cm3]
  svector *_drainage_depth;  // The depth of drainage [m]
  svector *_sand2;  // Sand content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_sand3;  // Sand content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_clay2;  // Clay content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_clay3;  // Clay content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_silt2;  // Silt content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_silt3;  // Silt content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_organic2;  // Organic content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_organic3;  // Organic content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_bulkdensity2;  // Bulk density of layer 2 [g/cm3], only needed when opt_depthprofile = 3
  svector *_bulkdensity3;  // Bulk density of layer 3 [g/cm3], only needed when opt_depthprofile = 3
  svector *_silt1;  // Silt content of layer 1 [decimal], only needed when opt_pedotransf = 1 or 2
  svector *_no3_rain;  // The nitrate concentration in rain water [mgN/L], only needed when nitrogen_sim_1 = 1
  svector *_N_fertilization;  // The fertilization amount [g/m2], only needed when opt_fert_input = 1
  /* end of GIS */

  /* GroundTs */
  svector *_LAI;  // Leaf area index [-]
  ifstream if__LAI;  // Leaf area index [-]
  /* end of GroundTs */

  /* ManagementTs */
  /* end of ManagementTs */

  /* Storages */ 
  svector *_I;  // Canopy storage [m]
  svector *_snow;  // Snow depth in [m]
  svector *_pond;  // Ponding water in [m]
  svector *_theta1;  // Soil moisture in layer 1 [decimal]
  svector *_theta2;  // Soil moisture in layer 2 [decimal]
  svector *_theta3;  // Soil moisture in layer 3 [decimal]
  svector *_vadose;  // Vadose storage (unsaturated zone) [m]
  svector *_GW;  // Groundwater storage [m]
  svector *_chanS;  // Channel storage [m]
  svector *_I_old;  // Canopy storage [m]
  svector *_snow_old;  // Snow depth in [m]
  svector *_pond_old;  // Ponding water in [m]
  svector *_theta1_old;  // Soil moisture in layer 1 [decimal]
  svector *_theta2_old;  // Soil moisture in layer 2 [decimal]
  svector *_theta3_old;  // Soil moisture in layer 3 [decimal]
  svector *_vadose_old;  // Vadose storage [m]
  svector *_GW_old;  // Groundwater storage [m]
  svector *_chanS_old;  // Channel storage [m3]
  svector *_LAI_old;  // Leaf area index [-]
  /* end of Storages */ 
 

  /* Fluxes */
  svector *_Th;  // Throughfall [m]
  svector *_snowmelt;  // Snow melt [m]
  svector *_infilt;  // Inflitration into soil layer 1 [m]
  svector *_preferential_flow;  // Preferential flow to vadose storage due to exstenice of macropores in rock landscapes [m]
  svector *_Perc1;  // Percolation into layer 2 [m]
  svector *_Perc2;  // Percolation into layer 3 [m]
  svector *_Perc3;  // Percolation into vadose storage [m]
  svector *_Perc_vadose;  // Percolation from vadose storage into gw reservior [m]
  svector *_rPerc_vadose;  // Repercolation from vadose storage into gw reservior [m]
  svector *_capillary_flow;  // Capillary flow from shallow GW zone to bottom soil layer [m]
  svector *_Ei;  // Canopy evaporation [m]
  svector *_Es;  // Soil evaporation [m]
  svector *_Tr;  // Total transpiration in three layers [m]
  svector *_Tr1;  // Transpiration in layer 1 [m]
  svector *_Tr2;  // Transpiration in layer 2 [m]
  svector *_Tr3;  // Transpiration in layer 3 [m]
  svector *_irrigation_from_river;  // Water extraction from river [m]
  svector *_irrigation_from_GW;  // Water extraction from GW [m]
  svector *_Ks1;  // Saturated hydraulic conductivity in layer 1
  svector *_Ks2;  // Saturated hydraulic conductivity in layer 2
  svector *_Ks3;  // Saturated hydraulic conductivity in layer 3
  svector *_thetaS1;  // Saturated soil moisture in layer 1
  svector *_thetaS2;  // Saturated soil moisture in layer 2
  svector *_thetaS3;  // Saturated soil moisture in layer 3
  svector *_thetaFC1;  // Field capacity in layer 1
  svector *_thetaFC2;  // Field capacity in layer 2
  svector *_thetaFC3;  // Field capacity in layer 3
  svector *_thetaWP1;  // Wilting point in layer 1
  svector *_thetaWP2;  // Wilting point in layer 2
  svector *_thetaWP3;  // Wilting point in layer 3
  svector *_ovf_in;  // Overland flow from upstream cell(s) [m]
  svector *_ovf_out;  // Overland flow to downstream cell [m]
  svector *_ovf_toChn;  // Overland flow to Channel [m]
  svector *_interf_in;  // Interflow from upstream cell(s) [m]
  svector *_interf_out;  // Interflow to downstream cell [m]
  svector *_interf_toChn;  // Interflow to Channel [m]
  svector *_GWf_in;  // GW flow from upstream cell(s) [m]
  svector *_GWf_out;  // GW flow to downstream cell [m]
  svector *_GWf_toChn;  // Groundwater flow to Channel [m]
  svector *_Q;  // Discharge [m3/s]
  svector *_Qupstream;  // Upstream inflow [m3/s]
  svector *_Echan;  // Channel evaporation [m]
  svector *_tmp;  // Temporal variable for testing [-]
  svector *_snowacc;  // Snow accumulation for testing [m]
  svector *_TchanS;  // Instream temperature conceptualised as 20-day's average of air temperature [degree C]
  svector *_rinfilt;  // Reinflitration into soil layer 1 [m]
  svector *_rPerc1;  // Repercolation into layer 2 due to overland flow routing [m]
  svector *_rPerc2;  // Repercolation into layer 3 due to overland flow routing [m]
  svector *_rPerc3;  // Repercolation into gw reservior due to overland flow routing [m]
  svector *_drainage_from_soil;  // Total drainage from all soil layers [m]
  svector *_drainage_from_layer1;  // Drainage from layer 1 [m]
  svector *_drainage_from_layer2;  // Drainage from layer 2 [m]
  svector *_drainage_from_layer3;  // Drainage from layer 3 [m]
  svector *_froot_layer1;  // froot coefficient for all soil profile
  svector *_froot_layer2;  // froot coefficient for layer 2
  svector *_froot_layer3;  // froot coefficient for layer 3
  svector *_p_perc1;  // Percolation proportion in layer 1
  svector *_p_perc2;  // Percolation proportion in layer 2
  svector *_p_perc3;  // Percolation proportion in layer 3
  svector *_PE;  // Potential evaporation [m]
  svector *_PT;  // Potential transpiration [m]
  svector *_flux_ovf_in_acc;  // Total amount of solutes in overland inflow [original unit * m]
  svector *_flux_interf_in_acc;  // Total amount of solutes in inter-inflow [original unit * m]
  svector *_flux_GWf_in_acc;  // Total amount of solutes in GW inflow [original unit * m]
  svector *_flux_Qupstream_acc;  // Total amount of solutes in upstream inflow to channel storage [original unit * m]
  /* end of Fluxes */


  /* Tracking */
  svector *_d18o_I;  // d18o in Canopy storage [‰]
  svector *_d18o_snow;  // d18o in Snow depth in [‰]
  svector *_d18o_pond;  // d18o in Ponding water in [‰]
  svector *_d18o_layer1;  // d18o in Soil moisture in layer 1 [‰]
  svector *_d18o_layer2;  // d18o in Soil moisture in layer 2 [‰]
  svector *_d18o_layer3;  // d18o in Soil moisture in layer 3 [‰]
  svector *_d18o_vadose;  // d18o in vadose storage [‰]
  svector *_d18o_GW;  // d18o in Groundwater storage [‰]
  svector *_d18o_chanS;  // d18o in Channel storage [‰]
  svector *_age_vadose;  // Cumulative age in vadose storage [‰]
  svector *_age_I;  // Cumulative age in Canopy storage [days]
  svector *_age_snow;  // Cumulative age in Snow depth in [days]
  svector *_age_pond;  // Cumulative age in Ponding water in [days]
  svector *_age_layer1;  // Cumulative age in Soil moisture in layer 1 [days]
  svector *_age_layer2;  // Cumulative age in Soil moisture in layer 2 [days]
  svector *_age_layer3;  // Cumulative age in Soil moisture in layer 3 [days]
  svector *_age_GW;  // Cumulative age in Groundwater storage [days]
  svector *_age_chanS;  // Cumulative age in Channel storage [days]
  svector *_trans_age_I;  // Transient age in Canopy storage [days]
  svector *_trans_age_snow;  // Transient age in Snow depth in [days]
  svector *_trans_age_pond;  // Transient age in Ponding water in [days]
  svector *_trans_age_layer1;  // Transient age in Soil moisture in layer 1 [days]
  svector *_trans_age_layer2;  // Transient age in Soil moisture in layer 2 [days]
  svector *_trans_age_layer3;  // Transient age in Soil moisture in layer 3 [days]
  svector *_trans_age_vadose;  // Transient age in vadose storage [‰]
  svector *_trans_age_GW;  // Transient age in Groundwater storage [days]
  svector *_trans_age_chanS;  // Transient age in Channel storage [days]
  /* end of Tracking */

  // Nitrogen addition and plant uptakes are identical for each year, so they only need to be sorted once (or once after change in parameterisation)
  // 2d vector [num_landuse][366 days]
  vector<vector <double>> _fertN_add_layer1_IN;
  vector<vector <double>> _fertN_add_layer2_IN;
  vector<vector <double>> _fertN_add_layer1_fast_NP;
  vector<vector <double>> _fertN_add_layer2_fast_NP;
  vector<vector <double>> _resN_add_layer1_fast_NP;
  vector<vector <double>> _resN_add_layer2_fast_NP;
  vector<vector <double>> _resN_add_layer1_humus_NP;
  vector<vector <double>> _resN_add_layer2_humus_NP;

  vector<vector <double>> _potential_uptake_layer1;
  vector<vector <double>> _potential_uptake_layer2;
  vector<vector <double>> _potential_uptake_layer3;
  /* Nitrogen addition */
  vector<double> is_crop;
  vector<double> fert_add;
  vector<double> fert_day;
  vector<double> fert_down;
  vector<double> fert_period;
  vector<double> fert_IN;
  vector<double> manure_add;
  vector<double> manure_day;
  vector<double> manure_down;
  vector<double> manure_period;
  vector<double> manure_IN;
  vector<double> residue_add;
  vector<double> residue_day;
  vector<double> residue_down;
  vector<double> residue_period;
  vector<double> residue_fast_NP;
  vector<double> up1;
  vector<double> up2;
  vector<double> up3;
  vector<double> upper_uptake;
  vector<double> plant_day;
  vector<double> emerge_day;
  vector<double> harvest_day;
  /* end of Nitrogen addition */

  /* Irrigation */
  vector<double> irrigation_thres;
  /* end of Irrigation */

  /* Phenology */
  svector *_NPP;  // Net primary production [gC/(m2*Ts)] 
  svector *_canopy_conductance;  // Stomatal conductance for whole canopy  [m s-1]
  /* end of Phenology */

  /* Nitrogen */
  svector *_plant_mobile_N;  // Plant mobile nitrogen [mgN/L*m = gN/m2]
  svector *_no3_I;  // no3 in Canopy storage [mgN/L]
  svector *_no3_snow;  // no3 in Snow depth in [mgN/L]
  svector *_no3_pond;  // no3 in Ponding water in [mgN/L]
  svector *_no3_layer1;  // no3 in Soil moisture in layer 1 [mgN/L]
  svector *_no3_layer2;  // no3 in Soil moisture in layer 2 [mgN/L]
  svector *_no3_layer3;  // no3 in Soil moisture in layer 3 [mgN/L]
  svector *_no3_vadose;  // no3 in vadose storage [mgN/L]
  svector *_no3_GW;  // no3 in Groundwater storage [mgN/L]
  svector *_no3_chanS;  // no3 in Channel storage [mgN/L]
  svector *_nitrogen_add;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
  svector *_plant_uptake;  // Plant uptake [mgN/L*m = gN/m2]
  svector *_deni_soil;  // Soil denitrification [mgN/L*m = gN/m2]
  svector *_minerl_soil;  // Soil mineralisation (Soil decomposition may take additional nitorgen from dissolved inorganic nitrogen pool to build humus) [mgN/L*m = gN/m2]
  svector *_deni_river;  // Aquatic denitrification [mgN/L*m = gN/m2]
  svector *_fast_NP1_nonwood;  // Fast nonwood nitrogen storage in layer 1 (non-wood) [mgN/L*m = gN/m2]; needed as nitrogen carbon ratio of nonwood pools are variable due to reserve inputs
  svector *_fast_NP1;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
  svector *_humus_N;  // Humus nitrogen storage in all soil layers [mgN/L*m = gN/m2]
  svector *_fast_N;  // Fast nitrogen storage in all soil layers [mgN/L*m = gN/m2]
  svector *_leaching_mass_no3;  // Leaching of NO3 [gN/m2]
  svector *_drainage_mass_no3;  // Drainage of NO3 [gN/m2]
  /* end of Nitrogen */


  /* Carbon */
  svector *_plant_green_CP;  //  Carbon pool that contains carbon of the "green" or living parts of plants (leaves, fine roots, vascular tissues), except carbon stored as reserve  [gC/m2]
  svector *_plant_wood_CP;  //   Carbon pool that contains the carbon of the woody parts of plants (stems, branches, roots)  [gC/m2]
  svector *_plant_reserve_CP;  //  Carbon pool that contains the carbon stored in sugars and starches that the plants keep as an energy reserve (free of nitrogen)  [gC/m2]
  svector *_plant_C;  //  The total carbon content of plants (sum of green, wood, and reserve pool)  [gC/m2]
  svector *_acid_CP1_nonwood;  // Acid hydrolyzable carbon pool (non-wood) in layer 1
  svector *_ethanol_CP1_nonwood;  // Ethanol soluble carbon pool (non-wood) in layer 1
  svector *_nonsoluble_CP1_nonwood;  // Neither hydrolyzable nor soluble carbon pool (non-wood) in layer 1
  svector *_soluble_CP1_nonwood;  // Soluble carbon pool (non-wood) in layer 1
  svector *_acid_CP1_wood;  // Acid hydrolyzable carbon pool (wood) in layer 1
  svector *_ethanol_CP1_wood;  // Ethanol soluble carbon pool (wood) in layer 1
  svector *_nonsoluble_CP1_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 1
  svector *_soluble_CP1_wood;  // Soluble carbon pool (wood) in layer 1
  svector *_humus_CP1;  // Humus carbon pool (wood and non-wood) in layer 1
  svector *_acid_CP2_wood;  // Acid hydrolyzable carbon pool (wood) in layer 2
  svector *_ethanol_CP2_wood;  // Ethanol soluble carbon pool (wood) in layer 2
  svector *_nonsoluble_CP2_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 2
  svector *_soluble_CP2_wood;  // Soluble carbon pool (wood) in layer 2
  svector *_humus_CP2;  // Humus carbon pool (wood) in layer 2
  svector *_acid_CP3_wood;  // Acid hydrolyzable carbon pool (wood) in layer 3
  svector *_ethanol_CP3_wood;  // Ethanol soluble carbon pool (wood) in layer 3
  svector *_nonsoluble_CP3_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 3
  svector *_soluble_CP3_wood;  // Soluble carbon pool (wood) in layer 3
  svector *_humus_CP3;  // Humus carbon pool (wood) in layer 3
  svector *_humus_C;  // Humus carbon storage in all soil layers [mgN/L*m = gN/m2]
  svector *_fast_C;  // Fast carbon storage in all soil layers [mgN/L*m = gN/m2]
  svector *_soluble_C;  // Soluble carbon storage in all soil layers [mgN/L*m = gN/m2]
  svector *_doc_I;  // DOC in Canopy storage [mgN/L]
  svector *_doc_snow;  // DOC in Snow depth in [mgN/L]
  svector *_doc_pond;  // DOC in Ponding water in [mgN/L]
  svector *_doc_layer1;  // DOC in Soil moisture in layer 1 [mgN/L]
  svector *_doc_layer2;  // DOC in Soil moisture in layer 2 [mgN/L]
  svector *_doc_layer3;  // DOC in Soil moisture in layer 3 [mgN/L]
  svector *_doc_vadose;  // DOC in vadose storage [mgN/L]
  svector *_doc_GW;  // DOC in Groundwater storage [mgN/L]
  svector *_doc_chanS;  // DOC in Channel storage [mgN/L]
  svector *_litter_fall_C;  // Litter fall summarised from green and reserve pool to non-wood litter pool, and wood pool to litter wood pool [gC/m2]
  svector *_soil_respiration_C;  // Soil respiration summarised in carbon [gC/m2]
  svector *_soil_decomposition_C;  // Soil decomposition summarised in carbon [gC/m2]
  svector *_respiration_river_C;  // Aquatic heterotrophic respiration summarised in carbon [gC/m2]
  svector *_C4_flag;  //  C4 dominant vegetaion? 0 - No (C3); 1 - Yes (C4)
  svector *_doc_rain;  // The organic carbon concentration in rain water [mgC/L], only needed when carbon_sim_1 = 1
  svector *_leaching_mass_doc;  // Leaching of DOC [gC/m2]
  svector *_drainage_mass_doc;  // Drainage of DOC [gC/m2]
  /* end of Carbon */

  /* Unit transformer */
  double molC_m2_to_gC_m2;  // 1 mol(C)/m2 = 12.01 gC/m2

  double ratio_day_time;  // Ratio of day time to total time [-]

  /* Assimilation_constant */
  // Radiation
  double ratio_diffuse;  // Ratio of diffuse radiation to total radiation [-]
  double ratio_par_to_Rsw;  // Ratio of Photosynthetically Active Radiation to Shortwave radiation [-]
  double canopy_albedo;  // Canopy albedo [-]
  double R_gas;  // Gas constant [J/mol-1K-1]
  double Epar;  // Photosynthetically Active Radiation in J / mol(photons)
  
  // Photosynthesis
  double KC0;   // Michaelis-menten Constant for CO2 at 25C [mol(CO2) / mol(air)]
  double KO0;   // Michaelis-menten Constant for O2 at 25C [mol(O2) / mol(air)]
  double EC;     // Activation energy for KC [J/mol]
  double EO;     // Activation energy for KO [J/mol]
  double EV;     // Activation energy for Vcmax [J/mol]
  double ER;     // Activation energy for dark respiration [J/mol]
  double FRDC3;  // Ratio of dark respiration to PVM at 25C for C3 plants
  double frac_photon_capture;  // Efficiency ofphoton capture
  double o2_mol;  // Oxygen concentration [mol(o2) / mol(air)]
  double co2_mol;  // CO2 concentration [mol(co2) / mol(air)]
  double ratio_co2_leaf_to_air_C3;  // Ratio of CO2 in leaf to air for C3 plants
  double ratio_co2_leaf_to_air_C4;  // Ratio of CO2 in leaf to air for C4 plants
  double min_of_max_carboxylation_rate; // Minimum of maximum carboxylation rate [10^(-6) mol/(m^2 s)]
  
  // Canopy conductance (Eq. 3.3.2.12 in ECHAM3 manual / JSBACH)
  double conductance_k;    // Parameter for canopy conductance/resistance [-]
  double conductance_a;   // Parameter for conductance/resistance [Jm-3]
  double conductance_b;     // Parameter for canopy conductance/resistance [Wm-2]
  double conductance_c;    // Parameter for conductance/resistance [ms-1]

  /* Phenology_constant */
  double WoodLitterSize;  // Litter size of wood pool

  /* Carbon_constant */
  double C_trans_ratio_acid_2_soluble;
  double C_trans_ratio_acid_2_ethanol;
  double C_trans_ratio_acid_2_nonsoluble;
  double C_trans_ratio_soluble_2_acid;
  double C_trans_ratio_soluble_2_ethanol;
  double C_trans_ratio_soluble_2_nonsoluble;
  double C_trans_ratio_ethanol_2_acid;
  double C_trans_ratio_ethanol_2_soluble;
  double C_trans_ratio_ethanol_2_nonsoluble;
  double C_trans_ratio_nonsoluble_2_acid;
  double C_trans_ratio_nonsoluble_2_soluble;
  double C_trans_ratio_nonsoluble_2_ethanol;
  double C_trans_ratio_all_2_humus;
  double ref_decomp_rate_acid;
  double ref_decomp_rate_soluble;
  double ref_decomp_rate_ethanol;
  double ref_decomp_rate_nonsoluble;
  double ref_decomp_rate_humus;
  double C_respiration_ratio_acid;
  double C_respiration_ratio_soluble;
  double C_respiration_ratio_ethanol;
  double C_respiration_ratio_nonsoluble;


  


  /* Save TS output to speed up calibration; Temporary implementation; TODO */
  vector<double> vector_Q;
  vector<double> vector_d18o_chanS;
  vector<double> vector_no3_chanS;
  vector<double> vector_doc_chanS;
  
 
  
  Basin(Control &ctrl, Param &par);  // constrcuctor of Basin
  //dtor
  ~Basin();  // destrcuctor of Basin
  int dtor(Control &ctrl);



  /* ===== Interface ===== */
  int Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm);
  int Solve_canopy(Control &ctrl, Param &par, Atmosphere &atm);
  int Solve_surface(Control &ctrl, Param &par, Atmosphere &atm);
  int Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm);
  int Solve_routing(Control &ctrl, Param &par);
  int Solve_channel(Control &ctrl, Param &par, Atmosphere &atm);
  int Statistic_summary(Control &ctrl, Param &par);
  /* ===== Interface for biogeochemistry - carbon and nitrogen ===== */
  int Solve_canopy_nutrient(Control &ctrl, Atmosphere &atm);  // Canopy storage mixing with precipitation and erichment due to evaporation
  int Solve_surface_nutrient(Control &ctrl, Atmosphere &atm, Param &par);  // Ponding water mixing with snow melt
  int Solve_soil_profile_nutrient(Control &ctrl, Atmosphere &atm, Param &par);  // Soil storage mixing and transformation
  int Solve_vadose_nutrient(Control &ctrl, Atmosphere &atm);  // vadose storage mixing
  int Solve_GW_nutrient(Control &ctrl, Atmosphere &atm);  // GW storage mixing
  int Solve_routing_nutrient(Control &ctrl, Param &par);  // Mixing of overland flow, interflow, and GW flow
  int Solve_channel_nutrient(Control &ctrl, Atmosphere &atm, Param &par);  // Enrichment due to channel evaporation, and instream nutrient transformation



  /* Canopy interception */
  int Interception_1(Control &ctrl, Param &par, Atmosphere &atm);
  int Interception_2(Control &ctrl, Param &par, Atmosphere &atm);
  /* Snow accumulation and melt */
  int Snow_acc_melt(Param &par, Atmosphere &atm, int j);
  /* Soil profiles */
  // Calculate soil proporties
  int Soil_proporty(Control &ctrl, Param &par);
  int Pedo_transfer_1(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, \
                      svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  int Pedo_transfer_2(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, \
                        svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  int Pedo_transfer_3(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  \
                          svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  // Infiltration
  int Infiltration_1(Control &ctrl, Param &par);
  int Reinfiltration_1(Control &ctrl, Param &par, int j, double &db_rinfilt, double &db_theta1, double &db_pond);
  // Evapotranspiration
  int Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm);
  int Seperate_PET(Param &par, Atmosphere &atm);  // Seperate PET to PE and PT based on LAI and a rExtinct parameter; Rutter (1972)
  int Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm);  // Evapotranspiration based on Rutter (1972)
  int Evapotranspiration_2(Control &ctrl, Param &par, Atmosphere &atm);  // Evapotranspiration based on 
  // Percolation
  int Percolation_1(Control &ctrl, Param &par);
  int Percolation_2(Control &ctrl, Param &par);
  int Percolation_3(Control &ctrl, Param &par);
  int Repercolation_1(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);
  int Repercolation_2(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);
  int Repercolation_3(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);
  int GWrecharge_1(Control &ctrl, Param &par);
  int GWrecharge_2(Control &ctrl, Param &par);
  int ReGWrecharge_1(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose);
  int ReGWrecharge_2(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose);
  // Capillary flow
  int Capillary_flow(Control &ctrl, Param &par);
  /* Lateral routing */
  int Routing_drainage(); // Drainage routing to channel
  int Routing_ovf_1(Control &ctrl, Param &par); // overland flow routing; All ponding water goes to next cell
  int Routing_interflow_1(Control &ctrl, Param &par); // Interflow routing based on linear approximation of Kinematic Wave
  int Routing_Q_1(Control &ctrl, Param &par); // Stream routing based on Kinematic Wave
  int Routing_GWflow_1(Control &ctrl, Param &par); // GW flow routing based on linear approximation of Kinematic Wave
  /* Energy balance */
  double Get_soil_temperature(const double Ta, const double LAI);
  /* Channel */
  int Channel_evaporation_1(Control &ctrl, Atmosphere &atm, Param &par);  // Penman equation
  int Channel_evaporation_2(Control &ctrl, Atmosphere &atm, Param &par);  // Priestley-Taylor equation
  /* Summary hydrological statistics */
  int Hydrology_summary();
  

  /* ===== Management module ===== */
  int Irrigation(Control &ctrl, Param &par);
  int Drainage(Control &ctrl, Param &par);  // Drainage based on relative depths of drainage pipe and groundwater table

  /* ===== Isotopic and Age tracking ===== */
  int Mixing_full(double storage, double &cstorage, double input, double cinput);  // Full mixing within the timestep
  int Mixing_baseflow(double storage, double &coutput, double input, double cinput, double output);   // Baseflow mixing for GW storage
  int Mixing_canopy_tracking(Control &ctrl, Atmosphere &atm);  // Canopy storage mixing and fractionaton
  int Mixing_surface_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Canopy snowpack and throughfall
  int Mixing_soil_profile_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Soil storage mixing and fractionaton
  int Mixing_vadose_tracking(Control &ctrl, Atmosphere &atm);  // Vadose storage mixing
  int Mixing_GW_tracking(Control &ctrl, Atmosphere &atm);  // GW storage mixing
  int Mixing_routing_tracking(Control &ctrl, Param &par);  // Mixing of overland flow, interflow, and GW flow
  int Mixing_channel_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Fractionation due to channel evaporation
  int Fractionation(Atmosphere &atm, Param &par, svector &sv_evap, svector &sv_V_new, svector &sv_di_old, svector &sv_di_new, svector &sv_di_evap, int issoil);  // Fractionation due to canopy or soil evaporation
  int Advance_age(); // Advance water ages by 1
  int Advance_trans_age(); // Advance transient water ages by 1

  /* ===== Solute mixing and transport module ===== */
  int Solve_canopy_transport(Atmosphere &atm, svector &_sv_conc_I, svector &_sv_conc_P, svector &_sv_conc_pond, bool enrich_flag);
  int Solve_surface_transport(Control &ctrl, Atmosphere &atm, Param &par, svector &sv_conc_I, svector &sv_conc_snow, svector &sv_conc_pond, svector &sv_conc_chanS, svector &sv_conc_GW, bool enrich_flag);                             
  int Solve_soil_transport(Param &par, svector &sv_conc_pond, svector &sv_conc_layer1, svector &sv_conc_layer2, svector &sv_conc_layer3, svector &sv_conc_vadose, svector &sv_conc_chanS, svector &sv_drainage_mass, bool enrich_flag, double drainage_flag, bool diffuse_flag);
  int Solve_routing_transport(Control &ctrl, Param &par, svector &_sv_conc_pond, svector &_sv_conc_layer1, svector &_sv_conc_layer2, svector &_sv_conc_layer3, svector &_sv_conc_vadose, svector &_sv_conc_GW, svector &_sv_conc_chanS);
  
   
  /* ===== Carbon module ===== */
  int Assimilation(Control &ctrl, Atmosphere &atm, Param &par);  // GPP and NPP calculation
  int Photosynthesis_C3(int j, int timestep, double PAR_mol, double RH, double LAI, double Ta_k, double TC_c, double air_pressure, double energy_scaling_factor, double co2_mol, double co2_leaf_mol, 
    double KC, double KO, double VC_max, double Jmax, double gamma, double water_limitation_factor, double carboxylation_rate, svector &sv_NPP, svector &sv_canopy_conductance);  // C3 photosynthesis based on Farquhar (1980)
  int Set_carbon_constant();  // Set constants for carbon simulation (tansformation rates between different carbon pools)
  int Solve_soil_profile_carbon(Control &ctrl, Atmosphere &atm, Param &par);  // Solve soil carbon processes (addition, transport, decomposition)
  int Carbon_addition(Control &ctrl, Param &par);  // Carbon addition process (from vegetation pools to litter pools)
  int Carbon_management(Control &ctrl, Param &par);  // Carbon management process (harvest and herbivory loss)
  int Carbon_transformation(Control &ctrl, Atmosphere &atm, Param &par);   // Solve soil carbon decomposition
  int Carbon_transformation_process(  Control &ctrl, Atmosphere &atm, Param &par, int j,
    double &db_soluble_CP, double &db_humus_CP, double &db_acid_CP, double &db_ethanol_CP, double &db_nonsoluble_CP,
    double &db_soil_respiration_C, double &db_soil_decomposition_C,
    double &db_available_N, double &db_minerl_soil,
    double db_fct_Ts, double db_fct_theta, double db_fct_size, double db_NC_ratio_fast);  // Carbon transformation process for soil profile
  int Carbon_instream_transformation(Control &ctrl, Atmosphere &atm, Param &par);  // In-stream decomposition of DOC
  int Carbon_summary(Control &ctrl, Param &par);  // Summary carbon states and fluxes
  double Calculate_fraction_soluble_CP_to_DOC(double soil_storage, double percolation, double ref_frac_soluble_to_doc);

  /* Nitrogen module */
  int Sort_nitrogen_addition(Control &ctrl, Param &par);  // Sort 366 days at first iteration
  int Nitrogen_addition(Control &ctrl, Param &par);
  int Sort_plant_uptake(Control &ctrl, Param &par);
  int Plant_uptake(Control &ctrl, Param &par, Atmosphere &atm);
  int Soil_denitrification(Control &ctrl, Atmosphere &atm, Param &par);
  //int Soil_transformation(Control &ctrl, Atmosphere &atm, Param &par);  // Disabled in v2.0
  int Nitrogen_instream_transformation(Control &ctrl, Atmosphere &atm, Param &par);
  int Nitrogen_summary(Control &ctrl, Param &par);  // Summary nitrogen states and fluxes

  /* ===== Global functions ===== */
  int Sort_percolation_travel_time(Control &ctrl, Param &par);
  int Sort_root_fraction(Control &ctrl,Param &par);  // Estimate root fraction
  double Temp_factor(double T);  // Temperature factor of nitrogen transformation
  double Moist_factor(const double db_theta, const double db_thetaWP, const double db_thetaFC, const double db_thetaS, const double db_depth); // Moisture factor of nitrogen transformation

  /* ===== Initialisation ===== */
  int Initialisation(Control &ctrl, Param &par, Atmosphere &atm);
  int Initialisation_each_timestep(Control &ctrl, Param &par);
  int Store_states();  // Store all water storages for mixing

  /* ===== IO functions ===== */
  int ReadCropFile(Control &ctrl, Param &par, string fname);
  int open_groundTs(Control &ctrl);
  int read_groundTs(Control &ctrl);
  int open_groundTs_maps(string fname, ifstream &ifHandle);
  int read_groundTs_maps(ifstream &ifHandle, svector &GroundTsMap);
  int init_groundTs(Control &ctrl);
  int update_groundTs(Control &ctrl, Param &par);
  int init_groundTs_maps(string fname, ifstream &ifHandle);
  int update_groundTs_maps(ifstream &ifHandle, Param &par, svector &GroundTsMap);
  int open_managementTs(Control &ctrl);  // Open and read management inputs such as drainage depth
  int read_managementTs(Control &ctrl);
  int init_managementTs(Control &ctrl);
  int update_managementTs(Control &ctrl, Param &par);

  // Model test
  //int Check_mass_balance(Control &ctrl, Param &par, Atmosphere &atm);

  /* Save TS output to speed up calibration; Temporary implementation */
  int Report_for_cali(Control &ctrl);
  int Save_for_cali(Control &ctrl);
  bool save_vector_to_binary(const std::vector<double>& vec, const std::string& filename);

};

#endif /* BASIN_H_ */
