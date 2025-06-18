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

int Basin::Instream_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double no3_chanS, IN_chanS, fct_TchanS, fct_conc, chanS_m3, deni_river;
    double dx_double = ctrl._dx * ctrl._dx;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _TchanS->val[j] += (atm._Ta->val[j] - _TchanS->val[j]) / 20.0;  // Instream temperature conceptualised as 20-day's average of air temperature

    }

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        if (_chnlength->val[j] > 0){    // If this is a channel cell

            deni_river = 0;

            if (_chanS->val[j] > 0){

                no3_chanS =  _no3_chanS->val[j];
                chanS_m3 = _chanS->val[j] * dx_double;  // Channel storage in m3
                IN_chanS = no3_chanS * chanS_m3;  // in-stream IN storage [mgN/L * m3 = gN]

                
                fct_TchanS = Temp_factor(_TchanS->val[j]);  // Instream temperature factor [-]
                fct_conc = no3_chanS / (no3_chanS + 1.5);  // Concentration factor [-]

                // Instream denitrification
                deni_river = min(par._denitrification_river->val[j] * fct_TchanS * fct_conc * (_chnlength->val[j] * _chnwidth->val[j]) / DT, IN_chanS);  // [gN]

                // Update global variables
                _no3_chanS->val[j] = (IN_chanS - deni_river) / (chanS_m3);  // [gN/m3 = mgN/L]
                _deni_river->val[j] = deni_river / dx_double; // from [gN] to [gN/m2]; consistent with other N processes

            } else {
                _deni_river->val[j] = 0;
                _no3_chanS->val[j] = 0;
            }
        }
    }

    return EXIT_SUCCESS;
}


