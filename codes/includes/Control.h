#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>
using namespace std;


struct Control{

  int _rowNum0, _colNum0;
  double _dx0, _nodata0;

  /* Folders */
  string path_BasinFolder; //folder where basin property maps are located
  string path_ClimateFolder; //folder where weather maps series are located
  string path_ResultsFolder; //folder where results will be placed
  /* end of Folders */

  /* Settings */ 
  int Simul_start;
  int Simul_end;
  int Simul_tstep;
  int Clim_input_tstep;
  int Report_interval;
  /* end of Settings */

  /* Options */
  int opt_climate_input_format;  //how is climate inputs orgainsed? 1 = raster; 2 = aggregated binary file (climate_zone file should be specified)
  int opt_tracking_isotope;  //if enable isotopic tracking?
  int opt_canopy;  //Which canopy process to use?
  /* end of Options */


  /* Internal varaibles */
  int current_ts;
  string fn__climzones;
  /* end of Internal varaibles */

  /* GIS */
  string fn__dem;  // surface evelation [m]
  string fn__fdir;  // flow direction [d8 method]
  string fn__chnwidth;  // channel width [m]
  string fn__chndepth;  // channel depth [m]
  string fn__chnlength;  // channel length [m]
  string fn__depth1;  // depth of soil layer 1 [m]
  string fn__depth2;  // depth of soil layer 2 [m]
  string fn__depth3;  // depth of soil layer 3 [m]
  string fn__Gauge_to_Report;  // Gauges that require outputs
  /* end of GIS */ 

  /* Climate */
  string fn__P;  // precipitation [m]
  string fn__Ta;  // air temperature [degree C]
  string fn__Tmin;  // minimum air temperature [degree C]
  string fn__Tmax;  // maximum air temperature [degree C]
  string fn__RH;  // relative humidity [decimal]
  string fn__LAI;  // leaf area index [decimal]
  /* end of Climate */

  /* Storages */
  string fn__I;  // interception/canopy storage [m]
  string fn__snow;  // snow depth in [m]
  string fn__theta1;  // soil moisture in layer 1 [decimal]
  string fn__theta2;  // soil moisture in layer 2 [decimal]
  string fn__theta3;  // soil moisture in layer 3 [decimal]
  /* end of Storages */
  
  /* Fluxes */
  /* end of Fluxes */

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  int report__I;  // report interception/canopy storage [m]
  int report__snow;  // report snow depth in [m]
  int report__theta1;  // report soil moisture in layer 1 [decimal]
  int report__theta2;  // report soil moisture in layer 2 [decimal]
  int report__theta3;  // report soil moisture in layer 3 [decimal]
  int report__D;  // report interception [m]
  int report__Th;  // report throughfall [m]
  int report__snowmelt;  // report snow melt [m]
  int report__Qs;  // report overland flow [m]
  int report__infilt;  // report inflitration into soil layer 1 [m]
  int report__preferential2;  // report preferential flow to layer 2 [m]
  int report__preferential3;  // report preferential flow to layer 3 [m]
  int report__Perc1;  // report percolation into layer 2 [m]
  int report__Perc2;  // report percolation into layer 3 [m]
  int report__Perc3;  // report percolation into gw reservior [m]
  int report__Ei;  // report canopy evaporation [m]
  int report__Es;  // report soil evaporation [m]
  int report__Tr;  // report total transpiration in three layers [m]
  int report__Tr1;  // report transpiration in layer 1 [m]
  int report__Tr2;  // report transpiration in layer 2 [m]
  int report__Tr3;  // report transpiration in layer 3 [m]
  /* end of Report */

  public:
  //ctor from raster ascii file
  Control();
  //dtor


  int getAsciiHeader(string fname);
  int ReadConfigFile(string confilename = "config.ini");

  template<class T> static T string_as_T( const string& s);
  template<class T> void readInto(T &value, string key, vector<string> lines);
  
};

