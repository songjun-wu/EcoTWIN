#ifndef BASIN_H_
#define BASIN_H_

#include "Param.h"
#include "Atmosphere.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Basin {
  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  sortedGrid _sortedGrid;
  /* end of Properties */

  public:
  /* GIS */
  svector *_dem;  // Surface evelation [m]
  svector *_chnwidth;  // Channel width [m]
  svector *_chndepth;  // Channel depth [m]
  svector *_chnlength;  // Channel length [m]
  svector *_depth1;  // Depth of soil layer 1 [m]
  svector *_depth2;  // Depth of soil layer 2 [m]
  /* end of GIS */


  /* Storages */ 
  svector *_I;  // Canopy storage [m]
  svector *_snow;  // Snow depth in [m]
  svector *_theta1;  // Soil moisture in layer 1 [decimal]
  svector *_theta2;  // Soil moisture in layer 2 [decimal]
  svector *_theta3;  // Soil moisture in layer 3 [decimal]
  /* end of Storages */ 
 

  /* Fluxes */
  svector *_D;  // Interception [m]
  svector *_Th;  // Throughfall [m]
  svector *_snowmelt;  // Snow melt [m]
  svector *_Qs;  // Overland flow [m]
  svector *_infilt;  // Inflitration into soil layer 1 [m]
  svector *_Perc1;  // Percolation into layer 2 [m]
  svector *_Perc2;  // Percolation into layer 3 [m]
  svector *_Perc3;  // Percolation into gw reservior [m]
  svector *_Ei;  // Canopy evaporation [m]
  svector *_Es;  // Soil evaporation [m]
  svector *_Tr;  // Total transpiration in three layers [m]
  svector *_Tr1;  // Transpiration in layer 1 [m]
  svector *_Tr2;  // Transpiration in layer 2 [m]
  svector *_Tr3;  // Transpiration in layer 3 [m]
  svector *_Ks1;  // Saturated hydraulic conductivity in layer 1
  svector *_Ks2;  // Saturated hydraulic conductivity in layer 2
  svector *_Ks3;  // Saturated hydraulic conductivity in layer 3
  svector *_thetaFC1;  // Field capacity in layer 1
  svector *_thetaFC2;  // Field capacity in layer 2
  svector *_thetaFC3;  // Field capacity in layer 3
  svector *_thetaWP1;  // Wilting point in layer 1
  svector *_thetaWP2;  // Wilting point in layer 2
  svector *_thetaWP3;  // Wilting point in layer 3
  svector *_froot_soil;  // froot coefficient for all soil profile
  svector *_froot_layer2;  // froot coefficient for layer 2
  svector *_froot_layer3;  // froot coefficient for layer 3
  /* end of Fluxes */

 
  
  Basin(Control &ctrl);  // constrcuctor of Basin
  //dtor
  ~Basin();  // destrcuctor of Basin
  int dtor(Control &ctrl);


  int Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm);

  /* Canopy interception */
  int Solve_canopy(Control &ctrl, Param &par, Atmosphere &atm);
  int Interception_1(Param &par, Atmosphere &atm, int j);
  int Interception_2(Param &par, Atmosphere &atm, int j);

  /* Snow accumulation and melt */
  int Solve_snowpack(Control &ctrl, Param &par, Atmosphere &atm);
  int Snow_acc_melt(Param &par, Atmosphere &atm, int j);

  /* Soil profiles */
  int Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm);
  
  int Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm, int j);


  int Soil_proporty_1(int opt_pedotransf, int opt_fieldcapacity, Param &par);
  int Soil_proporty_2(int opt_pedotransf, int opt_fieldcapacity, Param &par);
  int Soil_proporty_3(int opt_pedotransf, int opt_fieldcapacity, Param &par);
  int Van_Genuchten_1(double &VG_alpha, double &VG_n, double &VG_m, double clay, double silt, double organic_content, double bulk_density, int topsoil_factor);
  int Van_Genuchten_2(double &VG_alpha, double &VG_n, double &VG_m, double clay, double organic_content, double bulk_density, int topsoil_factor);
  int Van_Genuchten_3(double &VG_alpha, double &VG_n, double &VG_m, double clay, double sand, double organic_content, double bulk_density, int topsoil_factor);




  
  /* routing */
  int Routing_ovf(Control &ctrl, Param &par); // overland flow routing

};

#endif /* BASIN_H_ */
