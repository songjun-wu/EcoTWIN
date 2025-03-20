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
    int reportTS(Control &ctrl, const grid *input, string varname, string filepath);
    int reportMap(Control &ctrl, const grid *input, string varname, string filepath);

};