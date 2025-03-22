#include "Control.h"

sortedTSmask Control::sortTSmask(){
  sortedTSmask TSmask;
  for(int i = 1; i < _rowNum-1; i++){
    for(int j = 1; j < _colNum-1; j++){
        if (_Gauge_to_Report->matrix[i][j] >= 0){
            TSmask.row.push_back(i);
            TSmask.col.push_back(j);
        }
    }
  }
  return TSmask;
}