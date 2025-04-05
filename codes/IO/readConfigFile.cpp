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
  readInto(Report_interval, "Report_interval", lines);
  readInto(Update_interval, "Update_interval", lines);
  readInto(num_cliamte_zones, "num_cliamte_zones", lines);
  readInto(num_category, "num_category", lines);
  /* end of Settings */

  /* Options */
  readInto(opt_climate_input_format, "opt_climate_input_format", lines);
  readInto(opt_tracking_isotope, "opt_tracking_isotope", lines);
  readInto(opt_intecept, "opt_intecept", lines);
  readInto(opt_snow, "opt_snow", lines);
  readInto(opt_pedotransf, "opt_pedotransf", lines);
  readInto(opt_fieldcapacity, "opt_fieldcapacity", lines);
  readInto(opt_depthprofile, "opt_depthprofile", lines);
  readInto(opt_infil, "opt_infil", lines);
  readInto(opt_percolation, "opt_percolation", lines);
  readInto(opt_evap, "opt_evap", lines);
  readInto(opt_routOvf, "opt_routOvf", lines);
  readInto(opt_routinterf, "opt_routinterf", lines);
  readInto(opt_routGWf, "opt_routGWf", lines);
  readInto(opt_routQ, "opt_routQ", lines);
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
  readInto(fn__fdir, "flow_direction", lines);
  readInto(fn__Gauge_to_Report, "Gauge_mask", lines);
  /* end of GIS */

  readInto(fn__climzones, "climate_zones", lines);
  /* Climate */
  readInto(fn__P, "Precipitation", lines);
  readInto(fn__Ta, "Air_temperature", lines);
  readInto(fn__RH, "Relative_humidity", lines);
  readInto(fn__PET, "Potential_evapotranspiration", lines);
  readInto(fn__LAI, "Leaf_area_index", lines);
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


  /* Parameters */
  readInto(fn__depth3, "Soil_depth3", lines);
  readInto(fn__alpha, "alpha", lines);
  readInto(fn__rE, "rE", lines);
  readInto(fn__snow_rain_thre, "snow_rain_threshold", lines);
  readInto(fn__deg_day_min, "deg_day_min", lines);
  readInto(fn__deg_day_max, "deg_day_max", lines);
  readInto(fn__deg_day_increase, "deg_day_increase", lines);
  readInto(fn__froot_coeff, "froot_coeff", lines);
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
  readInto(fn__pOvf_toChn, "pOvf_toChn", lines);
  readInto(fn__interfExp, "interfExp", lines);
  readInto(fn__winterf, "winterf", lines);
  readInto(fn__GWfExp, "GWfExp", lines);
  readInto(fn__pActiveGW, "pActiveGW", lines);
  readInto(fn__Manningn, "Manningn", lines);
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
  readInto(report__D, "report_interception", lines);
  readInto(report__Th, "report_throufall", lines);
  readInto(report__snowmelt, "report_snowmelt", lines);
  readInto(report__infilt, "report_infiltration", lines);
  readInto(report__Perc1, "report_perc_layer1", lines);
  readInto(report__Perc2, "report_perc_layer2", lines);
  readInto(report__Perc3, "report_perc_layer3", lines);
  readInto(report__Ei, "report_canopy_evap", lines);
  readInto(report__Es, "report_soil_evap", lines);
  readInto(report__Tr, "report_transp", lines);
  readInto(report__Tr1, "report_transp_layer1", lines);
  readInto(report__Tr2, "report_transp_layer2", lines);
  readInto(report__Tr3, "report_transp_layer3", lines);
  readInto(report__ovf_in, "report_overland_flow_input", lines);
  readInto(report__ovf_out, "report_overland_flow_output", lines);
  readInto(report__ovf_toChn, "report_overland_flow_toChn", lines);
  readInto(report__interf_in, "report_interflow_input", lines);
  readInto(report__interf_out, "report_interflow_output", lines);
  readInto(report__interf_toChn, "report_interflow_toChn", lines);
  readInto(report__gwf_toChn, "report_groundwater_flow_toChn", lines);
  readInto(report__Q, "report_discharge", lines);
  /* end of Report */

  return EXIT_SUCCESS;
}



template<class T>
void Control::readInto(T &value, string key, vector<string> lines){
  int position;

  position = find(lines.begin(), lines.end(), key)-lines.begin();

  if (position >= lines.size()){
    throw runtime_error(string("File or Folder not found: ") + key);
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