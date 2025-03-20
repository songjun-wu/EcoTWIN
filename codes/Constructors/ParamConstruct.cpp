#include "Param.h"

Param::Param(Control &ctrl){
  _rowNum = ctrl._rowNum0;
  _colNum = ctrl._colNum0;
  _dx = ctrl._dx0;
  _nodata = ctrl._nodata0;

  string fname = "param.ini";
  /* Parameters */
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new grid(_rowNum, _colNum);
    _deg_day_min = new grid(_rowNum, _colNum);
    _deg_day_max = new grid(_rowNum, _colNum);
    _deg_day_increase = new grid(_rowNum, _colNum);
  }
  /* end of Parameters */
  ReadParamFile(ctrl, fname);

  param_category = new grid_3d(ctrl.num_category ,_rowNum, _colNum);

}