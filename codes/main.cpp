/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* main.cpp
  * Created  on: 30.02.2025
  * Modified on: 28.05.2025
***************************************************************/




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
  float advance_groundTs = 0;  // reset to zero when ground_input (e.g., LAI) is updated
  float advance_landuse = 0; // resets to zero when land use inputs is updated
  float advance_age = 0;     // resets to zero when water ages are advanced
  

  oControl = new Control;
  oParam = new Param(*oControl);
  oBasin = new Basin(*oControl, *oParam);
  oAtmosphere = new Atmosphere(*oControl);
  oReport = new Report(*oControl);
  
  oBasin->Initialisation(*oControl, *oParam, *oAtmosphere);
  oReport->Report_Initialisation(*oControl);  // To be re-enabled
  
  auto stop1 = std::chrono::high_resolution_clock::now();

  while (oControl->current_ts < oControl->Simul_end){

    oControl->Get_year_month_day();
    oBasin->Solve_timesteps(*oControl, *oParam, *oAtmosphere);

    // report outputs
    oReport->Report_all(*oControl, *oBasin);  // To be re-enabled

    // Temporary for faster calibration; todo
    oBasin->Report_for_cali(*oControl);

    // Update counter
    oControl->current_ts += oControl->Simul_tstep;
    advance_climate += oControl->Simul_tstep;
    advance_groundTs += oControl->Simul_tstep;
    advance_landuse += oControl->Simul_tstep;
    advance_age += oControl->Simul_tstep;


    // Advance water age
    if (oControl->opt_tracking_age==1){
      if (advance_age >= 86400){
        oBasin->Advance_age();
        advance_age = 0;
      }       
    }



    // Update climate inputs
    if (advance_climate >= oControl->Clim_input_tstep) {
      if (oControl->opt_climate_input_format == 1){
        oAtmosphere->read_climate(*oControl);   
      } else if  (oControl->opt_climate_input_format == 2) {
        oAtmosphere->update_climate(*oControl);
      }
      advance_climate = 0;
    }

    // Update Ground inputs
    if (advance_groundTs >= oControl->Ground_input_tstep) {
      if (oControl->opt_groundTs_input_format == 1){
        oBasin->read_groundTs(*oControl);
      } else if  (oControl->opt_groundTs_input_format == 2) {
        oBasin->update_groundTs(*oControl, *oParam);
      }
      advance_groundTs = 0;
    }

    // Update land use inputs
    if (advance_landuse >= oControl->Update_interval) {
      oParam->Parameterisation(*oControl); // Parameterisation
      advance_landuse = 0;
  }

  }

  // Temporary for faster calibration; todo
  oBasin->Save_for_cali(*oControl);

  // Deconstructor
  //oAtmosphere->dtor(*oControl);
  //oBasin->dtor(*oControl);
  //oParam->dtor(*oControl);
  //oControl->dtor();
  oReport->dtor(*oControl); // To be re-enabled
  
  auto stop2  = std::chrono::high_resolution_clock::now();

  auto duration1 = chrono::duration_cast<chrono::microseconds>(stop1 - start);
  auto duration2 = chrono::duration_cast<chrono::microseconds>(stop2 - stop1);

  cout << "Configuration takes : "
         << duration1.count() / 1e6 << " seconds" << endl;
  cout << "Iteration takes : "
         << duration2.count() / 1e6 << " seconds" << endl;

  return 0;
}