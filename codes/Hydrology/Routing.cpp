#include "Basin.h"

int Basin::Routing(Control &ctrl, Param &par){

    _ovf_in->reset();
    _interf_in->reset();
    _Qupstream->reset();

    if (ctrl.opt_routOvf==1) {
        Routing_ovf_1(ctrl, par);
    }

    if (ctrl.opt_routinterf==1) {
        Routing_interflow_1(ctrl, par);
    }

    if (ctrl.opt_routQ==1) {
        Routing_Q_1(ctrl, par);
    }


    return EXIT_SUCCESS;
}