/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Report.h
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


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
    ofstream of__vadose;  // Vadose storage (unsaturated zone) [m]
    ofstream of__GW;  // Groundwater storage [m]
    ofstream of__chanS;  // Channel storage [m]
    ofstream of__Th;  // Throughfall [m]
    ofstream of__snowmelt;  // Snow melt [m]
    ofstream of__infilt;  // Inflitration into soil layer 1 [m]
    ofstream of__preferential_flow;  // Preferential flow to vadose storage due to exstenice of macropores in rock landscapes [m]
    ofstream of__Perc1;  // Percolation into layer 2 [m]
    ofstream of__Perc2;  // Percolation into layer 3 [m]
    ofstream of__Perc3;  // Percolation into vadose storage [m]
    ofstream of__Perc_vadose;  // Percolation from vadose storage into gw reservior [m]
    ofstream of__rinfilt;  // Reinflitration into soil layer 1 [m]
    ofstream of__rPerc1;  // Repercolation into layer 2 due to overland flow routing [m]
    ofstream of__rPerc2;  // Repercolation into layer 3 due to overland flow routing [m]
    ofstream of__rPerc3;  // Repercolation into gw reservior due to overland flow routing [m]
    ofstream of__rPerc_vadose;  // Repercolation from vadose storage into gw reservior [m]
    ofstream of__capillary_flow;  // Capillary flow from shallow GW zone to bottom soil layer [m]
    ofstream of__Ei;  // Canopy evaporation [m]
    ofstream of__Es;  // Soil evaporation [m]
    ofstream of__Tr;  // Total transpiration in three layers [m]
    ofstream of__Tr1;  // Transpiration in layer 1 [m]
    ofstream of__Tr2;  // Transpiration in layer 2 [m]
    ofstream of__Tr3;  // Transpiration in layer 3 [m]
    ofstream of__irrigation_from_river;  // Water extraction from river [m]
    ofstream of__irrigation_from_GW;  // Water extraction from GW [m]
    ofstream of__drainage_from_soil;  // Total drainage from all soil layers [m]
    ofstream of__drainage_from_layer1;  // Drainage from layer 1 [m]
    ofstream of__drainage_from_layer2;  // Drainage from layer 2 [m]
    ofstream of__drainage_from_layer3;  // Drainage from layer 3 [m]
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
    ofstream of__d18o_vadose;  // d18o in vadose storage [‰]
    ofstream of__d18o_GW;  // d18o in Groundwater storage [‰]
    ofstream of__d18o_chanS;  // d18o in Channel storage [‰]
    ofstream of__age_I;  // Cumulative age in Canopy storage [days]
    ofstream of__age_snow;  // Cumulative age in Snow depth in [days]
    ofstream of__age_pond;  // Cumulative age in Ponding water in [days]
    ofstream of__age_layer1;  // Cumulative age in Soil moisture in layer 1 [days]
    ofstream of__age_layer2;  // Cumulative age in Soil moisture in layer 2 [days]
    ofstream of__age_layer3;  // Cumulative age in Soil moisture in layer 3 [days]
    ofstream of__age_vadose;  // Cumulative age in vadose storage [‰]
    ofstream of__age_GW;  // Cumulative age in Groundwater storage [days]
    ofstream of__age_chanS;  // Cumulative age in Channel storage [days]
    ofstream of__trans_age_I;  // Transient age in Canopy storage [days]
    ofstream of__trans_age_snow;  // Transient age in Snow depth in [days]
    ofstream of__trans_age_pond;  // Transient age in Ponding water in [days]
    ofstream of__trans_age_layer1;  // Transient age in Soil moisture in layer 1 [days]
    ofstream of__trans_age_layer2;  // Transient age in Soil moisture in layer 2 [days]
    ofstream of__trans_age_layer3;  // Transient age in Soil moisture in layer 3 [days]
    ofstream of__trans_age_vadose;  // Transient age in vadose storage [‰]
    ofstream of__trans_age_GW;  // Transient age in Groundwater storage [days]
    ofstream of__trans_age_chanS;  // Transient age in Channel storage [days]
    ofstream of__NPP;  // Net primary production [gC/(m2*Ts)] 
    ofstream of__canopy_conductance;  // Stomatal conductance for whole canopy  [m s-1]
    ofstream of__plant_green_CP;  //  Carbon pool that contains carbon of the "green" or living parts of plants (leaves, fine roots, vascular tissues), except carbon stored as reserve  [gC/m2]
    ofstream of__plant_wood_CP;  //   Carbon pool that contains the carbon of the woody parts of plants (stems, branches, roots)  [gC/m2]
    ofstream of__plant_reserve_CP;  //  Carbon pool that contains the carbon stored in sugars and starches that the plants keep as an energy reserve (free of nitrogen)  [gC/m2]
    ofstream of__plant_C;  //  The total carbon content of plants (sum of green, wood, and reserve pool)  [gC/m2]
    ofstream of__acid_CP1_nonwood;  // Acid hydrolyzable carbon pool (non-wood) in layer 1
    ofstream of__ethanol_CP1_nonwood;  // Ethanol soluble carbon pool (non-wood) in layer 1
    ofstream of__nonsoluble_CP1_nonwood;  // Neither hydrolyzable nor soluble carbon pool (non-wood) in layer 1
    ofstream of__soluble_CP1_nonwood;  // Soluble carbon pool (non-wood) in layer 1
    ofstream of__acid_CP1_wood;  // Acid hydrolyzable carbon pool (wood) in layer 1
    ofstream of__ethanol_CP1_wood;  // Ethanol soluble carbon pool (wood) in layer 1
    ofstream of__nonsoluble_CP1_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 1
    ofstream of__soluble_CP1_wood;  // Soluble carbon pool (wood) in layer 1
    ofstream of__humus_CP1;  // Humus carbon pool (wood and non-wood) in layer 1
    ofstream of__acid_CP2_wood;  // Acid hydrolyzable carbon pool (wood) in layer 2
    ofstream of__ethanol_CP2_wood;  // Ethanol soluble carbon pool (wood) in layer 2
    ofstream of__nonsoluble_CP2_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 2
    ofstream of__soluble_CP2_wood;  // Soluble carbon pool (wood) in layer 2
    ofstream of__humus_CP2;  // Humus carbon pool (wood) in layer 2
    ofstream of__acid_CP3_wood;  // Acid hydrolyzable carbon pool (wood) in layer 3
    ofstream of__ethanol_CP3_wood;  // Ethanol soluble carbon pool (wood) in layer 3
    ofstream of__nonsoluble_CP3_wood;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 3
    ofstream of__soluble_CP3_wood;  // Soluble carbon pool (wood) in layer 3
    ofstream of__humus_CP3;  // Humus carbon pool (wood) in layer 3
    ofstream of__humus_C;  // Humus carbon storage in all soil layers [mgN/L*m = gN/m2]
    ofstream of__fast_C;  // Fast carbon storage in all soil layers [mgN/L*m = gN/m2]
    ofstream of__soluble_C;  // Soluble carbon storage in all soil layers [mgN/L*m = gN/m2]
    ofstream of__doc_I;  // DOC in Canopy storage [mgN/L]
    ofstream of__doc_snow;  // DOC in Snow depth in [mgN/L]
    ofstream of__doc_pond;  // DOC in Ponding water in [mgN/L]
    ofstream of__doc_layer1;  // DOC in Soil moisture in layer 1 [mgN/L]
    ofstream of__doc_layer2;  // DOC in Soil moisture in layer 2 [mgN/L]
    ofstream of__doc_layer3;  // DOC in Soil moisture in layer 3 [mgN/L]
    ofstream of__doc_vadose;  // DOC in vadose storage [mgN/L]
    ofstream of__doc_GW;  // DOC in Groundwater storage [mgN/L]
    ofstream of__doc_chanS;  // DOC in Channel storage [mgN/L]
    ofstream of__litter_fall_C;  // Litter fall summarised from green and reserve pool to non-wood litter pool, and wood pool to litter wood pool [gC/m2]
    ofstream of__soil_respiration_C;  // Soil respiration summarised in carbon [gC/m2]
    ofstream of__soil_decomposition_C;  // Soil decomposition summarised in carbon [gC/m2]
    ofstream of__respiration_river_C;  // Aquatic heterotrophic respiration summarised in carbon [gC/m2]
    ofstream of__C4_flag;  //  C4 dominant vegetaion? 0 - No (C3); 1 - Yes (C4)
    ofstream of__doc_rain;  // The organic carbon concentration in rain water [mgC/L], only needed when carbon_sim_1 = 1
    ofstream of__leaching_mass_doc;  // Leaching of DOC [gC/m2]
    ofstream of__drainage_mass_doc;  // Drainage of DOC [gC/m2]
    ofstream of__plant_mobile_N;  // Plant mobile nitrogen [mgN/L*m = gN/m2]
    ofstream of__no3_I;  // no3 in Canopy storage [mgN/L]
    ofstream of__no3_snow;  // no3 in Snow depth in [mgN/L]
    ofstream of__no3_pond;  // no3 in Ponding water in [mgN/L]
    ofstream of__no3_layer1;  // no3 in Soil moisture in layer 1 [mgN/L]
    ofstream of__no3_layer2;  // no3 in Soil moisture in layer 2 [mgN/L]
    ofstream of__no3_layer3;  // no3 in Soil moisture in layer 3 [mgN/L]
    ofstream of__no3_vadose;  // no3 in vadose storage [mgN/L]
    ofstream of__no3_GW;  // no3 in Groundwater storage [mgN/L]
    ofstream of__no3_chanS;  // no3 in Channel storage [mgN/L]
    ofstream of__nitrogen_add;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
    ofstream of__plant_uptake;  // Plant uptake [mgN/L*m = gN/m2]
    ofstream of__deni_soil;  // Soil denitrification [mgN/L*m = gN/m2]
    ofstream of__minerl_soil;  // Soil mineralisation (Soil decomposition may take additional nitorgen from dissolved inorganic nitrogen pool to build humus) [mgN/L*m = gN/m2]
    ofstream of__deni_river;  // Aquatic denitrification [mgN/L*m = gN/m2]
    ofstream of__fast_NP1_nonwood;  // Fast nonwood nitrogen storage in layer 1 (non-wood) [mgN/L*m = gN/m2]; needed as nitrogen carbon ratio of nonwood pools are variable due to reserve inputs
    ofstream of__fast_NP1;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    ofstream of__humus_N;  // Humus nitrogen storage in all soil layers [mgN/L*m = gN/m2]
    ofstream of__fast_N;  // Fast nitrogen storage in all soil layers [mgN/L*m = gN/m2]
    ofstream of__leaching_mass_no3;  // Leaching of NO3 [gN/m2]
    ofstream of__drainage_mass_no3;  // Drainage of NO3 [gN/m2]

    svector *_I_acc;  // Canopy storage [m]
    svector *_snow_acc;  // Snow depth in [m]
    svector *_pond_acc;  // Ponding water in [m]
    svector *_theta1_acc;  // Soil moisture in layer 1 [decimal]
    svector *_theta2_acc;  // Soil moisture in layer 2 [decimal]
    svector *_theta3_acc;  // Soil moisture in layer 3 [decimal]
    svector *_vadose_acc;  // Vadose storage (unsaturated zone) [m]
    svector *_GW_acc;  // Groundwater storage [m]
    svector *_chanS_acc;  // Channel storage [m]
    svector *_Th_acc;  // Throughfall [m]
    svector *_snowmelt_acc;  // Snow melt [m]
    svector *_infilt_acc;  // Inflitration into soil layer 1 [m]
    svector *_preferential_flow_acc;  // Preferential flow to vadose storage due to exstenice of macropores in rock landscapes [m]
    svector *_Perc1_acc;  // Percolation into layer 2 [m]
    svector *_Perc2_acc;  // Percolation into layer 3 [m]
    svector *_Perc3_acc;  // Percolation into vadose storage [m]
    svector *_Perc_vadose_acc;  // Percolation from vadose storage into gw reservior [m]
    svector *_rinfilt_acc;  // Reinflitration into soil layer 1 [m]
    svector *_rPerc1_acc;  // Repercolation into layer 2 due to overland flow routing [m]
    svector *_rPerc2_acc;  // Repercolation into layer 3 due to overland flow routing [m]
    svector *_rPerc3_acc;  // Repercolation into gw reservior due to overland flow routing [m]
    svector *_rPerc_vadose_acc;  // Repercolation from vadose storage into gw reservior [m]
    svector *_capillary_flow_acc;  // Capillary flow from shallow GW zone to bottom soil layer [m]
    svector *_Ei_acc;  // Canopy evaporation [m]
    svector *_Es_acc;  // Soil evaporation [m]
    svector *_Tr_acc;  // Total transpiration in three layers [m]
    svector *_Tr1_acc;  // Transpiration in layer 1 [m]
    svector *_Tr2_acc;  // Transpiration in layer 2 [m]
    svector *_Tr3_acc;  // Transpiration in layer 3 [m]
    svector *_irrigation_from_river_acc;  // Water extraction from river [m]
    svector *_irrigation_from_GW_acc;  // Water extraction from GW [m]
    svector *_drainage_from_soil_acc;  // Total drainage from all soil layers [m]
    svector *_drainage_from_layer1_acc;  // Drainage from layer 1 [m]
    svector *_drainage_from_layer2_acc;  // Drainage from layer 2 [m]
    svector *_drainage_from_layer3_acc;  // Drainage from layer 3 [m]
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
    svector *_d18o_vadose_acc;  // d18o in vadose storage [‰]
    svector *_d18o_GW_acc;  // d18o in Groundwater storage [‰]
    svector *_d18o_chanS_acc;  // d18o in Channel storage [‰]
    svector *_age_I_acc;  // Cumulative age in Canopy storage [days]
    svector *_age_snow_acc;  // Cumulative age in Snow depth in [days]
    svector *_age_pond_acc;  // Cumulative age in Ponding water in [days]
    svector *_age_layer1_acc;  // Cumulative age in Soil moisture in layer 1 [days]
    svector *_age_layer2_acc;  // Cumulative age in Soil moisture in layer 2 [days]
    svector *_age_layer3_acc;  // Cumulative age in Soil moisture in layer 3 [days]
    svector *_age_vadose_acc;  // Cumulative age in vadose storage [‰]
    svector *_age_GW_acc;  // Cumulative age in Groundwater storage [days]
    svector *_age_chanS_acc;  // Cumulative age in Channel storage [days]
    svector *_trans_age_I_acc;  // Transient age in Canopy storage [days]
    svector *_trans_age_snow_acc;  // Transient age in Snow depth in [days]
    svector *_trans_age_pond_acc;  // Transient age in Ponding water in [days]
    svector *_trans_age_layer1_acc;  // Transient age in Soil moisture in layer 1 [days]
    svector *_trans_age_layer2_acc;  // Transient age in Soil moisture in layer 2 [days]
    svector *_trans_age_layer3_acc;  // Transient age in Soil moisture in layer 3 [days]
    svector *_trans_age_vadose_acc;  // Transient age in vadose storage [‰]
    svector *_trans_age_GW_acc;  // Transient age in Groundwater storage [days]
    svector *_trans_age_chanS_acc;  // Transient age in Channel storage [days]
    svector *_NPP_acc;  // Net primary production [gC/(m2*Ts)] 
    svector *_canopy_conductance_acc;  // Stomatal conductance for whole canopy  [m s-1]
    svector *_plant_green_CP_acc;  //  Carbon pool that contains carbon of the "green" or living parts of plants (leaves, fine roots, vascular tissues), except carbon stored as reserve  [gC/m2]
    svector *_plant_wood_CP_acc;  //   Carbon pool that contains the carbon of the woody parts of plants (stems, branches, roots)  [gC/m2]
    svector *_plant_reserve_CP_acc;  //  Carbon pool that contains the carbon stored in sugars and starches that the plants keep as an energy reserve (free of nitrogen)  [gC/m2]
    svector *_plant_C_acc;  //  The total carbon content of plants (sum of green, wood, and reserve pool)  [gC/m2]
    svector *_acid_CP1_nonwood_acc;  // Acid hydrolyzable carbon pool (non-wood) in layer 1
    svector *_ethanol_CP1_nonwood_acc;  // Ethanol soluble carbon pool (non-wood) in layer 1
    svector *_nonsoluble_CP1_nonwood_acc;  // Neither hydrolyzable nor soluble carbon pool (non-wood) in layer 1
    svector *_soluble_CP1_nonwood_acc;  // Soluble carbon pool (non-wood) in layer 1
    svector *_acid_CP1_wood_acc;  // Acid hydrolyzable carbon pool (wood) in layer 1
    svector *_ethanol_CP1_wood_acc;  // Ethanol soluble carbon pool (wood) in layer 1
    svector *_nonsoluble_CP1_wood_acc;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 1
    svector *_soluble_CP1_wood_acc;  // Soluble carbon pool (wood) in layer 1
    svector *_humus_CP1_acc;  // Humus carbon pool (wood and non-wood) in layer 1
    svector *_acid_CP2_wood_acc;  // Acid hydrolyzable carbon pool (wood) in layer 2
    svector *_ethanol_CP2_wood_acc;  // Ethanol soluble carbon pool (wood) in layer 2
    svector *_nonsoluble_CP2_wood_acc;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 2
    svector *_soluble_CP2_wood_acc;  // Soluble carbon pool (wood) in layer 2
    svector *_humus_CP2_acc;  // Humus carbon pool (wood) in layer 2
    svector *_acid_CP3_wood_acc;  // Acid hydrolyzable carbon pool (wood) in layer 3
    svector *_ethanol_CP3_wood_acc;  // Ethanol soluble carbon pool (wood) in layer 3
    svector *_nonsoluble_CP3_wood_acc;  // Neither hydrolyzable nor soluble carbon pool (wood) in layer 3
    svector *_soluble_CP3_wood_acc;  // Soluble carbon pool (wood) in layer 3
    svector *_humus_CP3_acc;  // Humus carbon pool (wood) in layer 3
    svector *_humus_C_acc;  // Humus carbon storage in all soil layers [mgN/L*m = gN/m2]
    svector *_fast_C_acc;  // Fast carbon storage in all soil layers [mgN/L*m = gN/m2]
    svector *_soluble_C_acc;  // Soluble carbon storage in all soil layers [mgN/L*m = gN/m2]
    svector *_doc_I_acc;  // DOC in Canopy storage [mgN/L]
    svector *_doc_snow_acc;  // DOC in Snow depth in [mgN/L]
    svector *_doc_pond_acc;  // DOC in Ponding water in [mgN/L]
    svector *_doc_layer1_acc;  // DOC in Soil moisture in layer 1 [mgN/L]
    svector *_doc_layer2_acc;  // DOC in Soil moisture in layer 2 [mgN/L]
    svector *_doc_layer3_acc;  // DOC in Soil moisture in layer 3 [mgN/L]
    svector *_doc_vadose_acc;  // DOC in vadose storage [mgN/L]
    svector *_doc_GW_acc;  // DOC in Groundwater storage [mgN/L]
    svector *_doc_chanS_acc;  // DOC in Channel storage [mgN/L]
    svector *_litter_fall_C_acc;  // Litter fall summarised from green and reserve pool to non-wood litter pool, and wood pool to litter wood pool [gC/m2]
    svector *_soil_respiration_C_acc;  // Soil respiration summarised in carbon [gC/m2]
    svector *_soil_decomposition_C_acc;  // Soil decomposition summarised in carbon [gC/m2]
    svector *_respiration_river_C_acc;  // Aquatic heterotrophic respiration summarised in carbon [gC/m2]
    svector *_C4_flag_acc;  //  C4 dominant vegetaion? 0 - No (C3); 1 - Yes (C4)
    svector *_doc_rain_acc;  // The organic carbon concentration in rain water [mgC/L], only needed when carbon_sim_1 = 1
    svector *_leaching_mass_doc_acc;  // Leaching of DOC [gC/m2]
    svector *_drainage_mass_doc_acc;  // Drainage of DOC [gC/m2]
    svector *_plant_mobile_N_acc;  // Plant mobile nitrogen [mgN/L*m = gN/m2]
    svector *_no3_I_acc;  // no3 in Canopy storage [mgN/L]
    svector *_no3_snow_acc;  // no3 in Snow depth in [mgN/L]
    svector *_no3_pond_acc;  // no3 in Ponding water in [mgN/L]
    svector *_no3_layer1_acc;  // no3 in Soil moisture in layer 1 [mgN/L]
    svector *_no3_layer2_acc;  // no3 in Soil moisture in layer 2 [mgN/L]
    svector *_no3_layer3_acc;  // no3 in Soil moisture in layer 3 [mgN/L]
    svector *_no3_vadose_acc;  // no3 in vadose storage [mgN/L]
    svector *_no3_GW_acc;  // no3 in Groundwater storage [mgN/L]
    svector *_no3_chanS_acc;  // no3 in Channel storage [mgN/L]
    svector *_nitrogen_add_acc;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
    svector *_plant_uptake_acc;  // Plant uptake [mgN/L*m = gN/m2]
    svector *_deni_soil_acc;  // Soil denitrification [mgN/L*m = gN/m2]
    svector *_minerl_soil_acc;  // Soil mineralisation (Soil decomposition may take additional nitorgen from dissolved inorganic nitrogen pool to build humus) [mgN/L*m = gN/m2]
    svector *_deni_river_acc;  // Aquatic denitrification [mgN/L*m = gN/m2]
    svector *_fast_NP1_nonwood_acc;  // Fast nonwood nitrogen storage in layer 1 (non-wood) [mgN/L*m = gN/m2]; needed as nitrogen carbon ratio of nonwood pools are variable due to reserve inputs
    svector *_fast_NP1_acc;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
    svector *_humus_N_acc;  // Humus nitrogen storage in all soil layers [mgN/L*m = gN/m2]
    svector *_fast_N_acc;  // Fast nitrogen storage in all soil layers [mgN/L*m = gN/m2]
    svector *_leaching_mass_no3_acc;  // Leaching of NO3 [gN/m2]
    svector *_drainage_mass_no3_acc;  // Drainage of NO3 [gN/m2]
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