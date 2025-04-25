#include "Basin.h"

int Basin::Instream_transformation(Control &ctrl, Atmosphere &atm, Param &par){

    double no3_chanS, IN_chanS, fct_TchanS, fct_conc, chanS_m3;
    double dx_double = ctrl._dx * ctrl._dx;
    double DT = ctrl.Simul_tstep / 86400;  // all rates are calculated at daily timesteps


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _TchanS->val[j] += (atm._Ta->val[j] - _TchanS->val[j]) / 20.0;  // Instream temperature conceptualised as 20-day's average of air temperature

    }

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        if (_chnlength > 0){    // If this is a channel cell

            if (_chanS->val[j] > 0){

                no3_chanS =  _no3_chanS->val[j];
                chanS_m3 = _chanS->val[j] * dx_double;  // Channel storage in m3
                IN_chanS = no3_chanS * chanS_m3;  // in-stream IN storage [mgN/L * m3 = gN]

                
                fct_TchanS = Temp_factor(_TchanS->val[j]);  // Instream temperature factor [-]
                fct_conc = no3_chanS / (no3_chanS + 1.5);  // Concentration factor [-]

                // Instream denitrification
                _deni_river->val[j] = min(par._denitrification_river->val[j] * fct_TchanS * fct_conc * (_chnlength->val[j] * _chnwidth->val[j]) / DT, IN_chanS);  // [gN]


                // Update global variables
                _no3_chanS->val[j] = (IN_chanS - _deni_river->val[j]) / (chanS_m3);  // [g/m3 = mg/L]

            } else {
                _deni_river->val[j] = 0;
                _no3_chanS->val[j] = 0;
            }
        }
    }

    return EXIT_SUCCESS;
}


