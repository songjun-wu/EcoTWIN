#include "Param.h"

int Param::Parameterisation(Control &ctrl){

  // Update the parameterisation due to the changes in land use types
  param_category->update(ctrl.path_BasinFolder+"category_", ctrl.num_category ,_rowNum, _colNum, _sortedGrid);

  /* Parameters */
  int nodata = ctrl._nodata;


  _depth3->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (depth3[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _depth3->val[j] += param_category->val[k][j] * depth3[k];
   }}}

  _alpha->reset();
  for (int k=0; k<param_category->n_category; k++){
    if (alpha[k]!=nodata) {
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _alpha->val[j] += param_category->val[k][j] * alpha[k];
   }}}

  if (ctrl.opt_intecept == 2){
  
  _rE->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (rE[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _rE->val[j] += param_category->val[k][j] * rE[k];
     }}}

  }

  if (ctrl.opt_snow == 1){
  
  _snow_rain_thre->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (snow_rain_thre[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _snow_rain_thre->val[j] += param_category->val[k][j] * snow_rain_thre[k];
     }}}
  
  _deg_day_min->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_min[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _deg_day_min->val[j] += param_category->val[k][j] * deg_day_min[k];
     }}}
  
  _deg_day_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_max[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _deg_day_max->val[j] += param_category->val[k][j] * deg_day_max[k];
     }}}
  
  _deg_day_increase->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_increase[k]!=nodata) {
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _deg_day_increase->val[j] += param_category->val[k][j] * deg_day_increase[k];
     }}}

  }
  /* end of Parameters */
  
  return EXIT_SUCCESS;
}