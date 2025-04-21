#include "Basin.h"

Basin::~Basin(){}

int Basin::dtor(Control &ctrl){
  
  /* GIS */
  if(_chnwidth) delete _chnwidth;
  if(_chndepth) delete _chndepth;
  if(_chnlength) delete _chnlength;
  if(_slope) delete _slope;
  if(_depth1) delete _depth1;
  if(_depth2) delete _depth2;
  if(_sand1) delete _sand1;
  if(_clay1) delete _clay1;
  if(_organic1) delete _organic1;
  if(_bulkdensity1) delete _bulkdensity1;
  if (ctrl.opt_depthprofile == 3){
    if(_sand2) delete _sand2;
    if(_sand3) delete _sand3;
    if(_clay2) delete _clay2;
    if(_clay3) delete _clay3;
    if(_silt2) delete _silt2;
    if(_silt3) delete _silt3;
    if(_organic2) delete _organic2;
    if(_organic3) delete _organic3;
    if(_bulkdensity2) delete _bulkdensity2;
    if(_bulkdensity3) delete _bulkdensity3;
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2){
    if(_silt1) delete _silt1;
  }
  /* end of GIS */

  /* GroundTs */
  if (if__LAI.is_open())  if__LAI.close();
  if(_LAI) delete _LAI;
  /* end of GroundTs */

  /* Storages */
  if(_I) delete _I;
  if(_snow) delete _snow;
  if(_pond) delete _pond;
  if(_theta1) delete _theta1;
  if(_theta2) delete _theta2;
  if(_theta3) delete _theta3;
  if(_GW) delete _GW;
  if(_chanS) delete _chanS;
  if (ctrl.opt_tracking_isotope == 1 or ctrl.opt_tracking_age == 1 or ctrl.opt_nitrogen_sim == 1){
    if(_I_old) delete _I_old;
    if(_snow_old) delete _snow_old;
    if(_pond_old) delete _pond_old;
    if(_theta1_old) delete _theta1_old;
    if(_theta2_old) delete _theta2_old;
    if(_theta3_old) delete _theta3_old;
    if(_GW_old) delete _GW_old;
    if(_chanS_old) delete _chanS_old;
  }
  /* end of Storages */

  /* Fluxes */
  if(_Th) delete _Th;
  if(_snowmelt) delete _snowmelt;
  if(_infilt) delete _infilt;
  if(_Perc1) delete _Perc1;
  if(_Perc2) delete _Perc2;
  if(_Perc3) delete _Perc3;
  if(_rrPerc3) delete _rrPerc3;
  if(_Ei) delete _Ei;
  if(_Es) delete _Es;
  if(_Tr) delete _Tr;
  if(_Tr1) delete _Tr1;
  if(_Tr2) delete _Tr2;
  if(_Tr3) delete _Tr3;
  if(_Ks1) delete _Ks1;
  if(_Ks2) delete _Ks2;
  if(_Ks3) delete _Ks3;
  if(_thetaS1) delete _thetaS1;
  if(_thetaS2) delete _thetaS2;
  if(_thetaS3) delete _thetaS3;
  if(_thetaFC1) delete _thetaFC1;
  if(_thetaFC2) delete _thetaFC2;
  if(_thetaFC3) delete _thetaFC3;
  if(_thetaWP1) delete _thetaWP1;
  if(_thetaWP2) delete _thetaWP2;
  if(_thetaWP3) delete _thetaWP3;
  if(_ovf_in) delete _ovf_in;
  if(_ovf_out) delete _ovf_out;
  if(_ovf_toChn) delete _ovf_toChn;
  if(_interf_in) delete _interf_in;
  if(_interf_out) delete _interf_out;
  if(_interf_toChn) delete _interf_toChn;
  if(_GWf_in) delete _GWf_in;
  if(_GWf_out) delete _GWf_out;
  if(_GWf_toChn) delete _GWf_toChn;
  if(_Q) delete _Q;
  if(_Qupstream) delete _Qupstream;
  if(_tmp) delete _tmp;
  if(_snowacc) delete _snowacc;
  if (ctrl.opt_reinfil == 1){
    if(_rinfilt) delete _rinfilt;
    if(_rPerc1) delete _rPerc1;
    if(_rPerc2) delete _rPerc2;
    if(_rPerc3) delete _rPerc3;
  }
  if (ctrl.opt_evap == 1){
    if(_froot_layer1) delete _froot_layer1;
    if(_froot_layer2) delete _froot_layer2;
    if(_froot_layer3) delete _froot_layer3;
    if(_PE) delete _PE;
    if(_PT) delete _PT;
  }
  if (ctrl.opt_percolation == 1){
    if(_p_perc1) delete _p_perc1;
    if(_p_perc2) delete _p_perc2;
    if(_p_perc3) delete _p_perc3;
  }
  if (ctrl.opt_nitrogen_sim == 1){
    if(_deni_soil) delete _deni_soil;
    if(_minerl_soil) delete _minerl_soil;
  }
  /* end of Fluxes */

  /* Tracking */
  if (ctrl.opt_tracking_isotope == 1){
    if(_d18o_I) delete _d18o_I;
    if(_d18o_snow) delete _d18o_snow;
    if(_d18o_pond) delete _d18o_pond;
    if(_d18o_layer1) delete _d18o_layer1;
    if(_d18o_layer2) delete _d18o_layer2;
    if(_d18o_layer3) delete _d18o_layer3;
    if(_d18o_GW) delete _d18o_GW;
    if(_d18o_chanS) delete _d18o_chanS;
    if(_d18o_ovf_in_acc) delete _d18o_ovf_in_acc;
    if(_d18o_interf_in_acc) delete _d18o_interf_in_acc;
    if(_d18o_GWf_in_acc) delete _d18o_GWf_in_acc;
    if(_d18o_Qupstream_acc) delete _d18o_Qupstream_acc;
  }
  /* end of Tracking */

  /* Nitrogen */
  if (ctrl.opt_nitrogen_sim == 1){
    if(_no3_I) delete _no3_I;
    if(_no3_snow) delete _no3_snow;
    if(_no3_pond) delete _no3_pond;
    if(_no3_layer1) delete _no3_layer1;
    if(_no3_layer2) delete _no3_layer2;
    if(_no3_layer3) delete _no3_layer3;
    if(_no3_GW) delete _no3_GW;
    if(_no3_chanS) delete _no3_chanS;
    if(_humusN1) delete _humusN1;
    if(_humusN2) delete _humusN2;
    if(_humusN3) delete _humusN3;
    if(_fastN1) delete _fastN1;
    if(_fastN2) delete _fastN2;
    if(_fastN3) delete _fastN3;
    if(_no3_ovf_in_acc) delete _no3_ovf_in_acc;
    if(_no3_interf_in_acc) delete _no3_interf_in_acc;
    if(_no3_GWf_in_acc) delete _no3_GWf_in_acc;
    if(_no3_Qupstream_acc) delete _no3_Qupstream_acc;
  }
  /* end of Nitrogen */

  return EXIT_SUCCESS;
}