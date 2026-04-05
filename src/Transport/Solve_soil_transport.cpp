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

int Basin::Solve_soil_transport(Param &par, svector &sv_conc_pond, svector &sv_conc_layer1, svector &sv_conc_layer2, svector &sv_conc_layer3, svector &sv_conc_vadose, svector &sv_conc_chanS,
                                svector &sv_leaching_mass, svector &sv_drainage_mass,
                                bool enrich_flag, double drainage_flag, bool diffuse_flag){

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


    // Variables for mxing between soil layers and vadose zone
    double conc_pond, conc_layer1, conc_layer2, conc_layer3, conc_vadose;
    double ST1, ST2, ST3;
    double pond_old, conc_pond_old, conc_layer1_old, pond_to_mix;
    double input_water, input_mass, input_conc;

    // Variables for Fickian diffusion
    double diffuse_molecular;
    double mass_layer_diffusion;

    // Variables for drainage
    double mass_drainage;
    int to_channel;

    if (drainage_flag == 1) {
      _tmp->equals(*_chanS_old);  // Initialize temporary channel storage
    }
  
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        conc_pond = sv_conc_pond.val[j];
        conc_layer1 = sv_conc_layer1.val[j];
        conc_layer2 = sv_conc_layer2.val[j];
        conc_layer3 = sv_conc_layer3.val[j];
        conc_vadose = sv_conc_vadose.val[j];
        ST1 = _theta1_old->val[j] * _depth1->val[j];
        ST2 = _theta2_old->val[j] * _depth2->val[j];
        ST3 = _theta3_old->val[j] * par._depth3->val[j];

        /* Mixing */
        // Mix ponding water with top layer storage (not used in current version)
        /*
        pond_old = _pond->val[j] + _infilt->val[j];
        if (pond_old > roundoffERR and ST1 > roundoffERR){
            conc_pond_old = conc_pond;
            conc_layer1_old = sv_conc_layer1.val[j];
            pond_to_mix = min(pond_old * par._nearsurface_mixing->val[j], ST1);
            conc_pond = (conc_pond_old * (pond_old - pond_to_mix) + conc_layer1_old * pond_to_mix) / pond_old;
            conc_layer1 = (conc_pond_old * pond_to_mix + conc_layer1_old * (ST1 - pond_to_mix)) / ST1;
        }
        */

        
        // Mixing layer 1-3
        Mixing_full(ST1, conc_layer1, _infilt->val[j], conc_pond);
        Mixing_full(ST2, conc_layer2, _Perc1->val[j], conc_layer1);
        Mixing_full(ST3, conc_layer3, _Perc2->val[j], conc_layer2);
        if (drainage_flag == 1) {
          ST1 += (_infilt->val[j] - _Perc1->val[j] - _drainage_from_layer1->val[j]);
          ST2 += (_Perc1->val[j] - _Perc2->val[j] - _drainage_from_layer2->val[j]);
          ST3 += (_Perc2->val[j] - _Perc3->val[j] - _drainage_from_layer3->val[j]);
        } else {
          ST1 += (_infilt->val[j] - _Perc1->val[j]);
          ST2 += (_Perc1->val[j] - _Perc2->val[j]);
          ST3 += (_Perc2->val[j] - _Perc3->val[j]);
        }

        
        // Mixing vadose storage (percolation from layer 3 and preferential flow from ponding)
        input_water = _preferential_flow->val[j] + _Perc3->val[j];
        input_mass = conc_pond * _preferential_flow->val[j] + conc_layer3 * _Perc3->val[j];
        input_conc = input_mass / input_water;
        sv_leaching_mass.val[j] = input_mass;
        Mixing_full(_vadose_old->val[j], conc_vadose, input_water, input_conc);
        
        

        // Mixing drainage with channel storage if activated
        if (drainage_flag == 1) {
          to_channel = _sortedGrid.to_channel[j];
          // There is no need for mixing if this is the outlet or there is not stream network within the catchment
          // In this context, drainage just routes beyond catchment boundary without further tracking
          if (_drainage_from_soil->val[j] > roundoffERR and to_channel != -1) { 
            mass_drainage = _drainage_from_layer1->val[j] * conc_layer1 + _drainage_from_layer2->val[j] * conc_layer2 + _drainage_from_layer3->val[j] * conc_layer3;
            sv_conc_chanS.val[to_channel] = (sv_conc_chanS.val[to_channel] * _tmp->val[to_channel] + mass_drainage) / (_tmp->val[to_channel] + _drainage_from_soil->val[j]);
            _tmp->val[to_channel] += _drainage_from_soil->val[j];
            sv_drainage_mass.val[j] = mass_drainage;   // Summary statistics of drainage mass
          } else {
            sv_drainage_mass.val[j] = 0;
          } // End of if (_drainage_from_soil->val[j] > roundoffERR)
        }  // End of if (drainage_flag == 1)


        // Mixing capillary flow with layer 3
        Mixing_full(ST3, conc_layer3, _capillary_flow->val[j], conc_vadose);
        ST3 += _capillary_flow->val[j];

        // Solute enrichment due to evapotranspiration
        if (enrich_flag){
          // Evapotranspiration happens after percolation
          // Layer 1: erichment due to evaporation and transpiration
          conc_layer1 = (ST1 - _Es->val[j] - _Tr1->val[j])>roundoffERR ? ST1 * conc_layer1 / (ST1 - _Es->val[j] - _Tr1->val[j]) : 0;
          ST1 -= (_Es->val[j] + _Tr1->val[j]);

          // Layer 2: erichment due to transpiration
          conc_layer2 = (ST2 - _Tr2->val[j])>roundoffERR ? ST2 * conc_layer2 / (ST2 - _Tr2->val[j]) : 0;
          ST2 -= (_Tr2->val[j]);

          // Layer 3: erichment due to transpiration
          conc_layer3 = (ST3 - _Tr3->val[j])>roundoffERR ? ST3 * conc_layer3 / (ST3 - _Tr3->val[j]) : 0;
          ST3 -= (_Tr3->val[j]);
        }


        // Mixing layers due to potential capillary flow exchange
        // Fickian diffusion: diffuse_molecular * concentration gradient (Fick's first law)
        /*
        if (diffuse_flag){
          diffuse_molecular  = par._diffuse_molecular_coefficient->val[j];
          // Layer 1 and 2        
          mass_layer_diffusion = diffuse_molecular * (conc_layer1 - conc_layer2)/(min(_depth1->val[j], _depth2->val[j]));
          conc_layer1 -= mass_layer_diffusion / ST1;
          conc_layer2 += mass_layer_diffusion / ST2;
          // Layer 2 and 3
          mass_layer_diffusion = diffuse_molecular * (conc_layer2 - conc_layer3)/(min(_depth2->val[j], par._depth3->val[j]));
          conc_layer2 -= mass_layer_diffusion /ST2;
          conc_layer3 += mass_layer_diffusion /ST3;
        } 
          */
       
        
        // Update global variables
        sv_conc_pond.val[j] = conc_pond;
        sv_conc_layer1.val[j] = conc_layer1;
        sv_conc_layer2.val[j] = conc_layer2;
        sv_conc_layer3.val[j] = conc_layer3;
        sv_conc_vadose.val[j] = conc_vadose;
    }

    return EXIT_SUCCESS;
}


