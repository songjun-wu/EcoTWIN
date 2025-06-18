/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ParamDestruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Param.h"

Param::~Param(){}

int Param::dtor(Control &ctrl){
  
  /* Parameters */
  if(_depth3) delete _depth3;
  if(_alpha) delete _alpha;
  if(_irrigation_FC_thres) delete _irrigation_FC_thres;
  if(_perc_vadose_coeff) delete _perc_vadose_coeff;
  if(_nearsurface_mixing) delete _nearsurface_mixing;
  if(_ratio_to_interf) delete _ratio_to_interf;
  if (ctrl.opt_intecept == 2 or ctrl.opt_evap == 1){
    if(_rE) delete _rE;
  }
  if (ctrl.opt_snow == 1){
    if(_snow_rain_thre) delete _snow_rain_thre;
    if(_deg_day_min) delete _deg_day_min;
    if(_deg_day_max) delete _deg_day_max;
    if(_deg_day_increase) delete _deg_day_increase;
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2 or ctrl.opt_pedotransf == 3){
    if(_ref_thetaS) delete _ref_thetaS;
    if(_PTF_VG_clay) delete _PTF_VG_clay;
    if(_PTF_VG_Db) delete _PTF_VG_Db;
    if(_PTF_Ks_const) delete _PTF_Ks_const;
    if(_PTF_Ks_sand) delete _PTF_Ks_sand;
    if(_PTF_Ks_clay) delete _PTF_Ks_clay;
  }
  if (ctrl.opt_fieldcapacity == 1){
    if(_SWP) delete _SWP;
  }
  if (ctrl.opt_infil == 1 or ctrl.opt_depthprofile == 2){
    if(_KvKh) delete _KvKh;
    if(_psiAE) delete _psiAE;
  }
  if (ctrl.opt_depthprofile == 2){
    if(_KKs) delete _KKs;
    if(_Ksat) delete _Ksat;
    if(_BClambda) delete _BClambda;
  }
  if (ctrl.opt_percolation == 2){
    if(_percExp) delete _percExp;
  }
  if (ctrl.opt_evap == 1){
    if(_froot_coeff) delete _froot_coeff;
    if(_ET_reduction) delete _ET_reduction;
  }
  if (ctrl.opt_init_GW == 1){
    if(_init_GW) delete _init_GW;
  }
  if (ctrl.opt_routinterf == 1){
    if(_pOvf_toChn) delete _pOvf_toChn;
    if(_Ks_vadose) delete _Ks_vadose;
    if(_lat_to_Chn_vadose) delete _lat_to_Chn_vadose;
    if(_interfExp) delete _interfExp;
  }
  if (ctrl.opt_routGWf == 1){
    if(_Ks_GW) delete _Ks_GW;
    if(_lat_to_Chn_GW) delete _lat_to_Chn_GW;
    if(_GWfExp) delete _GWfExp;
  }
  if (ctrl.opt_routQ == 1){
    if(_Manningn) delete _Manningn;
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    if(_Echan_alpha) delete _Echan_alpha;
  }
  if (ctrl.opt_irrigation == 1){
    if(_irrigation_coeff) delete _irrigation_coeff;
  }
  if (ctrl.opt_tracking_isotope == 1){
    if(_CG_n_soil) delete _CG_n_soil;
  }
  if (ctrl.opt_init_d18o == 1){
    if(_delta_d18o_init_GW) delete _delta_d18o_init_GW;
  }
  if (ctrl.opt_init_no3 == 1){
    if(_delta_no3_init_GW) delete _delta_no3_init_GW;
  }
  if (ctrl.opt_nitrogen_sim == 1){
    if(_denitrification_river) delete _denitrification_river;
    if(_denitrification_soil) delete _denitrification_soil;
    if(_degradation_soil) delete _degradation_soil;
    if(_mineralisation_soil) delete _mineralisation_soil;
    if(_deni_soil_moisture_thres) delete _deni_soil_moisture_thres;
  }
  /* end of Parameters */

  if(param_category) delete param_category;

  return EXIT_SUCCESS;

}