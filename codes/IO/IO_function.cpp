/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* IO_function.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Control.h"

int Control::getAsciiHeader(string fname){
  ifstream input;
  string tags;
    
  input.open(fname.c_str());
  if (!input.good()){
    throw runtime_error(string("file not found: ") + fname.c_str());
  }
  input >> tags;
  input >> _colNum;
  input >> tags;
  input >> _rowNum;

  for (int i=0; i<3; i++){
    getline(input, tags);
  }

  input >> tags;
  input >> _dx;
  input >> tags;
  input >> _nodata;

  input.close();
  return EXIT_SUCCESS;
}

