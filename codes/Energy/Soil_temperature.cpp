#include "Basin.h"

// Estimation of soil temperature from air temperature and LAI
// Amato and Gimenez, (2024). Predicting monthly near-surface soil temperature from air temperature and the leaf area index. Agricultural and Forest Meteorology. https://doi.org/10.1016/j.agrformet.2023.109838
double Basin::Get_soil_temperature(const double Ta, const double LAI){
    double Ts;
    if (Ta <= 0){
        Ts = 0.291 * Ta;
    } else {
        Ts = Ta * (0.885 + 0.326 * exp(-0.55 * LAI));
    }

    return Ts;
}
      

