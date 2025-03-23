#ifndef PARAM_H_
#define PARAM_H_

#include "Control.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Param {

  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  sortedGrid _sortedGrid;
  /* end of Properties */

  string line_string;

  public:
  /* Parameters */
  vector<double> depth3;
  vector<double> alpha;
  vector<double> rE;
  vector<double> snow_rain_thre;
  vector<double> deg_day_min;
  vector<double> deg_day_max;
  vector<double> deg_day_increase;
  svector *_depth3;  // Depth of soil layer 3 [m]
  svector *_alpha;  // The weighting parameter that links LAI and maximum canopy storage
  svector *_rE;  // Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)
  svector *_snow_rain_thre;  // The temperature for snow melt  [m]
  svector *_deg_day_min;  // Degree-day factor with no precipitation [m-1 degreeC-1]
  svector *_deg_day_max;  // Maximum Degree-day factor [m-1 degreeC-1]
  svector *_deg_day_increase;  // Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]
  /* end of Parameters */

  svector_2d *param_category;

  //ctor from raster ascii file
  Param(Control &ctrl);
  //dtor
  ~Param();
  int dtor(Control &ctrl);

  // Functions
  int ReadParamFile(Control &ctrl, string fname = "param.ini");  // Read parameters into array
  int Parameterisation(Control &ctrl); // Assign parameter values to each grid

  void readIntoParam(vector<double>& param_arr, string key, vector<string> lines);


};

#endif /* PARAM_H_ */