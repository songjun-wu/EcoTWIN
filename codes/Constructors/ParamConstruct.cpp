#include "Param.h"

Param::Param(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;
  
  _sortedGrid = ctrl._sortedGrid;

  string fname = "param.ini";
  /* Parameters */
  _depth3 = new svector(_sortedGrid.size);
  _alpha = new svector(_sortedGrid.size);
  if (ctrl.opt_intecept == 2){
    _rE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new svector(_sortedGrid.size);
    _deg_day_min = new svector(_sortedGrid.size);
    _deg_day_max = new svector(_sortedGrid.size);
    _deg_day_increase = new svector(_sortedGrid.size);
  }
  /* end of Parameters */

  // Read parameter values from param.ini
  ReadParamFile(ctrl, fname);

  param_category = new svector_2d(ctrl.num_category , _sortedGrid);

  // Assign parameter spatially
  Parameterisation(ctrl);
}