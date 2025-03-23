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

struct grid_3d{
    int n_category, nrow, ncol;
    double ***matrix;
    //ctor from raster ascii file
    grid_3d(string fname, int num_category, int rowNum, int colNum);
    //dtor
    ~grid_3d();
};

struct svector{
    double *value;
    //ctor from raster ascii file
    svector(string fname, sortedGrid _sortedGrid);
    //dtor
    ~svector();
}



struct sortedGrid{
    int numCells;
    int zone_climate;
    vector<int> row;
    vector<int> col;
    vector<int> dir;
};

struct sortedTSmask{
    vector<int> row;
    vector<int> col;
};