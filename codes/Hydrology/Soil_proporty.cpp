#include "Basin.h"

/*
Soil_profile_1 :
Pedo-transfer function for estimation of hydrological conductivity, based on Wosten et al., (1999)
Citation: Wösten, H., Lilly, A., Nemes, A., & Le Bas, C. (1999). Development and use of a database of hydraulic properties of European Soils. Geoderma, 90, 169-185. https://doi.org/10.1016/S0016-7061(98)00132-3
*/
int Basin::Van_Genuchten_1(double &VG_alpha, double &VG_n, double &VG_m, double clay, double silt, double organic_content, double bulk_density, int topsoil_factor){

    VG_alpha = exp(-14.96 + 0.03135 * clay + 0.0351 * silt + 0.646 * organic_content + 15.29 * bulk_density \
        - 0.192 * topsoil_factor - 4.671 * bulk_density * bulk_density - 0.000781 * clay * clay \
        - 0.00687 * organic_content * organic_content + 0.0449 / organic_content + 0.0663 * log(silt) \
        + 0.1482 * log(organic_content) - 0.04546 * bulk_density * silt - 0.4852 * bulk_density * organic_content \
        + 0.00673 * topsoil_factor * clay);
    
    VG_n = exp(-25.23 - 0.02195 * clay + 0.0074 * silt - 0.194 * organic_content + 45.5 * bulk_density \
        - 7.24*bulk_density*bulk_density + 0.0003658*clay*clay + 0.002885*organic_content*organic_content \
        - 12.81/bulk_density - 0.1524/silt - 0.01958/organic_content - 0.2876*log(silt) \
        - 0.0709*log(organic_content) - 44.6*log(bulk_density) - 0.02264*bulk_density*clay \
        + 0.0896*bulk_density*organic_content + 0.00718*topsoil_factor*clay) + 1;

    return EXIT_SUCCESS;
}

int Basin::Van_Genuchten_2(double &VG_alpha, double &VG_n, double &VG_m, double clay, double organic_content, double bulk_density, int topsoil_factor){

    VG_alpha = exp(11 - 2.298 * bulk_density * bulk_density - 12.41 / bulk_density + 0.838 * organic_content \
        + 0.343 / organic_content + 2.03 * log(organic_content) - 1.263 * bulk_density * organic_content);

    VG_n = exp(-0.34 + 1.224/bulk_density - 0.7952*log(clay) - 0.3201*log(organic_content) \
                    + 0.0651*bulk_density*organic_content) + 1;

    return EXIT_SUCCESS;
}

int Basin::Van_Genuchten_3(double &VG_alpha, double &VG_n, double &VG_m, double clay, double sand, double organic_content, double bulk_density, int topsoil_factor){

    if (sand < 66.5) {
        VG_alpha = exp(-0.648 + 0.023 * sand + 0.044 * clay - 3.168 * bulk_density); 
        VG_n = 1.392 - 0.418 * pow(sand, -0.024) + 1.212 * pow(clay, -0.704);
    } else{
        VG_alpha = exp(-4.197 + 0.013 * sand + 0.076 * clay - 0.276 * bulk_density);
        VG_n = -2.562 + 7e-9 * pow(sand, 4.004) + 3.75 * pow(clay, -0.016);
    }

    return EXIT_SUCCESS;
}

    

int Basin::Soil_proporty_1(const int opt_pedotransf, const int opt_fieldcapacity, Param &par){

    double sand = 40;  // percent
    double clay = 30;
    double silt = 74;
    double organic_content = 5; 
    double bulk_density = 1.15; // g/cm3
    int topsoil_factor = 0; // Topsoil = 1; subsoil = 0
    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters

    double organic_content_pow = organic_content * organic_content;
    double bulk_density_square = bulk_density * bulk_density;
    double silt_log = log(silt);
    double organic_content_log = log(organic_content);
    

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
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
        const double thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        double Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1e-6;  // cm/day to m/s
        _Ks1->val[j] = min(Ks, 1.3e-7); // Ks > 1 mm/d

        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            _thetaFC1->val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            _thetaFC1->val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
        
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        _thetaWP1->val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);
    
    }

    return EXIT_SUCCESS;
}



int Basin::Soil_proporty_2(const int opt_pedotransf, const int opt_fieldcapacity, Param &par){

    double sand = 40;  // percent
    double clay = 30;
    double silt = 74;
    double organic_content = 5; 
    double bulk_density = 1.15; // g/cm3
    int topsoil_factor = 0; // Topsoil = 1; subsoil = 0

    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
    
        // Calculate Van Genuchten parameters
        // Wosten et al., (1997)
        VG_alpha = exp(11 - 2.298 * bulk_density * bulk_density - 12.41 / bulk_density + 0.838 * organic_content \
            + 0.343 / organic_content + 2.03 * log(organic_content) - 1.263 * bulk_density * organic_content);

        VG_n = exp(-0.34 + 1.224/bulk_density - 0.7952*log(clay) - 0.3201*log(organic_content) \
                        + 0.0651*bulk_density*organic_content) + 1;
            
        // Calculate Van Genuchten's n
        VG_m = 1 - 1 / VG_n;

        // Calculate saturated theta
        const double thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        double Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1e-6;  // cm/day to m/s
        _Ks1->val[j] = min(Ks, 1.3e-7); // Ks > 1 mm/d

        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            _thetaFC1->val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            _thetaFC1->val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
        
        
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        _thetaWP1->val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);    
    }

    return EXIT_SUCCESS;
}



int Basin::Soil_proporty_3(const int opt_pedotransf, const int opt_fieldcapacity, Param &par){

    double sand = 40;  // precent
    double clay = 30;
    double silt = 74;
    double organic_content = 5; 
    double bulk_density = 1.15; // g/cm3
    int topsoil_factor = 0; // Topsoil = 1; subsoil = 0

    double VG_alpha, VG_n, VG_m; // Van Genuchten parameters


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        
        // Calculate Van Genuchten parameters
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
        const double thetaS = par._ref_thetaS->val[j] + par._PTF_VG_clay->val[j] * clay - par._PTF_VG_Db->val[j] * bulk_density;

        // Calculate saturated hydraulic conductivity based on Cosby et al., (1984); https://doi.org/10.1029/WR020i006p00682
        // Additional flexibiltiy was given
        double Ks = par._PTF_Ks_slope->val[j] * exp10((par._PTF_Ks_const->val[j] + par._PTF_Ks_sand->val[j] * sand + par._PTF_Ks_clay->val[j] * clay)) * 1e-6;  // cm/day to m/s
        _Ks1->val[j] = min(Ks, 1.3e-7); // Ks > 1 mm/d

        // Calculate field capacity 
        // theta_r is set to 0.0
        if (opt_fieldcapacity == 1){  // Based on Van Genuchten model
            _thetaFC1->val[j] = thetaS / pow(1 + pow(VG_alpha * par._SWP->val[j], VG_n), VG_m);
        } else if (opt_fieldcapacity == 2) { // Based on Equation (7) in Twarakavi et al., (2007); https://doi.org/10.1029/2009WR007944
            _thetaFC1->val[j] = thetaS * pow(VG_n, -0.6 * (2 + log10(Ks * 8640000)));  // The unit of Ks in original formula is cm/day
        }
            
        // Calculate wilting point based on Van Genuchten model
        // theta_r is set to 0.0
        _thetaWP1->val[j] = thetaS / pow(1 + pow(VG_alpha * 15000, VG_n), VG_m);   
    }

    return EXIT_SUCCESS;
}