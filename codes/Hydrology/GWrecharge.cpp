#include "Basin.h"



int Basin::GWrecharge_1(Control &ctrl, Param &par) {

    double perc3;
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double depth3 = par._depth3->val[j];
        double theta3 = _theta3->val[j];

        if (theta3 > _thetaFC3->val[j]){
            perc3 = (theta3 - _thetaFC3->val[j]) * depth3 * _p_perc3->val[j] * par._wRecharge->val[j];
            theta3 -= perc3 / depth3;
            _GW->val[j] += perc3;
        }

        _theta3->val[j] = theta3;
        _Perc3->val[j] = perc3;     
    }
    return EXIT_SUCCESS;
}


int Basin::ReGWrecharge_1(Control &ctrl, Param &par, int j, double &db_theta3, double &db_GW, double &db_rPerc3) {

    double perc3;
    double depth3 = par._depth3->val[j];
    double theta3 = db_theta3;

    if (theta3 > _thetaFC3->val[j]){
        perc3 = (theta3 - _thetaFC3->val[j]) * depth3 * _p_perc3->val[j] * par._wRecharge->val[j];
        theta3 -= perc3 / depth3;
        db_GW += perc3;
    }

    db_theta3 = theta3;
    db_rPerc3 = perc3;     

    return EXIT_SUCCESS;
}