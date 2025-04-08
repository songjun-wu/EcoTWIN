#include "Basin.h"

int Basin::Routing_GWflow_1(Control &ctrl, Param &par){

    int from_j;

    double GWflow_to_go; // Available water for GWflow
    double GWflow;  // Total output of GWflow
    double GWflow_toChn;  // Output of GWflow to stream

    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double dtdx = ctrl.Simul_tstep / dx;
    double alpha;
    double Ks3;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {


        double tmppp = _GW->val[j];  // todo

        double chnlength = _chnlength->val[j];


        double GWflow_in = _GWf_in->val[j];
        double GWflow_out = 0;
        double GWflow_toTrestrial = 0;
        double GWflow_toChn = 0;
    
        from_j = _sortedGrid.to_cell[j];

        // Available GWflowflow = GWflowflow from upstream + GW storage
        // Should GWflow_in be included here, or after stream recharge?
        GWflow_to_go = GWflow_in + _GW->val[j];

               
        if (GWflow_to_go > 0)  {
            
            Ks3 = _Ks3->val[j];  // [m/s]
            // GWflow to channel
            if (chnlength > 0){  // If there is channel in this grid cell
                GWflow_toChn = GWflow_to_go * Ks3 * (1 - exp(-1 * par._GWfExp->val[j] * GWflow_to_go)) * par._wGWf->val[j];  // [m2/s]
                GWflow_toChn *= dtdx; // Store GWflow to channel in [m]
                GWflow_toChn *= (chnlength/dx); // Adjusted with channel length; [m]
                GWflow_toChn = min(GWflow_toChn, GWflow_to_go);  // Cannot exceed water to go
                GWflow_to_go -=  GWflow_toChn;    // [m]
                GWflow_out += GWflow_toChn;  // [m2/s]
            }

            // GWflow to downstream grid
            // Linear approximation of Kinematic wave approach
            // Assumption: Q = head * alpha
            alpha = Ks3 * sin(atan(_slope->val[j])) * par._wGWf->val[j];  // [m/s]
            GWflow_toTrestrial = GWflow_to_go / (1 + alpha * dtdx) * alpha; // qx+1 = hx+1[m] * alpha; [m2/s]
            GWflow_toTrestrial *= dtdx; // Store qx+1 in m
            GWflow_toTrestrial = min(GWflow_toTrestrial, GWflow_to_go);  // Cannot exceed water to go
            GWflow_to_go -= GWflow_toTrestrial; // [m]
            GWflow_out += GWflow_toTrestrial;  // [m]

            // Remaining water = GW storage
            _GW->val[j] = GWflow_to_go;

            _GWf_toChn->val[j] = GWflow_toChn;  // GWflow to channel; [m]
            _GWf_out->val[j] = GWflow_out;  // GWflow sum (to channel and to downstream territrial cell); [m]

            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _GWf_in->val[from_j] += (GWflow_out - GWflow_toChn);
            }

        }               
    }
    return EXIT_SUCCESS;
}