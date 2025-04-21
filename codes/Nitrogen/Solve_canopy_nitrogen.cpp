#include "Basin.h"

int Basin::Solve_canopy_nitrogen(Control &ctrl, Atmosphere &atm){

    /*
    ### Canopy
    (_I_old)                        
    + precip
    - Throughfall
    - Canopy evaporation
    (_I)                        
    */
    

    // Mixing canopy storage with precipitation input
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        // The Nitrate concentration in rainfall is defined as a constant value of 2.0
        Mixing_full(_I_old->val[j], _no3_I->val[j], atm._P->val[j], 2.0);
        _no3_pond->val[j] = _no3_I->val[j]; // Align the composition in ponding water with that in throughfall

        // Enrichment due to canopy evaporation (disabled)
        //if (_I->val[j] > roundoffERR and _Ei->val[j] > roundoffERR){
        //    _no3_I->val[j] = _no3_I->val[j] * (_I->val[j] + _Ei->val[j]) / _I->val[j];
        //}
    }

    return EXIT_SUCCESS;
}
