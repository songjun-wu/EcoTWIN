#ifndef BASIN_H_
#define BASIN_H_

#include "Param.h"
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
  grid *_dem;  // Surface evelation [m]
  grid *_chnwidth;  // Channel width [m]
  grid *_chndepth;  // Channel depth [m]
  grid *_chnlength;  // Channel length [m]
  grid *_depth1;  // Depth of soil layer 1 [m]
  grid *_depth2;  // Depth of soil layer 2 [m]
  grid *_depth3;  // Depth of soil layer 3 [m]
  /* end of GIS */


  /* Storages */ 
  grid *_I;  // Interception/canopy storage [m]
  grid *_snow;  // Snow depth in [m]
  grid *_theta1;  // Soil moisture in layer 1 [decimal]
  grid *_theta2;  // Soil moisture in layer 2 [decimal]
  grid *_theta3;  // Soil moisture in layer 3 [decimal]
  grid *_I_old;  // Interception/canopy storage in previous timestep in [m]
  /* end of Storages */ 
 

  /* Fluxes */
  grid *_D;  // Interception [m]
  grid *_Th;  // Throughfall [m]
  grid *_snowmelt;  // Snow melt [m]
  grid *_Qs;  // Overland flow [m]
  grid *_infilt;  // Inflitration into soil layer 1 [m]
  grid *_preferential2;  // Preferential flow to layer 2 [m]
  grid *_preferential3;  // Preferential flow to layer 3 [m]
  grid *_Perc1;  // Percolation into layer 2 [m]
  grid *_Perc2;  // Percolation into layer 3 [m]
  grid *_Perc3;  // Percolation into gw reservior [m]
  grid *_Ei;  // Canopy evaporation [m]
  grid *_Es;  // Soil evaporation [m]
  grid *_Tr;  // Total transpiration in three layers [m]
  grid *_Tr1;  // Transpiration in layer 1 [m]
  grid *_Tr2;  // Transpiration in layer 2 [m]
  grid *_Tr3;  // Transpiration in layer 3 [m]
  /* end of Fluxes */

 
  
  Basin(Control &ctrl);  // constrcuctor of Basin
  //dtor
  ~Basin();  // destrcuctor of Basin



};

#endif /* BASIN_H_ */
