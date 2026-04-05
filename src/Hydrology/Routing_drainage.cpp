/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Routing_drainage.cpp
  * Created  on: 22.12.2025
  * Modified on: 22.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Routing_drainage(){

    double to_channel;  // The closest channel index of the current cell; -1 if there is no stream network within the catchment or at outlet cell

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        to_channel = _sortedGrid.to_channel[j];
        // Drainage is directly routed to the channel (similar to overland flow routing yet without reinfiltration and repercolation)
        if (_drainage_from_soil->val[j] > roundoffERR and to_channel != -1) {
            _chanS->val[_sortedGrid.to_channel[j]] += _drainage_from_soil->val[j];
        }

    }
    return EXIT_SUCCESS;
}