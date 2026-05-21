/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Param.h
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#ifndef PARAM_H_
#define PARAM_H_

#include "Control.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Param {

  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  sortedGrid _sortedGrid;
  /* end of Properties */

  string line_string;

  public:

  /* Flags */
  int sort_perc_travel_time_OK;  
  int sort_root_fraction_OK;  
  int sort_plant_uptake_OK;  // The plant uptake only needs to be calculated once (or once within each change)
  int sort_nitrogen_addition_OK;  // The nitrogen addtion only needs to be calculated once (or once within each change)
  int sort_parameter_correction_OK;  // The parameter correction only needs to be calculated once (or once within each change)


  /* Parameters */
  vector<double> depth3;
  vector<double> alpha;
  vector<double> rE;
  vector<double> snow_rain_thre;
  vector<double> deg_day_min;
  vector<double> deg_day_max;
  vector<double> deg_day_increase;
  vector<double> ref_thetaS;
  vector<double> PTF_VG_clay;
  vector<double> PTF_VG_Db;
  vector<double> PTF_Ks_const;
  vector<double> PTF_Ks_sand;
  vector<double> PTF_Ks_clay;
  vector<double> SWP;
  vector<double> KvKh;
  vector<double> psiAE;
  vector<double> KKs;
  vector<double> Ksat;
  vector<double> BClambda;
  vector<double> preferential_flow_coeff;
  vector<double> perc_optimal_theta;
  vector<double> percExp;
  vector<double> capillary_flow_rate;
  vector<double> froot_coeff;
  vector<double> ET_weight;
  vector<double> init_GW;
  vector<double> perc_vadose_coeff;
  vector<double> pOvf_toChn;
  vector<double> Ks_surface;
  vector<double> Ks_vadose;
  vector<double> Ks_GW;
  vector<double> lat_to_Chn_vadose;
  vector<double> lat_to_Chn_GW;
  vector<double> interfExp;
  vector<double> GWfExp;
  vector<double> Manningn;
  vector<double> Echan_alpha;
  vector<double> irrigation_FC_thres;
  vector<double> irrigation_coeff;
  vector<double> drainage_intensity;
  vector<double> herbivory_uptake_coeff;
  vector<double> harvest_coeff;
  vector<double> diffuse_molecular_coefficient;
  vector<double> ratio_to_interf;
  vector<double> CG_n_soil;
  vector<double> delta_d18o_init_GW;
  vector<double> delta_no3_init_GW;
  vector<double> denitrification_river;
  vector<double> denitrification_soil;
  vector<double> deni_soil_moisture_thres;
  vector<double> C_in_LeafArea;
  vector<double> LAI_shed_coef;
  vector<double> tau_wood_C;
  vector<double> plant_wood_CP_max;
  vector<double> plant_reserve_CP_max;
  vector<double> carboxylation_rate;
  vector<double> ETransport;
  vector<double> frac_NPP_to_green;
  vector<double> frac_NPP_to_wood;
  vector<double> frac_litter_to_soluble_nonwood;
  vector<double> frac_litter_to_acid_nonwood;
  vector<double> frac_litter_to_ethanol_nonwood;
  vector<double> frac_litter_to_nonsoluble_nonwood;
  vector<double> frac_litter_to_soluble_wood;
  vector<double> frac_litter_to_acid_wood;
  vector<double> frac_litter_to_ethanol_wood;
  vector<double> frac_litter_to_nonsoluble_wood;
  vector<double> transformation_exp_base;
  vector<double> fdepth_decay_Exp;
  vector<double> decomposition_weight_fast_pool;
  vector<double> decomposition_weight_humus_pool;
  vector<double> humus_C_decomposition_to_DOC_ratio;
  vector<double> ref_decomp_rate_doc;
  vector<double> C_trans_ratio_fast_2_humus;
  vector<double> ref_frac_soluble_to_doc;
  vector<double> respiration_river;
  vector<double> NC_ratio_plant_green;
  vector<double> NC_ratio_plant_wood;
  vector<double> NC_ratio_fast_pool_nonwood;
  vector<double> NC_ratio_fast_pool_wood;
  svector *_depth3;  // Depth of soil layer 3 [m]
  svector *_alpha;  // The weighting parameter that links LAI and maximum canopy storage [-]
  svector *_rE;  // Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)
  svector *_preferential_flow_coeff;  // The coefficient parameter for preferential flow [-]
  svector *_capillary_flow_rate;  // The reference conductivity of capillary flow from shallow GW zone to bottom soil layer [m/s]
  svector *_perc_vadose_coeff;  // The coefficient parameter for GW recharge [-], only needed when opt_recharge = 1 or 2
  svector *_irrigation_FC_thres;  // The soil moisture threshold for irrigation [-]
  svector *_diffuse_molecular_coefficient;  // The coefficient for Fickian diffusion [m2/s]
  svector *_ratio_to_interf;  // The proportion of excess storage in layer 1 that routs as interflow (otherwise percolate to GW) [decimal]
  svector *_snow_rain_thre;  // The temperature for snow melt  [m]
  svector *_deg_day_min;  // Degree-day factor with no precipitation [m-1 degreeC-1]
  svector *_deg_day_max;  // Maximum Degree-day factor [m-1 degreeC-1]
  svector *_deg_day_increase;  // Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]
  svector *_ref_thetaS;  // Reference saturated soil moisture [-]
  svector *_PTF_VG_clay;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  svector *_PTF_VG_Db;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  svector *_PTF_Ks_const;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_PTF_Ks_sand;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_PTF_Ks_clay;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_SWP;  // Soil water potentail for field capacity estimation [-], only needed when opt_fieldcapacity = 1
  svector *_KvKh;  // The coefficient to transform Ks to effective Ks [-], only needed when opt_infil = 1
  svector *_psiAE;  // The wetting front potential for Green-Ampt model [mm], only needed when opt_infil = 1
  svector *_KKs;  // The exponential parameter for depth-dependent saturated hydraulic conductivity [-], only needed when opt_depthprofile = 2
  svector *_Ksat;  // The exponential parameter for depth-dependent saturated moisture content  [-], only needed when opt_depthprofile = 2
  svector *_BClambda;  // The exponential parameter for depth-dependent field capacity  [-], only needed when opt_depthprofile = 2
  svector *_perc_optimal_theta;  // The specific threshold between field capacity and saturated content for percolation [0-1]
  svector *_percExp;  // The exponential parameter for percolation [-], only needed when opt_percolation = 2
  svector *_froot_coeff;  // Root fraction coefficient [-]
  svector *_ET_weight;  // Evaporation and Transpiration should be adjusted due to potential underestimation of daily simulaton compared to integral of hourly simulatont [-]
  svector *_init_GW;  // The initial GW storage [m], only needed when opt_init_GW = 1
  svector *_pOvf_toChn;  // The weighting linear parameter for overland flow routing towards channel  [-]
  svector *_Ks_surface;  // The reference conductivity of surface for overland flow routing [m/s]
  svector *_Ks_vadose;  // The reference conductivity of vadose zone for interflow routing [m/s]
  svector *_lat_to_Chn_vadose;  // The ratio between conductivities of lateral flow and channel recharge in vadose zone [-]
  svector *_interfExp;  // The exponetial weighting parameter for interflow flow routing towards channel  [-]
  svector *_Ks_GW;  // The reference conductivity of GW zone for interflow routing [m/s]
  svector *_lat_to_Chn_GW;  // The ratio between conductivities of lateral flow and channel recharge in GW zone [-]
  svector *_GWfExp;  // The exponetial weighting parameter for GW flow routing towards channel  [-]
  svector *_Manningn;  // Manning N for stream routing [-], only needed when opt_routQ = 1
  svector *_Echan_alpha;  // correction factor in Priestley-Taylor equation [-], only needed when opt_chanE = 1 or 2
  svector *_irrigation_coeff;  // Irrigation coefficient to determine the actual water demand from water deficit [-], only needed when irrigation is enabled
  svector *_drainage_intensity;  // The intensity of drainage based on the density of drainage network [-], only needed when drainage is enabled
  svector *_herbivory_uptake_coeff;  // The coefficient for herbivory uptake [-]
  svector *_harvest_coeff;  // The coefficient for crop harvest [-]
  svector *_C_in_LeafArea;  // Carbon content per leaf area in [m2(leaf)/mol(Carbon)]
  svector *_tau_wood_C;  // Life time scale of the wood pool and vegetation dynamics [days]
  svector *_plant_wood_CP_max;  // The maximum carbon content in wood pool [molC/m2] 
  svector *_plant_reserve_CP_max;  // Term to calculate maximum carbon content in reserve pool at optimal conditions [-]: first term is the ratio of ratio of vegetation green pool to reserve pool at maximum LAI, while second term is maximum LAI
  svector *_carboxylation_rate;  // Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)] (*1e-6?)
  svector *_ETransport;  // Maximum electron transport rate at 25 Celsius [1.E-6 * Mol/m^2 leafarea/s] (Jmax=1.9*V_max^25 for C3 plants)
  svector *_frac_NPP_to_green;  // The fraction of NPP addition to vegetation green pool [-] 
  svector *_frac_NPP_to_wood;  // The fraction of NPP addition to wood green pool [-] 
  svector *_frac_litter_to_soluble_nonwood;  // The fraction of nonwood litter going to soil soluble pool (DOC pool)  [-] 
  svector *_frac_litter_to_acid_nonwood;  // The fraction of non-woody litter going to soil acid pool  [-] 
  svector *_frac_litter_to_ethanol_nonwood;  // The fraction of non-woody litter going to soil ethano pool  [-] 
  svector *_frac_litter_to_nonsoluble_nonwood;  // The fraction of non-woody litter going to soil nonsoluble pool  [-] 
  svector *_frac_litter_to_soluble_wood;  // The fraction of wood litter going to soil soluble pool (DOC pool)  [-] 
  svector *_frac_litter_to_acid_wood;  // The fraction of wood litter going to soil acid pool  [-] 
  svector *_frac_litter_to_ethanol_wood;  // The fraction of wood litter going to soil ethano pool  [-] 
  svector *_frac_litter_to_nonsoluble_wood;  // The fraction of wood litter going to soil nonsoluble pool  [-] 
  svector *_transformation_exp_base;  // Exponential base for temperature function of soil decomposition and denitrification [-]
  svector *_fdepth_decay_Exp;  // Exponential decay function for soil decomposition based on depth [-]
  svector *_decomposition_weight_fast_pool;  // Correction of decomposition rates of past pool based on the magnitudes of carbon storages [-]
  svector *_decomposition_weight_humus_pool;  // Correction of decomposition rates of humus pool based on the magnitudes of carbon storages [-]
  svector *_humus_C_decomposition_to_DOC_ratio;  // The ratio of humus carbon decomposition to DOC pool [-]
  svector *_ref_decomp_rate_doc;  // Reference decomposition rate of DOC pool [day-1]
  svector *_C_trans_ratio_fast_2_humus;  // Fraction of decomposed fast pool that goes into humus pool [decimal]
  svector *_ref_frac_soluble_to_doc;  // Reference fraction of soluble carbon going to DOC pool [-]
  svector *_CG_n_soil;  // Parameter N in CG model for soil water fractionation [-]
  svector *_delta_d18o_init_GW;  // Initial d18O of GW storage [‰]
  svector *_delta_no3_init_GW;  // Initial no3 of GW storage [‰]
  svector *_denitrification_river;  // Reference rates of aquatic denitrification [day-1]
  svector *_denitrification_soil;  // Reference rates of soil denitrification [kg/ha]
  svector *_deni_soil_moisture_thres;  // The moisture threshold of soil denitrification
  svector *_respiration_river;  // Reference rates of aquatic heterotrophic respiration [day-1]
  svector *_NC_ratio_plant_green;  // Nitrogen carbon ratio in vegetation green pool  [gN/gC] 
  svector *_NC_ratio_plant_wood;  // Nitrogen carbon ratio in vegetation wood pool  [gN/gC] 
  svector *_NC_ratio_fast_pool_nonwood;  // Nitrogen carbon ratio in non-wood litter (fast) pool (acid, ethanol, and nonsoluble)  [gN/gC] 
  svector *_NC_ratio_fast_pool_wood;  // Nitrogen carbon ratio in wood litter (fast) pool (acid, ethanol, and nonsoluble)  [gN/gC] 
  svector *_LAI_shed_coef;  // Leaf shedding coefficient related to LAI [-]
  /* end of Parameters */

  svector_2d *param_category;

  //ctor from raster ascii file
  Param(Control &ctrl);
  //dtor
  ~Param();
  int dtor(Control &ctrl);

  // Functions
  int ReadParamFile(Control &ctrl, string fname = "param.ini");  // Read parameters into array
  int Parameterisation(Control &ctrl); // Assign parameter values to each grid

  void readIntoParam(vector<double>& param_arr, string key, vector<string> lines);


};

#endif /* PARAM_H_ */