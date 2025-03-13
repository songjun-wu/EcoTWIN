#include "Basin.h"

Basin::~Basin(){
  
  /* GIS */
  if(_dem) delete _dem;
  if(_fdir) delete _fdir;
  if(_chnwidth) delete _chnwidth;
  if(_chndepth) delete _chndepth;
  if(_chnlength) delete _chnlength;
  if(_depth1) delete _depth1;
  if(_depth2) delete _depth2;
  if(_depth3) delete _depth3;
  if(_Gauge_to_Report) delete _Gauge_to_Report;
  /* end of GIS */

  /* Storages */
  if(_I) delete _I;
  if(_snow) delete _snow;
  if(_theta1) delete _theta1;
  if(_theta2) delete _theta2;
  if(_theta3) delete _theta3;
  if(_I_old) delete _I_old;
  /* end of Storages */

  /* Fluxes */
  if(_D) delete _D;
  if(_Th) delete _Th;
  if(_snowmelt) delete _snowmelt;
  if(_Qs) delete _Qs;
  if(_infilt) delete _infilt;
  if(_preferential2) delete _preferential2;
  if(_preferential3) delete _preferential3;
  if(_Perc1) delete _Perc1;
  if(_Perc2) delete _Perc2;
  if(_Perc3) delete _Perc3;
  if(_Ei) delete _Ei;
  if(_Es) delete _Es;
  if(_Tr) delete _Tr;
  if(_Tr1) delete _Tr1;
  if(_Tr2) delete _Tr2;
  if(_Tr3) delete _Tr3;
  /* end of Fluxes */

}