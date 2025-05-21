#include "Basin.h"

int Basin::open_groundTs(Control &ctrl){
  open_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  return EXIT_SUCCESS;
}

int Basin::read_groundTs(Control &ctrl){
  read_groundTs_maps(if__LAI, *_LAI);
  return EXIT_SUCCESS;
}

int Basin::open_groundTs_maps(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file not found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Basin::read_groundTs_maps(ifstream &ifHandle, svector &climateMap){
  double *data=NULL;
  int dim  = _rowNum*_colNum;
  int r, c;
  data = new double[dim];
  ifHandle.read((char *)data, sizeof(double)*dim);
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    r = _sortedGrid.row[j];
    c = _sortedGrid.col[j];
    climateMap.val[j] = data[r*_colNum + c];
  }
  delete[] data;
  return EXIT_SUCCESS;
}

int Basin::init_groundTs(Control &ctrl){
  init_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  return EXIT_SUCCESS;
}

int Basin::update_groundTs(Control &ctrl, Param &par){
  update_groundTs_maps(if__LAI, par, *_LAI);
  return EXIT_SUCCESS;
}

int Basin::init_groundTs_maps(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file now found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Basin::update_groundTs_maps(ifstream &ifHandle, Param &par, svector &groundTsMap){
  double *data=NULL;
  int nzones = par.param_category->n_category;
  data = new double[nzones];
  ifHandle.read((char *)data, sizeof(double)*nzones); 
 
  groundTsMap.reset();
  for (int k=1; k<nzones; k++){  // The first category is for global inputs; Skipped because all GroundTs inputs are land use or soil dependent
      if (data[k]!=_nodata){
      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        groundTsMap.val[j] += par.param_category->val[k][j] * data[k];
   }}}
  delete[] data;
  return EXIT_SUCCESS;
}