/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Carbon_summary.cpp
  * Created  on: 17.12.2025
  * Modified on: 17.12.2025
***************************************************************/


#include "Basin.h"

int Basin::Carbon_summary(Control &ctrl, Param &par){

    // Summary carbon pools
    for (int j = 0; j < _sortedGrid.row.size(); j++){
      _fast_C->val[j] =  _acid_CP1_nonwood->val[j] + _ethanol_CP1_nonwood->val[j] + _soluble_CP1_nonwood->val[j] + _nonsoluble_CP1_nonwood->val[j] +
                          _acid_CP1_wood->val[j] + _ethanol_CP1_wood->val[j] + _soluble_CP1_wood->val[j] + _nonsoluble_CP1_wood->val[j] +
                          _acid_CP2_wood->val[j] + _ethanol_CP2_wood->val[j] + _soluble_CP2_wood->val[j] + _nonsoluble_CP2_wood->val[j] +
                          _acid_CP3_wood->val[j] + _ethanol_CP3_wood->val[j] + _soluble_CP3_wood->val[j] + _nonsoluble_CP3_wood->val[j];
      _humus_C->val[j] = _humus_CP1->val[j] + _humus_CP2->val[j] + _humus_CP3->val[j];

    }

    if (ctrl.opt_summary_statistics==1){
      for (int j = 0; j < _sortedGrid.row.size(); j++){
        _plant_C->val[j] = _plant_green_CP->val[j] + _plant_reserve_CP->val[j] + _plant_wood_CP->val[j];  // Total vegetation carbon [gC/m2]  
        _soluble_C->val[j] = _soluble_CP1_nonwood->val[j] + _soluble_CP1_wood->val[j] + _soluble_CP2_wood->val[j] + _soluble_CP3_wood->val[j] + 
                            _doc_layer1->val[j]*_theta1->val[j]*_depth1->val[j] + _doc_layer2->val[j]*_theta2->val[j]*_depth2->val[j] + _doc_layer3->val[j]*_theta3->val[j]*par._depth3->val[j];
      }
    }

    return EXIT_SUCCESS;
}

