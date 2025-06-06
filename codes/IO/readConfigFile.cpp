/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* readConfigFile.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Control.h"

int Control::ReadConfigFile(string fname){
  ifstream input;
  vector<string> lines;
  string s;

  // read all text in config file into string-based vector
  input.open(fname.c_str());
  if (!input.good()){
    throw runtime_error(string("file not found: ") + fname.c_str());
  }

  while (!input.eof()){
    input >> s;
    lines.push_back(s);
  }

  /* Folders */
  readInto(path_BasinFolder, "Maps_Folder", lines);
  readInto(path_ClimateFolder, "Clim_Maps_Folder", lines);
  readInto(path_ResultsFolder, "Output_Folder", lines);
  /* end of Folders */

  /* Settings */  
  readInto(Simul_start, "Simul_start", lines);
  readInto(Simul_end, "Simul_end", lines);
  readInto(Simul_tstep, "Simul_tstep", lines);
  readInto(Clim_input_tstep, "Clim_input_tstep", lines);
  readInto(Ground_input_tstep, "Ground_input_tstep", lines);  
  readInto(Report_interval, "Report_interval", lines);
  readInto(Update_interval, "Update_interval", lines);
  readInto(num_category, "num_category", lines);
  /* end of Settings */

  /* Options */
  readInto(opt_climate_input_format, "opt_climate_input_format", lines);
  readInto(opt_groundTs_input_format, "opt_groundTs_input_format", lines);
  readInto(opt_tracking_isotope, "opt_tracking_isotope", lines);
  readInto(opt_tracking_age, "opt_tracking_age", lines);
  readInto(opt_nitrogen_sim, "opt_nitrogen_sim", lines);
  readInto(opt_irrigation, "opt_irrigation", lines);
  readInto(opt_reinfil, "opt_reinfil", lines);
  readInto(opt_intecept, "opt_intecept", lines);
  readInto(opt_snow, "opt_snow", lines);
  readInto(opt_pedotransf, "opt_pedotransf", lines);
  readInto(opt_fieldcapacity, "opt_fieldcapacity", lines);
  readInto(opt_depthprofile, "opt_depthprofile", lines);
  readInto(opt_infil, "opt_infil", lines);
  readInto(opt_canopy_evap, "opt_canopy_evap", lines);
  readInto(opt_evap, "opt_evap", lines);
  readInto(opt_percolation, "opt_percolation", lines);
  readInto(opt_init_GW, "opt_init_GW", lines);
  readInto(opt_routOvf, "opt_routOvf", lines);
  readInto(opt_routinterf, "opt_routinterf", lines);
  readInto(opt_routGWf, "opt_routGWf", lines);
  readInto(opt_routQ, "opt_routQ", lines);
  readInto(opt_chanE, "opt_chanE", lines);
  readInto(opt_init_d18o, "opt_init_d18o", lines);
  readInto(opt_init_no3, "opt_init_no3", lines);
  readInto(opt_fert_input, "opt_fert_input", lines);
  /* end of Options */

  /* GIS */
  readInto(fn__chnwidth, "Channel_width", lines);
  readInto(fn__chndepth, "Channel_depth", lines);
  readInto(fn__chnlength, "Channel_length", lines);
  readInto(fn__slope, "slope", lines);
  readInto(fn__depth1, "Soil_depth1", lines);
  readInto(fn__depth2, "Soil_depth2", lines);
  readInto(fn__sand1, "sand1", lines);
  readInto(fn__sand2, "sand2", lines);
  readInto(fn__sand3, "sand3", lines);
  readInto(fn__clay1, "clay1", lines);
  readInto(fn__clay2, "clay2", lines);
  readInto(fn__clay3, "clay3", lines);
  readInto(fn__silt1, "silt1", lines);
  readInto(fn__silt2, "silt2", lines);
  readInto(fn__silt3, "silt3", lines);
  readInto(fn__organic1, "organic1", lines);
  readInto(fn__organic2, "organic2", lines);
  readInto(fn__organic3, "organic3", lines);
  readInto(fn__bulkdensity1, "bulk_density1", lines);
  readInto(fn__bulkdensity2, "bulk_density2", lines);
  readInto(fn__bulkdensity3, "bulk_density3", lines);
  readInto(fn__N_fertilization, "N_fertilization", lines);
  readInto(fn__fdir, "flow_direction", lines);
  readInto(fn__Gauge_to_Report, "Gauge_mask", lines);
  /* end of GIS */

  /* GroundTs */
  readInto(fn__LAI, "Leaf_area_index", lines);
  /* end of GroundTs */

  readInto(fn__climzones, "climate_zones", lines);
  /* Climate */
  readInto(fn__P, "Precipitation", lines);
  readInto(fn__Ta, "Air_temperature", lines);
  readInto(fn__RH, "Relative_humidity", lines);
  readInto(fn__PET, "Potential_evapotranspiration", lines);
  readInto(fn__airpressure, "Air_pressure", lines);
  readInto(fn__windspeed, "Wind_speed", lines);
  readInto(fn__Rnet, "Net_radiation", lines);
  readInto(fn__d18o_P, "d18O_Precipitation", lines);
  /* end of Climate */

  /* Storages */ 
  readInto(fn__I, "canopy_storage", lines);
  readInto(fn__snow, "snow_depth", lines);
  readInto(fn__pond, "pond", lines);
  readInto(fn__theta1, "SMC_layer1", lines);
  readInto(fn__theta2, "SMC_layer2", lines);
  readInto(fn__theta3, "SMC_layer3", lines);
  readInto(fn__GW, "groundwater_storage", lines);
  /* end of Storages */ 

  /* Fluxes */
  readInto(fn__Q, "discharge", lines);
  /* end of Fluxes */

  /* Tracking */
  readInto(fn__d18o_I, "d18o_canopy_storage", lines);
  readInto(fn__d18o_snow, "d18o_snow_depth", lines);
  readInto(fn__d18o_pond, "d18o_pond", lines);
  readInto(fn__d18o_layer1, "d18o_SMC_layer1", lines);
  readInto(fn__d18o_layer2, "d18o_SMC_layer2", lines);
  readInto(fn__d18o_layer3, "d18o_SMC_layer3", lines);
  readInto(fn__d18o_GW, "d18o_groundwater_storage", lines);
  readInto(fn__d18o_chanS, "d18o_chanS", lines);
  readInto(fn__age_I, "age_canopy_storage", lines);
  readInto(fn__age_snow, "age_snow_depth", lines);
  readInto(fn__age_pond, "age_pond", lines);
  readInto(fn__age_layer1, "age_SMC_layer1", lines);
  readInto(fn__age_layer2, "age_SMC_layer2", lines);
  readInto(fn__age_layer3, "age_SMC_layer3", lines);
  readInto(fn__age_GW, "age_groundwater_storage", lines);
  readInto(fn__age_chanS, "age_chanS", lines);
  /* end of Tracking */

  /* Nitrogen */
  readInto(fn__no3_I, "no3_canopy_storage", lines);
  readInto(fn__no3_snow, "no3_snow_depth", lines);
  readInto(fn__no3_pond, "no3_pond", lines);
  readInto(fn__no3_layer1, "no3_SMC_layer1", lines);
  readInto(fn__no3_layer2, "no3_SMC_layer2", lines);
  readInto(fn__no3_layer3, "no3_SMC_layer3", lines);
  readInto(fn__no3_GW, "no3_groundwater_storage", lines);
  readInto(fn__no3_chanS, "no3_chanS", lines);
  readInto(fn__humusN1, "humusN1", lines);
  readInto(fn__humusN2, "humusN2", lines);
  readInto(fn__humusN3, "humusN3", lines);
  readInto(fn__fastN1, "fastN1", lines);
  readInto(fn__fastN2, "fastN2", lines);
  readInto(fn__fastN3, "fastN3", lines);
  /* end of Nitrogen */


  /* Parameters */
  readInto(fn__depth3, "Soil_depth3", lines);
  readInto(fn__alpha, "alpha", lines);
  readInto(fn__rE, "rE", lines);
  readInto(fn__snow_rain_thre, "snow_rain_threshold", lines);
  readInto(fn__deg_day_min, "deg_day_min", lines);
  readInto(fn__deg_day_max, "deg_day_max", lines);
  readInto(fn__deg_day_increase, "deg_day_increase", lines);
  readInto(fn__ref_thetaS, "ref_thetaS", lines);
  readInto(fn__PTF_VG_clay, "PTF_VG_clay", lines);
  readInto(fn__PTF_VG_Db, "PTF_VG_Db", lines);
  readInto(fn__PTF_Ks_const, "PTF_Db", lines);
  readInto(fn__PTF_Ks_sand, "PTF_sand", lines);
  readInto(fn__PTF_Ks_clay, "PTF_clay", lines);
  readInto(fn__PTF_Ks_slope, "PTF_Ks_slope", lines);
  readInto(fn__SWP, "SWP", lines);
  readInto(fn__KvKh, "KvKh", lines);
  readInto(fn__psiAE, "psiAE", lines);
  readInto(fn__KKs, "Ksat", lines);
  readInto(fn__Ksat, "Kporos", lines);
  readInto(fn__BClambda, "BClambda", lines);
  readInto(fn__percExp, "percExp", lines);
  readInto(fn__froot_coeff, "froot_coeff", lines);
  readInto(fn__ET_reduction, "ET_reduction", lines);
  readInto(fn__init_GW, "init_GW", lines);
  readInto(fn__wRecharge, "wRecharge", lines);
  readInto(fn__pOvf_toChn, "pOvf_toChn", lines);
  readInto(fn__Ks_vadose, "Ks_vadose", lines);
  readInto(fn__Ks_GW, "Ks_GW", lines);
  readInto(fn__lat_to_Chn_vadose, "lat_to_Chn_vadose", lines);
  readInto(fn__lat_to_Chn_GW, "lat_to_Chn_GW", lines);
  readInto(fn__interfExp, "interfExp", lines);
  readInto(fn__GWfExp, "GWfExp", lines);
  readInto(fn__Manningn, "Manningn", lines);
  readInto(fn__Echan_alpha, "Echan_alpha", lines);
  readInto(fn__irrigation_coeff, "irrigation_coeff", lines);
  readInto(fn__nearsurface_mixing, "nearsurface_mixing", lines);
  readInto(fn__ratio_to_interf, "ratio_to_interf", lines);
  readInto(fn__CG_n_soil, "CG_n_soil", lines);
  readInto(fn__delta_d18o_init_GW, "delta_d18o_init_GW", lines);
  readInto(fn__delta_no3_init_GW, "delta_d18o_init_GW", lines);
  readInto(fn__denitrification_river, "denitrification_river", lines);
  readInto(fn__denitrification_soil, "denitrification_soil", lines);
  readInto(fn__degradation_soil, "degradation_soil", lines);
  readInto(fn__mineralisation_soil, "mineralisation_soil", lines);
  readInto(fn__deni_soil_moisture_thres, "deni_soil_moisture_thres", lines);
  /* end of Parameters */

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  readInto(report__I, "report_canopy_storage", lines);
  readInto(report__snow, "report_snow_depth", lines);
  readInto(report__pond, "report_pond", lines);
  readInto(report__theta1, "report_SMC_layer1", lines);
  readInto(report__theta2, "report_SMC_layer2", lines);
  readInto(report__theta3, "report_SMC_layer3", lines);
  readInto(report__GW, "report_groundwater_storage", lines);
  readInto(report__Th, "report_throufall", lines);
  readInto(report__snowmelt, "report_snowmelt", lines);
  readInto(report__infilt, "report_infiltration", lines);
  readInto(report__Perc1, "report_perc_layer1", lines);
  readInto(report__Perc2, "report_perc_layer2", lines);
  readInto(report__Perc3, "report_perc_layer3", lines);
  readInto(report__rinfilt, "report_rinfiltration", lines);
  readInto(report__rPerc1, "report_rperc_layer1", lines);
  readInto(report__rPerc2, "report_rperc_layer2", lines);
  readInto(report__rPerc3, "report_rperc_layer3", lines);
  readInto(report__rrPerc3, "report_rrperc_layer3", lines);
  readInto(report__Ei, "report_canopy_evap", lines);
  readInto(report__Es, "report_soil_evap", lines);
  readInto(report__Tr, "report_transp", lines);
  readInto(report__Tr1, "report_transp_layer1", lines);
  readInto(report__Tr2, "report_transp_layer2", lines);
  readInto(report__Tr3, "report_transp_layer3", lines);
  readInto(report__irrigation_from_river, "report_irrigation_from_river", lines);
  readInto(report__irrigation_from_GW, "report_irrigation_from_GW", lines);
  readInto(report__ovf_in, "report_overland_flow_input", lines);
  readInto(report__ovf_out, "report_overland_flow_output", lines);
  readInto(report__ovf_toChn, "report_overland_flow_toChn", lines);
  readInto(report__interf_in, "report_interflow_input", lines);
  readInto(report__interf_out, "report_interflow_output", lines);
  readInto(report__interf_toChn, "report_interflow_toChn", lines);
  readInto(report__GWf_in, "report_GWflow_input", lines);
  readInto(report__GWf_out, "report_GWflow_output", lines);
  readInto(report__GWf_toChn, "report_GWflow_toChn", lines);
  readInto(report__Q, "report_discharge", lines);
  readInto(report__Echan, "report_channel_evaporation", lines);
  readInto(report__d18o_I, "report_d18o_canopy_storage", lines);
  readInto(report__d18o_snow, "report_d18o_snow_depth", lines);
  readInto(report__d18o_pond, "report_d18o_pond", lines);
  readInto(report__d18o_layer1, "report_d18o_SMC_layer1", lines);
  readInto(report__d18o_layer2, "report_d18o_SMC_layer2", lines);
  readInto(report__d18o_layer3, "report_d18o_SMC_layer3", lines);
  readInto(report__d18o_GW, "report_d18o_groundwater_storage", lines);
  readInto(report__d18o_chanS, "report_d18o_chanS", lines);
  readInto(report__age_I, "report_age_canopy_storage", lines);
  readInto(report__age_snow, "report_age_snow_depth", lines);
  readInto(report__age_pond, "report_age_pond", lines);
  readInto(report__age_layer1, "report_age_SMC_layer1", lines);
  readInto(report__age_layer2, "report_age_SMC_layer2", lines);
  readInto(report__age_layer3, "report_age_SMC_layer3", lines);
  readInto(report__age_GW, "report_age_groundwater_storage", lines);
  readInto(report__age_chanS, "report_age_chanS", lines);
  readInto(report__no3_I, "report_no3_canopy_storage", lines);
  readInto(report__no3_snow, "report_no3_snow_depth", lines);
  readInto(report__no3_pond, "report_no3_pond", lines);
  readInto(report__no3_layer1, "report_no3_SMC_layer1", lines);
  readInto(report__no3_layer2, "report_no3_SMC_layer2", lines);
  readInto(report__no3_layer3, "report_no3_SMC_layer3", lines);
  readInto(report__no3_GW, "report_no3_groundwater_storage", lines);
  readInto(report__no3_chanS, "report_no3_chanS", lines);
  readInto(report__nitrogen_add, "report_nitrogen_addition", lines);
  readInto(report__plant_uptake, "report_plant_uptake", lines);
  readInto(report__deni_soil, "report_deni_soil", lines);
  readInto(report__minerl_soil, "report_minerl_soil", lines);
  readInto(report__degrad_soil, "report_degrad_soil", lines);
  readInto(report__deni_river, "report_deni_river", lines);
  /* end of Report */

  return EXIT_SUCCESS;
}



template<class T>
void Control::readInto(T &value, string key, vector<string> lines){
  int position;

  position = find(lines.begin(), lines.end(), key)-lines.begin();

  if (position >= lines.size()){
    throw runtime_error(string("Config not found: ") + key);
  } else {
    value = string_as_T<T>(lines[position+2]);
  }
}

template<class T>
T Control::string_as_T( const string& s )
{
	// Convert from a string to a T
	// Type T must support >> operator
	T t;
	istringstream ist(s);
	ist >> t;
	return t;
}