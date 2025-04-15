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
    /* Report */
    ofstream of__I;  // Canopy storage [m]
    ofstream of__snow;  // Snow depth in [m]
    ofstream of__pond;  // Ponding water in [m]
    ofstream of__theta1;  // Soil moisture in layer 1 [decimal]
    ofstream of__theta2;  // Soil moisture in layer 2 [decimal]
    ofstream of__theta3;  // Soil moisture in layer 3 [decimal]
    ofstream of__GW;  // Groundwater storage [m]
    ofstream of__Th;  // Throughfall [m]
    ofstream of__snowmelt;  // Snow melt [m]
    ofstream of__infilt;  // Inflitration into soil layer 1 [m]
    ofstream of__Perc1;  // Percolation into layer 2 [m]
    ofstream of__Perc2;  // Percolation into layer 3 [m]
    ofstream of__Perc3;  // Percolation into gw reservior [m]
    ofstream of__rinfilt;  // Reinflitration into soil layer 1 [m]
    ofstream of__rPerc1;  // Repercolation into layer 2 [m]
    ofstream of__rPerc2;  // Repercolation into layer 3 [m]
    ofstream of__rPerc3;  // Repercolation into gw reservior [m]
    ofstream of__Ei;  // Canopy evaporation [m]
    ofstream of__Es;  // Soil evaporation [m]
    ofstream of__Tr;  // Total transpiration in three layers [m]
    ofstream of__Tr1;  // Transpiration in layer 1 [m]
    ofstream of__Tr2;  // Transpiration in layer 2 [m]
    ofstream of__Tr3;  // Transpiration in layer 3 [m]
    ofstream of__ovf_in;  // Overland flow from upstream cell(s) [m]
    ofstream of__ovf_out;  // Overland flow to downstream cell [m]
    ofstream of__ovf_toChn;  // Overland flow to Channel [m]
    ofstream of__interf_in;  // Interflow from upstream cell(s) [m]
    ofstream of__interf_out;  // Interflow to downstream cell [m]
    ofstream of__interf_toChn;  // Interflow to Channel [m]
    ofstream of__GWf_in;  // GW flow from upstream cell(s) [m]
    ofstream of__GWf_out;  // GW flow to downstream cell [m]
    ofstream of__GWf_toChn;  // Groundwater flow to Channel [m]
    ofstream of__Q;  // Discharge [m3/s]
    /* end of Report */

    //ctor
    Report(Control &ctrl);
    //dtor
    ~Report();  // destrcuctor of Basin
    int dtor(Control &ctrl);

    // report time series at gauging stations or maps
    int report(Control &ctrl, Basin &Bsn);
    int Report_Initialisation(Control &ctrl);
    
    int report_create(string fname, ofstream &ofHandle);
    int reportTS(Control &ctrl, const svector *input, ofstream &ofHandle);
    int reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, ofstream &ofHandle);

};