/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_soil_profile_carbon.cpp
  * Created  on: 22.11.2025
  * Modified on: 23.11.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_soil_transport(Param &par, svector &sv_conc_pond, svector &sv_conc_layer1, svector &sv_conc_layer2, svector &sv_conc_layer3, svector &sv_conc_chanS,
                                bool enrich_flag, double drainage_flag){

    /* 
    ### Soil layer 1:
    (_thate1_old)
    + infiltration          (need to mix)
    - drainage_from_layer1
    - percolation1
    - Esoil
    - Transp1           
    (_thate1)
    + reinfiltration
    - repercolation1    


    ### Soil layer 2:
    (_thata2_old)
    + percolation1          (need to mix)
    - drainage_from_layer2
    - percolation2
    - Transp2           
    (_theta2)
    + repercolation1
    - repercolation2    

    ### Soil layer 3:
    (_theta3_old)           
    + percolation2          (need to mix)
    - drainage_from_layer3
    - percolation3
    - Transp3
    (_theta3)          
    + repercolation2
    - repercolation3
    + interflow_in      
    - interflow_out
    - interflow_toChn

    ### Channel
    (_chanS_old)
    + drainage_from_layer1
    + drainage_from_layer2
    + drainage_from_layer3
    */


    
    double conc_pond, conc_layer1, conc_layer2, conc_layer3;
    double ST1, ST2, ST3;
    double pond_old, conc_pond_old, conc_layer1_old, pond_to_mix;

    if (drainage_flag == 1) {
      _tmp->equals(*_chanS_old);  // Initialize temporary channel storage
    }
  
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        conc_pond = sv_conc_pond.val[j];
        conc_layer1 = sv_conc_layer1.val[j];
        conc_layer2 = sv_conc_layer2.val[j];
        conc_layer3 = sv_conc_layer3.val[j];
        ST1 = _theta1_old->val[j] * _depth1->val[j];
        ST2 = _theta2_old->val[j] * _depth2->val[j];
        ST3 = _theta3_old->val[j] * par._depth3->val[j];

        /* Mixing */
        // Mix ponding water with top layer storage
        pond_old = _pond->val[j] + _infilt->val[j];
        if (pond_old > roundoffERR and ST1 > roundoffERR){
            conc_pond_old = conc_pond;
            conc_layer1_old = sv_conc_layer1.val[j];
            pond_to_mix = min(pond_old * par._nearsurface_mixing->val[j], ST1);
            conc_pond = (conc_pond_old * (pond_old - pond_to_mix) + conc_layer1_old * pond_to_mix) / pond_old;
            conc_layer1 = (conc_pond_old * pond_to_mix + conc_layer1_old * (ST1 - pond_to_mix)) / ST1;
        }

        
        // Mixing layer 1
        Mixing_full(ST1, conc_layer1, _infilt->val[j], conc_pond);
        if (drainage_flag == 1) {
          ST1 += (_infilt->val[j] - _Perc1->val[j] - _drainage_from_layer1->val[j]);
        } else {
          ST1 += (_infilt->val[j] - _Perc1->val[j]);
        }
        
        // Mixing layer 2
        Mixing_full(ST2, conc_layer2, _Perc1->val[j], conc_layer1);
        if (drainage_flag == 1) {
          ST2 += (_Perc1->val[j] - _Perc2->val[j] - _drainage_from_layer2->val[j]);
        } else {
          ST2 += (_Perc1->val[j] - _Perc2->val[j]);
        }

        // Mixing layer 3
        Mixing_full(ST3, conc_layer3, _Perc2->val[j], conc_layer2);
        if (drainage_flag == 1) {
          ST3 += (_Perc2->val[j] - _Perc3->val[j] - _drainage_from_layer3->val[j]);
        } else {
          ST3 += (_Perc2->val[j] - _Perc3->val[j]);
        }
        

        // Mixing drainage with channel storage if activated
        double mass_drainage;
        int to_channel;
        if (drainage_flag == 1) {
          if (_drainage_from_soil->val[j] > roundoffERR) {
            to_channel = _sortedGrid.to_channel[j];
            mass_drainage = _drainage_from_layer1->val[j] * conc_layer1 + _drainage_from_layer2->val[j] * conc_layer2 + _drainage_from_layer3->val[j] * conc_layer3;
            sv_conc_chanS.val[to_channel] = (sv_conc_chanS.val[to_channel] * _tmp->val[to_channel] + mass_drainage) / (_tmp->val[to_channel] + _drainage_from_soil->val[j]);
            _tmp->val[to_channel] += _drainage_from_soil->val[j];
          }  // End of if (_drainage_from_soil->val[j] > roundoffERR)
        }  // End of if (drainage_flag == 1)
 
        if (enrich_flag){
          // Evapotranspiration happens after percolation
          // Layer 1: erichment due to evaporation and transpiration
          conc_layer1 = (ST1 - _Es->val[j] - _Tr1->val[j])>roundoffERR ? ST1 * conc_layer1 / (ST1 - _Es->val[j] - _Tr1->val[j]) : 0;
          //ST1 -= (_Es.val[j] + _Tr1.val[j]);

          // Layer 2: erichment due to transpiration
          conc_layer2 = (ST2 - _Tr2->val[j])>roundoffERR ? ST2 * conc_layer2 / (ST2 - _Tr2->val[j]) : 0;
          //ST2 -= (_Tr2.val[j]);

          // Layer 3: erichment due to transpiration
          conc_layer3 = (ST3 - _Tr3->val[j])>roundoffERR ? ST3 * conc_layer3 / (ST3 - _Tr3->val[j]) : 0;
          //ST3 -= (_Tr3.val[j]);
        }

       
        
        // Save outputs
        sv_conc_pond.val[j] = conc_pond;
        sv_conc_layer1.val[j] = conc_layer1;
        sv_conc_layer2.val[j] = conc_layer2;
        sv_conc_layer3.val[j] = conc_layer3;
    }

    return EXIT_SUCCESS;
}


