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


int Basin::Mixing_baseflow(double storage, double &coutput, double input, double cinput, double output){

    // Baseflow mixing equation from INCA model and mhM-nitrate model

    double k1, k2, k3, k4;
    double y1, y2, y3;

    double retention_storage = max(storage * 5e2, 1.0);

    k1 = (input * cinput - output * coutput) / retention_storage;
    y1 = coutput + k1 * 0.5;
    k2 = (input * cinput - output * y1) / retention_storage;
    y2 = coutput + k2 * 0.5;
    k3 = (input * cinput - output * y2) / retention_storage;
    y3 = coutput + k2;
    k4 = (input * cinput - output * y3) / retention_storage;

    coutput = coutput + (k1 + 2*k2 +2*k3 + k4)/6.0;

    return EXIT_SUCCESS;
}


