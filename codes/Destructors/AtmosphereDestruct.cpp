#include "Atmosphere.h"

Atmosphere::~Atmosphere(){}

int Atmosphere::dtor(Control &ctrl){

  if(_climzones)  delete _climzones;

  /* end of GIS */

  /* Climate */
  if (+if__P.is_open())  if__P.close();
  if(_P) delete _P;
  if (+if__Ta.is_open())  if__Ta.close();
  if(_Ta) delete _Ta;
  if (+if__RH.is_open())  if__RH.close();
  if(_RH) delete _RH;
  if (+if__LAI.is_open())  if__LAI.close();
  if(_LAI) delete _LAI;
  if (ctrl.opt_evap == 1){
    if (+if__PET.is_open())  if__PET.close();
    if(_PET) delete _PET;
  }
  /* end of Climate */

  return EXIT_SUCCESS;

}