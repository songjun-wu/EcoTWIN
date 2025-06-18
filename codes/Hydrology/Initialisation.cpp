/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Initialisation.cpp
  * Created  on: 30.02.2025
  * Modified on: 03.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Initialisation(Control &ctrl, Param &par, Atmosphere &atm){

    // Initialisation of GW storage
    if (ctrl.opt_init_GW == 1){
      _GW->equals(*par._init_GW);
    }

    // Initilisation of old storages
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
      Store_states();  // Store all water storages for mixing
    }

    // Adjust the initial d18o composition if needed
    if (ctrl.opt_tracking_isotope==1 and ctrl.opt_init_d18o==1){
    _d18o_chanS->plus(*par._delta_d18o_init_GW); // Asign isotopic composition to channel storage
    _d18o_layer1->plus(*par._delta_d18o_init_GW); // Asign isotopic composition to soil layer1
    _d18o_layer2->plus(*par._delta_d18o_init_GW); // Asign isotopic composition to soil layer2
    _d18o_layer3->plus(*par._delta_d18o_init_GW); // Asign isotopic composition to soil layer3
    _d18o_GW->plus(*par._delta_d18o_init_GW); // Asign isotopic composition to GW
    }


    // Adjust the initial no3 composition if needed
    if (ctrl.opt_nitrogen_sim==1 and ctrl.opt_init_no3==1){
    _no3_chanS->plus(*par._delta_no3_init_GW); // Asign isotopic composition to channel storage
    _no3_layer1->plus(*par._delta_no3_init_GW); // Asign isotopic composition to soil layer1
    _no3_layer2->plus(*par._delta_no3_init_GW); // Asign isotopic composition to soil layer2
    _no3_layer3->plus(*par._delta_no3_init_GW); // Asign isotopic composition to soil layer3
    _no3_GW->plus(*par._delta_no3_init_GW); // Asign isotopic composition to GW

    // Avoid negative values
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
      _no3_chanS->val[j] = max(0.0, _no3_chanS->val[j]);
      _no3_layer1->val[j] = max(0.0, _no3_layer1->val[j]);
      _no3_layer2->val[j] = max(0.0, _no3_layer2->val[j]);
      _no3_layer3->val[j] = max(0.0, _no3_layer3->val[j]);
      _no3_GW->val[j] = max(0.0, _no3_GW->val[j]);
    }

    }

    // Init channel temperature
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