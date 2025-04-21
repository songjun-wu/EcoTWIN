#include "Basin.h"

int Basin::Routing(Control &ctrl, Param &par){

    // Upstream inputs need to be reset to zero
    _ovf_in->reset();
    _interf_in->reset();
    _GWf_in->reset();
    _Qupstream->reset();

    if (ctrl.opt_reinfil==1){
        _rinfilt->reset();
        _rPerc1->reset();
        _rPerc2->reset();
        _rPerc3->reset();
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

    if (ctrl.opt_nitrogen_sim==1){
        Solve_routing_nitrogen(ctrl, par);  // Mixing for overland flow, for reinfiltration and repercolation, for interflow, and for GW flow
    }

    
    return EXIT_SUCCESS;
}