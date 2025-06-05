/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Control.h
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/








#ifndef CONTROL_H_
#define CONTROL_H_

#include "dataType.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <ctime>
using namespace std;


struct Control{

  int _rowNum, _colNum;
  double _dx, _nodata;

  /* Folders */
  string path_BasinFolder;  //folder where basin property maps are located
  string path_ClimateFolder;  //folder where weather maps series are located
  string path_ResultsFolder;  //folder where results will be placed
  /* end of Folders */

  /* Settings */ 
  long Simul_start;
  int Simul_end;
  int Simul_tstep;
  int Clim_input_tstep;
  int Ground_input_tstep;
  int Report_interval;
  int Update_interval;
  int num_category;  // Number of categories for parameterisation
  /* end of Settings */

  /* Year month day */
  time_t basetime;
  tm* current_time;
  int year;
  int month;
  int day;
  int day_of_year;

  /* Options */
  // How is climate inputs orgainsed?
  // 1: raster
  // 2: aggregated binary file (climate_zone file should be specified)
  int opt_climate_input_format;
  // How is Ground time series inputs orgainsed?
  // 1: raster
  // 2: aggregated binary file (Time series should be prepared for each of the category; input.bin.shape = (N of timestep, num_category))
  int opt_groundTs_input_format;
  // Enable isotopic tracking?
  // 0: disabled
  // 1: enabled
  int opt_tracking_isotope;
  // Enable water age tracking?
  // 0: disabled
  // 1: enabled
  int opt_tracking_age;
  // Enable nitrogen simulation?
  // 0: disabled
  // 1: enabled
  int opt_nitrogen_sim;
  // Agricultural irrigation
  // 0: disabled
  // 1: enabled
  int opt_irrigation;
  // Reinfiltration during overland flow routing
  int opt_reinfil;
  // Canopy interception
  // 1 :maximum canopy storage unmodified
  // 2 :storage corrected (Landarf et al., 2024)
  int opt_intecept;
  // Snow accumulation method
  // 1: Degree day factor method
  int opt_snow;
  // Pedo-transfer function to estimate Van Genuchten parameters
  // 1: Wosten et al., (1999)
  // 2: Wosten et al., (1997)
  // 3: Zacharias et al., (2007)
  int opt_pedotransf;
  // Method to estimate field capacity
  // 1: based on Van Genuchten Model
  // 2: Ks considered, Twarakavi et al., (2007)
  int opt_fieldcapacity;
  // The way to estimate soil characteristics in deeper layer
  // 1: All layers remain the same
  // 2: exponential profile based on depth
  // 3: Pedo-transfer function for each layer
  int opt_depthprofile;
  // Iniltration model
  // 1: Green-Ampt model
  // 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)
  int opt_infil;
  // Canopy evaporation function
  // 0: Disabled
  //1: based on PET and a exponential function Liang et al. (1994)
  int opt_canopy_evap;
  // Evapotranspiration function
  // 1: based on PET and a soil water dependent root extraction function (Feddes et al., 1976)
  int opt_evap;
  // Percolation model
  // 1: based on travel time and excess water above FC; SWAT
  // 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)                        
  // 3: based on soil deficit
  int opt_percolation;
  // Include initial GW storage into calibration 
  // 0: Read from asc inputs
  // 1: Included for calibration
  int opt_init_GW;
  // Overland flow routing
  // 1: All ponding water goes to next cell
  int opt_routOvf;
  // Interflow routing
  // 1: linear approximation of Kinematic Wave
  int opt_routinterf;
  // GW routing
  // 1: linear approximation of Kinematic Wave
  int opt_routGWf;
  // Stream routing
  // 1: Kinematic Wave
  int opt_routQ;
  // Channel evaporation
  // 0: Disabled
  // 1: Penman equation
  // 2: Penman equation with constant wind speed
  // 3: Priestley-Taylor equation
  int opt_chanE;
  // Whether to adjust the d18o compostion in inital storages
  // 0: NO
  // 1: YES (the parameter d18o_init_GW needs to be specified)
  int opt_init_d18o;
  // Whether to adjust the no3 compostion in inital storages
  // 0: NO
  // 1: YES (the parameter no3_init_GW needs to be specified)
  int opt_init_no3;
  // The format of fertilization inputs
  // 1: A raster map showing the potential fertilization amount in g/m2
  // 2: Specificed for each vegetation type in Crop_info.ini
  int opt_fert_input;
  /* end of Options */


  /* Internal varaibles */
  int current_ts;
  string fn__climzones;
  /* end of Internal varaibles */

  /* GIS */
  string fn__chnwidth;  // Channel width [m]
  string fn__chndepth;  // Channel depth [m]
  string fn__chnlength;  // Channel length [m]
  string fn__slope;  // Slope [m/m]
  string fn__depth1;  // Depth of soil layer 1 [m]
  string fn__depth2;  // Depth of soil layer 2 [m]
  string fn__sand1;  // Sand content of layer 1 [decimal]
  string fn__sand2;  // Sand content of layer 2 [decimal], only needed when opt_depthprofile = 3
  string fn__sand3;  // Sand content of layer 3 [decimal], only needed when opt_depthprofile = 3
  string fn__clay1;  // Clay content of layer 1 [decimal]
  string fn__clay2;  // Clay content of layer 2 [decimal], only needed when opt_depthprofile = 3
  string fn__clay3;  // Clay content of layer 3 [decimal], only needed when opt_depthprofile = 3
  string fn__silt1;  // Silt content of layer 1 [decimal], only needed when opt_pedotransf = 1 or 2
  string fn__silt2;  // Silt content of layer 2 [decimal], only needed when opt_depthprofile = 3
  string fn__silt3;  // Silt content of layer 3 [decimal], only needed when opt_depthprofile = 3
  string fn__organic1;  // Organic content of layer 1 [decimal]
  string fn__organic2;  // Organic content of layer 2 [decimal], only needed when opt_depthprofile = 3
  string fn__organic3;  // Organic content of layer 3 [decimal], only needed when opt_depthprofile = 3
  string fn__bulkdensity1;  // Bulk density of layer 1 [g/cm3]
  string fn__bulkdensity2;  // Bulk density of layer 2 [g/cm3], only needed when opt_depthprofile = 3
  string fn__bulkdensity3;  // Bulk density of layer 3 [g/cm3], only needed when opt_depthprofile = 3
  string fn__N_fertilization;  // The fertilization amount [g/m2], only needed when opt_fert_input = 1
  /* end of GIS */ 
  string fn__fdir;  // flow direction [d8 method]
  string fn__Gauge_to_Report;  // Gauges that require outputs

  grid *_fdir;  // flow direction [d8 method]
  svector *_Gauge_to_Report;  // Gauges that require outputs

  /* GroundTs */
  string fn__LAI;  // Leaf area index [decimal]
  /* end of GroundTs */

  /* Climate */
  string fn__P;  // Precipitation [m]
  string fn__Ta;  // Air temperature [degree C]
  string fn__RH;  // Relative humidity [decimal]
  string fn__PET;  // Potential evapotranspiration [m]
  string fn__airpressure;  // Air pressure [Pa]
  string fn__windspeed;  // Wind speed at 2 m [m/s]
  string fn__Rnet;  // Net radiation [W/m2]
  string fn__d18o_P;  // d18O in precipitation [‰]
  /* end of Climate */

  /* Storages */
  string fn__I;  // Canopy storage [m]
  string fn__snow;  // Snow depth in [m]
  string fn__pond;  // Ponding water in [m]
  string fn__theta1;  // Soil moisture in layer 1 [decimal]
  string fn__theta2;  // Soil moisture in layer 2 [decimal]
  string fn__theta3;  // Soil moisture in layer 3 [decimal]
  string fn__GW;  // Groundwater storage [m]
  /* end of Storages */
  
  /* Fluxes */
  string fn__Q;  // Discharge [m3/s]
  /* end of Fluxes */

  /* Tracking */
  string fn__d18o_I;  // d18o in Canopy storage [‰]
  string fn__d18o_snow;  // d18o in Snow depth in [‰]
  string fn__d18o_pond;  // d18o in Ponding water in [‰]
  string fn__d18o_layer1;  // d18o in Soil moisture in layer 1 [‰]
  string fn__d18o_layer2;  // d18o in Soil moisture in layer 2 [‰]
  string fn__d18o_layer3;  // d18o in Soil moisture in layer 3 [‰]
  string fn__d18o_GW;  // d18o in Groundwater storage [‰]
  string fn__d18o_chanS;  // d18o in Channel storage [‰]
  string fn__age_I;  // age in Canopy storage [days]
  string fn__age_snow;  // age in Snow depth in [days]
  string fn__age_pond;  // age in Ponding water in [days]
  string fn__age_layer1;  // age in Soil moisture in layer 1 [days]
  string fn__age_layer2;  // age in Soil moisture in layer 2 [days]
  string fn__age_layer3;  // age in Soil moisture in layer 3 [days]
  string fn__age_GW;  // age in Groundwater storage [days]
  string fn__age_chanS;  // age in Channel storage [days]
  /* end of Tracking */

  /* Nitrogen */
  string fn__no3_I;  // no3 in Canopy storage [mgN/L]
  string fn__no3_snow;  // no3 in Snow depth in [mgN/L]
  string fn__no3_pond;  // no3 in Ponding water in [mgN/L]
  string fn__no3_layer1;  // no3 in Soil moisture in layer 1 [mgN/L]
  string fn__no3_layer2;  // no3 in Soil moisture in layer 2 [mgN/L]
  string fn__no3_layer3;  // no3 in Soil moisture in layer 3 [mgN/L]
  string fn__no3_GW;  // no3 in Groundwater storage [mgN/L]
  string fn__no3_chanS;  // no3 in Channel storage [mgN/L]
  string fn__humusN1;  // Humus nitrogen storage in layer 1 [mgN/L*m = gN/m2]
  string fn__humusN2;  // Humus nitrogen storage in layer 2 [mgN/L*m = gN/m2]
  string fn__humusN3;  // Humus nitrogen storage in layer 3 [mgN/L*m = gN/m2]
  string fn__fastN1;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
  string fn__fastN2;  // Fast nitrogen storage in layer 2 [mgN/L*m = gN/m2]
  string fn__fastN3;  // Fast nitrogen storage in layer 3 [mgN/L*m = gN/m2]
  /* end of Nitrogen */

  /* Parameters */
  string fn__depth3;  // Depth of soil layer 3 [m]
  string fn__alpha;  // The weighting parameter that links LAI and maximum canopy storage [-]
  string fn__rE;  // Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)
  string fn__snow_rain_thre;  // The temperature for snow melt  [m]
  string fn__deg_day_min;  // Degree-day factor with no precipitation [m-1 degreeC-1]
  string fn__deg_day_max;  // Maximum Degree-day factor [m-1 degreeC-1]
  string fn__deg_day_increase;  // Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]
  string fn__froot_coeff;  // Root fraction coefficient [-]
  string fn__ref_thetaS;  // Reference saturated soil moisture [-]
  string fn__PTF_VG_clay;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  string fn__PTF_VG_Db;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  string fn__PTF_Ks_const;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  string fn__PTF_Ks_sand;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  string fn__PTF_Ks_clay;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  string fn__PTF_Ks_slope;  // Slope correction for estimation of saturated hydraulic conductivity [-]
  string fn__SWP;  // Soil water potentail for field capacity estimation [-], only needed when opt_fieldcapacity = 1
  string fn__KvKh;  // The coefficient to transform Ks to effective Ks [-], only needed when opt_infil = 1
  string fn__psiAE;  // The wetting front potential for Green-Ampt model [mm], only needed when opt_infil = 1
  string fn__KKs;  // The exponential parameter for depth-dependent saturated hydraulic conductivity [-], only needed when opt_depthprofile = 2
  string fn__Ksat;  // The exponential parameter for depth-dependent saturated moisture content  [-], only needed when opt_depthprofile = 2
  string fn__BClambda;  // The exponential parameter for depth-dependent field capacity  [-], only needed when opt_depthprofile = 2
  string fn__percExp;  // The exponential parameter for percolation [-], only needed when opt_percolation = 2
  string fn__init_GW;  // The initial GW storage [m], only needed when opt_init_GW = 1
  string fn__wRecharge;  // The weighting parameter for GW recharge [-], only needed when opt_recharge = 1
  string fn__pOvf_toChn;  // The weighting linear parameter for overland flow routing towards channel  [-]
  string fn__Ks_vadose;  // The reference conductivity of vadose zone for interflow routing [m/s]
  string fn__Ks_GW;  // The reference conductivity of GW zone for interflow routing [m/s]
  string fn__lat_to_Chn_vadose;  // The ratio between conductivities of lateral flow and channel recharge in vadose zone [-]
  string fn__lat_to_Chn_GW;  // The ratio between conductivities of lateral flow and channel recharge in GW zone [-]
  string fn__interfExp;  // The exponetial weighting parameter for interflow flow routing towards channel  [-]
  string fn__GWfExp;  // The exponetial weighting parameter for GW flow routing towards channel  [-]
  string fn__Manningn;  // Manning N for stream routing [-], only needed when opt_routQ = 1
  string fn__Echan_alpha;  // correction factor in Priestley-Taylor equation [-], only needed when opt_chanE = 1 or 2
  string fn__irrigation_coeff;  // Irrigation coefficient to determine the actual water demand from water deficit [-], only needed when irrigation is enabled
  string fn__nearsurface_mixing;  // The proportion of pond to mix with layer1  [decimal]
  string fn__ratio_to_interf;  // The proportion of excess storage in layer 1 that routs as interflow (otherwise percolate to GW) [decimal]
  string fn__CG_n_soil;  // Parameter N in CG model for soil water fractionation [-]
  string fn__delta_d18o_init_GW;  // Initial d18O of GW storage [‰]
  string fn__delta_no3_init_GW;  // Initial no3 of GW storage [‰]
  string fn__denitrification_river;  // Reference rates of aquatic denitrification [-]
  string fn__denitrification_soil;  // Reference rates of soil denitrification [kg/ha]
  string fn__degradation_soil;  // Reference rates of soil degradation [kg/ha]
  string fn__mineralisation_soil;  // Reference rates of soil mineralisation [kg/ha]
  string fn__deni_soil_moisture_thres;  // The moisture threshold of soil denitrification
  /* end of Parameters */

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  int report__I;  // report Canopy storage [m]
  int report__snow;  // report Snow depth in [m]
  int report__pond;  // report Ponding water in [m]
  int report__theta1;  // report Soil moisture in layer 1 [decimal]
  int report__theta2;  // report Soil moisture in layer 2 [decimal]
  int report__theta3;  // report Soil moisture in layer 3 [decimal]
  int report__GW;  // report Groundwater storage [m]
  int report__Th;  // report Throughfall [m]
  int report__snowmelt;  // report Snow melt [m]
  int report__infilt;  // report Inflitration into soil layer 1 [m]
  int report__Perc1;  // report Percolation into layer 2 [m]
  int report__Perc2;  // report Percolation into layer 3 [m]
  int report__Perc3;  // report Percolation into gw reservior [m]
  int report__rinfilt;  // report Reinflitration into soil layer 1 [m]
  int report__rPerc1;  // report Repercolation into layer 2 due to overland flow routing [m]
  int report__rPerc2;  // report Repercolation into layer 3 due to overland flow routing [m]
  int report__rPerc3;  // report Repercolation into gw reservior due to overland flow routing [m]
  int report__rrPerc3;  // report Repercolation into gw reservior due to interflow routing [m]
  int report__Ei;  // report Canopy evaporation [m]
  int report__Es;  // report Soil evaporation [m]
  int report__Tr;  // report Total transpiration in three layers [m]
  int report__Tr1;  // report Transpiration in layer 1 [m]
  int report__Tr2;  // report Transpiration in layer 2 [m]
  int report__Tr3;  // report Transpiration in layer 3 [m]
  int report__irrigation_from_river;  // report Water extraction from river [m]
  int report__irrigation_from_GW;  // report Water extraction from GW [m]
  int report__ovf_in;  // report Overland flow from upstream cell(s) [m]
  int report__ovf_out;  // report Overland flow to downstream cell [m]
  int report__ovf_toChn;  // report Overland flow to Channel [m]
  int report__interf_in;  // report Interflow from upstream cell(s) [m]
  int report__interf_out;  // report Interflow to downstream cell [m]
  int report__interf_toChn;  // report Interflow to Channel [m]
  int report__GWf_in;  // report GW flow from upstream cell(s) [m]
  int report__GWf_out;  // report GW flow to downstream cell [m]
  int report__GWf_toChn;  // report Groundwater flow to Channel [m]
  int report__Q;  // report Discharge [m3/s]
  int report__Echan;  // report Channel evaporation [m]
  int report__d18o_I;  // report d18o in Canopy storage [‰]
  int report__d18o_snow;  // report d18o in Snow depth in [‰]
  int report__d18o_pond;  // report d18o in Ponding water in [‰]
  int report__d18o_layer1;  // report d18o in Soil moisture in layer 1 [‰]
  int report__d18o_layer2;  // report d18o in Soil moisture in layer 2 [‰]
  int report__d18o_layer3;  // report d18o in Soil moisture in layer 3 [‰]
  int report__d18o_GW;  // report d18o in Groundwater storage [‰]
  int report__d18o_chanS;  // report d18o in Channel storage [‰]
  int report__age_I;  // report age in Canopy storage [days]
  int report__age_snow;  // report age in Snow depth in [days]
  int report__age_pond;  // report age in Ponding water in [days]
  int report__age_layer1;  // report age in Soil moisture in layer 1 [days]
  int report__age_layer2;  // report age in Soil moisture in layer 2 [days]
  int report__age_layer3;  // report age in Soil moisture in layer 3 [days]
  int report__age_GW;  // report age in Groundwater storage [days]
  int report__age_chanS;  // report age in Channel storage [days]
  int report__no3_I;  // report no3 in Canopy storage [mgN/L]
  int report__no3_snow;  // report no3 in Snow depth in [mgN/L]
  int report__no3_pond;  // report no3 in Ponding water in [mgN/L]
  int report__no3_layer1;  // report no3 in Soil moisture in layer 1 [mgN/L]
  int report__no3_layer2;  // report no3 in Soil moisture in layer 2 [mgN/L]
  int report__no3_layer3;  // report no3 in Soil moisture in layer 3 [mgN/L]
  int report__no3_GW;  // report no3 in Groundwater storage [mgN/L]
  int report__no3_chanS;  // report no3 in Channel storage [mgN/L]
  int report__nitrogen_add;  // report Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
  int report__plant_uptake;  // report Plant uptake [mgN/L*m = gN/m2]
  int report__deni_soil;  // report Soil denitrification [mgN/L*m = gN/m2]
  int report__minerl_soil;  // report Soil mineralisation [mgN/L*m = gN/m2]
  int report__degrad_soil;  // report Soil degradation [mgN/L*m = gN/m2]
  int report__deni_river;  // report Aquatic denitrification [mgN/L*m = gN/m2]
  /* end of Report */

  public:
  //ctor from raster ascii file
  Control();
  //dtor
  ~Control();
  int dtor();
  

  // Read configurations
  int getAsciiHeader(string fname);
  int ReadConfigFile(string confilename = "config.ini");


  /* Grids sorting */
  sortedGrid _sortedGrid;
  sortedTSmask _Tsmask;  // Gauges that require outputs
  sortedGrid SortGridLDD();
  sortedTSmask sortTSmask();
  /* end of Grids sorting*/

  /* Time sorting */
  time_t Set_reference_timestep();
  int Get_year_month_day();
  bool is_next_month();
  bool is_next_year();
  /* end of Time sorting */

  template<class T> static T string_as_T( const string& s);
  template<class T> void readInto(T &value, string key, vector<string> lines);
  vector<int> VectorArgSort(vector<int> &v);
  
};

#endif /* CONTROL_H_ */