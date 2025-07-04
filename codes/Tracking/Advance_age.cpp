/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Advance_age.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Advance_age(){


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        _age_I->val[j] += 1;
        _age_snow->val[j] += 1;
        _age_pond->val[j] += 1;
        _age_layer1->val[j] += 1;
        _age_layer2->val[j] += 1;
        _age_layer3->val[j] += 1;
        _age_vadose->val[j] += 1;
        //_age_GW->val[j] += 1;
        _age_chanS->val[j] += 1;
        
    }

    return EXIT_SUCCESS;
}


int Basin::Advance_trans_age(){


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        _trans_age_I->val[j] += 1;
        _trans_age_snow->val[j] += 1;
        _trans_age_pond->val[j] += 1;
        _trans_age_layer1->val[j] += 1;
        _trans_age_layer2->val[j] += 1;
        _trans_age_layer3->val[j] += 1;
        _trans_age_vadose->val[j] += 1;
        //_trans_age_GW->val[j] += 1;
        _trans_age_chanS->val[j] += 1;
        
    }

    return EXIT_SUCCESS;
}
