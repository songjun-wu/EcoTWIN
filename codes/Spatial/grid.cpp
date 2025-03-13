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