/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* dataType.h
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#ifndef dataType_H_
#define dataType_H_
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;


struct grid{
    int nrow, ncol;
    double **matrix;
    //ctor from raster ascii file
    grid(int rowNum, int colNum);
    grid(string fname, int rowNum, int colNum);
    //dtor
    ~grid();

    int reset();
};



struct sortedGrid{
    int size;
    //int zone_climate;
    vector<int> row;  // row ID
    vector<int> col;  // col ID
    vector<int> to_cell;  // vector ID of downstream cell
    vector<int> lat_ok;  // 1: there is a downstream cell; 0: outlet
};

struct sortedTSmask{
    vector<int> cell;
};


struct svector{
    int size;
    double *val;
    //ctor from raster ascii file
    svector(string fname, int rowNum, int colNum, sortedGrid _sortedGrid);
    svector(int length);
    //dtor
    ~svector();

    int reset();
    int equals(svector &sv);
    int plus(svector &sv);
    int minus(svector &sv);
    int multiply(svector &sv);
    int higherthan(double max);
};

struct svector_2d{
    int parameterisation_OK; // = 0 for a fresh update for each parameterisation
    int sort_PTF; // = 0 for a fresh update for each parameterisation
    int sort_perc_travel_time_OK; // = 0 for a fresh update for each parameterisation
    int parameterisation_count; // How many times of parametersation have been done?
    int n_category, size;
    double **val;
    //ctor from raster ascii file
    svector_2d(int num_category, sortedGrid _sortedGrid);
    //dtor
    ~svector_2d();
    int update(string fname, int num_category, int rowNum, int colNum, sortedGrid _sortedGrid);
};

#endif /* dataType_H_ */