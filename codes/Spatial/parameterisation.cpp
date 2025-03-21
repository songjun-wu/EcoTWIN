#include "Param.h"

int Param::Parameterisation(Control &ctrl){
    
  /* Parameters */
  int r;
  int c;
int nodata = ctrl._nodata;


  if (ctrl.opt_snow == 1){
  
  _snow_rain_thre->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (snow_rain_thre[k]!=nodata) {
  
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];
        _snow_rain_thre->matrix[r][c] += param_category->matrix[k][r][c] * snow_rain_thre[k];
     }
     }
     }

  
  _deg_day_min->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_min[k]!=nodata) {
  
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];
        _deg_day_min->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_min[k];
     }
     }
     }

  
  _deg_day_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_max[k]!=nodata) {
  
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];
        _deg_day_max->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_max[k];
     }
     }
     }

  
  _deg_day_increase->reset();
    for (int k=0; k<param_category->n_category; k++){
      if (deg_day_increase[k]!=nodata) {
  
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];
        _deg_day_increase->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_increase[k];
     }
     }
     }


  }
  /* end of Parameters */

    return EXIT_SUCCESS;
}