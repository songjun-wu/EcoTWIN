#include "Basin.h"

int Basin::Initialisation(Control &ctrl, Param &par, Atmosphere &atm){

    // Initialisation of GW storage
    if (ctrl.opt_init_GW == 1){
      _GW->equals(*par._init_GW);
    }

    // Initilisation of old storages
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
      Store_states();  // Store all water storages for mixing
      _d18o_GW->equals(*par._d18o_init_GW); // Asign isotopic composition to GW
    }

    if (ctrl.opt_nitrogen_sim==1){
      _TchanS->equals(*atm._Ta);
    }

    // Initilisation of channel storage
    double sqrtS, Manningn, a, Q, chnwidth;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        chnwidth = _chnwidth->val[j];  // [m]
        if(chnwidth > 0) {
            sqrtS = pow(_slope->val[j], 0.5);
            Manningn = par._Manningn->val[j] * _chnlength->val[j];  // Manning's N scaled with channel length
            Q = _Q->val[j]; // Discharge [m3/s]
            
            a = pow(pow(chnwidth,0.67)*Manningn/sqrtS, 0.6); //wetted perimeter approximated with channel width
            _chanS->val[j] = Q > 0 ? a * pow(Q, 0.6)/_chnlength->val[j] : 0.0;
          } else {
            _chanS->val[j] = 0.0;
          }

    }
    return EXIT_SUCCESS;
}