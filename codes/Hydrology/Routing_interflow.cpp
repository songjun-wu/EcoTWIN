#include "Basin.h"

int Basin::Routing_interflow_1(Control &ctrl, Param &par){

    int from_j;
    double interflow_to_go = 0;
    double interflow_out = 0;
    double interflow_toChn = 0;
    double interflow_toTrestrial;
    double excess_ST3 = 0;

    double dx = ctrl._dx;
    double dx_square = dx * dx;
    double dtdx = ctrl.Simul_tstep / dx;
    double alpha = 0;
    double Ks3 = 0;
    double theta3, thetaS3, depth3;
    double interflow_in, rrPerc3;
    double chnlength;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        chnlength = _chnlength->val[j];
        theta3 = _theta3->val[j];
        depth3 = par._depth3->val[j];
        thetaS3 = _thetaS3->val[j];
        interflow_in = _interf_in->val[j];
        interflow_to_go = 0; // Available water for interflow
        interflow_toTrestrial = 0;   // Output of interflow to downstream cell
        interflow_toChn = 0;   // Output of interflow to stream
        rrPerc3 = 0;
        excess_ST3 = 0;
    
        from_j = _sortedGrid.to_cell[j];
       
        // Available interflow = interflow from upstream + excess water above field capacity
        // Should interflow_in be included here, or after stream recharge?
        
        interflow_to_go = interflow_in + (theta3 > _thetaFC3->val[j] ? (theta3 - _thetaFC3->val[j]) * depth3 : 0.0);
        theta3 = theta3 > _thetaFC3->val[j] ? _thetaFC3->val[j] : theta3;
               
        if (interflow_to_go > roundoffERR)  {
            
            Ks3 = _Ks3->val[j];  // [m/s]

            // Interflow to channel
            if (chnlength > 0){  // If there is channel in this grid cell
                interflow_toChn = interflow_to_go * Ks3 * (1 - exp(-1 * par._interfExp->val[j] * interflow_to_go)) * par._winterf->val[j];  // [m2/s]
                interflow_toChn *= dtdx; // Store interflow to channel in [m]
                interflow_toChn *= (chnlength/dx); // Adjusted with channel length; [m]
                interflow_toChn = min(interflow_toChn, interflow_to_go);  // Cannot exceed water to go
                interflow_to_go -=  interflow_toChn;    // [m]
            }

            // Interflow to downstream grid
            // Linear approximation of Kinematic wave approach
            // Assumption: Q = head * alpha
            alpha = Ks3 * sin(atan(_slope->val[j])) * par._winterf->val[j];  // [m/s]
            interflow_toTrestrial = interflow_to_go / (1 + alpha * dtdx) * alpha; // qx+1 = hx+1[m] * alpha; [m2/s]
            interflow_toTrestrial *= dtdx; // Store qx+1 in m
            interflow_toTrestrial = min(interflow_toTrestrial, interflow_to_go);  // Cannot exceed water to go [m]
            interflow_to_go -= interflow_toTrestrial; // [m]

            // Remaining water goes into layer 3
            theta3 += interflow_to_go / depth3;
            interflow_to_go = 0;
            
            // Excess interflow all routed to the layer 3 of downstream cell (current solution)?  Or percolate to GW?
            if (theta3 > thetaS3){
                excess_ST3 = (theta3 - thetaS3) * depth3;
                theta3 = thetaS3;
                interflow_toTrestrial += excess_ST3 * par._ratio_to_interf->val[j];  // Some excess water becomes interflow to downstream cell
                _GW->val[j] += excess_ST3 * (1 - par._ratio_to_interf->val[j]);  // The remaining goes into GW storage
                rrPerc3 = excess_ST3 * (1 - par._ratio_to_interf->val[j]);  // Update re-percolation3
            }
        
            
            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _interf_in->val[from_j] += interflow_toTrestrial;
            }
        }
        
        _theta3->val[j] = theta3;
        _interf_toChn->val[j] = interflow_toChn;  // Interflow to channel; [m]
        _interf_out->val[j] = interflow_toTrestrial;  // Interflow to downstream territrial cell [m]
        _rrPerc3->val[j] = rrPerc3;  // Re-percolation to GW due to excess soil storage in layer 3
    }
    return EXIT_SUCCESS;
}