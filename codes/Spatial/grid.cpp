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


svector::svector(string fname , int rowNum, int colNum, sortedGrid _sortedGrid){
  ifstream input;
  string tags;
  size = _sortedGrid.size;
  val = new double[size];
  grid *temp;
  int r, c;

  temp = new grid(fname, rowNum, colNum);

  for (int j=0; j<size; j++){
    r = _sortedGrid.row[j];
    c = _sortedGrid.col[j];
    val[j] = temp->matrix[r][c];
  }
  delete temp;
}

svector_2d::svector_2d(int num_category, sortedGrid _sortedGrid){
  n_category = num_category;
  size = _sortedGrid.size;
  parameterisation_count = 0;

  val = new double*[num_category];

  for (int k=0; k<num_category; k++){
    val[k] = new double[size];
  }

}

int svector_2d::update(string fname, int num_category, int rowNum, int colNum, sortedGrid _sortedGrid){
  ifstream input;
  int r,c;
  int dim = rowNum*colNum;

  double *data=NULL;
  
  for (int k=0; k<num_category; k++){

    data = new double[dim];
    input.open((fname+to_string(k)+".bin").c_str(), ios::binary);
    if (!input.good()){
      throw runtime_error("file not found    :" + fname+to_string(k)+".bin");
    }
    input.seekg(sizeof(double)*dim*parameterisation_count);
    input.read((char *)data, sizeof(double)*dim);

    

    for (int j=0; j<size; j++){
      r = _sortedGrid.row[j];
      c = _sortedGrid.col[j];
      val[k][j] = data[r*colNum + c];
      
    }
    delete data;
    input.close();
    }

  parameterisation_count += 1;

  return EXIT_SUCCESS;
}

svector::svector(int length){
  size = length;
  val = new double[size];

  for (int j=0; j<size; j++){
    val[j] = 0;
  }
}

svector::~svector(){
  delete[] val;
}

svector_2d::~svector_2d(){
  for (int k = 0; k < n_category; k++){
    delete[] val[k];
  }
  delete[] val;
}

int svector::reset(){

  for (int j=0; j<size; j++){
    val[j] = 0;
  }
  return EXIT_SUCCESS;
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
      this->matrix[i][j] = 0;
    }
  }
}


int grid::reset(){
  for (int i=0; i<nrow; i++){
    for (int j=0; j<ncol; j++){
      matrix[i][j] = 0;
    }
  }
  return EXIT_SUCCESS;
}

grid::~grid(){
  for (int i = 0; i < nrow; i++)
    delete[] matrix[i];
  delete[] matrix;
}



