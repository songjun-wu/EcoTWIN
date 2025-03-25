#include "Basin.h"

Basin::~Basin(){}

int Basin::dtor(Control &ctrl){
  
  /* GIS */
  if(_dem) delete _dem;
  if(_chnwidth) delete _chnwidth;
  if(_chndepth) delete _chndepth;
  if(_chnlength) delete _chnlength;
  if(_depth1) delete _depth1;
  if(_depth2) delete _depth2;
  /* end of GIS */

  /* Storages */
  if(_I) delete _I;
  if(_snow) delete _snow;
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
  if(_Perc3) delete _Perc3;
  if(_Ei) delete _Ei;
  if(_Es) delete _Es;
  if(_Tr) delete _Tr;
  if(_Tr1) delete _Tr1;
  if(_Tr2) delete _Tr2;
  if(_Tr3) delete _Tr3;
  if(_Ks1) delete _Ks1;
  if(_Ks2) delete _Ks2;
  if(_Ks3) delete _Ks3;
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