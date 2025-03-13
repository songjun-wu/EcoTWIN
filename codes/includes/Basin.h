#ifndef BASIN_H_
#define BASIN_H_

#include "dataType.h"
#include "Control.h"

#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Basin {
  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  
  /* end of Properties */

  public:


  /* GIS */
  grid *_dem;  // surface evelation [m]
  grid *_fdir;  // flow direction [d8 method]
  grid *_chnwidth;  // channel width [m]
  grid *_chndepth;  // channel depth [m]
  grid *_chnlength;  // channel length [m]
  grid *_depth1;  // depth of soil layer 1 [m]
  grid *_depth2;  // depth of soil layer 2 [m]
  grid *_depth3;  // depth of soil layer 3 [m]
  grid *_Gauge_to_Report;  // Gauges that require outputs
  /* end of GIS */

  /* Grids sorting */
  sortedGrid _sortedGrid;
  sortedTSmask _Tsmask;  // Gauges that require outputs
  sortedGrid SortGridLDD();
  sortedTSmask sortTSmask();
  /* end of Grids sorting*/

  /* Storages */ 
  grid *_I;  // interception/canopy storage [m]
  grid *_snow;  // snow depth in [m]
  grid *_theta1;  // soil moisture in layer 1 [decimal]
  grid *_theta2;  // soil moisture in layer 2 [decimal]
  grid *_theta3;  // soil moisture in layer 3 [decimal]
  grid *_I_old;  // interception/canopy storage in previous timestep in [m]
  /* end of Storages */ 
 

  /* Fluxes */
  grid *_D;  // interception [m]
  grid *_Th;  // throughfall [m]
  grid *_snowmelt;  // snow melt [m]
  grid *_Qs;  // overland flow [m]
  grid *_infilt;  // inflitration into soil layer 1 [m]
  grid *_preferential2;  // preferential flow to layer 2 [m]
  grid *_preferential3;  // preferential flow to layer 3 [m]
  grid *_Perc1;  // percolation into layer 2 [m]
  grid *_Perc2;  // percolation into layer 3 [m]
  grid *_Perc3;  // percolation into gw reservior [m]
  grid *_Ei;  // canopy evaporation [m]
  grid *_Es;  // soil evaporation [m]
  grid *_Tr;  // total transpiration in three layers [m]
  grid *_Tr1;  // transpiration in layer 1 [m]
  grid *_Tr2;  // transpiration in layer 2 [m]
  grid *_Tr3;  // transpiration in layer 3 [m]
  /* end of Fluxes */

 
  
  Basin(Control &ctrl);  // constrcuctor of Basin
  //dtor
  ~Basin();  // destrcuctor of Basin

  // report time series at gauging stations or maps
  int report(Control &ctrl);  
  int reportMap(const grid *input, string varname, string filepath);
  int reportTS(const grid *input, string varname, string filepath);




  

};

#endif /* BASIN_H_ */
