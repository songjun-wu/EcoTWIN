#include "Basin.h"

int Basin::Routing_interflow_1(Control &ctrl, Param &par){

    int from_j;

    double interflow_to_go; // Available water for interflow
    double interflow_out;  // Total output of interflow
    double interflow_toChn;  // Output of interflow to stream

    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double dtdx = ctrl.Simul_tstep / dx;
    double alpha;
    double Ks3;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double chnlength = _chnlength->val[j];
        double theta3 = _theta3->val[j];
        double depth3 = par._depth3->val[j];
        double thetaS3 = _thetaS3->val[j];

        double interflow_in = _interf_in->val[j];
        double interflow_out = 0;
        double interflow_toTrestrial = 0;
        double interflow_toChn = 0;
        double excess_ST3 = 0;
    
        from_j = _sortedGrid.to_cell[j];

        // Available interflow = interflow from upstream + excess water above field capacity
        // Should interflow_in be included here, or after stream recharge?
        interflow_to_go = interflow_in + (theta3 > _thetaFC3->val[j] ? (theta3 - _thetaFC3->val[j]) * depth3 : 0.0);
        theta3 = theta3 > _thetaFC3->val[j] ? _thetaFC3->val[j] : theta3;
               
        if (interflow_to_go > 0)  {
            
            Ks3 = _Ks3->val[j];  // [m/s]

            // Interflow to channel
            if (chnlength > 0){  // If there is channel in this grid cell
                interflow_toChn = interflow_to_go * Ks3 * (1 - exp(-1 * par._interfExp->val[j] * interflow_to_go)) * par._winterf->val[j];  // [m2/s]
                interflow_toChn *= dtdx; // Store interflow to channel in [m]
                interflow_toChn *= (chnlength/dx); // Adjusted with channel length; [m]
                interflow_toChn = min(interflow_toChn, interflow_to_go);  // Cannot exceed water to go
                interflow_to_go -=  interflow_toChn;    // [m]
                interflow_out += interflow_toChn;  // [m2/s]
            }

            // Interflow to downstream grid
            // Linear approximation of Kinematic wave approach
            // Assumption: Q = head * alpha
            alpha = Ks3 * sin(atan(_slope->val[j])) * par._winterf->val[j];  // [m/s]
            interflow_toTrestrial = interflow_to_go / (1 + alpha * dtdx) * alpha; // qx+1 = hx+1[m] * alpha; [m2/s]
            interflow_toTrestrial *= dtdx; // Store qx+1 in m
            interflow_toTrestrial = min(interflow_toTrestrial, interflow_to_go);  // Cannot exceed water to go
            interflow_to_go -= interflow_toTrestrial; // [m]
            interflow_out += interflow_toTrestrial;  // [m]

            // Remaining water goes into layer 3
            theta3 += interflow_to_go / depth3;
            interflow_to_go = 0;
            
            // Excess interflow all routed to the layer 3 of downstream cell (current solution)?  Or percolate to GW?
            if (theta3 > thetaS3){
                excess_ST3 = (theta3 - thetaS3) * depth3;
                interflow_toTrestrial += excess_ST3;
                interflow_out += excess_ST3;
                theta3 = thetaS3;
            }
          
            _theta3->val[j] = theta3;
            _interf_toChn->val[j] = interflow_toChn;  // Interflow to channel; [m]
            _interf_out->val[j] = interflow_out;  // Interflow sum (to channel and to downstream territrial cell); [m]

            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _interf_in->val[from_j] += (interflow_out - interflow_toChn);
            }
        }               
    }
    return EXIT_SUCCESS;
}