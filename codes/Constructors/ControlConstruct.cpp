#include "Control.h"

Control::Control(){
  string confilename = "config.ini";

  ReadConfigFile(confilename);
  getAsciiHeader(path_BasinFolder+fn__dem);

  //sort grids spatially
  _fdir = new grid(path_BasinFolder + fn__fdir, _rowNum, _colNum);
  _sortedGrid = SortGridLDD();
  
  _Gauge_to_Report = new svector(path_BasinFolder + fn__Gauge_to_Report, _rowNum, _colNum, _sortedGrid);
  _Tsmask = sortTSmask();

  
}