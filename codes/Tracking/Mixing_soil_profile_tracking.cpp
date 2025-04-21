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

    if (ctrl.opt_tracking_isotope==1) {
        
        // Mixing layer 1
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

            // Mix ponding water with top layer storage
            double pond_old = _pond->val[j] + _infilt->val[j];
            double ST1 = _theta1_old->val[j] * _depth1->val[j];
            if (pond_old > roundoffERR and ST1 > roundoffERR){
                double d18o_pond_old = _d18o_pond->val[j];
                double d18o_layer1_old = _d18o_layer1->val[j];
                double nearsurface_mixing =  par._nearsurface_mixing->val[j];
                double pond_to_mix = pond_old * nearsurface_mixing;
                _d18o_pond->val[j] = d18o_pond_old * (1 - nearsurface_mixing) + d18o_layer1_old * nearsurface_mixing;
                _d18o_layer1->val[j] = (d18o_pond_old * pond_to_mix + d18o_layer1_old * (ST1 - pond_to_mix)) / ST1;
            }

            // Mix infiltration with top layer storage
            Mixing_full(_theta1_old->val[j] * _depth1->val[j], _d18o_layer1->val[j], _infilt->val[j], _d18o_pond->val[j]);
            
        }
        
        _tmp->equals(*_theta1_old);
        _tmp->multiply(*_depth1);
        _tmp->plus(*_infilt);
        _tmp->minus(*_Perc1);

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
