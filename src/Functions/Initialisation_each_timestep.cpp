/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_root_fraction.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Initialisation_each_timestep(Control &ctrl) {

    // Hydrological variables
    // Vars for drainage
    _drainage_from_soil->reset();
    _drainage_from_layer1->reset();
    _drainage_from_layer2->reset();
    _drainage_from_layer3->reset();
    
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

    
    // Nitrogen variables
    if (ctrl.opt_nitrogen_sim==1) {
        _NPP->reset();
        _canopy_conductance->reset();
        //_plant_uptake->reset();
        _minerl_soil->reset();
        //_n2o_emission->reset();
    }

    return EXIT_SUCCESS;
}