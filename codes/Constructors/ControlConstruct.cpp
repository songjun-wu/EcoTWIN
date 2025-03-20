#include "Control.h"

Control::Control(){
  string confilename = "config.ini";

  ReadConfigFile(confilename);
  
  getAsciiHeader(path_BasinFolder+fn__dem);

  _fdir = new grid(path_BasinFolder + fn__fdir, _rowNum, _colNum);
  _Gauge_to_Report = new grid(path_BasinFolder + fn__Gauge_to_Report, _rowNum, _colNum);

  //sort grids spatially
  _sortedGrid = SortGridLDD();
  _Tsmask = sortTSmask();
  
}