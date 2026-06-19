/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_routing.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_routing(Control &ctrl, Param &par){


    if (ctrl.opt_drainage==1) {
        Routing_drainage();
    }

    if (ctrl.opt_routOvf==1) {
        Routing_ovf_1(ctrl, par);
    }

    if (ctrl.opt_routinterf==1) {
        Routing_interflow_1(ctrl, par);
    }

    if (ctrl.opt_routGWf) {
        Routing_GWflow_1(ctrl, par);
    }

    if (ctrl.opt_routQ==1) {
        Routing_Q_1(ctrl, par);
    }


    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_routing_tracking(ctrl, par);  // Mixing for overland flow, for reinfiltration and repercolation, for interflow, and for GW flow
    }

    if (ctrl.opt_carbon_sim==1 or ctrl.opt_nitrogen_sim==1){
        Solve_routing_nutrient(ctrl, par);  // Mixing for overland flow, for reinfiltration and repercolation, for interflow, and for GW flow
    }

    
    return EXIT_SUCCESS;
}