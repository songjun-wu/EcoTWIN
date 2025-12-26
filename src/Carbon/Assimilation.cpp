/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Assimilation.cpp
  * Created  on: 22.11.2025
  * Modified on: 23.11.2025
***************************************************************/


#include "Basin.h"

int Basin::Assimilation(Control &ctrl, Atmosphere &atm, Param &par){

  double Ta_k, T1_k, TC_c, T0_c;
  double KC, KO, gamma, VC_max, hitin_hib, dark_hib, Jmax;
  double carboxylation_rate, frac_PAR_per_lai;

  double dark_respiration;
  double maintenance_respiration; 
  double grow_respiration;

  double PAR_mol;  // Photosynthetically Active Radiation in J / mol(photons)
  double absorb_PAR_per_lai; // Absored PAR by canopy J / (mol(photons) * LAI)
  double JC; // Carboxylilation controlled assimilation
  double JE; // Light limited Assimilation
  double GPP;  // Gross primary production
  double N_limitation_factor = 1.0; // TODO: No nutrient limitation
  double water_limitation_factor; // Water stress factor
  double G0, B, C, J1, W1;

  

  // C4
  double K;
  double LAI;  // leaf area index = _LAI->val[j]
  double Rsw, Rsw_tmp; // Shortwave downward radiation [W m-2]
  double canopy_conductance, conductance_d;  // Canopy conductance and related parameters

  // Farquhar-von Caemmerer-Berry Model
  // A = min{JC, JE} - RD

  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

    LAI = _LAI->val[j];
    // Only calculate assimilation with LAI presence
    if (LAI < roundoffERR){
      _NPP->val[j] = 0;
      continue;
    }

    Rsw = atm._Rswd->val[j]; // Shortwave downward radiation [W m-2]

    // Calculate the canopy conductance; Eq.3.3.2.12 in ECHAM3 manual / JSBACH
    if (LAI > roundoffERR){
      Rsw_tmp = max(roundoffERR, Rsw);
      conductance_d = (conductance_a + conductance_b * conductance_c) / (conductance_c * Rsw_tmp);
      canopy_conductance = (log((conductance_d * exp(conductance_k*LAI) + 1) / (conductance_d + 1)) * conductance_b / (conductance_d * Rsw_tmp) - \
                            log((conductance_d + exp(-1*conductance_k*LAI)) / (conductance_d + 1)) ) \
                            / (conductance_k * conductance_c);  // Potential canopy conductance without water stress
    } else {
      canopy_conductance = roundoffERR;  // Potential canopy conductance without water stress (low LAI)
    }
    // water limitation factor weighted by root distribution in three layers
    water_limitation_factor = \  
    _froot_layer1->val[j] * (_theta1->val[j] - _thetaWP1->val[j]) / (_thetaFC1->val[j] - _thetaWP1->val[j]) + \
    _froot_layer2->val[j] * (_theta2->val[j] - _thetaWP2->val[j]) / (_thetaFC2->val[j] - _thetaWP2->val[j]) + \
    _froot_layer3->val[j] * (_theta3->val[j] - _thetaWP3->val[j]) / (_thetaFC3->val[j] - _thetaWP3->val[j]);
    water_limitation_factor = min(max(0.0, water_limitation_factor), 1.0);
    canopy_conductance *= water_limitation_factor; // Canopy conductance with water stress
    
    
    
    // =============================
    // ======= Photosythesis =======
    // =============================
    PAR_mol = Rsw / Epar;   // Photosynthetically Active Radiation in J / mol(photons)
    absorb_PAR_per_lai = PAR_mol * (1 - exp(-0.5*LAI)/LAI) ; // Absored PAR by canopy J / (mol(photons) * LAI)
    // absorbed fraction = 1 - exp(-k*LAI)/LAI; k is related to zenith angles (0.5 / cos_zenith_angle), but this is ommitted for simplification 
    
    Ta_k = atm._Ta->val[j] + 273.15;  // Air temperature in Kalvin
    T1_k = 25.0 + 273.15;  // 25 degree Celcius in Kalvin
    TC_c = atm._Ta->val[j]; // Air temperature in Celcius
    T0_c = TC_c - 25;  // Temperature relative to 25 degree Celcius
    carboxylation_rate = par._carboxylation_rate->val[j];  // Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]

    // =============== C3 Plants ===============
    if (_C4_flag->val[j]==0){
      // C3 plant: Dark respiration and gross photosynthesis
      // Michaelis-Menten constant corrected by temperature
      // k = k(25C) * EXP((Veg Temp - 25) * aktivation energy *  / 298.16 * R_gas * (Veg Temp + 273.16))
      KC = KC0 * exp(EC / R_gas * T0_c / T1_k / Ta_k);
      KO = KO0 * exp(EO / R_gas * T0_c / T1_k / Ta_k);
      // Maximum carboxylation rate corrected by temperature
      VC_max = par._carboxylation_rate->val[j] * N_limitation_factor * exp(EV / R_gas * T0_c / T1_k / Ta_k);

      // CO2 compensation point without leaf respiration
      gamma = max(1.7e-6*TC_c, 0.0);

      // Dark respiration following Farqhuar et al. (1980)
      dark_hib = 0.5 + 0.5 * exp(-2e5 * max(0.0, PAR_mol));
      hitin_hib = 1 / (1 + exp(1.3*(TC_c - 55)));
      dark_respiration = FRDC3 * par._carboxylation_rate->val[j] * N_limitation_factor * \
                          exp(ER / R_gas * T0_c / T1_k / Ta_k) * dark_hib * hitin_hib;
      
      // Maximum electron transport rate
      Jmax = par._ETransport->val[j] * N_limitation_factor * TC_c / 25;
      Jmax = max(Jmax, min_of_max_carboxylation_rate);

      // Calculate Carboxylilation controlled assimilation JE
      // Known: A = JE - RD
      // Known: A = canopy_conductance / 1.6 * (CA - Ci) * pressure / R / t_air 
      // => JE - RD = canopy_conductance / 1.6 * (CA - Ci) * pressure / R / t_air
      // after transformation we get: Ci = CA - (JE - RD) / (canopy_conductance / 1.6 * pressure / R / t_air)
      // Here we esemble denominator as G0 (eq1): G0 = canopy_conductance / 1.6 * pressure / R / t_air AND
      // We get eq2: Ci = CA - (JE - RD) / G0
      // Then, Known eq3: JE = J1 * (Ci - Gam) / 4 / (Ci + 2 * Gam) with J calculated in eq4
      // Replace Ci in eq3 with eq2, we get:
      // => JE = J1 * (CA-(JE-RD)/G0 - gam) / 4 / (CA-(JE-RD)/G0 + 2 * Gam)
      // => 4*JE*(CA-(JE-RD)/G0 + 2 * Gam) = J1 * (CA-(JE-RD)/G0 - gam)
      // => JE^2*(-4/G0) + JE*(4*(CA+RD/G0+2*Gam)) = JE*(-1*J1/G0) + J1*(CA+RD/G0 - gam)
      // => 0 = JE^2 - JE*((CA+2*Gam)*G0 + RD + J1/4) + J1/4*G0*(CA+RD/G0 - gam)
      // Solving this quadratic formula (0 = x2 - Bx + C) in eq5
      // eq2
      G0 = canopy_conductance / 1.6 * atm._airpressure->val[j] / R_gas / Ta_k;
      // eq4
      if (Jmax > min_of_max_carboxylation_rate){
        J1 = frac_photon_capture * absorb_PAR_per_lai * Jmax / sqrt(pow(Jmax, 2) + pow(frac_photon_capture*absorb_PAR_per_lai, 2));
      } else {
        J1 = 0;
      }
      // eq5: Solve quadratic formula
      W1 = J1 / 4;
      B = dark_respiration + W1 + (co2_mol + 2*gamma) * G0;
      C = W1 * G0 * (co2_mol - gamma) + W1 * dark_respiration;
      if (Jmax > min_of_max_carboxylation_rate){
        JE = B/2 - sqrt(max(pow(B,2)/4 - C, 0.0));
      } else {
        JE = 0.0;
      }

      // Simialr procedure applies for the light limited Assimilation Jc;
      // Set Ci in eqation : JC = VC_max * (Ci - Gam) / (Ci + KC * (1 + OX/KO))
      // We get quadratic formula:
      // 0 = JC^2 -(RD+VC_max+G0*(CA+K2))*JC +VC_max*G0*(CA-gam)+RD*VC_max
      B = dark_respiration + VC_max + G0 * (co2_mol + KC * (1 + o2_mol/KO));
      C = VC_max * G0 * (co2_mol - gamma) + VC_max * dark_respiration;
      JC = B/2 - sqrt(max(pow(B,2)/4 - C, 0.0));
      
      // Calculate GPP and NPP
      GPP = min(JE, JC) * hitin_hib;
      
    } else {
      // =============== C4 Plants ===============
      K = 0;
    }

    

    maintenance_respiration = dark_respiration / 0.4;  // leaf fraction of plant-total (autotrophic) respiration
    grow_respiration = max(0.0, (0.25/1.25 * (GPP - maintenance_respiration)));
    _NPP->val[j] = (GPP - maintenance_respiration - grow_respiration) * ctrl.Simul_tstep * molC_m2_to_gC_m2;
    

      
  }

    return EXIT_SUCCESS;
}

