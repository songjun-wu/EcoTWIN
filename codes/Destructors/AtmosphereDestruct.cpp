#include "Atmosphere.h"

Atmosphere::~Atmosphere(){}

int Atmosphere::dtor(Control &ctrl){

  if(_climzones)  delete _climzones;

  /* end of GIS */

  /* Climate */
  if (if__P.is_open())  if__P.close();
  if(_P) delete _P;
  if (if__Ta.is_open())  if__Ta.close();
  if(_Ta) delete _Ta;
  if (if__RH.is_open())  if__RH.close();
  if(_RH) delete _RH;
  if (ctrl.opt_evap == 1){
    if (if__PET.is_open())  if__PET.close();
    if(_PET) delete _PET;
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    if (if__airpressure.is_open())  if__airpressure.close();
    if(_airpressure) delete _airpressure;
    if (if__Rnet.is_open())  if__Rnet.close();
    if(_Rnet) delete _Rnet;
  }
  if (ctrl.opt_chanE == 1){
    if (if__windspeed.is_open())  if__windspeed.close();
    if(_windspeed) delete _windspeed;
  }
  if (ctrl.opt_tracking_isotope == 1){
    if (if__d18o_P.is_open())  if__d18o_P.close();
    if(_d18o_P) delete _d18o_P;
  }
  /* end of Climate */

  return EXIT_SUCCESS;

}