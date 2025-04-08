#include "Basin.h"

/*
Soil_profile_1 :
Pedo-transfer function for estimation of hydrological conductivity, based on Wosten et al., (1999)
Citation: Wösten, H., Lilly, A., Nemes, A., & Le Bas, C. (1999). Development and use of a database of hydraulic properties of European Soils. Geoderma, 90, 169-185. https://doi.org/10.1016/S0016-7061(98)00132-3
*/

int Basin::Pedo_transfer_1(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP){
    
    const int topsoil_factor = 0; // Topsoil = 1; subsoil = 0
    const int opt_fieldcapacity = ctrl.opt_fieldcapacity;
    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters
    double thetaS;
    double Ks;
    

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double sand = sv_sand.val[j] * 100;  // percent
        double clay = sv_clay.val[j] * 100;  // percent
        double silt = sv_silt.val[j] * 100;  // percent
        double organic_content = sv_organic_content.val[j] * 100; 
        double bulk_density = sv_bulk_density.val[j]; // g/cm3

        double organic_content_pow = organic_content * organic_content;
        double bulk_density_square = bulk_density * bulk_density;
        double silt_log = log(silt);
        double organic_content_log = log(organic_content);
        
        // Calculate Van Genuchten parameters
        // Wosten et al., (1999)
        VG_alpha = exp(-14.96 + 0.03135 * clay + 0.0351 * silt + 0.646 * organic_content + 15.29 * bulk_density \
            - 0.192 * topsoil_factor - 4.671 * bulk_density_square - 0.000781 * clay * clay \
            - 0.00687 * organic_content_pow + 0.0449 / organic_content + 0.0663 * silt_log \
            + 0.1482 * organic_content_log - 0.04546 * bulk_density * silt - 0.4852 * bulk_density * organic_content \
            + 0.00673 * topsoil_factor * clay);
        
        VG_n = exp(-25.23 - 0.02195 * clay + 0.0074 * silt - 0.194 * organic_content + 45.5 * bulk_density \
            - 7.24*bulk_density_square + 0.0003658*clay*clay + 0.002885*organic_content_pow \
            - 12.81/bulk_density - 0.1524/silt - 0.01958/organic_content - 0.2876*silt_log \
            - 0.0709*organic_content_log - 44.6*log(bulk_density) - 0.02264*bulk_density*clay \
            + 0.0896*bulk_density*organic_content + 0.00718*topsoil_factor*clay) + 1;

        // Calculate Van Genuchten's n
        VG_m = 1 - 1 / VG_n;

        // Calculate saturated theta
        thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1.16e-7;  // cm/day to m/s
        sv_Ks.val[j] = max(Ks, 1.3e-7); // Ks > 1 mm/d


        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            sv_thetaFC.val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            sv_thetaFC.val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
        
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        sv_thetaWP.val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);

        sv_thetaS.val[j] = thetaS;

    }
    return EXIT_SUCCESS;
}

int Basin::Pedo_transfer_2(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP){
    
    const int topsoil_factor = 0; // Topsoil = 1; subsoil = 0
    const int opt_fieldcapacity = ctrl.opt_fieldcapacity;
    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters
    double thetaS;
    double Ks;
    

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double sand = sv_sand.val[j] * 100;  // percent
        double clay = sv_clay.val[j] * 100;  // percent
        double silt = sv_silt.val[j] * 100;  // percent
        double organic_content = sv_organic_content.val[j] * 100; 
        double bulk_density = sv_bulk_density.val[j]; // g/cm3

        double organic_content_pow = organic_content * organic_content;
        double bulk_density_square = bulk_density * bulk_density;
        double silt_log = log(silt);
        double organic_content_log = log(organic_content);
        

        // Calculate Van Genuchten parameters
        // Wosten et al., (1997)
        VG_alpha = exp(11 - 2.298 * bulk_density * bulk_density - 12.41 / bulk_density + 0.838 * organic_content \
            + 0.343 / organic_content + 2.03 * organic_content_log - 1.263 * bulk_density * organic_content);

        VG_n = exp(-0.34 + 1.224/bulk_density - 0.7952*log(clay) - 0.3201*organic_content_log \
                        + 0.0651*bulk_density*organic_content) + 1;

        // Calculate Van Genuchten's n
        VG_m = 1 - 1 / VG_n;

        // Calculate saturated theta
        thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1.16e-7;  // cm/day to m/s
        sv_Ks.val[j] = max(Ks, 1.3e-7); // Ks > 1 mm/d


        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            sv_thetaFC.val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            sv_thetaFC.val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
        
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        sv_thetaWP.val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);

        sv_thetaS.val[j] = thetaS;

    }

    return EXIT_SUCCESS;
}

int Basin::Pedo_transfer_3(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP){
    
    const int topsoil_factor = 0; // Topsoil = 1; subsoil = 0
    const int opt_fieldcapacity = ctrl.opt_fieldcapacity;
    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters
    double thetaS;
    double Ks;
    

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        double sand = sv_sand.val[j] * 100;  // percent
        double clay = sv_clay.val[j] * 100;  // percent
        double bulk_density = sv_bulk_density.val[j]; // g/cm3
        

        // Calculate Van Genuchten parameters
        // Zacharias et al., (2007)
        if (sand < 66.5) {
            VG_alpha = exp(-0.648 + 0.023 * sand + 0.044 * clay - 3.168 * bulk_density); 
            VG_n = 1.392 - 0.418 * pow(sand, -0.024) + 1.212 * pow(clay, -0.704);
        } else{
            VG_alpha = exp(-4.197 + 0.013 * sand + 0.076 * clay - 0.276 * bulk_density);
            VG_n = -2.562 + 7e-9 * pow(sand, 4.004) + 3.75 * pow(clay, -0.016);
        }
        

        // Calculate Van Genuchten's n
        VG_m = 1 - 1 / VG_n;

        // Calculate saturated theta
        thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1.16e-7;  // cm/day to m/s
        sv_Ks.val[j] = max(Ks, 1.3e-7); // Ks > 1 mm/d


        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            sv_thetaFC.val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            sv_thetaFC.val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
        
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        sv_thetaWP.val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);

        sv_thetaS.val[j] = thetaS;

    }

    return EXIT_SUCCESS;
}

int Basin::Soil_proporty(Control &ctrl, Param &par){

    // Calculate soil proporties in layer 1
    if (ctrl.opt_pedotransf == 1){  // Wosten et al., (1999)
        Pedo_transfer_1(ctrl, par, *_sand1,  *_clay1,  *_silt1,  *_organic1, *_bulkdensity1, *_Ks1, *_thetaS1, *_thetaFC1, *_thetaWP1);
    }
    else if (ctrl.opt_pedotransf == 2){  // Wosten et al., (1997)
        Pedo_transfer_2(ctrl, par, *_sand1,  *_clay1,  *_silt1,  *_organic1, *_bulkdensity1, *_Ks1, *_thetaS1, *_thetaFC1, *_thetaWP1);
    }
    else if (ctrl.opt_pedotransf == 3){ // Zacharias et al., (2007)
        Pedo_transfer_3(ctrl, par, *_sand1,  *_clay1,  *_bulkdensity1, *_Ks1, *_thetaS1, *_thetaFC1, *_thetaWP1);
    }


    // Calculate for the remaining layer (2 and 3)
    // Same for all depths
    if (ctrl.opt_depthprofile==1){  
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        _thetaS2->val[j] = _thetaS1->val[j];
        _thetaS3->val[j] = _thetaS1->val[j];
        _thetaFC2->val[j] = _thetaFC1->val[j];
        _thetaFC3->val[j] = _thetaFC1->val[j];
        _thetaWP2->val[j] = _thetaWP1->val[j];
        _thetaWP3->val[j] = _thetaWP1->val[j];
        }
    } 
    
    // Depth dependent
    else if (ctrl.opt_depthprofile==2) {  
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        double depth1 = _depth1->val[j];
        double depth2 = _depth2->val[j];
        double depth3 = par._depth3->val[j];

        double Ks0 = _Ks1->val[j];
        double thetaS0 = _thetaS1->val[j];
        double thetaFC0 = _thetaFC1->val[j];
        double thetaWP0 = _thetaWP1->val[j];

        double KKs = par._KKs->val[j];
        double Ksat = par._Ksat->val[j];
        double bclamda = par._BClambda->val[j];
        double psiAE = par._psiAE->val[j];

        // Hydraulic conductivity decreases with depth
        _Ks1->val[j] = KKs * Ks0 * (1 - exp(-depth1 / KKs)) / depth1;
        _Ks2->val[j] = KKs * Ks0 * (exp(-depth1 / KKs) - exp(-(depth1+depth2) / KKs)) / depth2;
        _Ks3->val[j] = KKs * Ks0 * (exp(-(depth1+depth2) / KKs) - exp(-(depth1+depth2+depth3) / KKs)) / depth3;

        // Saturated moisture content decreases with depth
        _thetaS1->val[j] = Ksat * thetaS0 * (1 - exp(-depth1 / Ksat)) / depth1;
        _thetaS2->val[j] = Ksat * thetaS0 * (exp(-depth1 / Ksat) - exp(-(depth1+depth2) / Ksat)) / depth2;
        _thetaS3->val[j] = Ksat * thetaS0 * (exp(-(depth1+depth2) / Ksat) - exp(-(depth1+depth2+depth3) / Ksat)) / depth3;

        // Field capacity
        _thetaFC1->val[j] = pow(psiAE / 3.36, 1 / bclamda) * (_thetaS1->val[j] - thetaWP0) + thetaWP0;
        _thetaFC2->val[j] = pow(psiAE / 3.36, 1 / bclamda) * (_thetaS2->val[j] - thetaWP0) + thetaWP0;
        _thetaFC3->val[j] = pow(psiAE / 3.36, 1 / bclamda) * (_thetaS3->val[j] - thetaWP0) + thetaWP0;
    }
    } 

     // Pedo-transfer fucntion for each layer
    else if (ctrl.opt_depthprofile==3) {
        // Calculate soil proporties in layer 2 and 3
        if (ctrl.opt_pedotransf == 1){  // Wosten et al., (1999)
            Pedo_transfer_1(ctrl, par, *_sand2,  *_clay2,  *_silt2,  *_organic2, *_bulkdensity2, *_Ks2, *_thetaS2, *_thetaFC2, *_thetaWP2);
            Pedo_transfer_1(ctrl, par, *_sand3,  *_clay3,  *_silt3,  *_organic3, *_bulkdensity3, *_Ks3, *_thetaS3, *_thetaFC3, *_thetaWP3);
        }
        else if (ctrl.opt_pedotransf == 2){  // Wosten et al., (1997)
            Pedo_transfer_2(ctrl, par, *_sand2,  *_clay2,  *_silt2,  *_organic2, *_bulkdensity2, *_Ks2, *_thetaS2, *_thetaFC2, *_thetaWP2);
            Pedo_transfer_2(ctrl, par, *_sand3,  *_clay3,  *_silt3,  *_organic3, *_bulkdensity3, *_Ks3, *_thetaS3, *_thetaFC3, *_thetaWP3);
        }
        else if (ctrl.opt_pedotransf == 3){ // Zacharias et al., (2007)
            Pedo_transfer_3(ctrl, par, *_sand2,  *_clay2,  *_bulkdensity2, *_Ks2, *_thetaS2, *_thetaFC2, *_thetaWP2);
            Pedo_transfer_3(ctrl, par, *_sand3,  *_clay3,  *_bulkdensity3, *_Ks3, *_thetaS3, *_thetaFC3, *_thetaWP3);
        }

    }

    return EXIT_SUCCESS;
}



