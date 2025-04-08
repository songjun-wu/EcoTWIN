#include "Basin.h"



int Basin::Repercolation_1(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3,  double &db_rPerc1, double &db_rPerc2) {


    double theta1 = _theta1->val[j];
    double theta2 = _theta2->val[j];
    double theta3 = _theta3->val[j];

    double depth1 = _depth1->val[j];
    double depth2 = _depth2->val[j];
    double depth3 = par._depth3->val[j];

    double perc1 = 0;
    double perc2 = 0;

    // Percolation from layer 1
    perc1 = max((theta1 - _thetaFC1->val[j]) * _p_perc1->val[j], 0.0) * depth1;
    theta1 -= perc1 / depth1;
    theta2 += perc1 / depth2;

    // Percolation from layer 2
    perc2 = max((theta2 - _thetaFC2->val[j]) * _p_perc2->val[j], 0.0) * depth2;
    theta2 -= perc2 / depth2;
    theta3 += perc2 / depth3;

    db_theta1 = theta1;
    db_theta2 = theta2;
    db_theta3 = theta3;
    db_rPerc1 = perc1;
    db_rPerc2 = perc2;

    return EXIT_SUCCESS;
}

int Basin::Repercolation_2(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3,  double &db_rPerc1, double &db_rPerc2) {

    double dt = ctrl.Simul_tstep;
    double travel_time_ratio;

    double p_perc1, p_perc2;

    double theta1 = _theta1->val[j];
    double theta2 = _theta2->val[j];
    double theta3 = _theta3->val[j];

    double thetaS1 = _thetaS1->val[j];
    double thetaS2 = _thetaS2->val[j];
    double thetaS3 = _thetaS3->val[j];

    double depth1 = _depth1->val[j];
    double depth2 = _depth2->val[j];
    double depth3 = par._depth3->val[j];

    double perc1 = 0;
    double perc2 = 0;
    double perc_in = 0;
    double delta_theta;



    // Percolation from layer 1
    // Only happens when saturation is met, because infiltration has been added to layer 1
    if (theta1 > thetaS1){
        perc1 = (theta1 - thetaS1) * depth1;  // Percolation to layer 2
        theta1 = thetaS1;
    } else{
        exit(EXIT_SUCCESS);
    }
    
    // Percolation from layer 2
    // if saturation is not met then fill the deficit, otherwise all water pass to next layer
    perc_in = perc1;
    if (theta2 < thetaS2){ 
        delta_theta = perc_in * (1 - exp(par._percExp->val[j] * log(theta2/thetaS2))) / depth2;
        if ((theta2 + delta_theta) > thetaS2){
            theta2 = thetaS2;
            perc_in -= (thetaS2 - theta2) * depth2;
        } else{
            theta2 += delta_theta;
            perc_in -= delta_theta * depth2;
        }
    }
    perc2 = perc_in;  // Percolation to next layer

    // Update soil storage in layer 3
    // Percolation for layer 3 (groundwater recharge is calculated independently)
    theta3 += perc_in / depth3;

    // Local to global
    db_theta1 = theta1;
    db_theta2 = theta2;
    db_theta3 = theta3;
    db_rPerc1 = perc1;
    db_rPerc2 = perc2;
  

    return EXIT_SUCCESS;
}


int Basin::Repercolation_3(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3,  double &db_rPerc1, double &db_rPerc2) {


    double theta1 = _theta1->val[j];
    double theta2 = _theta2->val[j];
    double theta3 = _theta3->val[j];

    double thetaS1 = _thetaS1->val[j];
    double thetaS2 = _thetaS2->val[j];
    double thetaS3 = _thetaS3->val[j];

    double depth1 = _depth1->val[j];
    double depth2 = _depth2->val[j];
    double depth3 = par._depth3->val[j];

    double perc1 = 0;
    double perc2 = 0;
    double perc_in = 0;
    double delta_theta;



    // Percolation from layer 1
    // if saturation is not met then fill the deficit, otherwise all water pass to next layer
    if (theta1 > thetaS1){
        perc1 = (theta1 - thetaS1) * depth1;  // Percolation to next layer
        theta1 = thetaS1;
        theta2 += perc1 / depth2;
    }

    if (theta2 > thetaS2){
        perc2 = (theta2 - thetaS2) * depth2;  // Percolation to next layer
        theta2 = thetaS2;
        theta3 += perc2 / depth3;
    }
    
    // Local to global
    db_theta1 = theta1;
    db_theta2 = theta2;
    db_theta3 = theta3;
    db_rPerc1 = perc1;
    db_rPerc2 = perc2;

    return EXIT_SUCCESS;
}