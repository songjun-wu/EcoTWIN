 #include "Basin.h"

 Basin::Basin(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;

  _sortedGrid = ctrl._sortedGrid;

  /* GIS */
  _chnwidth = new svector(ctrl.path_BasinFolder + ctrl.fn__chnwidth, _rowNum, _colNum, _sortedGrid);
  _chndepth = new svector(ctrl.path_BasinFolder + ctrl.fn__chndepth, _rowNum, _colNum, _sortedGrid);
  _chnlength = new svector(ctrl.path_BasinFolder + ctrl.fn__chnlength, _rowNum, _colNum, _sortedGrid);
  _depth1 = new svector(ctrl.path_BasinFolder + ctrl.fn__depth1, _rowNum, _colNum, _sortedGrid);
  _depth2 = new svector(ctrl.path_BasinFolder + ctrl.fn__depth2, _rowNum, _colNum, _sortedGrid);
  _sand1 = new svector(ctrl.path_BasinFolder + ctrl.fn__sand1, _rowNum, _colNum, _sortedGrid);
  _clay1 = new svector(ctrl.path_BasinFolder + ctrl.fn__clay1, _rowNum, _colNum, _sortedGrid);
  _organic1 = new svector(ctrl.path_BasinFolder + ctrl.fn__organic1, _rowNum, _colNum, _sortedGrid);
  _bulkdensity1 = new svector(ctrl.path_BasinFolder + ctrl.fn__bulkdensity1, _rowNum, _colNum, _sortedGrid);
  if (ctrl.opt_depthprofile == 3){
    _sand2 = new svector(ctrl.path_BasinFolder + ctrl.fn__sand2, _rowNum, _colNum, _sortedGrid);
    _sand3 = new svector(ctrl.path_BasinFolder + ctrl.fn__sand3, _rowNum, _colNum, _sortedGrid);
    _clay2 = new svector(ctrl.path_BasinFolder + ctrl.fn__clay2, _rowNum, _colNum, _sortedGrid);
    _clay3 = new svector(ctrl.path_BasinFolder + ctrl.fn__clay3, _rowNum, _colNum, _sortedGrid);
    _silt2 = new svector(ctrl.path_BasinFolder + ctrl.fn__silt2, _rowNum, _colNum, _sortedGrid);
    _organic2 = new svector(ctrl.path_BasinFolder + ctrl.fn__organic2, _rowNum, _colNum, _sortedGrid);
    _organic3 = new svector(ctrl.path_BasinFolder + ctrl.fn__organic3, _rowNum, _colNum, _sortedGrid);
    _bulkdensity2 = new svector(ctrl.path_BasinFolder + ctrl.fn__bulkdensity2, _rowNum, _colNum, _sortedGrid);
    _bulkdensity3 = new svector(ctrl.path_BasinFolder + ctrl.fn__bulkdensity3, _rowNum, _colNum, _sortedGrid);
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2){
    _silt1 = new svector(ctrl.path_BasinFolder + ctrl.fn__silt1, _rowNum, _colNum, _sortedGrid);
  }
  if (ctrl.opt_depthprofile == 3 or ctrl.opt_pedotransf == 2){
    _silt3 = new svector(ctrl.path_BasinFolder + ctrl.fn__silt3, _rowNum, _colNum, _sortedGrid);
  }
  /* end of GIS */

  /* Storages */
  _I = new svector(ctrl.path_BasinFolder + ctrl.fn__I, _rowNum, _colNum, _sortedGrid);
  _snow = new svector(ctrl.path_BasinFolder + ctrl.fn__snow, _rowNum, _colNum, _sortedGrid);
  _pond = new svector(ctrl.path_BasinFolder + ctrl.fn__pond, _rowNum, _colNum, _sortedGrid);
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
  _Recharge = new svector(_sortedGrid.size);
  _Ei = new svector(_sortedGrid.size);
  _Es = new svector(_sortedGrid.size);
  _Tr = new svector(_sortedGrid.size);
  _Tr1 = new svector(_sortedGrid.size);
  _Tr2 = new svector(_sortedGrid.size);
  _Tr3 = new svector(_sortedGrid.size);
  _Ks1 = new svector(_sortedGrid.size);
  _Ks2 = new svector(_sortedGrid.size);
  _Ks3 = new svector(_sortedGrid.size);
  _thetaS1 = new svector(_sortedGrid.size);
  _thetaS2 = new svector(_sortedGrid.size);
  _thetaS3 = new svector(_sortedGrid.size);
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
