#include "Basin.h"



int Basin::Percolation_1(Control &ctrl, Param &par) {

    double dt = ctrl.Simul_tstep;
    double travel_time_ratio;

    double p_perc1, p_perc2, p_perc3;
    
    if (par.param_category->sort_perc_travel_time_OK == 0){

        par.param_category->sort_perc_travel_time_OK = 1;

        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            travel_time_ratio = dt / ((_thetaS1->val[j] - _thetaFC1->val[j]) / _Ks1->val[j]);  // The time for excess water to percolate versus hydraulic conductvity
            _p_perc1->val[j] = (1 - exp(-1 * travel_time_ratio));

            travel_time_ratio = dt / ((_thetaS2->val[j] - _thetaFC2->val[j]) / _Ks2->val[j]);
            _p_perc2->val[j] = (1 - exp(-1 * travel_time_ratio));

            travel_time_ratio = dt / ((_thetaS3->val[j] - _thetaFC3->val[j]) / _Ks3->val[j]);
            _p_perc3->val[j] = (1 - exp(-1 * travel_time_ratio));
        }
        
    }

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double theta1 = _theta1->val[j];
        double theta2 = _theta2->val[j];
        double theta3 = _theta2->val[j];

        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j];

        double perc1 = 0;
        double perc2 = 0;
        double perc3 = 0;

        // Percolation from layer 1
        perc1 = max((theta1 - _thetaFC1->val[j]) * _p_perc1->val[j], 0.0) * depth1;
        theta1 -= perc1 / depth1;
        theta2 += perc1 / depth2;

        // Percolation from layer 2
        perc2 = max((theta2 - _thetaFC2->val[j]) * _p_perc2->val[j], 0.0) * depth2;
        theta2 -= perc2 / depth2;
        theta3 += perc2 / depth3;

        // Percolation from layer 3 (GW recharge)
        perc3 = max((theta3 - _thetaFC3->val[j]) * _p_perc3->val[j], 0.0) * depth3;
        theta3 -= perc3 / depth3;        
        // Percolate to GW storage 


        _theta1->val[j] = theta1;
        _theta2->val[j] = theta2;
        _theta3->val[j] = theta3;
        _Perc1->val[j] = perc1;
        _Perc2->val[j] = perc2;
        _Perc3->val[j] = perc3;
        _GW->val[j] += perc3;
 
        if (j==100){
            //cout << ctrl.current_ts / 86400 << " " << perc1 << " "<<perc2 <<"  "<< theta1 << " " << theta2 << endl;
            //cout << _p_perc1->val[j] << " "<< _thetaFC1->val[j] << endl << endl;
        }
        
    }
    return EXIT_SUCCESS;
}