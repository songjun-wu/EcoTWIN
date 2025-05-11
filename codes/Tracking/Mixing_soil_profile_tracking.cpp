#include "Basin.h"

int Basin::Mixing_soil_profile_tracking(Control &ctrl, Atmosphere &atm, Param &par){

    /* 
    ### Soil layer 1:
    (_thate1_old)
    + infiltration          (need to mix)
    - percolation1
    - Esoil
    - Transp1           
    (_thate1)
    + reinfiltration
    - repercolation1    

    ### Soil layer 2:
    (_thata2_old)
    + percolation1          (need to mix)
    - percolation2
    - Transp2           
    (_theta2)
    + repercolation1
    - repercolation2    

    ### Soil layer 3:
    (_theta3_old)           
    + percolation2          (need to mix)
    - percolation3
    - Transp3
    (_theta3)          
    + repercolation2
    - repercolation3
    + interflow_in      
    - interflow_out
    - interflow_toChn   
    */

    double pond_old, ST1, nearsurface_mixing, pond_to_mix, d18o_pond_old, d18o_layer1_old, age_pond_old, age_layer1_old;

    // Isotope tracking
    if (ctrl.opt_tracking_isotope==1) {
        
        // Mixing layer 1
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mix ponding water with top layer storage
            pond_old = _pond->val[j] + _infilt->val[j];
            ST1 = _theta1_old->val[j] * _depth1->val[j];
            if (pond_old > roundoffERR and ST1 > roundoffERR){
                d18o_pond_old = _d18o_pond->val[j];
                d18o_layer1_old = _d18o_layer1->val[j];
                nearsurface_mixing =  par._nearsurface_mixing->val[j];
                pond_to_mix = min(pond_old * nearsurface_mixing, ST1);
                _d18o_pond->val[j] = (d18o_pond_old * (pond_old - pond_to_mix) + d18o_layer1_old * pond_to_mix) / pond_old;
                _d18o_layer1->val[j] = (d18o_pond_old * pond_to_mix + d18o_layer1_old * (ST1 - pond_to_mix)) / ST1;
            }

            // Mix infiltration with top layer storage
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _d18o_layer1->val[j], _infilt->val[j], _d18o_pond->val[j]);
            
        }
        
        // Mixing layer 2
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta2_old->val[j] * _depth2->val[j], _d18o_layer2->val[j], _Perc1->val[j], _d18o_layer1->val[j]);
        }


        // Mixing layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _d18o_layer3->val[j], _Perc2->val[j], _d18o_layer2->val[j]);
        }

        // Fractionation due to soil evaporation (only for layer 1 but happens after percolation)
        _tmp->equals(*_theta1_old);
        _tmp->multiply(*_depth1);
        _tmp->plus(*_infilt);
        _tmp->minus(*_Perc1);
        Fractionation(atm, par, *_Es, *_tmp, *_d18o_layer1, *_d18o_layer1, *_tmp, 1);  // issoil = 1; todo

    }




    // Age tracking
    if (ctrl.opt_tracking_age==1) {
        
        // Mixing layer 1
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mix ponding water with top layer storage
            pond_old = _pond->val[j] + _infilt->val[j];
            ST1 = _theta1_old->val[j] * _depth1->val[j];
            if (pond_old > roundoffERR and ST1 > roundoffERR){
                age_pond_old = _age_pond->val[j];
                age_layer1_old = _age_layer1->val[j];
                nearsurface_mixing =  par._nearsurface_mixing->val[j];
                pond_to_mix = min(pond_old * nearsurface_mixing, ST1);
                _age_pond->val[j] = (age_pond_old * (pond_old - pond_to_mix) + age_layer1_old * pond_to_mix) / pond_old;
                _age_layer1->val[j] = (age_pond_old * pond_to_mix + age_layer1_old * (ST1 - pond_to_mix)) / ST1;
            }

            // Mix infiltration with top layer storage
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _age_layer1->val[j], _infilt->val[j], _age_pond->val[j]);
        }
        
        // Mixing layer 2
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta2_old->val[j] * _depth2->val[j], _age_layer2->val[j], _Perc1->val[j], _age_layer1->val[j]);
        }


        // Mixing layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_theta3_old->val[j] * par._depth3->val[j], _age_layer3->val[j], _Perc2->val[j], _age_layer2->val[j]);
        }

    }



    return EXIT_SUCCESS;
}
