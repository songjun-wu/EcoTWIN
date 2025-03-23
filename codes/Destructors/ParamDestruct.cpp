#include "Param.h"

Param::~Param(){}

int Param::dtor(Control &ctrl){
  
  /* Parameters */
  if(_alpha) delete _alpha;
  if (ctrl.opt_intecept == 2){
    if(_rE) delete _rE;
  }
  if (ctrl.opt_snow == 1){
    if(_snow_rain_thre) delete _snow_rain_thre;
    if(_deg_day_min) delete _deg_day_min;
    if(_deg_day_max) delete _deg_day_max;
    if(_deg_day_increase) delete _deg_day_increase;
  }
  /* end of Parameters */

  if(param_category) delete param_category;

  return EXIT_SUCCESS;

}