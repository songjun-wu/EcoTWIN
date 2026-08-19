/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ParamConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Param.h"

Param::Param(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;
  _sortedGrid = ctrl._sortedGrid;

  // Init flags
  sort_perc_travel_time_OK = 0;  
  sort_root_fraction_OK = 0;  
  sort_plant_uptake_OK = 0;  // The plant uptake only needs to be calculated once (or once within each change)
  sort_crop_management_OK = 0;  // The crop management only needs to be calculated once (or once within each change)
  sort_nitrogen_addition_OK = 0;  // The nitrogen addtion only needs to be calculated once (or once within each change)

  string fname = "param.ini";
  /* Parameters */
  _depth3 = new svector(_sortedGrid.size);
  _alpha = new svector(_sortedGrid.size);
  _rE = new svector(_sortedGrid.size);
  _preferential_flow_coeff = new svector(_sortedGrid.size);
  _capillary_flow_rate = new svector(_sortedGrid.size);
  _perc_vadose_coeff = new svector(_sortedGrid.size);
  _irrigation_FC_thres = new svector(_sortedGrid.size);
  _diffuse_molecular_coefficient = new svector(_sortedGrid.size);
  _nearsurface_mixing = new svector(_sortedGrid.size);
  _ratio_to_interf = new svector(_sortedGrid.size);
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new svector(_sortedGrid.size);
    _deg_day_min = new svector(_sortedGrid.size);
    _deg_day_max = new svector(_sortedGrid.size);
    _deg_day_increase = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2 or ctrl.opt_pedotransf == 3){
    _ref_thetaS = new svector(_sortedGrid.size);
    _PTF_VG_clay = new svector(_sortedGrid.size);
    _PTF_VG_Db = new svector(_sortedGrid.size);
    _PTF_Ks_const = new svector(_sortedGrid.size);
    _PTF_Ks_sand = new svector(_sortedGrid.size);
    _PTF_Ks_clay = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_fieldcapacity == 1){
    _SWP = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_infil == 1 or ctrl.opt_depthprofile == 2){
    _KvKh = new svector(_sortedGrid.size);
    _psiAE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_depthprofile == 2){
    _KKs = new svector(_sortedGrid.size);
    _Ksat = new svector(_sortedGrid.size);
    _BClambda = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_percolation == 1){
    _perc_optimal_theta = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_percolation == 2){
    _percExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_evap == 1 or ctrl.opt_evap == 2){
    _froot_coeff = new svector(_sortedGrid.size);
    _ET_weight = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_GW == 1){
    _init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routinterf == 1){
    _pOvf_toChn = new svector(_sortedGrid.size);
    _Ks_surface = new svector(_sortedGrid.size);
    _Ks_vadose = new svector(_sortedGrid.size);
    _lat_to_Chn_vadose = new svector(_sortedGrid.size);
    _interfExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routGWf == 1){
    _Ks_GW = new svector(_sortedGrid.size);
    _lat_to_Chn_GW = new svector(_sortedGrid.size);
    _GWfExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routQ == 1){
    _Manningn = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    _Echan_alpha = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_irrigation == 1){
    _irrigation_coeff = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_drainage == 1){
    _drainage_intensity = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_carbon_sim == 1){
    _herbivory_uptake_coeff = new svector(_sortedGrid.size);
    _C_in_LeafArea = new svector(_sortedGrid.size);
    _tau_wood_C = new svector(_sortedGrid.size);
    _plant_wood_CP_max = new svector(_sortedGrid.size);
    _plant_reserve_CP_max = new svector(_sortedGrid.size);
    _carboxylation_rate = new svector(_sortedGrid.size);
    _ETransport = new svector(_sortedGrid.size);
    _frac_NPP_to_green = new svector(_sortedGrid.size);
    _frac_NPP_to_wood = new svector(_sortedGrid.size);
    _alpha_litter_distribution_nonwood = new svector(_sortedGrid.size);
    _frac_leaf_in_litter = new svector(_sortedGrid.size);
    _frac_DOC_production_from_litter_CP = new svector(_sortedGrid.size);
    _frac_DOC_production_from_soil_CP = new svector(_sortedGrid.size);
    _ref_frac_soluble_to_doc = new svector(_sortedGrid.size);
    _frac_soluble_to_doc_weights = new svector(_sortedGrid.size);
    _f_groundwater_depth_decay_exp_base = new svector(_sortedGrid.size);
    _f_groundwater_depth_rescale_factor = new svector(_sortedGrid.size);
    _fdepth_decay_Exp = new svector(_sortedGrid.size);
    _ref_decomp_rate_doc = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_tracking_isotope == 1){
    _CG_n_soil = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_d18o == 1){
    _delta_d18o_init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_no3 == 1){
    _delta_no3_init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_nitrogen_sim == 1){
    _denitrification_river = new svector(_sortedGrid.size);
    _denitrification_soil = new svector(_sortedGrid.size);
    _deni_soil_moisture_thres = new svector(_sortedGrid.size);
    _respiration_river = new svector(_sortedGrid.size);
    _NC_ratio_plant_green = new svector(_sortedGrid.size);
    _NC_ratio_plant_wood = new svector(_sortedGrid.size);
    _NC_ratio_dpm_litter = new svector(_sortedGrid.size);
    _NC_ratio_rpm_litter = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_carbon_sim == 1 or ctrl.opt_carbon_sim == 1){
    _LAI_shed_coef = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_doc == 1){
    _delta_doc_init_GW = new svector(_sortedGrid.size);
  }
  /* end of Parameters */

  // Read parameter values from param.ini
  ReadParamFile(ctrl, fname);

  param_category = new svector_2d(ctrl.num_category , _sortedGrid);

  // Assign parameter spatially
  Parameterisation(ctrl);

}