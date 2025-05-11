#include "Basin.h"

int Basin::Advance_age(){


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        _age_I->val[j] += 1;
        _age_snow->val[j] += 1;
        _age_pond->val[j] += 1;
        _age_layer1->val[j] += 1;
        _age_layer2->val[j] += 1;
        _age_layer3->val[j] += 1;
        //_age_GW->val[j] += 1;
        _age_chanS->val[j] += 1;
        
    }


    return EXIT_SUCCESS;
}
