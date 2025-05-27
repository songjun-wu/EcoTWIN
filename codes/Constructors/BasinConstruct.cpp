/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* BasinConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


 #include "Basin.h"

 Basin::Basin(Control &ctrl, Param &par){
  
  roundoffERR = 1e-12;
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;

  _sortedGrid = ctrl._sortedGrid;

  /* GIS */
  _chnwidth = new svector(ctrl.path_BasinFolder + ctrl.fn__chnwidth, _rowNum, _colNum, _sortedGrid);
  _chndepth = new svector(ctrl.path_BasinFolder + ctrl.fn__chndepth, _rowNum, _colNum, _sortedGrid);
  _chnlength = new svector(ctrl.path_BasinFolder + ctrl.fn__chnlength, _rowNum, _colNum, _sortedGrid);
  _slope = new svector(ctrl.path_BasinFolder + ctrl.fn__slope, _rowNum, _colNum, _sortedGrid);
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
    _silt3 = new svector(ctrl.path_BasinFolder + ctrl.fn__silt3, _rowNum, _colNum, _sortedGrid);
    _organic2 = new svector(ctrl.path_BasinFolder + ctrl.fn__organic2, _rowNum, _colNum, _sortedGrid);
    _organic3 = new svector(ctrl.path_BasinFolder + ctrl.fn__organic3, _rowNum, _colNum, _sortedGrid);
    _bulkdensity2 = new svector(ctrl.path_BasinFolder + ctrl.fn__bulkdensity2, _rowNum, _colNum, _sortedGrid);
    _bulkdensity3 = new svector(ctrl.path_BasinFolder + ctrl.fn__bulkdensity3, _rowNum, _colNum, _sortedGrid);
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2){
    _silt1 = new svector(ctrl.path_BasinFolder + ctrl.fn__silt1, _rowNum, _colNum, _sortedGrid);
  }
  /* end of GIS */

  /* GroundTs */
  _LAI = new svector(_sortedGrid.size);
  /* end of GroundTs */

  /* Storages */
  _I = new svector(ctrl.path_BasinFolder + ctrl.fn__I, _rowNum, _colNum, _sortedGrid);
  _snow = new svector(ctrl.path_BasinFolder + ctrl.fn__snow, _rowNum, _colNum, _sortedGrid);
  _pond = new svector(ctrl.path_BasinFolder + ctrl.fn__pond, _rowNum, _colNum, _sortedGrid);
  _theta1 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta1, _rowNum, _colNum, _sortedGrid);
  _theta2 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta2, _rowNum, _colNum, _sortedGrid);
  _theta3 = new svector(ctrl.path_BasinFolder + ctrl.fn__theta3, _rowNum, _colNum, _sortedGrid);
  _GW = new svector(ctrl.path_BasinFolder + ctrl.fn__GW, _rowNum, _colNum, _sortedGrid);
  _chanS = new svector(_sortedGrid.size);
  if (ctrl.opt_tracking_isotope == 1 or ctrl.opt_tracking_age == 1 or ctrl.opt_nitrogen_sim == 1){
    _I_old = new svector(_sortedGrid.size);
    _snow_old = new svector(_sortedGrid.size);
    _pond_old = new svector(_sortedGrid.size);
    _theta1_old = new svector(_sortedGrid.size);
    _theta2_old = new svector(_sortedGrid.size);
    _theta3_old = new svector(_sortedGrid.size);
    _GW_old = new svector(_sortedGrid.size);
    _chanS_old = new svector(_sortedGrid.size);
  }
  /* end of Storages */

  /* Fluxes */
  _Th = new svector(_sortedGrid.size);
  _snowmelt = new svector(_sortedGrid.size);
  _infilt = new svector(_sortedGrid.size);
  _Perc1 = new svector(_sortedGrid.size);
  _Perc2 = new svector(_sortedGrid.size);
  _Perc3 = new svector(_sortedGrid.size);
  _rrPerc3 = new svector(_sortedGrid.size);
  _Ei = new svector(_sortedGrid.size);
  _Es = new svector(_sortedGrid.size);
  _Tr = new svector(_sortedGrid.size);
  _Tr1 = new svector(_sortedGrid.size);
  _Tr2 = new svector(_sortedGrid.size);
  _Tr3 = new svector(_sortedGrid.size);
  _irrigation_from_river = new svector(_sortedGrid.size);
  _irrigation_from_GW = new svector(_sortedGrid.size);
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
  _ovf_in = new svector(_sortedGrid.size);
  _ovf_out = new svector(_sortedGrid.size);
  _ovf_toChn = new svector(_sortedGrid.size);
  _interf_in = new svector(_sortedGrid.size);
  _interf_out = new svector(_sortedGrid.size);
  _interf_toChn = new svector(_sortedGrid.size);
  _GWf_in = new svector(_sortedGrid.size);
  _GWf_out = new svector(_sortedGrid.size);
  _GWf_toChn = new svector(_sortedGrid.size);
  _Q = new svector(ctrl.path_BasinFolder + ctrl.fn__Q, _rowNum, _colNum, _sortedGrid);
  _Qupstream = new svector(_sortedGrid.size);
  _Echan = new svector(_sortedGrid.size);
  _tmp = new svector(_sortedGrid.size);
  _snowacc = new svector(_sortedGrid.size);
  _TchanS = new svector(_sortedGrid.size);
  if (ctrl.opt_reinfil == 1){
    _rinfilt = new svector(_sortedGrid.size);
    _rPerc1 = new svector(_sortedGrid.size);
    _rPerc2 = new svector(_sortedGrid.size);
    _rPerc3 = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_evap == 1){
    _froot_layer1 = new svector(_sortedGrid.size);
    _froot_layer2 = new svector(_sortedGrid.size);
    _froot_layer3 = new svector(_sortedGrid.size);
    _PE = new svector(_sortedGrid.size);
    _PT = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_percolation == 1){
    _p_perc1 = new svector(_sortedGrid.size);
    _p_perc2 = new svector(_sortedGrid.size);
    _p_perc3 = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_tracking_isotope == 1 or ctrl.opt_tracking_age == 1 or ctrl.opt_nitrogen_sim == 1){
    _flux_ovf_in_acc = new svector(_sortedGrid.size);
    _flux_interf_in_acc = new svector(_sortedGrid.size);
    _flux_GWf_in_acc = new svector(_sortedGrid.size);
    _flux_Qupstream_acc = new svector(_sortedGrid.size);
  }
  /* end of Fluxes */

  /* Tracking */
  if (ctrl.opt_tracking_isotope == 1){
    _d18o_I = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_I, _rowNum, _colNum, _sortedGrid);
    _d18o_snow = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_snow, _rowNum, _colNum, _sortedGrid);
    _d18o_pond = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_pond, _rowNum, _colNum, _sortedGrid);
    _d18o_layer1 = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_layer1, _rowNum, _colNum, _sortedGrid);
    _d18o_layer2 = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_layer2, _rowNum, _colNum, _sortedGrid);
    _d18o_layer3 = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_layer3, _rowNum, _colNum, _sortedGrid);
    _d18o_GW = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_GW, _rowNum, _colNum, _sortedGrid);
    _d18o_chanS = new svector(ctrl.path_BasinFolder + ctrl.fn__d18o_chanS, _rowNum, _colNum, _sortedGrid);
  }
  if (ctrl.opt_tracking_age == 1){
    _age_I = new svector(ctrl.path_BasinFolder + ctrl.fn__age_I, _rowNum, _colNum, _sortedGrid);
    _age_snow = new svector(ctrl.path_BasinFolder + ctrl.fn__age_snow, _rowNum, _colNum, _sortedGrid);
    _age_pond = new svector(ctrl.path_BasinFolder + ctrl.fn__age_pond, _rowNum, _colNum, _sortedGrid);
    _age_layer1 = new svector(ctrl.path_BasinFolder + ctrl.fn__age_layer1, _rowNum, _colNum, _sortedGrid);
    _age_layer2 = new svector(ctrl.path_BasinFolder + ctrl.fn__age_layer2, _rowNum, _colNum, _sortedGrid);
    _age_layer3 = new svector(ctrl.path_BasinFolder + ctrl.fn__age_layer3, _rowNum, _colNum, _sortedGrid);
    _age_GW = new svector(ctrl.path_BasinFolder + ctrl.fn__age_GW, _rowNum, _colNum, _sortedGrid);
    _age_chanS = new svector(ctrl.path_BasinFolder + ctrl.fn__age_chanS, _rowNum, _colNum, _sortedGrid);
  }
  /* end of Tracking */

  /* Nitrogen */
  if (ctrl.opt_nitrogen_sim == 1){
    _no3_I = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_I, _rowNum, _colNum, _sortedGrid);
    _no3_snow = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_snow, _rowNum, _colNum, _sortedGrid);
    _no3_pond = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_pond, _rowNum, _colNum, _sortedGrid);
    _no3_layer1 = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_layer1, _rowNum, _colNum, _sortedGrid);
    _no3_layer2 = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_layer2, _rowNum, _colNum, _sortedGrid);
    _no3_layer3 = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_layer3, _rowNum, _colNum, _sortedGrid);
    _no3_GW = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_GW, _rowNum, _colNum, _sortedGrid);
    _no3_chanS = new svector(ctrl.path_BasinFolder + ctrl.fn__no3_chanS, _rowNum, _colNum, _sortedGrid);
    _nitrogen_add = new svector(_sortedGrid.size);
    _plant_uptake = new svector(_sortedGrid.size);
    _deni_soil = new svector(_sortedGrid.size);
    _minerl_soil = new svector(_sortedGrid.size);
    _degrad_soil = new svector(_sortedGrid.size);
    _deni_river = new svector(_sortedGrid.size);
    _humusN1 = new svector(ctrl.path_BasinFolder + ctrl.fn__humusN1, _rowNum, _colNum, _sortedGrid);
    _humusN2 = new svector(ctrl.path_BasinFolder + ctrl.fn__humusN2, _rowNum, _colNum, _sortedGrid);
    _humusN3 = new svector(ctrl.path_BasinFolder + ctrl.fn__humusN3, _rowNum, _colNum, _sortedGrid);
    _fastN1 = new svector(ctrl.path_BasinFolder + ctrl.fn__fastN1, _rowNum, _colNum, _sortedGrid);
    _fastN2 = new svector(ctrl.path_BasinFolder + ctrl.fn__fastN2, _rowNum, _colNum, _sortedGrid);
    _fastN3 = new svector(ctrl.path_BasinFolder + ctrl.fn__fastN3, _rowNum, _colNum, _sortedGrid);
  }
  /* end of Nitrogen */

  _slope->higherthan(0.01);

  if (ctrl.opt_groundTs_input_format == 1){
    open_groundTs(ctrl);
    read_groundTs(ctrl);
  } else if  (ctrl.opt_groundTs_input_format == 2) {
    init_groundTs(ctrl); // create maps for Ground inputs
    update_groundTs(ctrl, par); // update maps for Ground inputs
  }

  // Read nitrogen addition information
  if (ctrl.opt_nitrogen_sim==1 or ctrl.opt_irrigation==1){
    ReadCropFile(ctrl, par, "Crop_info.ini");
  }
  
 
 }
