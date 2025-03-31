#include "Basin.h"

int Basin::Routing_ovf_1(Control &ctrl, Param &par){

    int from_j;
    
    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double proportion_ovf_toChn;
    double ovf_to_go;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double chnwidth = _chnwidth->val[j];
        //double chndepth = _chndepth->val[j];
        double chnlength = _chnlength->val[j];
        from_j = _sortedGrid.to_cell[j];

        if (_sortedGrid.lat_ok[j] == 1){  // If there is a downstream cell

            ovf_to_go = _ovf_in->val[j] + _pond->val[j];  // Available surface water = ponding water + overland inflow from upstream cells

            if (chnwidth > 0){  // If there is channel in this grid cell
                proportion_ovf_toChn = min(par._pOvf_toChn->val[j] * (chnwidth * chnlength) / (dx_square) , 1.0);  // The proportion of overland flow that routes into river              
                _ovf_toChn->val[j] = ovf_to_go * proportion_ovf_toChn;
                ovf_to_go -= _ovf_toChn->val[j];
            }

            // Terrestrial grid cell
            _ovf_out->val[j] = ovf_to_go;
            _ovf_in->val[from_j] += ovf_to_go;
              
        }        
    }
    return EXIT_SUCCESS;
}