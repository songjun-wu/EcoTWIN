#include "Basin.h"

int Basin::Routing_Q_1(Control &ctrl, Param &par){

    int from_j, count;
    double chnwidth, chnlength, Qall, Qupstream;
    double sqrtS, Manningn, a;
    double avQ, abQ, Qk, Qk1, fQj1i1, dfQj1i1, C;  // Variables used in Kinematic water solver
    

    double dx = ctrl._dx;
    double dt = ctrl.Simul_tstep;
    double dtdx = dt / dx;
    double dx_square = dx * dx;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        chnwidth = _chnwidth->val[j];  // [m]
        
        if (chnwidth>0){
            Qall = (_chanS->val[j] + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j]) * dx / dt; // Channel storage and all inflow from terrestrial grid [m] to [m2/s]
            Qupstream = _Qupstream->val[j];  // Upstream discharge [m3/s]

            
            chnlength = _chnlength->val[j];  // [m]

            from_j = _sortedGrid.to_cell[j];

            if (Qall + Qupstream > 0){

                

                sqrtS = pow(_slope->val[j], 0.5);

                Manningn = par._Manningn->val[j] * chnlength;  // Manning's N scaled with channel length
                a = pow(pow(chnwidth,0.67)*Manningn/sqrtS, 0.6); //wetted perimeter approximated with channel width

                //initial guess
                avQ = 0.5*(Qupstream);
                if (avQ==0) abQ=0;
                else abQ = a*0.6*pow(avQ, 0.6-1);

                Qk1 = ((dtdx*Qupstream) + dt*Qall)/(dtdx+abQ);

                C =  dtdx * Qupstream + dt*Qall;
                
                count = 0;
                do{
                    Qk=Qk1;
                    fQj1i1 = dtdx*Qk+a*powl(Qk, 0.6)-C;
                    dfQj1i1 = dtdx+a*0.6*powl(Qk, 0.6-1);
                    Qk1 = Qk - (fQj1i1/dfQj1i1);
                    if (Qk1 <=0){// if NR cannot converge then get some of the available water out and exit the loop
                        Qk1 = 0.61803*((dtdx*Qupstream) + dt*Qall)/(dtdx+abQ);
                        break;
                }
                    count++;
                }while(fabs(fQj1i1)>0.00001 && count < 500);
                if(count >=500){
                cout << "Kinematic wave solution did not converge" << endl;
            }

                _chanS->val[j] = std::max(0.0,(Qupstream+Qall*_dx  - Qk1)*dt) / dx_square;
                _Q->val[j] = Qk1; // Discharge [m3/s]
                
                if (_sortedGrid.lat_ok[j] == 1){
                    _Qupstream->val[from_j] += Qk1;  // Discharge inflow [m3/s]
                }

                //if (j==158794){
                //   cout << Qk1 << " "<< _chanS->val[j]*dx_square / dt << " " << Qall * dx << " " << Qupstream << endl;
                //}

            }
        }

        if (j==0){
           //cout << _Q->val[j] << endl;
        }
        
    }

    return EXIT_SUCCESS;
}