/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* sortGridLDD.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Control.h"

sortedGrid Control::SortGridLDD(){
  int value, value1, value2, value3, value4, value6, value7, value8, value9 = 0;
  int r, c, rr ,cc;
  int counter=0;
  grid *temp, *to_row, *to_col;
  sortedGrid map2array;

  temp = new grid(_rowNum, _colNum);

  to_row = new grid(_rowNum, _colNum);
  to_col = new grid(_rowNum, _colNum);

  *temp = *_fdir;

  for (r=1; r<_rowNum; r++){
    for (c=1; c<_colNum; c++){
      value = temp->matrix[r][c];
      if (value> -2 && value <130){
        counter++;
      }     
    }
  }

  int x, i, j = 0;

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
              
              switch (value) 
              {
              case -1:  // outlet
                  rr = -9999;
                  cc = -9999;
              case 5:  // outlet
                  rr = -9999;
                  cc = -9999;
              case 8:
                  rr = r+1;
                  cc = c-1;
                  break;
              case 4:
                  rr = r+1;
                  cc = c;
                  break;
              case 2:
                  rr = r+1;
                  cc = c+1;
                  break;
              case 16:
                  rr = r;
                  cc = c-1;
                  break;
              case 1:
                  rr = r;
                  cc = c+1;
                  break;
              case 32:
                  rr = r-1;
                  cc = c-1;
              break;
              case 64:
                  rr = r-1;
                  cc = c;
                  break;
              case 128:
                  rr = r-1;
                  cc = c+1;
                  break;
              default:
                  cout<< " Sorting flow direction FAILED!" <<endl;
                  cout<< " Invalid flow direction " << value << " was found in grid " << r << " "<< c << endl;
                  exit(EXIT_FAILURE);
                  }
                
              map2array.row.push_back(r);
              map2array.col.push_back(c);
              map2array.lat_ok.push_back(0);
              map2array.to_cell.push_back(-9999);
              to_row->matrix[r][c] = rr;
              to_col->matrix[r][c] = cc;
        }
      }
    }

    for (i=0; i<map2array.row.size(); i++){
      r = map2array.row[i];
      c = map2array.col[i];
      temp->matrix[r][c] = _nodata;
    }
  }while(map2array.row.size()<counter);

  for (i=0; i<(map2array.row.size() - 1); i++){
  //for (i=0; i<1; i++){
    r = map2array.row[i];
    c = map2array.col[i];
    rr = to_row->matrix[r][c];
    cc = to_col->matrix[r][c];

    for (j=i; j<map2array.row.size(); j++){
      if (rr==map2array.row[j] and cc==map2array.col[j]){
        map2array.to_cell[i] = j;
        map2array.lat_ok[i] = 1;
        
        break;
      }
    }
  }



  map2array.size = int(map2array.row.size());

  delete temp;
  delete to_row;
  delete to_col;

  return map2array;
}