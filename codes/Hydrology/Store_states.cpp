#include "Basin.h"


int Basin::Store_states() {
    
    _I_old->equals(*_I);
    _snow_old->equals(*_snow);   
    _theta1_old->equals(*_theta1);
    _theta2_old->equals(*_theta2);
    _theta3_old->equals(*_theta3);
    _GW_old->equals(*_GW);
    _chanS_old->equals(*_chanS);

    return EXIT_SUCCESS;
}