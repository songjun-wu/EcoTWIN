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

  double LAI_total;  // Total leaf area index
  double LAI_sun, LAI_shade;  // Sunlit and shaded leaf area index
  double PPFD_diffuse, PPFD_direct;  // Diffuse and direct photosynthetic photon flux density
  double PAR_sun, PAR_shade;  // Sunlit and shaded photosynthetic active radiation
  double Ta_k, T1_k, TC_c, T0_c, air_pressure;  // Climate variables for photosynthesis
  double KC, KO, gamma, VC_max, Jmax;
  double carboxylation_rate;  // Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]

  double co2_leaf_mol; // CO2 concentration in leaf [mol(CO2) / mol(air)]



  double PAR_mol;  // Photosynthetically Active Radiation in J / mol(photons)
  
  double energy_scaling_factor;  // Energy scaled factor relative to 25C
  double water_limitation_factor; // Water stress factor
  
  


  // Farquhar-von Caemmerer-Berry Model
  // A = min{JC, JE} - RD

  

  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

    // =============================
    // ======= Radiation =======
    // =============================

    // Photosynthetically Active Radiation in (mol photons) * (m-2 ground area) * (s-1);
    // atm._Rswd->val[j] => Shortwave downward radiation [W m-2]
    PAR_mol = atm._Rswd->val[j] * (1 - canopy_albedo) * ratio_par_to_Rsw / Epar;   

    // Only calculate assimilation with LAI presence
    LAI_total = _LAI->val[j];
    if (LAI_total < roundoffERR){
      _NPP->val[j] = 0;
      continue;
    }

    // === Split LAI into shaded and sunlit leaf area ===
    // LAI_sun = 2 * cos_zenith * (1 - exp(-0.5 * omega * LAI_total/ cos_zenith)) from Chen et al. (1999): https://doi.org/10.1016/S0304-3800(99)00156-8
    // cos_zenith = cos(zenith_angle) = 0.5 when zenith_angle = 60 degree
    // omega = 0.5; climping index
    LAI_sun = min(LAI_total, (1.0 - exp(-1 * LAI_total)));  
    LAI_shade = LAI_total - LAI_sun;

    // === Calculate shaded and sunlit leaf PAR per leaf area ===
    // Diffuse and direct PAR per ground area from total PAR
    PPFD_diffuse = PAR_mol * ratio_diffuse; // Diffuse PAR in mol photons * (m-2 ground area) * (s-1)
    PPFD_direct = PAR_mol - PPFD_diffuse; // Direct PAR in mol photons * (m-2 ground area) * (s-1)
    // Shaded leaf PAR
    // Chen et al. (1999): https://doi.org/10.1016/S0304-3800(99)00156-8
    // PAR_shade = (PPFD_diffuse - PPDF_diffuse_under_canopy) / LAI + C
    // PPDF_diffuse_under_canopy = PPFD_diffuse * exp(-0.5 * omega * LAI_total/ cos_zenith*))
    // where cos_zenith* = 0.537+0.025 * LAI_total
    // Here for simplicity, we use cos_zenith* = 0.5, omega = 0.5
    PAR_shade = PPFD_diffuse * ( 1 - exp(-0.5 * LAI_total)) / LAI_total;  // Diffuse PAR in mol photons * (m-2 leaf area) * (s-1)
    // Sunlit leaf PAR
    // PAR_sun = (PPFD_direct * cos_alpha / cos_zenith) + PAR_shade;  where alpha = 60 degrees as representative value for northern hemisphere
    PAR_sun = (PPFD_direct * 1) + PAR_shade;  // Direct PAR in mol photons * (m-2 leaf area) * (s-1)

    
    // Climate variables for photosynthesis
    Ta_k = atm._Ta->val[j] + 273.15;  // Air temperature in Kalvin
    T1_k = 25.0 + 273.15;  // 25 degree Celcius in Kalvin
    TC_c = atm._Ta->val[j]; // Air temperature in Celcius
    T0_c = TC_c - 25;  // Temperature relative to 25 degree Celcius
    air_pressure = atm._airpressure->val[j];  // Air pressure [Pa]
    
    // Energy scaled factor relative to 25C
    energy_scaling_factor = T0_c / R_gas / T1_k / Ta_k;

    // Michaelis-Menten constant corrected by temperature
    // k = k(25C) * EXP((Veg Temp - 25) * aktivation energy *  / 298.16 * R_gas * (Veg Temp + 273.16))
    KC = KC0 * exp(EC * energy_scaling_factor);
    KO = KO0 * exp(EO * energy_scaling_factor);

    // water limitation factor weighted by root distribution in three layers
    // For stomatal conductance correction due to water stress
    water_limitation_factor =\  
    _froot_layer1->val[j] * (_theta1->val[j] - _thetaWP1->val[j]) / (_thetaFC1->val[j] - _thetaWP1->val[j]) + 
    _froot_layer2->val[j] * (_theta2->val[j] - _thetaWP2->val[j]) / (_thetaFC2->val[j] - _thetaWP2->val[j]) + 
    _froot_layer3->val[j] * (_theta3->val[j] - _thetaWP3->val[j]) / (_thetaFC3->val[j] - _thetaWP3->val[j]);
    water_limitation_factor = min(max(0.0, water_limitation_factor), 1.0);
    water_limitation_factor /= water_limitation_factor + 0.3;  // Michaelis-Menten function for soil moisture limitation of photosynthesis

    // Maximum carboxylation rate corrected by temperature
    carboxylation_rate = par._carboxylation_rate->val[j];
    VC_max = carboxylation_rate * exp(EV * energy_scaling_factor) * water_limitation_factor;

    // Maximum electron transport rate
    Jmax = par._ETransport->val[j] * TC_c / 25;
    Jmax = max(Jmax, min_of_max_carboxylation_rate) * water_limitation_factor;

    // CO2 compensation point without leaf respiration
    gamma = max(1.7e-6*TC_c, 0.0);

    Photosynthesis_C3(j, ctrl.Simul_tstep, PAR_sun, atm._RH->val[j], LAI_sun, Ta_k, TC_c, air_pressure, energy_scaling_factor, co2_mol, co2_leaf_mol, 
      KC, KO, VC_max, Jmax, gamma, water_limitation_factor, carboxylation_rate, *_NPP, *_canopy_conductance);
    
    Photosynthesis_C3(j, ctrl.Simul_tstep, PAR_shade, atm._RH->val[j], LAI_shade, Ta_k, TC_c, air_pressure, energy_scaling_factor, co2_mol, co2_leaf_mol, 
      KC, KO, VC_max, Jmax, gamma, water_limitation_factor, carboxylation_rate, *_NPP, *_canopy_conductance);
    
  }  // end of for loop over grid cells

    return EXIT_SUCCESS;
}



int Basin::Photosynthesis_C3(int j, int timestep, double PAR_mol, double relative_humidity, double LAI, double Ta_k, double TC_c, double air_pressure, double energy_scaling_factor, double co2_mol, double co2_leaf_mol,
                    double KC, double KO, double VC_max, double Jmax, double gamma, double water_limitation_factor, double carboxylation_rate,  svector &sv_NPP, svector &sv_canopy_conductance){
   
    double dark_respiration;
    double maintenance_respiration; 
    double grow_respiration;
    double hitin_hib, dark_hib;  // Light dependance for respiration and temperature dependance for respiration
    double absorb_PAR_per_lai; // Absored PAR by canopy J / (mol(photons) * LAI)
    double JC; // Carboxylilation controlled assimilation
    double JE; // Light limited Assimilation
    double GPP;  // Gross primary production per leaf area
    double J1;  // Carboxylilation controlled assimilation JE without water stress
    double canopy_conductance_leaf;  // Canopy stomatal conductance per leaf area  [m s-1 leaf area]
    int iter; 

    // ========== C3 plant: Dark respiration and gross photosynthesis ==========
    absorb_PAR_per_lai = PAR_mol;  // Absored PAR by canopy per leaf area (mol photons) * (m-2 leaf area) * (s-1)

    // Some varaiables only needs to compute once
    // Dark respiration following Farqhuar et al. (1980)
    dark_hib = 0.5 + 0.5 * exp(-2e5 * max(0.0, PAR_mol));  // Light dependance for respiration
    hitin_hib = 1 / (1 + exp(1.3*(TC_c - 55)));  // Temperature dependance for respiration
    dark_respiration = carboxylation_rate * min(0.015, FRDC3 * exp(ER * energy_scaling_factor) * dark_hib * hitin_hib);
                        
    // Initial guess of CO2 in leaf
    co2_leaf_mol = co2_mol * ratio_co2_leaf_to_air_C3;  // CO2 concentration in leaf [mol(CO2) / mol(air)]
    // Calculate Carboxylilation controlled assimilation JE without water stress
    // The assimilation follows the Farqhuar (1980) formulation for C3 plants
    if (Jmax > min_of_max_carboxylation_rate){
      J1 = frac_photon_capture * absorb_PAR_per_lai * Jmax / sqrt(pow(Jmax, 2) + pow(frac_photon_capture*absorb_PAR_per_lai, 2));
    } else {
      J1 = 0;
    }
    // Vapour pressure deficit
    double Ea_s = 611 * exp((17.3 * TC_c)/(TC_c + 237.3));  // Saturated vapor pressure in atmosphere [Pa]
    double VPD = max(0.05, Ea_s - relative_humidity * Ea_s) / 1000;  // Vapour pressure deficit [KPa]

    // Iterative solution for co2_leaf_mol
    for (iter=0; iter<5; iter++){
      // Farquhar model for GPP calculation
      JE = J1 * (co2_leaf_mol - gamma) / 4 / (co2_leaf_mol + 2 * gamma);
      JC = VC_max * (co2_leaf_mol - gamma) / (co2_leaf_mol + KC * (1 + o2_mol/KO));
      // Calculate GPP without water stress
      GPP = min(JE, JC) * hitin_hib;  // GPP in mol(CO2) / m2 (leaf area) s-1
      double A = GPP - dark_respiration;  // Assimilation in mol(CO2) / m2 (leaf area) s-1

      // Medlyn model for stomatal conductance calculation
      if (A <= 0.0) {
        canopy_conductance_leaf = 0.01;  // Stomatal conductance [mol(H2O) / m2 (leaf area) s-1]
      } else {
        canopy_conductance_leaf = 0.01 + 1.6 * (1 + 6 / sqrt(max(VPD,0.05))) * A / co2_mol;  // Stomatal conductance [mol(H2O) / m2 (leaf area) s-1]


      // Fick model for co2_leaf_mol calculation
      double co2_leaf_mol_new = co2_mol - 1.6 * A / canopy_conductance_leaf;  // CO2 concentration in leaf [mol(CO2) / mol(air)]
      co2_leaf_mol_new = max(0.1*co2_mol, min(0.9*co2_mol, co2_leaf_mol_new));

      if (fabs(co2_leaf_mol_new - co2_leaf_mol) < 1e-7) break;

      // Update co2_leaf_mol
      co2_leaf_mol = 0.5*co2_leaf_mol + 0.5*co2_leaf_mol_new;

      }
    }

    

    // Calculate NPP (gC/m²(ground)/yr) and canopy conductance (m s-1)
    maintenance_respiration = dark_respiration / 0.25;  // leaf fraction of plant-total (autotrophic) respiration
    grow_respiration = max(0.0, (0.25 * (GPP - maintenance_respiration)));
    sv_NPP.val[j] += (GPP - maintenance_respiration - grow_respiration) * timestep * molC_m2_to_gC_m2 * LAI;  // NPP in gC/m²(ground)/timestep
    sv_canopy_conductance.val[j] += canopy_conductance_leaf * R_gas * Ta_k / air_pressure * LAI;  // Canopy conductance in m s-1


    

  return EXIT_SUCCESS;
}

 
 
