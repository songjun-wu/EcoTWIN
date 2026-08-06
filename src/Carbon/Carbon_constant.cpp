/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Set_carbon_constant.cpp
  * Created  on: 26.11.2025
  * Modified on: 26.11.2025
***************************************************************/


#include "Basin.h"


int Basin::Set_carbon_constant(){

    ratio_day_time = 0.4;  // Ratio of day time to total time [-]

    // ======= Unit transformer =======
    molC_m2_to_gC_m2 = 12.01;  // 1 mol(C)/m2 = 12.01 gC/m2

    // ======= Radiation =======
    canopy_albedo = 0.15;  // Canopy albedo [-]
    ratio_diffuse = 0.1;    // Ratio of diffuse radiation to total radiation [-]
    ratio_par_to_Rsw = 0.45;  // Ratio of Photosynthetically Active Radiation to Shortwave radiation [-]
    R_gas = 8.314;  // Gas constant [J/mol-1K-1]
    Epar = 2.2e5;   //Energy content of PAR [J / mol(photons)]


    // Reference decomposition rates of carbon pools
    ref_decomp_rate_dpm_litter_CP = 10.0 / 365;  // Reference docomposition rate of decomposable plant material litter pool [1/day]
    ref_decomp_rate_rpm_litter_CP = 0.8 / 365;  // Reference docomposition rate of resistant plant material litter pool [1/day]; elevated to 0.8 to avoid overestimation of litter pools
    //ref_decomp_rate_rpm_litter_CP = 0.3 / 365;  // Reference docomposition rate of resistant plant material litter pool [1/day]
    ref_decomp_rate_bio_CP = 0.66 / 365;  // Reference docomposition rate of microbial biomass pool [1/day]
    ref_decomp_rate_humus_CP = 0.02 / 365;  // Reference docomposition rate of humus pool [1/day]



    // ======= Assimilation =======
    KC0 = 460e-6;   // Michaelis-menten Constant for CO2 at 25C [mol(CO2) / mol(air)]
    KO0 = 330e-3;   // Michaelis-menten Constant for O2 at 25C [mol(O2) / mol(air)]
    EC = 59356.0;     // Activation energy for KC [J/mol]
    EO = 35948.0;     // Activation energy for KO [J/mol]
    EV = 58520.0;     // Activation energy for Vcmax [J/mol]
    ER = 45000.0;     // Activation energy for dark respiration [J/mol]

    FRDC3 = 0.011;  // Ratio of dark respiration to PVM at 25C for C3 plants
    min_of_max_carboxylation_rate = 1e-12; // Minimum of maximum carboxylation rate [10^(-6) mol/(m^2 s)]

    // ======= Canopy conductance (Eq. 3.3.2.12 in ECHAM3 manual / JSBACH) =======
    conductance_k = 0.9;    // Parameter for canopy conductance/resistance []
    conductance_a = 5000;   // Parameter for conductance/resistance [Jm-3]
    conductance_b = 10;     // Parameter for canopy conductance/resistance [Wm-2]
    conductance_c = 100;    // Parameter for conductance/resistance [ms-1]

    // ======= Photosynthesis =======
    frac_photon_capture = 0.28;  // Efficiency of photon capture
    o2_mol = 209500e-6;  // Oxygen concentration [mol(o2) / mol(air)]
    co2_mol = 424.61e-6;  // CO2 mole mixing ratio [mol(co2) / mol(dry air)]
    ratio_co2_leaf_to_air_C3 = 0.8;  // Ratio of CO2 in leaf to air for C3 plants
    ratio_co2_leaf_to_air_C4 = 0.4;  // Ratio of CO2 in leaf to air for C4 plants
    
    

    return EXIT_SUCCESS;

}