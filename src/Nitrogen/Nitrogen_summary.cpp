/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Nitrogen_summary.NPp
  * Created  on: 17.12.2025
  * Modified on: 17.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Nitrogen_summary(Param &par){

    // Summary carbon pools
    double fast_NP1_wood;
    double fast_NP1;
    for (int j = 0; j < _sortedGrid.row.size(); j++){
        fast_NP1_wood = (_acid_CP1_wood->val[j] + _ethanol_CP1_wood->val[j] + _nonsoluble_CP1_wood->val[j]) * par._NC_ratio_fast_pool_wood->val[j];
        fast_NP1 =  _fast_NP1_nonwood->val[j] + fast_NP1_wood;
        _fast_N->val[j] = fast_NP1 + 
                          (_acid_CP1_wood->val[j] + _ethanol_CP1_wood->val[j] + _nonsoluble_CP1_wood->val[j] +
                          _acid_CP2_wood->val[j] + _ethanol_CP2_wood->val[j] + _nonsoluble_CP2_wood->val[j] +
                          _acid_CP3_wood->val[j] + _ethanol_CP3_wood->val[j] + _nonsoluble_CP3_wood->val[j]) * par._NC_ratio_fast_pool_wood->val[j];   // Fast nitrogen [gN/m2]; NC ratio is constant in wood pools in layer 2 and 3
        _humus_N->val[j] = (_humus_CP1->val[j] + _humus_CP2->val[j] + _humus_CP3->val[j]) * par._NC_ratio_humus_pool->val[j];  // Humus nitrogen [gN/m2]; NC ratio is constant in humus pools
      }

    return EXIT_SUCCESS;
}
