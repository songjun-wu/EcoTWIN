 #include "Basin.h"

 Basin::Basin(Control &ctrl){
  _rowNum = ctrl._rowNum0;
  _colNum = ctrl._colNum0;
  _dx = ctrl._dx0;
  _nodata = ctrl._nodata0;

  /* GIS */
  _dem = new grid(ctrl.path_BasinFolder + ctrl.fn__dem, _rowNum, _colNum);
  _fdir = new grid(ctrl.path_BasinFolder + ctrl.fn__fdir, _rowNum, _colNum);
  _chnwidth = new grid(ctrl.path_BasinFolder + ctrl.fn__chnwidth, _rowNum, _colNum);
  _chndepth = new grid(ctrl.path_BasinFolder + ctrl.fn__chndepth, _rowNum, _colNum);
  _chnlength = new grid(ctrl.path_BasinFolder + ctrl.fn__chnlength, _rowNum, _colNum);
  _depth1 = new grid(ctrl.path_BasinFolder + ctrl.fn__depth1, _rowNum, _colNum);
  _depth2 = new grid(ctrl.path_BasinFolder + ctrl.fn__depth2, _rowNum, _colNum);
  _depth3 = new grid(ctrl.path_BasinFolder + ctrl.fn__depth3, _rowNum, _colNum);
  _Gauge_to_Report = new grid(ctrl.path_BasinFolder + ctrl.fn__Gauge_to_Report, _rowNum, _colNum);
  /* end of GIS */

  /* Storages */
  _I = new grid(ctrl.path_BasinFolder + ctrl.fn__I, _rowNum, _colNum);
  _snow = new grid(ctrl.path_BasinFolder + ctrl.fn__snow, _rowNum, _colNum);
  _theta1 = new grid(ctrl.path_BasinFolder + ctrl.fn__theta1, _rowNum, _colNum);
  _theta2 = new grid(ctrl.path_BasinFolder + ctrl.fn__theta2, _rowNum, _colNum);
  _theta3 = new grid(ctrl.path_BasinFolder + ctrl.fn__theta3, _rowNum, _colNum);
  _I_old = new grid(_rowNum, _colNum);
  /* end of Storages */

  /* Fluxes */
  _D = new grid(_rowNum, _colNum);
  _Th = new grid(_rowNum, _colNum);
  _snowmelt = new grid(_rowNum, _colNum);
  _Qs = new grid(_rowNum, _colNum);
  _infilt = new grid(_rowNum, _colNum);
  _preferential2 = new grid(_rowNum, _colNum);
  _preferential3 = new grid(_rowNum, _colNum);
  _Perc1 = new grid(_rowNum, _colNum);
  _Perc2 = new grid(_rowNum, _colNum);
  _Perc3 = new grid(_rowNum, _colNum);
  _Ei = new grid(_rowNum, _colNum);
  _Es = new grid(_rowNum, _colNum);
  _Tr = new grid(_rowNum, _colNum);
  _Tr1 = new grid(_rowNum, _colNum);
  _Tr2 = new grid(_rowNum, _colNum);
  _Tr3 = new grid(_rowNum, _colNum);
  /* end of Fluxes */

  //sort grids spatially
  _sortedGrid = SortGridLDD();
  _Tsmask = sortTSmask();
 
 }
