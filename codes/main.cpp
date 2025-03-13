#include <iostream>
#include "Basin.h"
#include "Atmosphere.h"


int main(){
  Control *oControl;
  Basin *oBasin;
  Atmosphere *oAtmosphere;
  
  oControl = new Control;
  oBasin = new Basin(*oControl);
  oAtmosphere = new Atmosphere(*oControl, *oBasin); 
  
  while (oControl->current_ts < oControl->Simul_end){

    oBasin->report(*oControl); // report all basin outputs
    oAtmosphere->read_climate(*oControl);
    oControl->current_ts += oControl->Simul_tstep;
  }


  //delete oControl;
  delete oBasin;
  delete oAtmosphere;

  return 0;
}