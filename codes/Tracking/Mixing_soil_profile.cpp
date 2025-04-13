#include "Basin.h"

int Basin::Mixing_soil_profile(Control &ctrl, Atmosphere &atm, Param &par){

    if (ctrl.opt_tracking_isotope==1) {

        // Mixing layer 1
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _d18o_layer1->val[j], _infilt->val[j], _d18o_pond->val[j]);
        }

        _tmp->equals(*_theta1);
        _tmp->multiply(*_depth1);
        // Fractionation due to soil evaporation (only for layer 1)
        Fractionation(atm, *_Es, *_tmp, *_d18o_layer1, *_d18o_layer1, *_tmp, 1);  // issoil = 1
        
        // Mixing layer 2
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta2_old->val[j] * _depth2->val[j], _d18o_layer2->val[j], _Perc1->val[j], _d18o_layer1->val[j]);
        }


        // Mixing layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _d18o_layer3->val[j], _Perc2->val[j], _d18o_layer2->val[j]);
        }

    }
    return EXIT_SUCCESS;
}
