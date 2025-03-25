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
  int opt_climate_input_format;  //How is climate inputs orgainsed? 1: raster; 2: aggregated binary file (climate_zone file should be specified)
  int opt_tracking_isotope;  //Enable isotopic tracking? 0: disabled, 1: enabled
  int opt_intecept;  //Canopy interception. 1 :maximum canopy storage unmodified; 2 :storage corrected (Landarf et al., 2024)
  int opt_snow;  //Snow accumulation method. 1: Degree day factor method
  int opt_infilt;  //Infiltration function. 1: 
  int opt_evap;  //Evapotranspiration function. 1: based on PET and a soil water dependent root extraction function (Feddes et al., 1976)
  int opt_pedotransf;  //Pedo-transfer function to estimate Van Genuchten parameters. 1: Wosten et al., (1999); 2: Wosten et al., (1997);  3: Zacharias et al., (2007)
  int opt_fieldcapacity;  //Method to estimate field capacity. 1: based on Van Genuchten Model; 2: Ks considered, Twarakavi et al., (2007)
  /* end of Options */


  /* Internal varaibles */
  int current_ts;
  string fn__climzones;
  /* end of Internal varaibles */

  /* GIS */
  string fn__dem;  // Surface evelation [m]
  string fn__chnwidth;  // Channel width [m]
  string fn__chndepth;  // Channel depth [m]
  string fn__chnlength;  // Channel length [m]
  string fn__depth1;  // Depth of soil layer 1 [m]
  string fn__depth2;  // Depth of soil layer 2 [m]
  /* end of GIS */ 
  string fn__fdir;  // flow direction [d8 method]
  string fn__Gauge_to_Report;  // Gauges that require outputs

  grid *_fdir;  // flow direction [d8 method]
  svector *_Gauge_to_Report;  // Gauges that require outputs

  /* Climate */
  string fn__P;  // Precipitation [m]
  string fn__Ta;  // Air temperature [degree C]
  string fn__RH;  // Relative humidity [decimal]
  string fn__PET;  // Potential evapotranspiration [m]
  string fn__LAI;  // Leaf area index [decimal]
  /* end of Climate */

  /* Storages */
  string fn__I;  // Canopy storage [m]
  string fn__snow;  // Snow depth in [m]
  string fn__theta1;  // Soil moisture in layer 1 [decimal]
  string fn__theta2;  // Soil moisture in layer 2 [decimal]
  string fn__theta3;  // Soil moisture in layer 3 [decimal]
  /* end of Storages */
  
  /* Fluxes */
  /* end of Fluxes */

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
  /* end of Parameters */

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  int report__I;  // report Canopy storage [m]
  int report__snow;  // report Snow depth in [m]
  int report__theta1;  // report Soil moisture in layer 1 [decimal]
  int report__theta2;  // report Soil moisture in layer 2 [decimal]
  int report__theta3;  // report Soil moisture in layer 3 [decimal]
  int report__D;  // report Interception [m]
  int report__Th;  // report Throughfall [m]
  int report__snowmelt;  // report Snow melt [m]
  int report__Qs;  // report Overland flow [m]
  int report__infilt;  // report Inflitration into soil layer 1 [m]
  int report__Perc1;  // report Percolation into layer 2 [m]
  int report__Perc2;  // report Percolation into layer 3 [m]
  int report__Perc3;  // report Percolation into gw reservior [m]
  int report__Ei;  // report Canopy evaporation [m]
  int report__Es;  // report Soil evaporation [m]
  int report__Tr;  // report Total transpiration in three layers [m]
  int report__Tr1;  // report Transpiration in layer 1 [m]
  int report__Tr2;  // report Transpiration in layer 2 [m]
  int report__Tr3;  // report Transpiration in layer 3 [m]
  int report__froot_soil;  // report froot coefficient for all soil profile
  int report__froot_layer2;  // report froot coefficient for layer 2
  int report__froot_layer3;  // report froot coefficient for layer 3
  int report__Ks1;  // report Saturated hydraulic conductivity in layer 1
  int report__Ks2;  // report Saturated hydraulic conductivity in layer 2
  int report__Ks3;  // report Saturated hydraulic conductivity in layer 3
  int report__thetaFC1;  // report Field capacity in layer 1
  int report__thetaFC2;  // report Field capacity in layer 2
  int report__thetaFC3;  // report Field capacity in layer 3
  int report__thetaWP1;  // report Wilting point in layer 1
  int report__thetaWP2;  // report Wilting point in layer 2
  int report__thetaWP3;  // report Wilting point in layer 3
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