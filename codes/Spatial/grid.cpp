#include "dataType.h"

grid::grid(string fname, int rowNum, int colNum){
  ifstream input;
  string tags;
  nrow = rowNum;
  ncol = colNum;
  matrix = new double*[rowNum];

  for (int i=0; i<rowNum; i++){
    matrix[i] = new double[colNum];
  }
  input.open(fname.c_str());
  if (!input.good()){
    throw runtime_error(string("file not found: ") + fname.c_str());
  }
  for (int i=0; i<6; i++){
    getline(input, tags);
  }

  for (int i=0; i<rowNum; i++){
    for (int j=0; j<colNum; j++){
      input >> matrix[i][j];
    }
  }
  input.close();  
}


grid::grid(int rowNum, int colNum){
  nrow = rowNum;
  ncol = colNum;
  matrix = new double*[rowNum];
  for (int i=0; i<rowNum; i++){
    matrix[i] = new double[colNum];
  }
  for (int i=0; i<rowNum; i++){
    for (int j=0; j<colNum; j++){
      matrix[i][j] = 0;
    }
  }
}

grid::~grid(){
  for (int i = 0; i < nrow; i++)
    delete[] matrix[i];
  delete[] matrix;
}

grid_3d::~grid_3d(){
  for (int k = 0; k < n_category; k++){
    for (int i = 0; i < nrow; i++){
      delete[] matrix[k][i];
    }
    delete[] matrix[k];
  }
  delete[] matrix;
}


grid_3d::grid_3d(int num_category, int rowNum, int colNum){
  ifstream input;
  string tags;
  n_category = num_category;
  nrow = rowNum;
  ncol = colNum;
  string fname = "category_";
  matrix = new double**[rowNum];

  for (int k=0; k<num_category; k++){
    matrix[k] = new double*[rowNum];
  for (int i=0; i<rowNum; i++){
    matrix[k][i] = new double[colNum];
  }
}

  for (int k=0; k<num_category; k++){
  cout<<(fname+"_"+to_string(k)+".asc").c_str()<<endl;
  input.open((fname+to_string(k)+".asc").c_str());
  if (!input.good()){
    throw runtime_error(string("file not found: ") + (fname+"_"+to_string(k)+".asc").c_str());
  }
  for (int i=0; i<6; i++){
    getline(input, tags);
  }

  for (int i=0; i<rowNum; i++){
    for (int j=0; j<colNum; j++){
      input >> matrix[k][i][j];
    }
  }
  input.close();  
  }
}