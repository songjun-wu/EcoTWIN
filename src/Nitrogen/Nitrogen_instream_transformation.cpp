/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Instream_transformation.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Nitrogen_instream_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double no3_chanS, IN_chanS, fct_TchanS, fct_conc, deni_river;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps


    // Instream temperature is calculated in Carbon_instream_transformation.cpp
    //for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    //    _TchanS->val[j] += (atm._Ta->val[j] - _TchanS->val[j]) / 20.0;  // Instream temperature conceptualised as 20-day's average of air temperature
    //}

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        if (_chnlength->val[j] > 0){    // If this is a channel cell

            deni_river = 0;  // Denitrification in the river [gN/m2]

            if (_chanS->val[j] > 0){

                no3_chanS =  _no3_chanS->val[j];
                IN_chanS = no3_chanS * _chanS->val[j];  // in-stream IN storage [gN/m2]

                
                fct_TchanS = Temp_factor(_TchanS->val[j]);  // Instream temperature factor [-]
                fct_conc = no3_chanS / (no3_chanS + 1.5);  // Concentration factor [-]

                // Instream denitrification during the timestep DT; scaled by river temperature and channel length [gN/m2]
                deni_river = IN_chanS * min(par._denitrification_river->val[j] * fct_TchanS * fct_conc * (_chnlength->val[j] / ctrl._dx) * DT, 1.0);  // [gN/m2]

                // Update global variables
                _no3_chanS->val[j] = (IN_chanS - deni_river) / _chanS->val[j];  // [gN/m2/m = gN/m3 = mgN/L]
                _deni_river->val[j] = deni_river; // [gN/m2]

            } else {
                _deni_river->val[j] = 0;
                _no3_chanS->val[j] = 0;
            }
        }
    }

    return EXIT_SUCCESS;
}


