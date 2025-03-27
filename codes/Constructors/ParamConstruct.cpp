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
  if (ctrl.opt_intecept == 2 or ctrl.opt_evap == 1){
    _rE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new svector(_sortedGrid.size);
    _deg_day_min = new svector(_sortedGrid.size);
    _deg_day_max = new svector(_sortedGrid.size);
    _deg_day_increase = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_evap == 1){
    _froot_coeff = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_pedotransf == 1){
    _ref_thetaS = new svector(_sortedGrid.size);
    _PTF_VG_clay = new svector(_sortedGrid.size);
    _PTF_VG_Db = new svector(_sortedGrid.size);
    _PTF_Ks_const = new svector(_sortedGrid.size);
    _PTF_Ks_sand = new svector(_sortedGrid.size);
    _PTF_Ks_clay = new svector(_sortedGrid.size);
    _PTF_Ks_slope = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_fieldcapacity == 1){
    _SWP = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_infil == 1 or ctrl.opt_depthprofile == 2){
    _KvKh = new svector(_sortedGrid.size);
    _psiAE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_depthprofile == 2){
    _KKs = new svector(_sortedGrid.size);
    _Ksat = new svector(_sortedGrid.size);
    _BClambda = new svector(_sortedGrid.size);
  }
  /* end of Parameters */

  // Read parameter values from param.ini
  ReadParamFile(ctrl, fname);

  param_category = new svector_2d(ctrl.num_category , _sortedGrid);

  // Assign parameter spatially
  Parameterisation(ctrl);
}