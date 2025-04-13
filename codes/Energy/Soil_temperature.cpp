#include "Basin.h"

// Estimation of soil temperature from air temperature and LAI
// Amato and Gimenez, (2024). Predicting monthly near-surface soil temperature from air temperature and the leaf area index. Agricultural and Forest Meteorology. https://doi.org/10.1016/j.agrformet.2023.109838
int Basin::Get_soil_temperature(double &Ta, double &Ts, double &LAI){

    if (Ta <= 0){
        Ts = 0.291 * Ta;
    } else {
        Ts = Ta * (0.885 + 0.326 * exp(-0.55 * LAI));
    }

    return EXIT_SUCCESS;
}
      

