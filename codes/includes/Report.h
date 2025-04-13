#include "Basin.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Report {

    /* Properties */
    int _rowNum, _colNum;
    double _dx, _nodata;
    /* end of Properties */

    public:

    //ctor
    Report(Control &ctrl);

    // report time series at gauging stations or maps
    int report(Control &ctrl, Basin &Bsn);
    int Report_Initialisation(Control &ctrl);
    
    int report_create(string varname, string filepath, int Ts_or_map);
    int reportTS(Control &ctrl, const svector *input, string varname, string filepath);
    int reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, string varname, string filepath);

};