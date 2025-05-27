/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ReportConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/




#include "Report.h"

Report::Report(Control &ctrl){
    
    _rowNum = ctrl._rowNum;
    _colNum = ctrl._colNum;
    _dx = ctrl._dx;
    _nodata = ctrl._nodata;

    advance_report = 0;

    Report_create_maps(ctrl);
    
}