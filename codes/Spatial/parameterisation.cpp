#include "Param.h"

int Param::Parameterisation(Control &ctrl){
    
  /* Parameters */
  int r;
  int c;

  if (ctrl.opt_snow == 1){
    _snow_rain_thre->reset();
    _deg_day_min->reset();
    _deg_day_max->reset();
    _deg_day_increase->reset();
  
  for (unsigned int j = 0; j < ctrl._sortedGrid.row.size(); j++) {
      r = ctrl._sortedGrid.row[j];
      c = ctrl._sortedGrid.col[j];

      for (int k=0; k<param_category->n_category; k++){
        _snow_rain_thre->matrix[r][c] += param_category->matrix[k][r][c] * snow_rain_thre[k];
        _deg_day_min->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_min[k];
        _deg_day_max->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_max[k];
        _deg_day_increase->matrix[r][c] += param_category->matrix[k][r][c] * deg_day_increase[k];
     }
     }

  }
  /* end of Parameters */

    return EXIT_SUCCESS;
}