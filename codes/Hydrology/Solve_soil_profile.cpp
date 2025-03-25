#include "Basin.h"

int Basin::Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm){

    int opt_pedotransf = ctrl.opt_pedotransf;
    int opt_fieldcapacity = ctrl.opt_fieldcapacity;

    // Calculate saturated hydraulic conductivity, field capacity, and wilting point
    if (opt_pedotransf == 1){  // Wosten et al., (1999)
        Soil_proporty_1(opt_pedotransf, opt_fieldcapacity, par);
    }
    
    else if (opt_pedotransf == 2){  // Wosten et al., (1997)
        Soil_proporty_2(opt_pedotransf, opt_fieldcapacity, par);
    }
    // Zacharias et al., (2007)
    else if (opt_pedotransf == 3){ // Zacharias et al., (2007)
        Soil_proporty_3(opt_pedotransf, opt_fieldcapacity, par);
    }
    


        //infiltration_1(ctrl, par);
        //Evapotranspiration_1(ctrl, par, atm, j);



    return EXIT_SUCCESS;
}
