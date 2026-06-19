/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_root_fraction.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Initialisation_each_timestep(Control &ctrl, Param &par) {

    // ===== Update internal parameters (only needed when parameters are updated) =====
    // Hydraulic proporties
      if (par.param_category->sort_PTF == 0){
        // Estimate saturated hydraulic conductivity, field capacity, and wilting point
        Soil_proporty(ctrl, par);
        par.param_category->sort_PTF = 1;
    }
    // Root fraction
    if (ctrl.opt_evap == 1 or ctrl.opt_evap == 2 or ctrl.opt_nitrogen_sim==1){
        Sort_root_fraction(ctrl, par);
    }
    // Travel time of percolation
    if (ctrl.opt_percolation == 1){
        Sort_percolation_travel_time(ctrl, par);
    }

    // Parameter correction
    if (par.sort_parameter_correction_OK == 0){
      Parameter_correction(ctrl, par);
    }
    
    // ===== Hydrological variables =====
    // Vars for drainage
    if (ctrl.opt_drainage == 1){
      _drainage_from_soil->reset();
      _drainage_from_layer1->reset();
      _drainage_from_layer2->reset();
      _drainage_from_layer3->reset();
    }
    
    // Vars for routing
    _ovf_in->reset();
    _interf_in->reset();
    _GWf_in->reset();
    _Qupstream->reset();
    // Vars for reinfiltration and repercolation (if activated)
    if (ctrl.opt_reinfil==1){
        _rinfilt->reset();
        _rPerc1->reset();
        _rPerc2->reset();
        _rPerc3->reset();
    }

    
    // ===== Carbon and Nitrogen variables =====
    if (ctrl.opt_carbon_sim==1) {
        _NPP->reset();
        _canopy_conductance->reset();
        //_plant_uptake->reset();
        _soil_respiration_C->reset();
        _soil_decomposition_C->reset();
        //_n2o_emission->reset();
    }
    if (ctrl.opt_nitrogen_sim==1) {
      _nitrogen_add->reset();
      _minerl_soil->reset();
    }

    return EXIT_SUCCESS;
}