/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Soil_temperature.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Basin.h"

// Estimation of soil temperature from air temperature and LAI
// Amato and Gimenez, (2024). Predicting monthly near-surface soil temperature from air temperature and the leaf area index. Agricultural and Forest Meteorology. https://doi.org/10.1016/j.agrformet.2023.109838
double Basin::Get_soil_temperature(const double Ta, const double LAI){
    double Ts;
    if (Ta <= 0){
        Ts = 0.291 * Ta;
    } else {
        Ts = Ta * (0.885 + 0.326 * exp(-0.55 * LAI));
    }

    return Ts;
}
      

