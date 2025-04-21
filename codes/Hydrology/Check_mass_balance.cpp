#include "Basin.h"

int Basin::Check_mass_balance(Control &ctrl, Param &par, Atmosphere &atm) {

    for (unsigned int ccc = 0; ccc < _sortedGrid.row.size(); ccc++){
        // Water balance
        //cout << ctrl.current_ts/ctrl.Simul_tstep << endl;
        double canopy_balance = (_I->val[ccc] - _I_old->val[ccc]) - (atm._P->val[ccc] - _Th->val[ccc] - _Ei->val[ccc]);
        if (abs(canopy_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " canopy" << ccc << " " << endl;

        double ponding_balance = (_Th->val[ccc] + _snowmelt->val[ccc] - _snowacc->val[ccc] - _infilt->val[ccc] - _rinfilt->val[ccc] + _ovf_in->val[ccc] - _ovf_out->val[ccc] - _ovf_toChn->val[ccc]);
        if (abs(ponding_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " ponding  " << ccc << " " << ponding_balance << endl;

        double layer1_balance = (_theta1->val[ccc] - _theta1_old->val[ccc])*_depth1->val[ccc] - ( _infilt->val[ccc] + _rinfilt->val[ccc] - _Perc1->val[ccc] - _rPerc1->val[ccc] - _Es->val[ccc] - _Tr1->val[ccc]);
        if (abs(layer1_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " layer1  " << ccc << " " << layer1_balance << endl;

        double layer2_balance = (_theta2->val[ccc] - _theta2_old->val[ccc])*_depth2->val[ccc] - ( _Perc1->val[ccc] + _rPerc1->val[ccc] - _Perc2->val[ccc] - _rPerc2->val[ccc] - _Tr2->val[ccc]);
        if (abs(layer2_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " layer2  " << ccc << " " << layer2_balance << endl;

        double layer3_balance = (_theta3->val[ccc] - _theta3_old->val[ccc])*par._depth3->val[ccc]  - ( _Perc2->val[ccc] + _rPerc2->val[ccc] - _Perc3->val[ccc] - _rPerc3->val[ccc] - _Tr3->val[ccc] + _interf_in->val[ccc] - _interf_out->val[ccc] - _interf_toChn->val[ccc]);
        if (abs(layer3_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " layer3  " << ccc << " " << layer3_balance << endl;

        double GW_balance = (_GW->val[ccc] - _GW_old->val[ccc]) - (_Perc3->val[ccc] + _rPerc3->val[ccc] + _GWf_in->val[ccc] - _GWf_out->val[ccc] - _GWf_toChn->val[ccc]);
        if (abs(GW_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " GW  " << ccc << " " << GW_balance << endl;

        double m3s_to_m = ctrl.Simul_tstep/(ctrl._dx*ctrl._dx);
        double chanS_balance = (_chanS->val[ccc] - _chanS_old->val[ccc]) - (_Qupstream->val[ccc]*m3s_to_m + _ovf_toChn->val[ccc] + _interf_toChn->val[ccc] +_GWf_toChn->val[ccc] - _Q->val[ccc]*m3s_to_m);
        if (abs(chanS_balance) > 1e-10) cout << ctrl.current_ts/ctrl.Simul_tstep << " channel  " << ccc << " " << chanS_balance << endl;

        if (ctrl.current_ts/ctrl.Simul_tstep >= 0 and ctrl.current_ts/ctrl.Simul_tstep < 1 and ccc==271) { // todo
            //cout << ctrl.current_ts/ctrl.Simul_tstep << " "  << ponding_balance << " "<< atm._P->val[ccc] << endl;
            //cout << _Perc3->val[ccc] <<" "<< _rPerc3->val[ccc] <<" "<< _GWf_in->val[ccc]<<" "<< _GWf_out->val[ccc] <<" "<< _GWf_toChn->val[ccc] <<" "<< _ovf_in->val[ccc] <<" "<< _ovf_out->val[ccc] <<" "<< _ovf_toChn->val[ccc] << endl;
        }

        // Isotopic balance




    }

return EXIT_SUCCESS;
}