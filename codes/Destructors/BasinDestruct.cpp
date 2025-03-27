#include "Basin.h"

Basin::~Basin(){}

int Basin::dtor(Control &ctrl){
  
  /* GIS */
  if(_chnwidth) delete _chnwidth;
  if(_chndepth) delete _chndepth;
  if(_chnlength) delete _chnlength;
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
    if(_organic2) delete _organic2;
    if(_organic3) delete _organic3;
    if(_bulkdensity2) delete _bulkdensity2;
    if(_bulkdensity3) delete _bulkdensity3;
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2){
    if(_silt1) delete _silt1;
  }
  if (ctrl.opt_depthprofile == 3 or ctrl.opt_pedotransf == 2){
    if(_silt3) delete _silt3;
  }
  /* end of GIS */

  /* Storages */
  if(_I) delete _I;
  if(_snow) delete _snow;
  if(_pond) delete _pond;
  if(_theta1) delete _theta1;
  if(_theta2) delete _theta2;
  if(_theta3) delete _theta3;
  /* end of Storages */

  /* Fluxes */
  if(_D) delete _D;
  if(_Th) delete _Th;
  if(_snowmelt) delete _snowmelt;
  if(_Qs) delete _Qs;
  if(_infilt) delete _infilt;
  if(_Perc1) delete _Perc1;
  if(_Perc2) delete _Perc2;
  if(_Recharge) delete _Recharge;
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
  if (ctrl.opt_evap == 1){
    if(_froot_soil) delete _froot_soil;
    if(_froot_layer2) delete _froot_layer2;
    if(_froot_layer3) delete _froot_layer3;
  }
  /* end of Fluxes */

  return EXIT_SUCCESS;
}