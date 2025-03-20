#include "Param.h"

int Param::Parameterisation(Control &ctrl){
    
  /* Parameters */
  if (ctrl.opt_snow == 1){
    _snow_rain_thre->reset();
    for (int k=0; k<param_category->n_category; k++){
      for (int i=0; i<param_category->nrow; i++){
        for (int j=0; j<param_category->ncol; j++){
          _snow_rain_thre->matrix[i][j] += param_category->matrix[k][i][j] * snow_rain_thre[k];
    }}}
    _deg_day_min->reset();
    for (int k=0; k<param_category->n_category; k++){
      for (int i=0; i<param_category->nrow; i++){
        for (int j=0; j<param_category->ncol; j++){
          _deg_day_min->matrix[i][j] += param_category->matrix[k][i][j] * deg_day_min[k];
    }}}
    _deg_day_max->reset();
    for (int k=0; k<param_category->n_category; k++){
      for (int i=0; i<param_category->nrow; i++){
        for (int j=0; j<param_category->ncol; j++){
          _deg_day_max->matrix[i][j] += param_category->matrix[k][i][j] * deg_day_max[k];
    }}}
    _deg_day_increase->reset();
    for (int k=0; k<param_category->n_category; k++){
      for (int i=0; i<param_category->nrow; i++){
        for (int j=0; j<param_category->ncol; j++){
          _deg_day_increase->matrix[i][j] += param_category->matrix[k][i][j] * deg_day_increase[k];
    }}}
  }
  /* end of Parameters */

    return EXIT_SUCCESS;
}