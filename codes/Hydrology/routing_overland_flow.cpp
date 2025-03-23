#include "Basin.h"

int Basin::Routing_ovf(Control &ctrl, Param &par){

    int to_j, lat_ok;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        _Qs->val[j] = 1;
    }

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    

        if (_sortedGrid.lat_ok[j] == 1){
            _Qs->val[_sortedGrid.to_cell[j]] += _Qs->val[j];
        }
        
    }

    return EXIT_SUCCESS;
}