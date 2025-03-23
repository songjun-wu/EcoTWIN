#include "Control.h"

sortedTSmask Control::sortTSmask(){
  sortedTSmask TSmask;
  
  for(int j = 0; j < _sortedGrid.size; j++){
    if (_Gauge_to_Report->val[j] >= 0){
      TSmask.cell.push_back(j);
  }
  }

  return TSmask;
}