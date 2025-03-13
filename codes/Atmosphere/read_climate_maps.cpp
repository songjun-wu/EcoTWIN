#include "Atmosphere.h"

int Atmosphere::open_climate(Control &ctrl){
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Tmin, if__Tmin);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Tmax, if__Tmax);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate(Control &ctrl){
  read_climate_maps(if__P, *_P);
  read_climate_maps(if__Ta, *_Ta);
  read_climate_maps(if__Tmin, *_Tmin);
  read_climate_maps(if__Tmax, *_Tmax);
  read_climate_maps(if__RH, *_RH);
  read_climate_maps(if__LAI, *_LAI);
  return EXIT_SUCCESS;
}

int Atmosphere::open_climate_maps(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file now found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate_maps(ifstream &ifHandle, grid &climateMap){
  double *data=NULL;
  int dim  = _rowNum*_colNum;
  data = new double[dim];
  ifHandle.read((char *)data, sizeof(double)*dim);

  for (int r = 1; r < _rowNum; r++){
    for (int c = 1; c < _colNum; c++){
      climateMap.matrix[r][c] = data[r*_colNum + c];
    }
  }
  delete[] data;
  return EXIT_SUCCESS;
}

int Atmosphere::init_climate(Control &ctrl){
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Tmin, if__Tmin);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Tmax, if__Tmax);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  return EXIT_SUCCESS;
}

int Atmosphere::update_climate(Control &ctrl){
  update_climate_maps(if__P, *_P);
  update_climate_maps(if__Ta, *_Ta);
  update_climate_maps(if__Tmin, *_Tmin);
  update_climate_maps(if__Tmax, *_Tmax);
  update_climate_maps(if__RH, *_RH);
  update_climate_maps(if__LAI, *_LAI);
  return EXIT_SUCCESS;
}

int Atmosphere::init_climate_maps(string fname, ifstream &ifHandle){
  int max = 0;
  int r, c;
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file now found    :" + fname);
  }
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
	  r = _sortedGrid.row[j];
	  c = _sortedGrid.col[j];
    if (_climzones->matrix[r][c] > max){
      max = _climzones->matrix[r][c];
    }
  _nzones = max+1;
  }
  return EXIT_SUCCESS;
}

int Atmosphere::update_climate_maps(ifstream &ifHandle, grid &climateMap){
  double *data=NULL;
  int r, c;
  int zoneID;

  data = new double[_nzones];
  ifHandle.read((char *)data, sizeof(double)*_nzones);  
  
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
	  r = _sortedGrid.row[j];
	  c = _sortedGrid.col[j];
    zoneID = _climzones->matrix[r][c];
    climateMap.matrix[r][c] = data[zoneID];
    }
  delete[] data;
  return EXIT_SUCCESS;
}