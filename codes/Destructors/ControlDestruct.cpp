#include "Param.h"

Control::~Control(){}


int Control::dtor(){

  if (_Gauge_to_Report) delete _Gauge_to_Report;

  return EXIT_SUCCESS;

}