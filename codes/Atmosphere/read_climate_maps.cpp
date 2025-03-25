#include "Atmosphere.h"

int Atmosphere::open_climate(Control &ctrl){
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  if (ctrl.opt_evap == 1){
    open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__PET, if__PET);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate(Control &ctrl){
  read_climate_maps(if__P, *_P);
  read_climate_maps(if__Ta, *_Ta);
  read_climate_maps(if__RH, *_RH);
  read_climate_maps(if__LAI, *_LAI);
  if (ctrl.opt_evap == 1){
    read_climate_maps(if__PET, *_PET);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::open_climate_maps(string fname, ifstream &ifHandle){
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file not found    :" + fname);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::read_climate_maps(ifstream &ifHandle, svector &climateMap){
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

int Atmosphere::init_climate(Control &ctrl){
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__P, if__P);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__Ta, if__Ta);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__RH, if__RH);
  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__LAI, if__LAI);
  if (ctrl.opt_evap == 1){
    init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn__PET, if__PET);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::update_climate(Control &ctrl){
  update_climate_maps(if__P, *_P);
  update_climate_maps(if__Ta, *_Ta);
  update_climate_maps(if__RH, *_RH);
  update_climate_maps(if__LAI, *_LAI);
  if (ctrl.opt_evap == 1){
    update_climate_maps(if__PET, *_PET);
  }
  return EXIT_SUCCESS;
}

int Atmosphere::init_climate_maps(string fname, ifstream &ifHandle){
  int max = 0;
  ifHandle.open(fname, ios::binary);
  if (!ifHandle.good()){
    throw runtime_error("file now found    :" + fname);
  }
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    if (_climzones->val[j] > max){
      max = _climzones->val[j];
    }
  _nzones = max+1;
  }
  return EXIT_SUCCESS;
}

int Atmosphere::update_climate_maps(ifstream &ifHandle, svector &climateMap){
  double *data=NULL;
  int zoneID;
  data = new double[_nzones];
  ifHandle.read((char *)data, sizeof(double)*_nzones);  
  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

    zoneID = _climzones->val[j];
    climateMap.val[j] = data[zoneID];
    }
  
  delete[] data;
  return EXIT_SUCCESS;
}