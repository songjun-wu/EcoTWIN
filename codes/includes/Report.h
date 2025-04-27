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
    int advance_report;
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
    ofstream of__rPerc1;  // Repercolation into layer 2 due to overland flow routing [m]
    ofstream of__rPerc2;  // Repercolation into layer 3 due to overland flow routing [m]
    ofstream of__rPerc3;  // Repercolation into gw reservior due to overland flow routing [m]
    ofstream of__rrPerc3;  // Repercolation into gw reservior due to interflow routing [m]
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
    ofstream of__Echan;  // Channel evaporation [m]
    ofstream of__d18o_I;  // d18o in Canopy storage [‰]
    ofstream of__d18o_snow;  // d18o in Snow depth in [‰]
    ofstream of__d18o_pond;  // d18o in Ponding water in [‰]
    ofstream of__d18o_layer1;  // d18o in Soil moisture in layer 1 [‰]
    ofstream of__d18o_layer2;  // d18o in Soil moisture in layer 2 [‰]
    ofstream of__d18o_layer3;  // d18o in Soil moisture in layer 3 [‰]
    ofstream of__d18o_GW;  // d18o in Groundwater storage [‰]
    ofstream of__d18o_chanS;  // d18o in Channel storage [‰]
    ofstream of__no3_I;  // no3 in Canopy storage [mgN/L]
    ofstream of__no3_snow;  // no3 in Snow depth in [mgN/L]
    ofstream of__no3_pond;  // no3 in Ponding water in [mgN/L]
    ofstream of__no3_layer1;  // no3 in Soil moisture in layer 1 [mgN/L]
    ofstream of__no3_layer2;  // no3 in Soil moisture in layer 2 [mgN/L]
    ofstream of__no3_layer3;  // no3 in Soil moisture in layer 3 [mgN/L]
    ofstream of__no3_GW;  // no3 in Groundwater storage [mgN/L]
    ofstream of__no3_chanS;  // no3 in Channel storage [mgN/L]
    ofstream of__nitrogen_add;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
    ofstream of__plant_uptake;  // Plant uptake [mgN/L*m = gN/m2]
    ofstream of__deni_soil;  // Soil denitrification [mgN/L*m = gN/m2]
    ofstream of__minerl_soil;  // Soil mineralisation [mgN/L*m = gN/m2]
    ofstream of__degrad_soil;  // Soil degradation [mgN/L*m = gN/m2]
    ofstream of__deni_river;  // Aquatic denitrification [mgN/L*m = gN/m2]
    ofstream of__humusN1;  // Humus nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    ofstream of__humusN2;  // Humus nitrogen storage in layer 2 [mgN/L*m = gN/m2]
    ofstream of__humusN3;  // Humus nitrogen storage in layer 3 [mgN/L*m = gN/m2]
    ofstream of__fastN1;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    ofstream of__fastN2;  // Fast nitrogen storage in layer 2 [mgN/L*m = gN/m2]
    ofstream of__fastN3;  // Fast nitrogen storage in layer 3 [mgN/L*m = gN/m2]

    svector *_I_acc;  // Canopy storage [m]
    svector *_snow_acc;  // Snow depth in [m]
    svector *_pond_acc;  // Ponding water in [m]
    svector *_theta1_acc;  // Soil moisture in layer 1 [decimal]
    svector *_theta2_acc;  // Soil moisture in layer 2 [decimal]
    svector *_theta3_acc;  // Soil moisture in layer 3 [decimal]
    svector *_GW_acc;  // Groundwater storage [m]
    svector *_Th_acc;  // Throughfall [m]
    svector *_snowmelt_acc;  // Snow melt [m]
    svector *_infilt_acc;  // Inflitration into soil layer 1 [m]
    svector *_Perc1_acc;  // Percolation into layer 2 [m]
    svector *_Perc2_acc;  // Percolation into layer 3 [m]
    svector *_Perc3_acc;  // Percolation into gw reservior [m]
    svector *_rinfilt_acc;  // Reinflitration into soil layer 1 [m]
    svector *_rPerc1_acc;  // Repercolation into layer 2 due to overland flow routing [m]
    svector *_rPerc2_acc;  // Repercolation into layer 3 due to overland flow routing [m]
    svector *_rPerc3_acc;  // Repercolation into gw reservior due to overland flow routing [m]
    svector *_rrPerc3_acc;  // Repercolation into gw reservior due to interflow routing [m]
    svector *_Ei_acc;  // Canopy evaporation [m]
    svector *_Es_acc;  // Soil evaporation [m]
    svector *_Tr_acc;  // Total transpiration in three layers [m]
    svector *_Tr1_acc;  // Transpiration in layer 1 [m]
    svector *_Tr2_acc;  // Transpiration in layer 2 [m]
    svector *_Tr3_acc;  // Transpiration in layer 3 [m]
    svector *_ovf_in_acc;  // Overland flow from upstream cell(s) [m]
    svector *_ovf_out_acc;  // Overland flow to downstream cell [m]
    svector *_ovf_toChn_acc;  // Overland flow to Channel [m]
    svector *_interf_in_acc;  // Interflow from upstream cell(s) [m]
    svector *_interf_out_acc;  // Interflow to downstream cell [m]
    svector *_interf_toChn_acc;  // Interflow to Channel [m]
    svector *_GWf_in_acc;  // GW flow from upstream cell(s) [m]
    svector *_GWf_out_acc;  // GW flow to downstream cell [m]
    svector *_GWf_toChn_acc;  // Groundwater flow to Channel [m]
    svector *_Q_acc;  // Discharge [m3/s]
    svector *_Echan_acc;  // Channel evaporation [m]
    svector *_d18o_I_acc;  // d18o in Canopy storage [‰]
    svector *_d18o_snow_acc;  // d18o in Snow depth in [‰]
    svector *_d18o_pond_acc;  // d18o in Ponding water in [‰]
    svector *_d18o_layer1_acc;  // d18o in Soil moisture in layer 1 [‰]
    svector *_d18o_layer2_acc;  // d18o in Soil moisture in layer 2 [‰]
    svector *_d18o_layer3_acc;  // d18o in Soil moisture in layer 3 [‰]
    svector *_d18o_GW_acc;  // d18o in Groundwater storage [‰]
    svector *_d18o_chanS_acc;  // d18o in Channel storage [‰]
    svector *_no3_I_acc;  // no3 in Canopy storage [mgN/L]
    svector *_no3_snow_acc;  // no3 in Snow depth in [mgN/L]
    svector *_no3_pond_acc;  // no3 in Ponding water in [mgN/L]
    svector *_no3_layer1_acc;  // no3 in Soil moisture in layer 1 [mgN/L]
    svector *_no3_layer2_acc;  // no3 in Soil moisture in layer 2 [mgN/L]
    svector *_no3_layer3_acc;  // no3 in Soil moisture in layer 3 [mgN/L]
    svector *_no3_GW_acc;  // no3 in Groundwater storage [mgN/L]
    svector *_no3_chanS_acc;  // no3 in Channel storage [mgN/L]
    svector *_nitrogen_add_acc;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
    svector *_plant_uptake_acc;  // Plant uptake [mgN/L*m = gN/m2]
    svector *_deni_soil_acc;  // Soil denitrification [mgN/L*m = gN/m2]
    svector *_minerl_soil_acc;  // Soil mineralisation [mgN/L*m = gN/m2]
    svector *_degrad_soil_acc;  // Soil degradation [mgN/L*m = gN/m2]
    svector *_deni_river_acc;  // Aquatic denitrification [mgN/L*m = gN/m2]
    svector *_humusN1_acc;  // Humus nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    svector *_humusN2_acc;  // Humus nitrogen storage in layer 2 [mgN/L*m = gN/m2]
    svector *_humusN3_acc;  // Humus nitrogen storage in layer 3 [mgN/L*m = gN/m2]
    svector *_fastN1_acc;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    svector *_fastN2_acc;  // Fast nitrogen storage in layer 2 [mgN/L*m = gN/m2]
    svector *_fastN3_acc;  // Fast nitrogen storage in layer 3 [mgN/L*m = gN/m2]
    /* end of Report */

    //ctor
    Report(Control &ctrl);
    //dtor
    ~Report();  // destrcuctor of Basin
    int dtor(Control &ctrl);

    // report time series at gauging stations or maps
    int Report_Initialisation(Control &ctrl);
    int Report_all(Control &ctrl, Basin &Bsn);
    
    int Report_create_maps(Control &ctrl);
    int Report_update_maps(Control &ctrl, Basin &Bsn);
    int Report_to_Ts(Control &ctrl, Basin &Bsn);
    int Report_to_maps(Control &ctrl);
    
    
    int report_create(string fname, ofstream &ofHandle);
    int reportTS(Control &ctrl, const svector *input, ofstream &ofHandle);
    int reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, ofstream &ofHandle);

};