#ifndef CONTROL_H_
#define CONTROL_H_

#include "dataType.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>
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
  int Simul_start;
  int Simul_end;
  int Simul_tstep;
  int Clim_input_tstep;
  int Report_interval;
  int Update_interval;
  int num_category;  // Number of categories for parameterisation
  int num_cliamte_zones;  // Number of climate zones
  /* end of Settings */

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
  // 1: based on PET and a exponential function Liang et al. (1994)
  int opt_canopy_evap;
  // Evapotranspiration function
  // 1: based on PET and a soil water dependent root extraction function (Feddes et al., 1976)
  int opt_evap;
  // Percolation model
  // 1: based on travel time and excess water above FC; SWAT
  // 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)                        
  // 3: based on soil deficit
  int opt_percolation;
  // GW recharge
  // 1: based on travel time, excess water above FC, and a weighting parameter
  int opt_recharge;
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
  string fn__d18o_I;  // d18o in Canopy storage [m]
  string fn__d18o_snow;  // d18o in Snow depth in [m]
  string fn__d18o_pond;  // d18o in Ponding water in [m]
  string fn__d18o_layer1;  // d18o in Soil moisture in layer 1 [decimal]
  string fn__d18o_layer2;  // d18o in Soil moisture in layer 2 [decimal]
  string fn__d18o_layer3;  // d18o in Soil moisture in layer 3 [decimal]
  string fn__d18o_GW;  // d18o in Groundwater storage [m]
  /* end of Tracking */

  /* Nitrogen */
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
  string fn__wRecharge;  // The weighting parameter for GW recharge [-], only needed when opt_recharge = 1
  string fn__pOvf_toChn;  // The weighting linear parameter for overland flow routing towards channel  [-]
  string fn__interfExp;  // The exponetial weighting parameter for interflow flow routing towards channel  [-]
  string fn__winterf;  // The weight parameter in kinematic wave solution  [-]
  string fn__GWfExp;  // The exponetial weighting parameter for GW flow routing towards channel  [-]
  string fn__wGWf;  // The active proportion of GW storage that contributes to channel recharge  [-]
  string fn__Manningn;  // Manning N for stream routing [-], only needed when opt_routQ = 1
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
  int report__rPerc1;  // report Repercolation into layer 2 [m]
  int report__rPerc2;  // report Repercolation into layer 3 [m]
  int report__rPerc3;  // report Repercolation into gw reservior [m]
  int report__Ei;  // report Canopy evaporation [m]
  int report__Es;  // report Soil evaporation [m]
  int report__Tr;  // report Total transpiration in three layers [m]
  int report__Tr1;  // report Transpiration in layer 1 [m]
  int report__Tr2;  // report Transpiration in layer 2 [m]
  int report__Tr3;  // report Transpiration in layer 3 [m]
  int report__froot_layer1;  // report froot coefficient for all soil profile
  int report__froot_layer2;  // report froot coefficient for layer 2
  int report__froot_layer3;  // report froot coefficient for layer 3
  int report__Ks1;  // report Saturated hydraulic conductivity in layer 1
  int report__Ks2;  // report Saturated hydraulic conductivity in layer 2
  int report__Ks3;  // report Saturated hydraulic conductivity in layer 3
  int report__thetaS1;  // report Saturated soil moisture in layer 1
  int report__thetaS2;  // report Saturated soil moisture in layer 2
  int report__thetaS3;  // report Saturated soil moisture in layer 3
  int report__thetaFC1;  // report Field capacity in layer 1
  int report__thetaFC2;  // report Field capacity in layer 2
  int report__thetaFC3;  // report Field capacity in layer 3
  int report__thetaWP1;  // report Wilting point in layer 1
  int report__thetaWP2;  // report Wilting point in layer 2
  int report__thetaWP3;  // report Wilting point in layer 3
  int report__p_perc1;  // report Percolation proportion in layer 1
  int report__p_perc2;  // report Percolation proportion in layer 2
  int report__p_perc3;  // report Percolation proportion in layer 3
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
  int report__Qupstream;  // report Upstream inflow [m3/s]
  int report__PE;  // report Potential evaporation [m]
  int report__PT;  // report Potential transpiration [m]
  int report__tmp;  // report Temporal variable for testing [-]
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

  template<class T> static T string_as_T( const string& s);
  template<class T> void readInto(T &value, string key, vector<string> lines);
  
};

#endif /* CONTROL_H_ */