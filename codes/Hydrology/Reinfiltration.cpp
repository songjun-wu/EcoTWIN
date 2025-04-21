#include "Basin.h"


int Basin::Reinfiltration_1(Control &ctrl, Param &par, int j, double &db_rinfilt, double &db_theta1, double &db_pond) {

    

    double dt = ctrl.Simul_tstep;  // Seconds in each timestep
    double eff_Ks1 = 0; // Effective hydrological conductivity
    double dtheta = 0; // Available room for infiltration
    double F = 0; // Cumulative infiltration amounts (if there's multiple land use types in one grid cell)
    double f = 0; // Infiltration rates at specific time
    double deltaF = 0; // Cumulative infiltration within the timestep



    deltaF = 0; // Initialisation

    double theta1 = _theta1->val[j];
    double depth1 = _depth1->val[j];

    eff_Ks1 = _Ks1->val[j] * par._KvKh->val[j]; // Effective hydrological conductivity
    dtheta =  _thetaS1->val[j] * (1 - max((theta1 - _thetaWP1->val[j]) / (_thetaS1->val[j] - _thetaWP1->val[j]), 0.0));
    

    // If soil is too saturated for further infiltration
    if (dtheta < 0){
        db_rinfilt = 0.0;
        return EXIT_SUCCESS;
    }

    
    // Else infiltration starts
    double input = db_pond;
    double input_dt = input / dt;  // m/s        

    // If all excess water can be infiltrated
    if (input_dt <= eff_Ks1){
        deltaF = input;
    }

    // Else estimate infiltration using Green-Ampt method
    else if (input_dt > eff_Ks1){
        double psidtheta = fabs(par._psiAE->val[j]) * dtheta;
        F = theta1 * depth1; // Soil storage 
        f = eff_Ks1 * (1 + psidtheta / F) ; // Theoratical infiltration rates at time t
        double i = min(input_dt, f);  // Actual infiltration rate at time t (should not exceed the infiltration rate of ponding water)
        double tp = (eff_Ks1 * psidtheta) / (i * (i - eff_Ks1)); // Time of the emergence of ponding water
        // tp is calculated by Green-ampt equation and the assumption of i == f (the water starts to pond when inflitration rate equals to the input rate; Fp = i * tp)

        
        
        if (tp > dt){  // If time of ponding is later then the end of timestep
            deltaF = i * dt;
        } else{  // Newton's method
            double Fp = i * tp; // Cumulative infiltration at the ponding time tp
            double F1 = eff_Ks1 * dt; // Initial guess
            double fF; // 
            double dfF; // Derivative of fF
            int counter = 0;
            do {
                deltaF = F1;
                fF = deltaF - Fp - eff_Ks1 * (dt - tp) - psidtheta * log((psidtheta + deltaF) / (psidtheta + Fp));
                dfF = deltaF / (psidtheta + deltaF);
                F1 -= fF / dfF;
                counter++;
            } while ((fabs(deltaF - F1) > 1e-6) and (counter < 50));
            
            if (counter > 50){
                cout << "Green-Ampt equation is not solved with 500 iterations " << endl;
            }
        }
       

    }
    
    deltaF = deltaF > input ? input : deltaF;
    db_rinfilt = deltaF;
    db_theta1 += deltaF / depth1;
    db_pond -= deltaF;

    return EXIT_SUCCESS;
}


