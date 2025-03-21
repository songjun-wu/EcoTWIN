#include <iostream>
#include "Basin.h"
#include "Atmosphere.h"
#include "Report.h"

int main(){
  Control *oControl;
  Basin *oBasin;
  Atmosphere *oAtmosphere;
  Param *oParam;
  Report *oReport;

  float advance_climate = 0; // resets to zero when Clim_input is updated
  float advance_landuse = 0; // resets to zero when land use inputs is updated
  
  oControl = new Control;
  oBasin = new Basin(*oControl);
  oAtmosphere = new Atmosphere(*oControl);
  oParam = new Param(*oControl);
  
  while (oControl->current_ts < oControl->Simul_end){
    



    // report outputs
    oReport->report(*oControl, *oBasin); 

    
   
    // Update climate and land use status
    oControl->current_ts += oControl->Simul_tstep;
    advance_climate += oControl->Simul_tstep;
    advance_landuse += oControl->Simul_tstep;

    // Update climate inputs
    if (advance_climate >= oControl->Clim_input_tstep) {
      if (oControl->opt_climate_input_format == 1){
      oAtmosphere->read_climate(*oControl);
    } else if  (oControl->opt_climate_input_format == 2) {
      oAtmosphere->update_climate(*oControl);
    }
      advance_climate = 0;
    }

    // Update land use inputs
    if (advance_landuse >= oControl->Clim_input_tstep) {
      oParam->Parameterisation(*oControl); // Parameterisation
      advance_landuse = 0;
  }

  }



  //delete oControl;
  delete oBasin;
  delete oAtmosphere;
  delete oParam;

  return 0;
}