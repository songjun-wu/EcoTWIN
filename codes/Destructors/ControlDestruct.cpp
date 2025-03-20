#include "Param.h"

Control::~Control(){
  
  if(_fdir) delete _fdir;
  if (_Gauge_to_Report) delete _Gauge_to_Report;

}