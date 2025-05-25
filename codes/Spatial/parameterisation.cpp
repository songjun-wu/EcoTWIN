#include "Param.h"

int Param::Parameterisation(Control &ctrl){

  // Init flags
  sort_perc_travel_time_OK = 0;  
  sort_root_fraction_OK = 0;  
  sort_plant_uptake_OK = 0;  // The plant uptake only needs to be calculated once (or once within each change)
  sort_nitrogen_addition_OK = 0;  // The nitrogen addtion only needs to be calculated once (or once within each change)

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
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _alpha->val[j] += param_category->val[k][j] * alpha[k];
   }}}

  _wRecharge->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (wRecharge[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _wRecharge->val[j] += param_category->val[k][j] * wRecharge[k];
   }}}

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

  if (ctrl.opt_intecept == 2 or ctrl.opt_evap == 1){
  
  _rE->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (rE[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _rE->val[j] += param_category->val[k][j] * rE[k];
     }}}

  }

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

  if (ctrl.opt_evap == 1){
  
  _froot_coeff->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (froot_coeff[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _froot_coeff->val[j] += param_category->val[k][j] * froot_coeff[k];
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
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _PTF_VG_clay->val[j] += param_category->val[k][j] * PTF_VG_clay[k];
     }}}
  
  _PTF_VG_Db->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_VG_Db[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _PTF_VG_Db->val[j] += param_category->val[k][j] * PTF_VG_Db[k];
     }}}
  
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
  
  _PTF_Ks_slope->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (PTF_Ks_slope[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _PTF_Ks_slope->val[j] += param_category->val[k][j] * PTF_Ks_slope[k];
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

  if (ctrl.opt_percolation == 2){
  
  _percExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (percExp[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _percExp->val[j] += param_category->val[k][j] * percExp[k];
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
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _pOvf_toChn->val[j] += param_category->val[k][j] * pOvf_toChn[k];
     }}}
  
  _interfExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (interfExp[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _interfExp->val[j] += param_category->val[k][j] * interfExp[k];
     }}}
  
  _winterf->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (winterf[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _winterf->val[j] += param_category->val[k][j] * winterf[k];
     }}}

  }

  if (ctrl.opt_routGWf == 1){
  
  _GWfExp->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (GWfExp[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _GWfExp->val[j] += param_category->val[k][j] * GWfExp[k];
     }}}
  
  _wGWf->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (wGWf[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _wGWf->val[j] += param_category->val[k][j] * wGWf[k];
     }}}

  }

  if (ctrl.opt_routQ == 1){
  
  _Manningn->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Manningn[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _Manningn->val[j] += param_category->val[k][j] * Manningn[k];
     }}}

  }

  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
  
  _Echan_alpha->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (Echan_alpha[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _Echan_alpha->val[j] += param_category->val[k][j] * Echan_alpha[k];
     }}}

  }

  if (ctrl.opt_irrigation == 1){
  
  _irrigation_coeff->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (irrigation_coeff[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _irrigation_coeff->val[j] += param_category->val[k][j] * irrigation_coeff[k];
     }}}

  }

  if (ctrl.opt_tracking_isotope == 1){
  
  _CG_n_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (CG_n_soil[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _CG_n_soil->val[j] += param_category->val[k][j] * CG_n_soil[k];
     }}}
  
  _d18o_init_GW->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (d18o_init_GW[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _d18o_init_GW->val[j] += param_category->val[k][j] * d18o_init_GW[k];
     }}}

  }

  if (ctrl.opt_nitrogen_sim == 1){
  
  _denitrification_river->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (denitrification_river[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _denitrification_river->val[j] += param_category->val[k][j] * denitrification_river[k];
     }}}
  
  _denitrification_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (denitrification_soil[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _denitrification_soil->val[j] += param_category->val[k][j] * denitrification_soil[k];
     }}}
  
  _degradation_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (degradation_soil[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _degradation_soil->val[j] += param_category->val[k][j] * degradation_soil[k];
     }}}
  
  _mineralisation_soil->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (mineralisation_soil[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _mineralisation_soil->val[j] += param_category->val[k][j] * mineralisation_soil[k];
     }}}
  
  _deni_soil_moisture_thres->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deni_soil_moisture_thres[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _deni_soil_moisture_thres->val[j] += param_category->val[k][j] * deni_soil_moisture_thres[k];
     }}}

  }
  /* end of Parameters */

  return EXIT_SUCCESS;
}