#include <iostream>
#include "Basin.h"
#include "Atmosphere.h"
#include "Report.h"

#include <chrono>

int main(){

  auto start = std::chrono::high_resolution_clock::now();
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
  
  oBasin->Initialisation(*oControl, *oParam);
  
  auto stop1 = std::chrono::high_resolution_clock::now();
  
  while (oControl->current_ts < oControl->Simul_end){


    oBasin->Solve_timesteps(*oControl, *oParam, *oAtmosphere);

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
    if (advance_landuse >= oControl->Update_interval) {
      oParam->Parameterisation(*oControl); // Parameterisation
      advance_landuse = 0;
  }

  }

  // Deconstructor
  //oAtmosphere->dtor(*oControl);
  //oBasin->dtor(*oControl);
  //oParam->dtor(*oControl);
  //oControl->dtor();

  
  auto stop2  = std::chrono::high_resolution_clock::now();

  auto duration1 = chrono::duration_cast<chrono::microseconds>(stop1 - start);
  auto duration2 = chrono::duration_cast<chrono::microseconds>(stop2 - stop1);

  cout << "Configuration takes : "
         << duration1.count() / 1e6 << " seconds" << endl;
  cout << "Iteration takes : "
         << duration2.count() / 1e6 << " seconds" << endl;

  return 0;
}