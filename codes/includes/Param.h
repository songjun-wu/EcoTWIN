
#include "Basin.h"

#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Param {

  /* Properties */
  int _rowNum, _colNum;
  double _dx, _nodata;
  /* end of Properties */

  string line_string;

  public:
  /* Parameters */
  vector<double> snow_rain_thre;
  vector<double> deg_day_min;
  vector<double> deg_day_max;
  vector<double> deg_day_increase;
  grid *_snow_rain_thre;  // The temperature  [m]
  grid *_deg_day_min;  // Degree-day factor with no precipitation [m-1 degreeC-1]
  grid *_deg_day_max;  // Maximum Degree-day factor [m-1 degreeC-1]
  grid *_deg_day_increase;  // Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]
  /* end of Parameters */

  grid_3d *param_category;

  //ctor from raster ascii file
  Param(Control &ctrl);
  //dtor
  ~Param();

  // Functions
  int ReadParamFile(Control &ctrl, string fname = "param.ini");  // Read parameters into array
  int Parameterisation(Control &ctrl); // Assign parameter values to each grid

  void readIntoParam(vector<double>& param_arr, string key, vector<string> lines);


};