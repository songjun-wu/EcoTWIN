/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Hydrology_summary.cpp
  * Created  on: 23.12.2025
  * Modified on: 23.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Hydrology_summary(){

    _infilt->plus(*_rinfilt);
    _Perc1->plus(*_rPerc1);
    _Perc2->plus(*_rPerc2);
    _Perc3->plus(*_rPerc3);
    _Perc_vadose->plus(*_rPerc_vadose);

    return EXIT_SUCCESS;
}