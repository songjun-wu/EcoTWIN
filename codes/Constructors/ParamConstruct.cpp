#include "Param.h"

Param::Param(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;
  
  _sortedGrid = ctrl._sortedGrid;

  string fname = "param.ini";
  /* Parameters */
  _alpha = new grid(_rowNum, _colNum);
  if (ctrl.opt_intecept == 2){
    _rE = new grid(_rowNum, _colNum);
  }
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new grid(_rowNum, _colNum);
    _deg_day_min = new grid(_rowNum, _colNum);
    _deg_day_max = new grid(_rowNum, _colNum);
    _deg_day_increase = new grid(_rowNum, _colNum);
  }
  /* end of Parameters */

  // Read parameter values from param.ini
  ReadParamFile(ctrl, fname);

  param_category = new grid_3d(ctrl.path_BasinFolder+"category_", ctrl.num_category ,_rowNum, _colNum);
  
  // Assign parameter spatially
  Parameterisation(ctrl);
}