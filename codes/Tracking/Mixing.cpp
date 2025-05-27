/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Mixing.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"

int Basin::Mixing_full(double storage, double &cstorage, double input, double cinput){

    if (input > roundoffERR){ // if there is inflow
        cstorage = (storage * cstorage + input * cinput) / (storage + input);
    } 
    else if ((input + storage) <= 0) {
        cstorage = 0.0;
    }


    return EXIT_SUCCESS;
}
