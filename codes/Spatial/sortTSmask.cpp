#include "Control.h"
#include <numeric>

sortedTSmask Control::sortTSmask(){
  sortedTSmask TSmask;
  vector<int> Gauge_vector;
  vector<int> sortedgrid_vector;
  vector<int> cell_id_vector;

  // Get the number of sites
  for(int j = 0; j < _sortedGrid.size; j++){
    if (_Gauge_to_Report->val[j] > 0){
      Gauge_vector.push_back(int(_Gauge_to_Report->val[j]));
      sortedgrid_vector.push_back(j);
    }
  }

  vector<int> sorted_idx = VectorArgSort(Gauge_vector);

  for(long unsigned int j = 0; j < sorted_idx.size(); j++){
    TSmask.cell.push_back(sortedgrid_vector[sorted_idx[j]]);
  }

  return TSmask;
}



vector<int> Control::VectorArgSort(vector<int> &v) {
    /* Get the indices that gives a sorted vector v*/

    vector<int> retIndices(v.size());
    iota(retIndices.begin(), retIndices.end(), 0);

    stable_sort(
        retIndices.begin(), retIndices.end(),
        [&v](int i1, int i2) {return v[i1] < v[i2];});

    return retIndices;
}

