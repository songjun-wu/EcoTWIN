/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Sort_datetime.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Control.h"

time_t Control::Set_reference_timestep(){
    // Base date: 1900-01-01 00:00:00
    tm base_tm = {};
    base_tm.tm_year = 0;  // 1900
    base_tm.tm_mon = 0;   // January
    base_tm.tm_mday = 1;  // 1st
    base_tm.tm_hour = 0;
    base_tm.tm_min = 0;
    base_tm.tm_sec = 0;
    base_tm.tm_isdst = -1;

    time_t basetime = std::mktime(&base_tm);

    return basetime;
}

int Control::Get_year_month_day(){
    long seconds_since_1990 = Simul_start + current_ts;
    time_t target_time = basetime + static_cast<time_t>(seconds_since_1990);

    // Convert to UTC time structure
    current_time = gmtime(&target_time);

    year = current_time->tm_year + 1900;
    month = current_time->tm_mon + 1;
    day = current_time->tm_mday;
    day_of_year = current_time->tm_yday + 1;

    return EXIT_SUCCESS;
}


bool Control::is_next_month(){
    tm next_day = *current_time;
    next_day.tm_mday += 1;
    mktime(&next_day);
    return (next_day.tm_mon != current_time->tm_mon);
}

bool Control::is_next_year(){
    tm next_day = *current_time;
    next_day.tm_mday += 1;
    mktime(&next_day);
    return (next_day.tm_year != current_time->tm_year);
}