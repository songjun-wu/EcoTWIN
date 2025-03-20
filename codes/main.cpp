#include <iostream>
#include "Basin.h"
#include "Atmosphere.h"
#include "Param.h"

int main(){
  Control *oControl;
  Basin *oBasin;
  Atmosphere *oAtmosphere;
  Param *oParam;

  float advance_climate = 0; // resets to zero when Clim_input is updated
  float advance_landuse = 0; // resets to zero when land use inputs is updated
  
  oControl = new Control;
  oBasin = new Basin(*oControl);
  oAtmosphere = new Atmosphere(*oControl, *oBasin);
  oParam = new Param(*oControl);
  
  while (oControl->current_ts < oControl->Simul_end){

    oBasin->report(*oControl); // report all basin outputs
    oAtmosphere->read_climate(*oControl);
    oControl->current_ts += oControl->Simul_tstep;
  }

  advance_climate += oControl->Simul_tstep;
  advance_landuse += oControl->Simul_tstep;
  // Update climate inputs
  if (advance_climate >= oControl->Clim_input_tstep) {
    oAtmosphere->read_climate(*oControl);
    advance_climate = 0;
  }
  // Update land use inputs
  if (advance_landuse >= oControl->Clim_input_tstep) {
    // do the parameterisation again; todo
    advance_landuse = 0;
  }

  //delete oControl;
  delete oBasin;
  delete oAtmosphere;
  delete oParam;

  return 0;
}