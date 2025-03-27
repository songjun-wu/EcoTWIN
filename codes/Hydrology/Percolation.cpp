#include "Basin.h"



int Basin::Percolation_2(Control &ctrl, Param &par) {

    double dt = ctrl.Simul_tstep;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) { 

        double travel_time_ratio = (_thetaS1->val[j] - _thetaFC1->val[j]) / _Ks1->val[j] * 3600 * 24 / dt;

        double infiltration = max((_theta1->val[j] - _thetaFC1->val[j]) *  par._depth3->val[j] * (1 - exp(-1 * travel_time_ratio)), 0.0);

        if (j==100){
            cout << infiltration << "  "<< _thetaS1->val[j] <<" "<< _thetaFC1->val[j] << " "<< travel_time_ratio << exp(-1 * travel_time_ratio) << endl;
        }
    }
    return EXIT_SUCCESS;
}