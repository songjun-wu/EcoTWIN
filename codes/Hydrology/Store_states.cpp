/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Store_states.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"


int Basin::Store_states() {
    
    _I_old->equals(*_I);
    _snow_old->equals(*_snow);
    _pond_old->equals(*_pond);
    _theta1_old->equals(*_theta1);
    _theta2_old->equals(*_theta2);
    _theta3_old->equals(*_theta3);
    _GW_old->equals(*_GW);
    _chanS_old->equals(*_chanS);

    return EXIT_SUCCESS;
}