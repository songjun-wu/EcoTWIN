#include "Param.h"

Param::~Param(){
  
  /* Parameters */
  if(_snow_rain_thre) delete _snow_rain_thre;
  if(_deg_day_min) delete _deg_day_min;
  if(_deg_day_max) delete _deg_day_max;
  if(_deg_day_increase) delete _deg_day_increase;
  /* end of Parameters */

  if(param_category) delete param_category;

}