/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* parameterisation.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Param.h"

int Param::Parameterisation(Control &ctrl){

  // Init flags
  sort_perc_travel_time_OK = 0;  
  sort_root_fraction_OK = 0;  
  sort_plant_uptake_OK = 0;  // The plant uptake only needs to be calculated once (or once within each change)
  sort_crop_management_OK = 0;  // The crop management only needs to be calculated once (or once within each change)
  sort_nitrogen_addition_OK = 0;  // The nitrogen addtion only needs to be calculated once (or once within each change)
  sort_parameter_correction_OK = 0;  // The parameter correction only needs to be calculated once (or once within each change)

  // Update the parameterisation due to the changes in land use types
  param_category->update(ctrl.path_BasinFolder+"category_", ctrl.num_category ,_rowNum, _colNum, _sortedGrid);

  /* Parameters */
  int nodata = ctrl._nodata;


  _depth3->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (depth3[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _depth3->val[j] += param_category->val[k][j] * depth3[k];
   }}}

  _alpha->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (alpha[k]!=nodata) {
      double logp = log(alpha[k]);
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _alpha->val[j] += param_category->val[k][j] * logp;
   }}}
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    _alpha->val[j] = exp(_alpha->val[j]);
   }

  _rE->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (rE[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _rE->val[j] += param_category->val[k][j] * rE[k];
   }}}

  _preferential_flow_coeff->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (preferential_flow_coeff[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _preferential_flow_coeff->val[j] += param_category->val[k][j] * preferential_flow_coeff[k];
   }}}

  _capillary_flow_rate->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (capillary_flow_rate[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _capillary_flow_rate->val[j] += param_category->val[k][j] * capillary_flow_rate[k];
   }}}

  _perc_vadose_coeff->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (perc_vadose_coeff[k]!=nodata) {
      double logp = log(perc_vadose_coeff[k]);
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _perc_vadose_coeff->val[j] += param_category->val[k][j] * logp;
   }}}
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    _perc_vadose_coeff->val[j] = exp(_perc_vadose_coeff->val[j]);
   }

  _irrigation_FC_thres->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (irrigation_FC_thres[k]!=nodata) {
      double logp = log(irrigation_FC_thres[k]);
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _irrigation_FC_thres->val[j] += param_category->val[k][j] * logp;
   }}}
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    _irrigation_FC_thres->val[j] = exp(_irrigation_FC_thres->val[j]);
   }

  _diffuse_molecular_coefficient->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (diffuse_molecular_coefficient[k]!=nodata) {
      double logp = log(diffuse_molecular_coefficient[k]);
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _diffuse_molecular_coefficient->val[j] += param_category->val[k][j] * logp;
   }}}
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    _diffuse_molecular_coefficient->val[j] = exp(_diffuse_molecular_coefficient->val[j]);
   }

  _nearsurface_mixing->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (nearsurface_mixing[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _nearsurface_mixing->val[j] += param_category->val[k][j] * nearsurface_mixing[k];
   }}}

  _ratio_to_interf->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (ratio_to_interf[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _ratio_to_interf->val[j] += param_category->val[k][j] * ratio_to_interf[k];
   }}}

  if (ctrl.opt_snow == 1){
  
  _snow_rain_thre->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (snow_rain_thre[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _snow_rain_thre->val[j] += param_category->val[k][j] * snow_rain_thre[k];
     }}}
  
  _deg_day_min->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_min[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _deg_day_min->val[j] += param_category->val[k][j] * deg_day_min[k];
     }}}
  
  _deg_day_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_max[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _deg_day_max->val[j] += param_category->val[k][j] * deg_day_max[k];
     }}}
  
  _deg_day_increase->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_increase[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _deg_day_increase->val[j] += param_category->val[k][j] * deg_day_increase[k];
     }}}

  }

  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2 or ctrl.opt_pedotransf == 3){
  
  _ref_thetaS->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (ref_thetaS[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _ref_thetaS->val[j] += param_category->val[k][j] * ref_thetaS[k];
     }}}
  
  _PTF_VG_clay->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_VG_clay[k]!=nodata) {
        double logp = log(PTF_VG_clay[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _PTF_VG_clay->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _PTF_VG_clay->val[j] = exp(_PTF_VG_clay->val[j]);
     }
  
  _PTF_VG_Db->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_VG_Db[k]!=nodata) {
        double logp = log(PTF_VG_Db[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _PTF_VG_Db->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _PTF_VG_Db->val[j] = exp(_PTF_VG_Db->val[j]);
     }
  
  _PTF_Ks_const->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_Ks_const[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _PTF_Ks_const->val[j] += param_category->val[k][j] * PTF_Ks_const[k];
     }}}
  
  _PTF_Ks_sand->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_Ks_sand[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _PTF_Ks_sand->val[j] += param_category->val[k][j] * PTF_Ks_sand[k];
     }}}
  
  _PTF_Ks_clay->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_Ks_clay[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _PTF_Ks_clay->val[j] += param_category->val[k][j] * PTF_Ks_clay[k];
     }}}

  }

  if (ctrl.opt_fieldcapacity == 1){
  
  _SWP->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (SWP[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _SWP->val[j] += param_category->val[k][j] * SWP[k];
     }}}

  }

  if (ctrl.opt_infil == 1 or ctrl.opt_depthprofile == 2){
  
  _KvKh->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (KvKh[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _KvKh->val[j] += param_category->val[k][j] * KvKh[k];
     }}}
  
  _psiAE->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (psiAE[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _psiAE->val[j] += param_category->val[k][j] * psiAE[k];
     }}}

  }

  if (ctrl.opt_depthprofile == 2){
  
  _KKs->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (KKs[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _KKs->val[j] += param_category->val[k][j] * KKs[k];
     }}}
  
  _Ksat->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Ksat[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Ksat->val[j] += param_category->val[k][j] * Ksat[k];
     }}}
  
  _BClambda->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (BClambda[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _BClambda->val[j] += param_category->val[k][j] * BClambda[k];
     }}}

  }

  if (ctrl.opt_percolation == 1){
  
  _perc_optimal_theta->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (perc_optimal_theta[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _perc_optimal_theta->val[j] += param_category->val[k][j] * perc_optimal_theta[k];
     }}}

  }

  if (ctrl.opt_percolation == 2){
  
  _percExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (percExp[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _percExp->val[j] += param_category->val[k][j] * percExp[k];
     }}}

  }

  if (ctrl.opt_evap == 1 or ctrl.opt_evap == 2){
  
  _froot_coeff->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (froot_coeff[k]!=nodata) {
        double logp = log(froot_coeff[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _froot_coeff->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _froot_coeff->val[j] = exp(_froot_coeff->val[j]);
     }
  
  _ET_weight->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (ET_weight[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _ET_weight->val[j] += param_category->val[k][j] * ET_weight[k];
     }}}

  }

  if (ctrl.opt_init_GW == 1){
  
  _init_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (init_GW[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _init_GW->val[j] += param_category->val[k][j] * init_GW[k];
     }}}

  }

  if (ctrl.opt_routinterf == 1){
  
  _pOvf_toChn->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (pOvf_toChn[k]!=nodata) {
        double logp = log(pOvf_toChn[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _pOvf_toChn->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _pOvf_toChn->val[j] = exp(_pOvf_toChn->val[j]);
     }
  
  _Ks_surface->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Ks_surface[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Ks_surface->val[j] += param_category->val[k][j] * Ks_surface[k];
     }}}
  
  _Ks_vadose->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Ks_vadose[k]!=nodata) {
        double logp = log(Ks_vadose[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Ks_vadose->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _Ks_vadose->val[j] = exp(_Ks_vadose->val[j]);
     }
  
  _lat_to_Chn_vadose->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (lat_to_Chn_vadose[k]!=nodata) {
        double logp = log(lat_to_Chn_vadose[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _lat_to_Chn_vadose->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _lat_to_Chn_vadose->val[j] = exp(_lat_to_Chn_vadose->val[j]);
     }
  
  _interfExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (interfExp[k]!=nodata) {
        double logp = log(interfExp[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _interfExp->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _interfExp->val[j] = exp(_interfExp->val[j]);
     }

  }

  if (ctrl.opt_routGWf == 1){
  
  _Ks_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Ks_GW[k]!=nodata) {
        double logp = log(Ks_GW[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Ks_GW->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _Ks_GW->val[j] = exp(_Ks_GW->val[j]);
     }
  
  _lat_to_Chn_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (lat_to_Chn_GW[k]!=nodata) {
        double logp = log(lat_to_Chn_GW[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _lat_to_Chn_GW->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _lat_to_Chn_GW->val[j] = exp(_lat_to_Chn_GW->val[j]);
     }
  
  _GWfExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (GWfExp[k]!=nodata) {
        double logp = log(GWfExp[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _GWfExp->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _GWfExp->val[j] = exp(_GWfExp->val[j]);
     }

  }

  if (ctrl.opt_routQ == 1){
  
  _Manningn->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Manningn[k]!=nodata) {
        double logp = log(Manningn[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Manningn->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _Manningn->val[j] = exp(_Manningn->val[j]);
     }

  }

  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
  
  _Echan_alpha->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Echan_alpha[k]!=nodata) {
        double logp = log(Echan_alpha[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _Echan_alpha->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _Echan_alpha->val[j] = exp(_Echan_alpha->val[j]);
     }

  }

  if (ctrl.opt_irrigation == 1){
  
  _irrigation_coeff->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (irrigation_coeff[k]!=nodata) {
        double logp = log(irrigation_coeff[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _irrigation_coeff->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _irrigation_coeff->val[j] = exp(_irrigation_coeff->val[j]);
     }

  }

  if (ctrl.opt_drainage == 1){
  
  _drainage_intensity->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (drainage_intensity[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _drainage_intensity->val[j] += param_category->val[k][j] * drainage_intensity[k];
     }}}

  }

  if (ctrl.opt_carbon_sim == 1){
  
  _herbivory_uptake_coeff->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (herbivory_uptake_coeff[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _herbivory_uptake_coeff->val[j] += param_category->val[k][j] * herbivory_uptake_coeff[k];
     }}}
  
  _C_in_LeafArea->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (C_in_LeafArea[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _C_in_LeafArea->val[j] += param_category->val[k][j] * C_in_LeafArea[k];
     }}}
  
  _tau_wood_C->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (tau_wood_C[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _tau_wood_C->val[j] += param_category->val[k][j] * tau_wood_C[k];
     }}}
  
  _plant_wood_CP_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (plant_wood_CP_max[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _plant_wood_CP_max->val[j] += param_category->val[k][j] * plant_wood_CP_max[k];
     }}}
  
  _plant_reserve_CP_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (plant_reserve_CP_max[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _plant_reserve_CP_max->val[j] += param_category->val[k][j] * plant_reserve_CP_max[k];
     }}}
  
  _carboxylation_rate->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (carboxylation_rate[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _carboxylation_rate->val[j] += param_category->val[k][j] * carboxylation_rate[k];
     }}}
  
  _ETransport->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (ETransport[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _ETransport->val[j] += param_category->val[k][j] * ETransport[k];
     }}}
  
  _frac_NPP_to_green->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_NPP_to_green[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_NPP_to_green->val[j] += param_category->val[k][j] * frac_NPP_to_green[k];
     }}}
  
  _frac_NPP_to_wood->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_NPP_to_wood[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_NPP_to_wood->val[j] += param_category->val[k][j] * frac_NPP_to_wood[k];
     }}}
  
  _alpha_litter_distribution_nonwood->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (alpha_litter_distribution_nonwood[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _alpha_litter_distribution_nonwood->val[j] += param_category->val[k][j] * alpha_litter_distribution_nonwood[k];
     }}}
  
  _frac_leaf_in_litter->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_leaf_in_litter[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_leaf_in_litter->val[j] += param_category->val[k][j] * frac_leaf_in_litter[k];
     }}}
  
  _frac_DOC_production_from_litter_CP->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_DOC_production_from_litter_CP[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_DOC_production_from_litter_CP->val[j] += param_category->val[k][j] * frac_DOC_production_from_litter_CP[k];
     }}}
  
  _frac_DOC_production_from_soil_CP->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_DOC_production_from_soil_CP[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_DOC_production_from_soil_CP->val[j] += param_category->val[k][j] * frac_DOC_production_from_soil_CP[k];
     }}}
  
  _ref_frac_soluble_to_doc->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (ref_frac_soluble_to_doc[k]!=nodata) {
        double logp = log(ref_frac_soluble_to_doc[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _ref_frac_soluble_to_doc->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _ref_frac_soluble_to_doc->val[j] = exp(_ref_frac_soluble_to_doc->val[j]);
     }
  
  _frac_soluble_to_doc_weights->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (frac_soluble_to_doc_weights[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _frac_soluble_to_doc_weights->val[j] += param_category->val[k][j] * frac_soluble_to_doc_weights[k];
     }}}
  
  _f_groundwater_depth_decay_exp_base->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (f_groundwater_depth_decay_exp_base[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _f_groundwater_depth_decay_exp_base->val[j] += param_category->val[k][j] * f_groundwater_depth_decay_exp_base[k];
     }}}
  
  _f_groundwater_depth_rescale_factor->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (f_groundwater_depth_rescale_factor[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _f_groundwater_depth_rescale_factor->val[j] += param_category->val[k][j] * f_groundwater_depth_rescale_factor[k];
     }}}
  
  _fdepth_decay_Exp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (fdepth_decay_Exp[k]!=nodata) {
        double logp = log(fdepth_decay_Exp[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _fdepth_decay_Exp->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _fdepth_decay_Exp->val[j] = exp(_fdepth_decay_Exp->val[j]);
     }
  
  _ref_decomp_rate_doc->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (ref_decomp_rate_doc[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _ref_decomp_rate_doc->val[j] += param_category->val[k][j] * ref_decomp_rate_doc[k];
     }}}

  }

  if (ctrl.opt_tracking_isotope == 1){
  
  _CG_n_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (CG_n_soil[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _CG_n_soil->val[j] += param_category->val[k][j] * CG_n_soil[k];
     }}}

  }

  if (ctrl.opt_init_d18o == 1){
  
  _delta_d18o_init_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (delta_d18o_init_GW[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _delta_d18o_init_GW->val[j] += param_category->val[k][j] * delta_d18o_init_GW[k];
     }}}

  }

  if (ctrl.opt_init_no3 == 1){
  
  _delta_no3_init_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (delta_no3_init_GW[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _delta_no3_init_GW->val[j] += param_category->val[k][j] * delta_no3_init_GW[k];
     }}}

  }

  if (ctrl.opt_nitrogen_sim == 1){
  
  _denitrification_river->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (denitrification_river[k]!=nodata) {
        double logp = log(denitrification_river[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _denitrification_river->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _denitrification_river->val[j] = exp(_denitrification_river->val[j]);
     }
  
  _denitrification_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (denitrification_soil[k]!=nodata) {
        double logp = log(denitrification_soil[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _denitrification_soil->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _denitrification_soil->val[j] = exp(_denitrification_soil->val[j]);
     }
  
  _deni_soil_moisture_thres->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deni_soil_moisture_thres[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _deni_soil_moisture_thres->val[j] += param_category->val[k][j] * deni_soil_moisture_thres[k];
     }}}
  
  _respiration_river->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (respiration_river[k]!=nodata) {
        double logp = log(respiration_river[k]);
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _respiration_river->val[j] += param_category->val[k][j] * logp;
     }}}
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _respiration_river->val[j] = exp(_respiration_river->val[j]);
     }
  
  _NC_ratio_plant_green->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (NC_ratio_plant_green[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _NC_ratio_plant_green->val[j] += param_category->val[k][j] * NC_ratio_plant_green[k];
     }}}
  
  _NC_ratio_plant_wood->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (NC_ratio_plant_wood[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _NC_ratio_plant_wood->val[j] += param_category->val[k][j] * NC_ratio_plant_wood[k];
     }}}
  
  _NC_ratio_dpm_litter->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (NC_ratio_dpm_litter[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _NC_ratio_dpm_litter->val[j] += param_category->val[k][j] * NC_ratio_dpm_litter[k];
     }}}
  
  _NC_ratio_rpm_litter->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (NC_ratio_rpm_litter[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _NC_ratio_rpm_litter->val[j] += param_category->val[k][j] * NC_ratio_rpm_litter[k];
     }}}

  }

  if (ctrl.opt_carbon_sim == 1 or ctrl.opt_carbon_sim == 1){
  
  _LAI_shed_coef->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (LAI_shed_coef[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _LAI_shed_coef->val[j] += param_category->val[k][j] * LAI_shed_coef[k];
     }}}

  }

  if (ctrl.opt_init_doc == 1){
  
  _delta_doc_init_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (delta_doc_init_GW[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
          _delta_doc_init_GW->val[j] += param_category->val[k][j] * delta_doc_init_GW[k];
     }}}

  }
  /* end of Parameters */


  
  return EXIT_SUCCESS;
}