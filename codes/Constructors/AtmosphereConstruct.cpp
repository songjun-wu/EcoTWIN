 #include "Atmosphere.h"

 Atmosphere::Atmosphere(Control &ctrl){

  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;

  _sortedGrid = ctrl._sortedGrid;

  /* Climate */
  _P = new svector(_sortedGrid.size);
  _Ta = new svector(_sortedGrid.size);
  _RH = new svector(_sortedGrid.size);
  _LAI = new svector(_sortedGrid.size);
  if (ctrl.opt_evap == 1){
    _PET = new svector(_sortedGrid.size);
  }
  /* end of Climate */


  if (ctrl.opt_climate_input_format == 2) {
    _climzones = new svector(ctrl.path_BasinFolder + ctrl.fn__climzones, _rowNum, _colNum, _sortedGrid);
  }
  
  if (ctrl.opt_climate_input_format == 1){
    open_climate(ctrl);
    read_climate(ctrl);
  } else if  (ctrl.opt_climate_input_format == 2) {
    init_climate(ctrl); // create maps for climate parameters
    update_climate(ctrl); // update maps for climate parameters
  }
  
 }