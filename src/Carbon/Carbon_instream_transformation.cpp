/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_instream_transformation.cpp
  * Created  on: 05.02.2026
  * Modified on: 05.02.2026
***************************************************************/


#include "Basin.h"

int Basin::Carbon_instream_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double doc_chanS, doc_CP_chanS, fct_TchanS, respiration_river;
    double dx = ctrl._dx;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps

    // Calculate instream temperature
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _TchanS->val[j] += (atm._Ta->val[j] - _TchanS->val[j]) / 20.0;  // Instream temperature conceptualised as 20-day's average of air temperature

    }

    // Calculate in-stream DOC production
    /*
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        if (_chnlength->val[j] > 0){    // If this is a channel cell
            if (_chanS->val[j] > 0){
                _doc_chanS->val[j] += _NPP->val[j] * 0.02 / dx / dx * _chnlength->val[j] * _chnwidth->val[j] / _chanS->val[j];
            }
        }
    }
    */

    // Calculate heterotrophic respiration of DOC
    /*
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        if (_chnlength->val[j] > 0){    // If this is a channel cell

            respiration_river = 0;  // DOC consumed by heterotrophic respiration [gC/m2]

            if (_chanS->val[j] > 0){

                doc_chanS =  _doc_chanS->val[j];
                doc_CP_chanS = doc_chanS * _chanS->val[j];  // in-stream IN storage [gC/m2]

                
                fct_TchanS = Temp_factor(_TchanS->val[j], par._transformation_exp_base->val[j]);  // Instream temperature factor [-]

                // Instream heterotrophic respiration during the timestep DT; scaled by river temperature and channel length
                respiration_river = doc_CP_chanS * min(par._respiration_river->val[j] * fct_TchanS * (_chnlength->val[j] / dx) * DT, 1.0);  // [gC/m2]

                // Update global variables
                
                _doc_chanS->val[j] = (doc_CP_chanS - respiration_river) / _chanS->val[j];  // [gC/m2/m = gC/m3 = mgC/L]
                _respiration_river_C->val[j] = respiration_river; // [gC/m2]               
                
            } else {
                _respiration_river_C->val[j] = 0;
                _doc_chanS->val[j] = 0;
            }
        }
    }
    */

    return EXIT_SUCCESS;
}


