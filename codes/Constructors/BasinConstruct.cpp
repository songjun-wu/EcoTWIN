 #include "Basin.h"

 Basin::Basin(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;

  _sortedGrid = ctrl._sortedGrid;

  /* GIS */
  _dem = new svector(ctrl.path_BasinFolder + ctrl.fn__dem, _rowNum, _colNum, _sortedGrid);
  _chnwidth = new svector(ctrl.path_BasinFolder + ctrl.fn__chnwidth, _rowNum, _colNum, _sortedGrid);
  _chndepth = new svector(ctrl.path_BasinFolder + ctrl.fn__chndepth, _rowNum, _colNum, _sortedGrid);
  _chnlength = new svector(ctrl.path_BasinFolder + ctrl.fn__chnlength, _rowNum, _colNum, _sortedGrid);
  _depth1 = new svector(ctrl.path_BasinFolder + ctrl.fn__depth1, _rowNum, _colNum, _sortedGrid);
  _depth2 = new svector(ctrl.path_BasinFolder + ctrl.fn__depth2, _rowNum, _colNum, _sortedGrid);
  /* end of GIS */

  /* Storages */
  _I = new svector(ctrl.path_BasinFolder + ctrl.fn__I, _rowNum, _colNum, _sortedGrid);
  _snow = new svector(ctrl.path_BasinFolder + ctrl.fn__snow, _rowNum, _colNum, _sortedGrid);
  _theta1 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta1, _rowNum, _colNum, _sortedGrid);
  _theta2 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta2, _rowNum, _colNum, _sortedGrid);
  _theta3 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta3, _rowNum, _colNum, _sortedGrid);
  /* end of Storages */

  /* Fluxes */
  _D = new svector(_sortedGrid.size);
  _Th = new svector(_sortedGrid.size);
  _snowmelt = new svector(_sortedGrid.size);
  _Qs = new svector(_sortedGrid.size);
  _infilt = new svector(_sortedGrid.size);
  _Perc1 = new svector(_sortedGrid.size);
  _Perc2 = new svector(_sortedGrid.size);
  _Perc3 = new svector(_sortedGrid.size);
  _Ei = new svector(_sortedGrid.size);
  _Es = new svector(_sortedGrid.size);
  _Tr = new svector(_sortedGrid.size);
  _Tr1 = new svector(_sortedGrid.size);
  _Tr2 = new svector(_sortedGrid.size);
  _Tr3 = new svector(_sortedGrid.size);
  _Ks1 = new svector(_sortedGrid.size);
  _Ks2 = new svector(_sortedGrid.size);
  _Ks3 = new svector(_sortedGrid.size);
  _thetaFC1 = new svector(_sortedGrid.size);
  _thetaFC2 = new svector(_sortedGrid.size);
  _thetaFC3 = new svector(_sortedGrid.size);
  _thetaWP1 = new svector(_sortedGrid.size);
  _thetaWP2 = new svector(_sortedGrid.size);
  _thetaWP3 = new svector(_sortedGrid.size);
  if (ctrl.opt_evap == 1){
    _froot_soil = new svector(_sortedGrid.size);
    _froot_layer2 = new svector(_sortedGrid.size);
    _froot_layer3 = new svector(_sortedGrid.size);
  }
  /* end of Fluxes */

  
 
 }
