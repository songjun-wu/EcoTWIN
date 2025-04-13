#include "Basin.h"

int Basin::Fractionation(Atmosphere &atm, svector &sv_evap, svector &sv_V_new, svector &sv_di_old, svector &sv_di_new, svector &sv_di_evap, int issoil){

    double Ta, Ts, ha, hs, ha_p, ea_s, es_s, alpha_p, eps, eps_p, eps_k, m, n, f;
    double di_atm, di_s, di_new, di_evap, di_old; // Isotopic signitures
    double V_new, V_old, evap;
    di_atm = di_s = di_new = di_evap = di_old = 0;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        V_new = sv_V_new.val[j];  // Water storage after evaporation
        // If there is not water, then reset d18O
        if (V_new < roundoffERR){
            continue;
        }
        // Only preceed if there is evaporation
        evap = sv_evap.val[j];
        if (evap > roundoffERR){        
            Ta = atm._Ta->val[j];  // Atmospheric temperature [Degree C]
            Ts = Get_soil_temperature(Ta, Ts, _LAI->val[j]);  // Soil temperature [Degree C]
            ha = atm._RH->val[j];  // Atmospheric relative humidity [decimal]         
            
            V_old = V_new + evap;  // Water storage before evaporation

            if (issoil == 1){
                // Saturated vapor pressure in atmosphere or soil [Pa]
                ea_s = 611 * expl((17.3 * Ta)/(Ta + 237.3));
                es_s = 611 * expl((17.3 * Ts)/(Ts + 237.3));
            }
            
            ha_p = (issoil == 1) ? min(ha * ea_s / es_s, 1.0) : (ha + 1) / 2;  // Corrected relative humidity at the surface; should not exceed 1.0

            hs = 1; // Soil relative humidity [decimal]
            hs = hs < ha_p ? ha_p : hs;  // Soil humidity > Atmospheric humidity

            // Oxygen 18
            alpha_p = exp((-7.685 + 6.7123*1000/(Ta+273.15) - 1.6664*1e6/pow(Ta+273.15,2) +
                0.35041*1e9/pow(Ta+273.15,3))/1000);
            
            // Equilibrium enrichment (Skrzypek et al., 2015)
            eps_p = (alpha_p - 1) * 1000;
            di_atm = (atm._d18o_P->val[j] - eps_p)/ alpha_p;  // Atmospheric Isotopic signiture

            //Water transport mode: from diffusive (=1, dry soil) to turbulent (=0.5, water body)
            n = (issoil==1) ? 1 : 0.5;

            // Kinetic fractionation factor epsilon_k; Merlivat (1978)
            eps_k = (1 - ha_p) * (1 - 0.9859) * 1000 * n;

            eps = eps_p + eps_k;   // Gibson and Reid (2010)
            di_s = (ha_p * di_atm + eps) / (ha_p - eps/1000);
            m = (1 - ha_p + eps_k/1000) < roundoffERR ? 0 : (ha_p - eps/1000) / (1 - ha_p + eps_k/1000);

            // Fractionation
            if (V_old>0) {
                f = V_new/V_old;	// Evaporative loss fraction

                // Isotopic signature of remaining water
                di_new = di_s - (di_s - di_old) * (powl(f,m) > 1 ? 1 : powl(f,m));  

                // Isotopic signature of evaporated water
                di_evap = (1 - ha_p + eps_k/1000) < roundoffERR ? di_new : (di_new - ha_p*di_atm - eps)/ (1 - ha_p + eps_k/1000);
            
                // Closure of mass balance?
                /*
                //evap = (V_old - V_new);
                //Vavg = (V_old + V_new)/2;
                //Vdiff = (V_new - V_old);
                //corr = 0;   // Correction factor (mass-balance closure)
                if(abs(di_evap - di_new) > RNDOFFERR){
                corr = -((Vdiff*di_old/2 - Vavg*di_old - evap*(ha_p*di_atm+eps)/(1-ha_p+eps_k/1000)) + 
                    di_new*(Vavg +Vdiff/2 + evap/(1-ha_p+eps_k/1000)))/
                        (Vavg + Vdiff/2 + evap/(1-ha_p+eps_k/1000));
                di_new = di_new + corr;
                di_evap = (1 - ha_p + eps_k/1000) < RNDOFFERR ? di_new :(di_new - ha_p*di_atm - eps)/ (1 - ha_p + eps_k/1000);
            
                if(di_evap > di_new){      // Check here if di_evap > di_new (not possible)
                    di_new = di_old;
                    di_evap = di_old;
                }
                }
                */
                di_new  = max(-1000.0, di_new);
                di_evap = max(-1000.0, di_evap);
            }

            sv_di_new.val[j]  = di_new;
            sv_di_evap.val[j] = di_evap;
        }   
    }
    return EXIT_SUCCESS;
}
      

