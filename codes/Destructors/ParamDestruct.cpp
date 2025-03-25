#include "Param.h"

Param::~Param(){}

int Param::dtor(Control &ctrl){
  
  /* Parameters */
  if(_depth3) delete _depth3;
  if(_alpha) delete _alpha;
  if (ctrl.opt_intecept == 2 or ctrl.opt_evap == 1){
    if(_rE) delete _rE;
  }
  if (ctrl.opt_snow == 1){
    if(_snow_rain_thre) delete _snow_rain_thre;
    if(_deg_day_min) delete _deg_day_min;
    if(_deg_day_max) delete _deg_day_max;
    if(_deg_day_increase) delete _deg_day_increase;
  }
  if (ctrl.opt_evap == 1){
    if(_froot_coeff) delete _froot_coeff;
  }
  if (ctrl.opt_pedotransf == 1){
    if(_ref_thetaS) delete _ref_thetaS;
    if(_PTF_VG_clay) delete _PTF_VG_clay;
    if(_PTF_VG_Db) delete _PTF_VG_Db;
    if(_PTF_Ks_const) delete _PTF_Ks_const;
    if(_PTF_Ks_sand) delete _PTF_Ks_sand;
    if(_PTF_Ks_clay) delete _PTF_Ks_clay;
    if(_PTF_Ks_slope) delete _PTF_Ks_slope;
  }
  if (ctrl.opt_fieldcapacity == 1){
    if(_SWP) delete _SWP;
  }
  /* end of Parameters */

  if(param_category) delete param_category;

  return EXIT_SUCCESS;

}