#include "Control.h"

sortedGrid Control::SortGridLDD(){
  int value, value1, value2, value3, value4, value6, value7, value8, value9 = 0;
  int r, c;
  int counter=0;
  grid *temp;
  sortedGrid map2array;

  temp = new grid(_rowNum, _colNum);

  *temp = *_fdir;

  for (r=1; r<_rowNum; r++){
    for (c=1; c<_colNum; c++){
      value = temp->matrix[r][c];
      if (value>0 && value <130 && value!=5){
        counter++;
        
      }     
    }
  }

  
  int x, i = 0;
  do{
    x++;
    for (r=1; r<_rowNum-1; r++){
      for (c=1; c<_colNum-1; c++){
        value = temp->matrix[r][c];
        if (value==_nodata) continue;
        value7 = temp->matrix[r-1][c-1];
	      value8 = temp->matrix[r-1][c];
	      value9 = temp->matrix[r-1][c+1];
	      value4 = temp->matrix[r][c-1];
	      value6 = temp->matrix[r][c+1];
	      value1 = temp->matrix[r+1][c-1];
	      value2 = temp->matrix[r+1][c];
	      value3 = temp->matrix[r+1][c+1];
        
        if (value7 != 2 &&
	          value8 != 4 &&
	          value9 != 8 &&
	          value4 != 1 &&
	          value6 != 16 &&
	          value1 != 128 &&
	          value2 != 64 &&
	          value3 != 32 &&
	          value != _nodata){
              map2array.row.push_back(r);
              map2array.col.push_back(c);
            }  
      }
    }
    for (; i<map2array.row.size(); i++){
      r = map2array.row[i];
      c = map2array.col[i];
      temp->matrix[r][c] = _nodata;
    }
  }while(map2array.row.size()<counter);

  //delete temp;
  return map2array;
}