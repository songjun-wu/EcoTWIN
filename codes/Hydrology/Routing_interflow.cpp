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

        double chnwidth = _chnwidth->val[j];
        //double chndepth = _chndepth->val[j];
        double chnlength = _chnlength->val[j];
        double theta3 = _theta3->val[j];
        double depth3 = par._depth3->val[j];
        double thetaS3 = _thetaS3->val[j];

        double interflow_in = _interf_in->val[j];
        double interflow_out = 0;
        double interflow_toTrestrial = 0;
        double interflow_toChn = 0;
        double interflow_balance = 0;
    
        from_j = _sortedGrid.to_cell[j];

        
        // Available interflow = interflow from upstream + excess water above field capacity
        // Should interflow_in be included here, or after stream recharge?
        interflow_to_go = interflow_in + max((theta3 - _thetaFC3->val[j]) * depth3, 0.0); 

        if (interflow_to_go > 0)  {
            
            Ks3 = _Ks3->val[j];  // [m/s]

            if (chnwidth > 0){  // If there is channel in this grid cell

                interflow_toChn = interflow_to_go * Ks3 * (1 - exp(-1 * par._interfExp->val[j] * interflow_to_go)) * par._winterf->val[j];  // [m2/s]
                interflow_toChn *= chnlength / dx * dtdx; // from [m2/s] to [m]
                interflow_to_go -=  interflow_toChn;    // [m]
                interflow_out += interflow_toChn;  // [m]
            }  

            alpha = Ks3 * sin(atan(_slope->val[j])) * par._winterf->val[j];  // [m/s]
            interflow_toTrestrial = interflow_to_go * (alpha * dtdx) / (1 + alpha * dtdx); // [m]
            interflow_out += interflow_toTrestrial;

            
            theta3 += (interflow_in - interflow_out)/ depth3;
            if (theta3 > thetaS3){
                theta3 = thetaS3;
                interflow_out += (theta3 - thetaS3); // Excess interflow all routed to the layer 3 of downstream cell?  Or percolate to GW?
            }
            _theta3->val[j] = theta3;
            _interf_toChn->val[j] = interflow_toChn;  // Interflow to channel
            _interf_out->val[j] = interflow_out;  // Interflow sum (to channel and to downstream territrial cell)

            if (_sortedGrid.lat_ok[j] == 1){   // If there is a downstream cell
                _interf_in->val[from_j] += interflow_out - interflow_toChn;
            } 
        }
                
               
    }
    return EXIT_SUCCESS;
}