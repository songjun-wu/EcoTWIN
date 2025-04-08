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
  vector<double> froot_coeff;
  vector<double> ref_thetaS;
  vector<double> PTF_VG_clay;
  vector<double> PTF_VG_Db;
  vector<double> PTF_Ks_const;
  vector<double> PTF_Ks_sand;
  vector<double> PTF_Ks_clay;
  vector<double> PTF_Ks_slope;
  vector<double> SWP;
  vector<double> KvKh;
  vector<double> psiAE;
  vector<double> KKs;
  vector<double> Ksat;
  vector<double> BClambda;
  vector<double> percExp;
  vector<double> wRecharge;
  vector<double> pOvf_toChn;
  vector<double> interfExp;
  vector<double> winterf;
  vector<double> GWfExp;
  vector<double> wGWf;
  vector<double> Manningn;
  svector *_depth3;  // Depth of soil layer 3 [m]
  svector *_alpha;  // The weighting parameter that links LAI and maximum canopy storage [-]
  svector *_rE;  // Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)
  svector *_snow_rain_thre;  // The temperature for snow melt  [m]
  svector *_deg_day_min;  // Degree-day factor with no precipitation [m-1 degreeC-1]
  svector *_deg_day_max;  // Maximum Degree-day factor [m-1 degreeC-1]
  svector *_deg_day_increase;  // Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]
  svector *_froot_coeff;  // Root fraction coefficient [-]
  svector *_ref_thetaS;  // Reference saturated soil moisture [-]
  svector *_PTF_VG_clay;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  svector *_PTF_VG_Db;  // Pedotransfer function for parameter estimation of Van Genuchten Model [-]
  svector *_PTF_Ks_const;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_PTF_Ks_sand;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_PTF_Ks_clay;  // Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]
  svector *_PTF_Ks_slope;  // Slope correction for estimation of saturated hydraulic conductivity [-]
  svector *_SWP;  // Soil water potentail for field capacity estimation [-], only needed when opt_fieldcapacity = 1
  svector *_KvKh;  // The coefficient to transform Ks to effective Ks [-], only needed when opt_infil = 1
  svector *_psiAE;  // The wetting front potential for Green-Ampt model [mm], only needed when opt_infil = 1
  svector *_KKs;  // The exponential parameter for depth-dependent saturated hydraulic conductivity [-], only needed when opt_depthprofile = 2
  svector *_Ksat;  // The exponential parameter for depth-dependent saturated moisture content  [-], only needed when opt_depthprofile = 2
  svector *_BClambda;  // The exponential parameter for depth-dependent field capacity  [-], only needed when opt_depthprofile = 2
  svector *_percExp;  // The exponential parameter for percolation [-], only needed when opt_percolation = 2
  svector *_wRecharge;  // The weighting parameter for GW recharge [-], only needed when opt_recharge = 1
  svector *_pOvf_toChn;  // The weighting linear parameter for overland flow routing towards channel  [-]
  svector *_interfExp;  // The exponetial weighting parameter for interflow flow routing towards channel  [-]
  svector *_winterf;  // The weight parameter in kinematic wave solution  [-]
  svector *_GWfExp;  // The exponetial weighting parameter for GW flow routing towards channel  [-]
  svector *_wGWf;  // The active proportion of GW storage that contributes to channel recharge  [-]
  svector *_Manningn;  // Manning N for stream routing [-], only needed when opt_routQ = 1
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