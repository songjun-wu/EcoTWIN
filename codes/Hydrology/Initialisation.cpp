#include "Basin.h"

int Basin::Initialisation(Control &ctrl, Param &par){
    double sqrtS, Manningn, a, Q, chnwidth;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        sqrtS = pow(_slope->val[j], 0.5);
        Manningn = par._Manningn->val[j] * _chnlength->val[j];  // Manning's N scaled with channel length
        chnwidth = _chnwidth->val[j];  // [m]
        Q = _Q->val[j]; // Discharge [m3/s]

        if(chnwidth > 0) {
            a = pow(pow(chnwidth,0.67)*Manningn/sqrtS, 0.6); //wetted perimeter approximated with channel width
            _chanS->val[j] = Q > 0 ? a * pow(Q, 0.6)/_chnlength->val[j] : 0.0;
          } else {
            _chanS->val[j] = 0.0;
          }

    }
    return EXIT_SUCCESS;
}