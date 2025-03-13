 #include "Atmosphere.h"

 Atmosphere::Atmosphere(Control &ctrl, Basin &bsn){

  _rowNum = ctrl._rowNum0;
  _colNum = ctrl._colNum0;
  _dx = ctrl._dx0;
  _nodata = ctrl._nodata0;

  _sortedGrid = bsn._sortedGrid;

  /* Climate */
  _P = new grid(_rowNum, _colNum);
  _Ta = new grid(_rowNum, _colNum);
  _Tmin = new grid(_rowNum, _colNum);
  _Tmax = new grid(_rowNum, _colNum);
  _RH = new grid(_rowNum, _colNum);
  _LAI = new grid(_rowNum, _colNum);
  /* end of Climate */


  if (ctrl.opt_climate_input_format == 2) {
    _climzones = new grid(ctrl.path_BasinFolder + ctrl.fn__climzones, _rowNum, _colNum);
  }
  
  if (ctrl.opt_climate_input_format == 1){
    open_climate(ctrl);
    read_climate(ctrl);
  } else if  (ctrl.opt_climate_input_format == 2) {
    init_climate(ctrl); // create maps for climate parameters
    update_climate(ctrl); // update maps for climate parameters
  }
  
 }