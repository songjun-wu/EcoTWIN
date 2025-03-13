#include "Control.h"

int Control::getAsciiHeader(string fname){
  ifstream input;
  string tags;
    
  input.open(fname.c_str());
  if (!input.good()){
    throw runtime_error(string("file not found: ") + fname.c_str());
  }
  input >> tags;
  input >> _colNum0;
  input >> tags;
  input >> _rowNum0;

  for (int i=0; i<3; i++){
    getline(input, tags);
  }

  input >> tags;
  input >> _dx0;
  input >> tags;
  input >> _nodata0;

  input.close();
  return EXIT_SUCCESS;
}

