/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing_channel_tracking.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Mixing_channel_tracking(Control &ctrl, Atmosphere &atm, Param &par){


    /* Update the storages for routing flux mixing
    ### chanS:
    - irrigation_from_river
    (_chanS_old)
    + _Qupstream        (need to mix)
    + _ovf_toChn        (need to mix)
    +  _interf_toChn    (need to mix)
    + _GWf_toChn        (need to mix)
    - _Q
    - _Echan
    (_chanS)
    */

    // Isotopes
    if (ctrl.opt_tracking_isotope==1) {

        if (ctrl.opt_chanE > 0){
            _tmp->equals(*_chanS);
            _tmp->plus(*_Echan);
            // Fractionation due to channel evaporation
            Fractionation(atm, par, *_Echan, *_tmp, *_d18o_chanS, *_d18o_chanS, *_tmp, 0);  // issoil = 0
        }
    }

    // Nothing to preceed for Age 


    return EXIT_SUCCESS;
}
