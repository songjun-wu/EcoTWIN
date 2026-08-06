/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ControlConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Control.h"

Control::Control(){

  current_ts = 0;

  basetime = Set_reference_timestep();

  string confilename = "config.ini";

  ReadConfigFile(confilename);
  getAsciiHeader(path_BasinFolder+fn__depth1);

  //sort grids spatially
  _fdir = new grid(path_BasinFolder + fn__fdir, _rowNum, _colNum);
  _chnwidth_grid = new grid(path_BasinFolder + fn__chnwidth, _rowNum, _colNum);
  _sortedGrid = SortGridLDD();
  
  _Gauge_to_Report = new svector(path_BasinFolder + fn__Gauge_to_Report, _rowNum, _colNum, _sortedGrid);
  _Tsmask = sortTSmask();


  // ===== Option correction =====
  // Nitrogen simulation is dependent on carbon simulation
  if (opt_nitrogen_sim==1){
    opt_carbon_sim = 1;
  } else if (opt_nitrogen_sim==0){
    opt_carbon_sim = 0;
  }

  if (opt_carbon_sim==0 and opt_evap==2){
    opt_evap = 1;
  }

  // Summary statistics
  if (opt_summary_statistics==0){
    if (opt_carbon_sim==1){
      report__plant_C = 0;
    }
    if (opt_nitrogen_sim==1){
    }

  /* Correction of report flags */
  if (!(opt_reinfil == 1)){
    report__rinfilt = 0;
    report__rPerc1 = 0;
    report__rPerc2 = 0;
    report__rPerc3 = 0;
  }
  if (!(opt_drainage == 1)){
    report__drainage_from_soil = 0;
    report__drainage_from_layer1 = 0;
    report__drainage_from_layer2 = 0;
    report__drainage_from_layer3 = 0;
  }
  if (!(opt_tracking_isotope == 1)){
    report__d18o_I = 0;
    report__d18o_snow = 0;
    report__d18o_pond = 0;
    report__d18o_layer1 = 0;
    report__d18o_layer2 = 0;
    report__d18o_layer3 = 0;
    report__d18o_vadose = 0;
    report__d18o_GW = 0;
    report__d18o_chanS = 0;
    report__age_vadose = 0;
  }
  if (!(opt_tracking_age == 1)){
    report__age_I = 0;
    report__age_snow = 0;
    report__age_pond = 0;
    report__age_layer1 = 0;
    report__age_layer2 = 0;
    report__age_layer3 = 0;
    report__age_GW = 0;
    report__age_chanS = 0;
  }
  if (!(opt_tracking_trans_age == 1)){
    report__trans_age_I = 0;
    report__trans_age_snow = 0;
    report__trans_age_pond = 0;
    report__trans_age_layer1 = 0;
    report__trans_age_layer2 = 0;
    report__trans_age_layer3 = 0;
    report__trans_age_vadose = 0;
    report__trans_age_GW = 0;
    report__trans_age_chanS = 0;
  }
  if (!(opt_carbon_sim == 1)){
    report__NPP = 0;
    report__plant_C = 0;
    report__dpm_litter_CP1 = 0;
    report__dpm_litter_CP2 = 0;
    report__dpm_litter_CP3 = 0;
    report__rpm_litter_CP1 = 0;
    report__rpm_litter_CP2 = 0;
    report__rpm_litter_CP3 = 0;
    report__bio_CP1 = 0;
    report__bio_CP2 = 0;
    report__bio_CP3 = 0;
    report__humus_CP1 = 0;
    report__humus_CP2 = 0;
    report__humus_CP3 = 0;
    report__soluble_CP1 = 0;
    report__soluble_CP2 = 0;
    report__soluble_CP3 = 0;
    report__doc_I = 0;
    report__doc_snow = 0;
    report__doc_pond = 0;
    report__doc_layer1 = 0;
    report__doc_layer2 = 0;
    report__doc_layer3 = 0;
    report__doc_vadose = 0;
    report__doc_GW = 0;
    report__doc_chanS = 0;
    report__litter_fall_C = 0;
    report__co2_emission_C = 0;
    report__soil_decomposition_C = 0;
    report__respiration_river_C = 0;
    report__leaching_mass_doc = 0;
    report__drainage_mass_doc = 0;
  }
  if (!(opt_nitrogen_sim == 1)){
    report__no3_I = 0;
    report__no3_snow = 0;
    report__no3_pond = 0;
    report__no3_layer1 = 0;
    report__no3_layer2 = 0;
    report__no3_layer3 = 0;
    report__no3_vadose = 0;
    report__no3_GW = 0;
    report__no3_chanS = 0;
    report__biological_fixiation_N = 0;
    report__nitrogen_addition_N = 0;
    report__plant_uptake_N = 0;
    report__soil_deni_N = 0;
    report__soil_minerl_N = 0;
    report__aquatic_deni_N = 0;
    report__leaching_mass_no3 = 0;
    report__drainage_mass_no3 = 0;
  }
  /* end of Correction of report flags */


  }

  
}