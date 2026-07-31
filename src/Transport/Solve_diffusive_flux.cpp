/***************************************************************
* EcoTWIN, a spatial-distributed ecohydrological model that
* tracks water, isotope, and nutrient fluxes across spatial scales

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * EcoTWIN is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_diffusive_flux.cpp
  * Created  on: 30.07.2026
  * Modified on: 30.07.2026
***************************************************************/


#include "Basin.h"


int Basin::Solve_diffusive_flux(Param &par, svector &sv_conc1, svector &sv_conc2, const svector &sv_storage1, const svector &sv_storage2, const svector &sv_length1, const svector &sv_length2,
                                bool theta_flag1, bool theta_flag2, bool isotope_flag){
    

    double storage1, storage2, conc1, conc2, length1, length2, diffusion_flux, equilibrium_mass;
    

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        storage1 = sv_storage1.val[j];
        storage2 = sv_storage2.val[j];
        length1 = sv_length1.val[j];
        length2 = sv_length2.val[j];

        if (theta_flag1){
            storage1 *= length1;
        }
        if (theta_flag2){
            storage2 *= length2;
        }
        conc1 = sv_conc1.val[j];
        conc2 = sv_conc2.val[j];

        if (storage1 > roundoffERR and storage2 > roundoffERR){

            // Unit conversion for stable water isotopes
            if (isotope_flag){
                conc1 = 1 + conc1/1000;
                conc2 = 1 + conc2/1000;
            }

            diffusion_flux = par._diffuse_molecular_coefficient->val[j] * (conc1 - conc2)/ ((length1 + length2)/2);
            equilibrium_mass = (conc1 - conc2) * storage2 * storage1 / (storage2 + storage1);

            if (diffusion_flux > 0) {
                //diffusion_flux = min(diffusion_flux, conc1 * storage1 * 0.5);
                diffusion_flux = min(diffusion_flux, equilibrium_mass);
            } else if (diffusion_flux < 0) {
                //diffusion_flux = max(diffusion_flux, -conc2 * storage2 * 0.5);
                diffusion_flux = max(diffusion_flux, equilibrium_mass);
            }
            conc1 -= diffusion_flux / storage1;
            conc2 += diffusion_flux / storage2;

            if (isotope_flag){
                conc1 = (conc1- 1) * 1000;
                conc2 = (conc2- 1) * 1000;
            }
            
            // Update the concentrations
            sv_conc1.val[j] = conc1;
            sv_conc2.val[j] = conc2;     
        }
    }

    return EXIT_SUCCESS;
}