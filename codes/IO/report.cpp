/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* report.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Report.h"

int Report::Report_all(Control &ctrl, Basin &Bsn){

  // Updates maps for each timestep
  Report_update_maps(ctrl, Bsn);
  advance_report += ctrl.Simul_tstep;
  // Report to TS for each timestep
  Report_to_Ts(ctrl, Bsn);
  // Report to maps (daily, monthly, annually, or at specific interval)
  if (ctrl.Report_interval == -1){           // Report daily
    if (advance_report >= 86400) Report_to_maps(ctrl);
  } else if (ctrl.Report_interval == -2){    // Report monthly
    if (ctrl.is_next_month()) Report_to_maps(ctrl);
  } else if (ctrl.Report_interval == -3){    // Report annually
    if (ctrl.is_next_year()) Report_to_maps(ctrl);
  } else if (ctrl.Report_interval > 0){       // Report at at specific interval
    if (advance_report >= ctrl.Report_interval) Report_to_maps(ctrl);
  }
  return EXIT_SUCCESS;
}


int Report::Report_create_maps(Control &ctrl){
  /* Create maps */
  if (ctrl.report__I==2) _I_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__snow==2) _snow_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__pond==2) _pond_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__theta1==2) _theta1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__theta2==2) _theta2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__theta3==2) _theta3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__GW==2) _GW_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Th==2) _Th_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__snowmelt==2) _snowmelt_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__infilt==2) _infilt_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Perc1==2) _Perc1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Perc2==2) _Perc2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Perc3==2) _Perc3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__rinfilt==2) _rinfilt_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__rPerc1==2) _rPerc1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__rPerc2==2) _rPerc2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__rPerc3==2) _rPerc3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__rrPerc3==2) _rrPerc3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Ei==2) _Ei_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Es==2) _Es_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Tr==2) _Tr_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Tr1==2) _Tr1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Tr2==2) _Tr2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Tr3==2) _Tr3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__irrigation_from_river==2) _irrigation_from_river_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__irrigation_from_GW==2) _irrigation_from_GW_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__ovf_in==2) _ovf_in_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__ovf_out==2) _ovf_out_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__ovf_toChn==2) _ovf_toChn_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__interf_in==2) _interf_in_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__interf_out==2) _interf_out_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__interf_toChn==2) _interf_toChn_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__GWf_in==2) _GWf_in_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__GWf_out==2) _GWf_out_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__GWf_toChn==2) _GWf_toChn_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Q==2) _Q_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__Echan==2) _Echan_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_I==2) _d18o_I_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_snow==2) _d18o_snow_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_pond==2) _d18o_pond_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_layer1==2) _d18o_layer1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_layer2==2) _d18o_layer2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_layer3==2) _d18o_layer3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_GW==2) _d18o_GW_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__d18o_chanS==2) _d18o_chanS_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_I==2) _age_I_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_snow==2) _age_snow_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_pond==2) _age_pond_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_layer1==2) _age_layer1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_layer2==2) _age_layer2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_layer3==2) _age_layer3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_GW==2) _age_GW_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__age_chanS==2) _age_chanS_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_I==2) _no3_I_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_snow==2) _no3_snow_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_pond==2) _no3_pond_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_layer1==2) _no3_layer1_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_layer2==2) _no3_layer2_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_layer3==2) _no3_layer3_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_GW==2) _no3_GW_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__no3_chanS==2) _no3_chanS_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__nitrogen_add==2) _nitrogen_add_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__plant_uptake==2) _plant_uptake_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__deni_soil==2) _deni_soil_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__minerl_soil==2) _minerl_soil_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__degrad_soil==2) _degrad_soil_acc = new svector(ctrl._sortedGrid.size);
  if (ctrl.report__deni_river==2) _deni_river_acc = new svector(ctrl._sortedGrid.size);
  /* end of Create maps */
  return EXIT_SUCCESS;
}

int Report::Report_update_maps(Control &ctrl, Basin &Bsn){

  /* Update maps */
  if (ctrl.report__I==2) _I_acc->plus(*Bsn._I);
  if (ctrl.report__snow==2) _snow_acc->plus(*Bsn._snow);
  if (ctrl.report__pond==2) _pond_acc->plus(*Bsn._pond);
  if (ctrl.report__theta1==2) _theta1_acc->plus(*Bsn._theta1);
  if (ctrl.report__theta2==2) _theta2_acc->plus(*Bsn._theta2);
  if (ctrl.report__theta3==2) _theta3_acc->plus(*Bsn._theta3);
  if (ctrl.report__GW==2) _GW_acc->plus(*Bsn._GW);
  if (ctrl.report__Th==2) _Th_acc->plus(*Bsn._Th);
  if (ctrl.report__snowmelt==2) _snowmelt_acc->plus(*Bsn._snowmelt);
  if (ctrl.report__infilt==2) _infilt_acc->plus(*Bsn._infilt);
  if (ctrl.report__Perc1==2) _Perc1_acc->plus(*Bsn._Perc1);
  if (ctrl.report__Perc2==2) _Perc2_acc->plus(*Bsn._Perc2);
  if (ctrl.report__Perc3==2) _Perc3_acc->plus(*Bsn._Perc3);
  if (ctrl.report__rinfilt==2) _rinfilt_acc->plus(*Bsn._rinfilt);
  if (ctrl.report__rPerc1==2) _rPerc1_acc->plus(*Bsn._rPerc1);
  if (ctrl.report__rPerc2==2) _rPerc2_acc->plus(*Bsn._rPerc2);
  if (ctrl.report__rPerc3==2) _rPerc3_acc->plus(*Bsn._rPerc3);
  if (ctrl.report__rrPerc3==2) _rrPerc3_acc->plus(*Bsn._rrPerc3);
  if (ctrl.report__Ei==2) _Ei_acc->plus(*Bsn._Ei);
  if (ctrl.report__Es==2) _Es_acc->plus(*Bsn._Es);
  if (ctrl.report__Tr==2) _Tr_acc->plus(*Bsn._Tr);
  if (ctrl.report__Tr1==2) _Tr1_acc->plus(*Bsn._Tr1);
  if (ctrl.report__Tr2==2) _Tr2_acc->plus(*Bsn._Tr2);
  if (ctrl.report__Tr3==2) _Tr3_acc->plus(*Bsn._Tr3);
  if (ctrl.report__irrigation_from_river==2) _irrigation_from_river_acc->plus(*Bsn._irrigation_from_river);
  if (ctrl.report__irrigation_from_GW==2) _irrigation_from_GW_acc->plus(*Bsn._irrigation_from_GW);
  if (ctrl.report__ovf_in==2) _ovf_in_acc->plus(*Bsn._ovf_in);
  if (ctrl.report__ovf_out==2) _ovf_out_acc->plus(*Bsn._ovf_out);
  if (ctrl.report__ovf_toChn==2) _ovf_toChn_acc->plus(*Bsn._ovf_toChn);
  if (ctrl.report__interf_in==2) _interf_in_acc->plus(*Bsn._interf_in);
  if (ctrl.report__interf_out==2) _interf_out_acc->plus(*Bsn._interf_out);
  if (ctrl.report__interf_toChn==2) _interf_toChn_acc->plus(*Bsn._interf_toChn);
  if (ctrl.report__GWf_in==2) _GWf_in_acc->plus(*Bsn._GWf_in);
  if (ctrl.report__GWf_out==2) _GWf_out_acc->plus(*Bsn._GWf_out);
  if (ctrl.report__GWf_toChn==2) _GWf_toChn_acc->plus(*Bsn._GWf_toChn);
  if (ctrl.report__Q==2) _Q_acc->plus(*Bsn._Q);
  if (ctrl.report__Echan==2) _Echan_acc->plus(*Bsn._Echan);
  if (ctrl.report__d18o_I==2) _d18o_I_acc->plus(*Bsn._d18o_I);
  if (ctrl.report__d18o_snow==2) _d18o_snow_acc->plus(*Bsn._d18o_snow);
  if (ctrl.report__d18o_pond==2) _d18o_pond_acc->plus(*Bsn._d18o_pond);
  if (ctrl.report__d18o_layer1==2) _d18o_layer1_acc->plus(*Bsn._d18o_layer1);
  if (ctrl.report__d18o_layer2==2) _d18o_layer2_acc->plus(*Bsn._d18o_layer2);
  if (ctrl.report__d18o_layer3==2) _d18o_layer3_acc->plus(*Bsn._d18o_layer3);
  if (ctrl.report__d18o_GW==2) _d18o_GW_acc->plus(*Bsn._d18o_GW);
  if (ctrl.report__d18o_chanS==2) _d18o_chanS_acc->plus(*Bsn._d18o_chanS);
  if (ctrl.report__age_I==2) _age_I_acc->plus(*Bsn._age_I);
  if (ctrl.report__age_snow==2) _age_snow_acc->plus(*Bsn._age_snow);
  if (ctrl.report__age_pond==2) _age_pond_acc->plus(*Bsn._age_pond);
  if (ctrl.report__age_layer1==2) _age_layer1_acc->plus(*Bsn._age_layer1);
  if (ctrl.report__age_layer2==2) _age_layer2_acc->plus(*Bsn._age_layer2);
  if (ctrl.report__age_layer3==2) _age_layer3_acc->plus(*Bsn._age_layer3);
  if (ctrl.report__age_GW==2) _age_GW_acc->plus(*Bsn._age_GW);
  if (ctrl.report__age_chanS==2) _age_chanS_acc->plus(*Bsn._age_chanS);
  if (ctrl.report__no3_I==2) _no3_I_acc->plus(*Bsn._no3_I);
  if (ctrl.report__no3_snow==2) _no3_snow_acc->plus(*Bsn._no3_snow);
  if (ctrl.report__no3_pond==2) _no3_pond_acc->plus(*Bsn._no3_pond);
  if (ctrl.report__no3_layer1==2) _no3_layer1_acc->plus(*Bsn._no3_layer1);
  if (ctrl.report__no3_layer2==2) _no3_layer2_acc->plus(*Bsn._no3_layer2);
  if (ctrl.report__no3_layer3==2) _no3_layer3_acc->plus(*Bsn._no3_layer3);
  if (ctrl.report__no3_GW==2) _no3_GW_acc->plus(*Bsn._no3_GW);
  if (ctrl.report__no3_chanS==2) _no3_chanS_acc->plus(*Bsn._no3_chanS);
  if (ctrl.report__nitrogen_add==2) _nitrogen_add_acc->plus(*Bsn._nitrogen_add);
  if (ctrl.report__plant_uptake==2) _plant_uptake_acc->plus(*Bsn._plant_uptake);
  if (ctrl.report__deni_soil==2) _deni_soil_acc->plus(*Bsn._deni_soil);
  if (ctrl.report__minerl_soil==2) _minerl_soil_acc->plus(*Bsn._minerl_soil);
  if (ctrl.report__degrad_soil==2) _degrad_soil_acc->plus(*Bsn._degrad_soil);
  if (ctrl.report__deni_river==2) _deni_river_acc->plus(*Bsn._deni_river);
  /* end of Update maps */
  
  return EXIT_SUCCESS;
}

int Report::Report_Initialisation(Control &ctrl){
  /* Init Report */
  // Create files for report
  if (ctrl.report__I==1)  report_create(ctrl.path_ResultsFolder+"canopy_storage_TS.bin", of__I);
  else if (ctrl.report__I==2)  report_create(ctrl.path_ResultsFolder+"canopy_storage_map.bin", of__I);

  if (ctrl.report__snow==1)  report_create(ctrl.path_ResultsFolder+"snow_depth_TS.bin", of__snow);
  else if (ctrl.report__snow==2)  report_create(ctrl.path_ResultsFolder+"snow_depth_map.bin", of__snow);

  if (ctrl.report__pond==1)  report_create(ctrl.path_ResultsFolder+"pond_TS.bin", of__pond);
  else if (ctrl.report__pond==2)  report_create(ctrl.path_ResultsFolder+"pond_map.bin", of__pond);

  if (ctrl.report__theta1==1)  report_create(ctrl.path_ResultsFolder+"SMC_layer1_TS.bin", of__theta1);
  else if (ctrl.report__theta1==2)  report_create(ctrl.path_ResultsFolder+"SMC_layer1_map.bin", of__theta1);

  if (ctrl.report__theta2==1)  report_create(ctrl.path_ResultsFolder+"SMC_layer2_TS.bin", of__theta2);
  else if (ctrl.report__theta2==2)  report_create(ctrl.path_ResultsFolder+"SMC_layer2_map.bin", of__theta2);

  if (ctrl.report__theta3==1)  report_create(ctrl.path_ResultsFolder+"SMC_layer3_TS.bin", of__theta3);
  else if (ctrl.report__theta3==2)  report_create(ctrl.path_ResultsFolder+"SMC_layer3_map.bin", of__theta3);

  if (ctrl.report__GW==1)  report_create(ctrl.path_ResultsFolder+"groundwater_storage_TS.bin", of__GW);
  else if (ctrl.report__GW==2)  report_create(ctrl.path_ResultsFolder+"groundwater_storage_map.bin", of__GW);

  if (ctrl.report__Th==1)  report_create(ctrl.path_ResultsFolder+"throufall_TS.bin", of__Th);
  else if (ctrl.report__Th==2)  report_create(ctrl.path_ResultsFolder+"throufall_map.bin", of__Th);

  if (ctrl.report__snowmelt==1)  report_create(ctrl.path_ResultsFolder+"snowmelt_TS.bin", of__snowmelt);
  else if (ctrl.report__snowmelt==2)  report_create(ctrl.path_ResultsFolder+"snowmelt_map.bin", of__snowmelt);

  if (ctrl.report__infilt==1)  report_create(ctrl.path_ResultsFolder+"infiltration_TS.bin", of__infilt);
  else if (ctrl.report__infilt==2)  report_create(ctrl.path_ResultsFolder+"infiltration_map.bin", of__infilt);

  if (ctrl.report__Perc1==1)  report_create(ctrl.path_ResultsFolder+"perc_layer1_TS.bin", of__Perc1);
  else if (ctrl.report__Perc1==2)  report_create(ctrl.path_ResultsFolder+"perc_layer1_map.bin", of__Perc1);

  if (ctrl.report__Perc2==1)  report_create(ctrl.path_ResultsFolder+"perc_layer2_TS.bin", of__Perc2);
  else if (ctrl.report__Perc2==2)  report_create(ctrl.path_ResultsFolder+"perc_layer2_map.bin", of__Perc2);

  if (ctrl.report__Perc3==1)  report_create(ctrl.path_ResultsFolder+"perc_layer3_TS.bin", of__Perc3);
  else if (ctrl.report__Perc3==2)  report_create(ctrl.path_ResultsFolder+"perc_layer3_map.bin", of__Perc3);

  if (ctrl.report__rinfilt==1)  report_create(ctrl.path_ResultsFolder+"rinfiltration_TS.bin", of__rinfilt);
  else if (ctrl.report__rinfilt==2)  report_create(ctrl.path_ResultsFolder+"rinfiltration_map.bin", of__rinfilt);

  if (ctrl.report__rPerc1==1)  report_create(ctrl.path_ResultsFolder+"rperc_layer1_TS.bin", of__rPerc1);
  else if (ctrl.report__rPerc1==2)  report_create(ctrl.path_ResultsFolder+"rperc_layer1_map.bin", of__rPerc1);

  if (ctrl.report__rPerc2==1)  report_create(ctrl.path_ResultsFolder+"rperc_layer2_TS.bin", of__rPerc2);
  else if (ctrl.report__rPerc2==2)  report_create(ctrl.path_ResultsFolder+"rperc_layer2_map.bin", of__rPerc2);

  if (ctrl.report__rPerc3==1)  report_create(ctrl.path_ResultsFolder+"rperc_layer3_TS.bin", of__rPerc3);
  else if (ctrl.report__rPerc3==2)  report_create(ctrl.path_ResultsFolder+"rperc_layer3_map.bin", of__rPerc3);

  if (ctrl.report__rrPerc3==1)  report_create(ctrl.path_ResultsFolder+"rrperc_layer3_TS.bin", of__rrPerc3);
  else if (ctrl.report__rrPerc3==2)  report_create(ctrl.path_ResultsFolder+"rrperc_layer3_map.bin", of__rrPerc3);

  if (ctrl.report__Ei==1)  report_create(ctrl.path_ResultsFolder+"canopy_evap_TS.bin", of__Ei);
  else if (ctrl.report__Ei==2)  report_create(ctrl.path_ResultsFolder+"canopy_evap_map.bin", of__Ei);

  if (ctrl.report__Es==1)  report_create(ctrl.path_ResultsFolder+"soil_evap_TS.bin", of__Es);
  else if (ctrl.report__Es==2)  report_create(ctrl.path_ResultsFolder+"soil_evap_map.bin", of__Es);

  if (ctrl.report__Tr==1)  report_create(ctrl.path_ResultsFolder+"transp_TS.bin", of__Tr);
  else if (ctrl.report__Tr==2)  report_create(ctrl.path_ResultsFolder+"transp_map.bin", of__Tr);

  if (ctrl.report__Tr1==1)  report_create(ctrl.path_ResultsFolder+"transp_layer1_TS.bin", of__Tr1);
  else if (ctrl.report__Tr1==2)  report_create(ctrl.path_ResultsFolder+"transp_layer1_map.bin", of__Tr1);

  if (ctrl.report__Tr2==1)  report_create(ctrl.path_ResultsFolder+"transp_layer2_TS.bin", of__Tr2);
  else if (ctrl.report__Tr2==2)  report_create(ctrl.path_ResultsFolder+"transp_layer2_map.bin", of__Tr2);

  if (ctrl.report__Tr3==1)  report_create(ctrl.path_ResultsFolder+"transp_layer3_TS.bin", of__Tr3);
  else if (ctrl.report__Tr3==2)  report_create(ctrl.path_ResultsFolder+"transp_layer3_map.bin", of__Tr3);

  if (ctrl.report__irrigation_from_river==1)  report_create(ctrl.path_ResultsFolder+"irrigation_from_river_TS.bin", of__irrigation_from_river);
  else if (ctrl.report__irrigation_from_river==2)  report_create(ctrl.path_ResultsFolder+"irrigation_from_river_map.bin", of__irrigation_from_river);

  if (ctrl.report__irrigation_from_GW==1)  report_create(ctrl.path_ResultsFolder+"irrigation_from_GW_TS.bin", of__irrigation_from_GW);
  else if (ctrl.report__irrigation_from_GW==2)  report_create(ctrl.path_ResultsFolder+"irrigation_from_GW_map.bin", of__irrigation_from_GW);

  if (ctrl.report__ovf_in==1)  report_create(ctrl.path_ResultsFolder+"overland_flow_input_TS.bin", of__ovf_in);
  else if (ctrl.report__ovf_in==2)  report_create(ctrl.path_ResultsFolder+"overland_flow_input_map.bin", of__ovf_in);

  if (ctrl.report__ovf_out==1)  report_create(ctrl.path_ResultsFolder+"overland_flow_output_TS.bin", of__ovf_out);
  else if (ctrl.report__ovf_out==2)  report_create(ctrl.path_ResultsFolder+"overland_flow_output_map.bin", of__ovf_out);

  if (ctrl.report__ovf_toChn==1)  report_create(ctrl.path_ResultsFolder+"overland_flow_toChn_TS.bin", of__ovf_toChn);
  else if (ctrl.report__ovf_toChn==2)  report_create(ctrl.path_ResultsFolder+"overland_flow_toChn_map.bin", of__ovf_toChn);

  if (ctrl.report__interf_in==1)  report_create(ctrl.path_ResultsFolder+"interflow_input_TS.bin", of__interf_in);
  else if (ctrl.report__interf_in==2)  report_create(ctrl.path_ResultsFolder+"interflow_input_map.bin", of__interf_in);

  if (ctrl.report__interf_out==1)  report_create(ctrl.path_ResultsFolder+"interflow_output_TS.bin", of__interf_out);
  else if (ctrl.report__interf_out==2)  report_create(ctrl.path_ResultsFolder+"interflow_output_map.bin", of__interf_out);

  if (ctrl.report__interf_toChn==1)  report_create(ctrl.path_ResultsFolder+"interflow_toChn_TS.bin", of__interf_toChn);
  else if (ctrl.report__interf_toChn==2)  report_create(ctrl.path_ResultsFolder+"interflow_toChn_map.bin", of__interf_toChn);

  if (ctrl.report__GWf_in==1)  report_create(ctrl.path_ResultsFolder+"GWflow_input_TS.bin", of__GWf_in);
  else if (ctrl.report__GWf_in==2)  report_create(ctrl.path_ResultsFolder+"GWflow_input_map.bin", of__GWf_in);

  if (ctrl.report__GWf_out==1)  report_create(ctrl.path_ResultsFolder+"GWflow_output_TS.bin", of__GWf_out);
  else if (ctrl.report__GWf_out==2)  report_create(ctrl.path_ResultsFolder+"GWflow_output_map.bin", of__GWf_out);

  if (ctrl.report__GWf_toChn==1)  report_create(ctrl.path_ResultsFolder+"GWflow_toChn_TS.bin", of__GWf_toChn);
  else if (ctrl.report__GWf_toChn==2)  report_create(ctrl.path_ResultsFolder+"GWflow_toChn_map.bin", of__GWf_toChn);

  if (ctrl.report__Q==1)  report_create(ctrl.path_ResultsFolder+"discharge_TS.bin", of__Q);
  else if (ctrl.report__Q==2)  report_create(ctrl.path_ResultsFolder+"discharge_map.bin", of__Q);

  if (ctrl.report__Echan==1)  report_create(ctrl.path_ResultsFolder+"channel_evaporation_TS.bin", of__Echan);
  else if (ctrl.report__Echan==2)  report_create(ctrl.path_ResultsFolder+"channel_evaporation_map.bin", of__Echan);

  if (ctrl.report__d18o_I==1)  report_create(ctrl.path_ResultsFolder+"d18o_canopy_storage_TS.bin", of__d18o_I);
  else if (ctrl.report__d18o_I==2)  report_create(ctrl.path_ResultsFolder+"d18o_canopy_storage_map.bin", of__d18o_I);

  if (ctrl.report__d18o_snow==1)  report_create(ctrl.path_ResultsFolder+"d18o_snow_depth_TS.bin", of__d18o_snow);
  else if (ctrl.report__d18o_snow==2)  report_create(ctrl.path_ResultsFolder+"d18o_snow_depth_map.bin", of__d18o_snow);

  if (ctrl.report__d18o_pond==1)  report_create(ctrl.path_ResultsFolder+"d18o_pond_TS.bin", of__d18o_pond);
  else if (ctrl.report__d18o_pond==2)  report_create(ctrl.path_ResultsFolder+"d18o_pond_map.bin", of__d18o_pond);

  if (ctrl.report__d18o_layer1==1)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer1_TS.bin", of__d18o_layer1);
  else if (ctrl.report__d18o_layer1==2)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer1_map.bin", of__d18o_layer1);

  if (ctrl.report__d18o_layer2==1)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer2_TS.bin", of__d18o_layer2);
  else if (ctrl.report__d18o_layer2==2)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer2_map.bin", of__d18o_layer2);

  if (ctrl.report__d18o_layer3==1)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer3_TS.bin", of__d18o_layer3);
  else if (ctrl.report__d18o_layer3==2)  report_create(ctrl.path_ResultsFolder+"d18o_SMC_layer3_map.bin", of__d18o_layer3);

  if (ctrl.report__d18o_GW==1)  report_create(ctrl.path_ResultsFolder+"d18o_groundwater_storage_TS.bin", of__d18o_GW);
  else if (ctrl.report__d18o_GW==2)  report_create(ctrl.path_ResultsFolder+"d18o_groundwater_storage_map.bin", of__d18o_GW);

  if (ctrl.report__d18o_chanS==1)  report_create(ctrl.path_ResultsFolder+"d18o_chanS_TS.bin", of__d18o_chanS);
  else if (ctrl.report__d18o_chanS==2)  report_create(ctrl.path_ResultsFolder+"d18o_chanS_map.bin", of__d18o_chanS);

  if (ctrl.report__age_I==1)  report_create(ctrl.path_ResultsFolder+"age_canopy_storage_TS.bin", of__age_I);
  else if (ctrl.report__age_I==2)  report_create(ctrl.path_ResultsFolder+"age_canopy_storage_map.bin", of__age_I);

  if (ctrl.report__age_snow==1)  report_create(ctrl.path_ResultsFolder+"age_snow_depth_TS.bin", of__age_snow);
  else if (ctrl.report__age_snow==2)  report_create(ctrl.path_ResultsFolder+"age_snow_depth_map.bin", of__age_snow);

  if (ctrl.report__age_pond==1)  report_create(ctrl.path_ResultsFolder+"age_pond_TS.bin", of__age_pond);
  else if (ctrl.report__age_pond==2)  report_create(ctrl.path_ResultsFolder+"age_pond_map.bin", of__age_pond);

  if (ctrl.report__age_layer1==1)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer1_TS.bin", of__age_layer1);
  else if (ctrl.report__age_layer1==2)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer1_map.bin", of__age_layer1);

  if (ctrl.report__age_layer2==1)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer2_TS.bin", of__age_layer2);
  else if (ctrl.report__age_layer2==2)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer2_map.bin", of__age_layer2);

  if (ctrl.report__age_layer3==1)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer3_TS.bin", of__age_layer3);
  else if (ctrl.report__age_layer3==2)  report_create(ctrl.path_ResultsFolder+"age_SMC_layer3_map.bin", of__age_layer3);

  if (ctrl.report__age_GW==1)  report_create(ctrl.path_ResultsFolder+"age_groundwater_storage_TS.bin", of__age_GW);
  else if (ctrl.report__age_GW==2)  report_create(ctrl.path_ResultsFolder+"age_groundwater_storage_map.bin", of__age_GW);

  if (ctrl.report__age_chanS==1)  report_create(ctrl.path_ResultsFolder+"age_chanS_TS.bin", of__age_chanS);
  else if (ctrl.report__age_chanS==2)  report_create(ctrl.path_ResultsFolder+"age_chanS_map.bin", of__age_chanS);

  if (ctrl.report__no3_I==1)  report_create(ctrl.path_ResultsFolder+"no3_canopy_storage_TS.bin", of__no3_I);
  else if (ctrl.report__no3_I==2)  report_create(ctrl.path_ResultsFolder+"no3_canopy_storage_map.bin", of__no3_I);

  if (ctrl.report__no3_snow==1)  report_create(ctrl.path_ResultsFolder+"no3_snow_depth_TS.bin", of__no3_snow);
  else if (ctrl.report__no3_snow==2)  report_create(ctrl.path_ResultsFolder+"no3_snow_depth_map.bin", of__no3_snow);

  if (ctrl.report__no3_pond==1)  report_create(ctrl.path_ResultsFolder+"no3_pond_TS.bin", of__no3_pond);
  else if (ctrl.report__no3_pond==2)  report_create(ctrl.path_ResultsFolder+"no3_pond_map.bin", of__no3_pond);

  if (ctrl.report__no3_layer1==1)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer1_TS.bin", of__no3_layer1);
  else if (ctrl.report__no3_layer1==2)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer1_map.bin", of__no3_layer1);

  if (ctrl.report__no3_layer2==1)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer2_TS.bin", of__no3_layer2);
  else if (ctrl.report__no3_layer2==2)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer2_map.bin", of__no3_layer2);

  if (ctrl.report__no3_layer3==1)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer3_TS.bin", of__no3_layer3);
  else if (ctrl.report__no3_layer3==2)  report_create(ctrl.path_ResultsFolder+"no3_SMC_layer3_map.bin", of__no3_layer3);

  if (ctrl.report__no3_GW==1)  report_create(ctrl.path_ResultsFolder+"no3_groundwater_storage_TS.bin", of__no3_GW);
  else if (ctrl.report__no3_GW==2)  report_create(ctrl.path_ResultsFolder+"no3_groundwater_storage_map.bin", of__no3_GW);

  if (ctrl.report__no3_chanS==1)  report_create(ctrl.path_ResultsFolder+"no3_chanS_TS.bin", of__no3_chanS);
  else if (ctrl.report__no3_chanS==2)  report_create(ctrl.path_ResultsFolder+"no3_chanS_map.bin", of__no3_chanS);

  if (ctrl.report__nitrogen_add==1)  report_create(ctrl.path_ResultsFolder+"nitrogen_addition_TS.bin", of__nitrogen_add);
  else if (ctrl.report__nitrogen_add==2)  report_create(ctrl.path_ResultsFolder+"nitrogen_addition_map.bin", of__nitrogen_add);

  if (ctrl.report__plant_uptake==1)  report_create(ctrl.path_ResultsFolder+"plant_uptake_TS.bin", of__plant_uptake);
  else if (ctrl.report__plant_uptake==2)  report_create(ctrl.path_ResultsFolder+"plant_uptake_map.bin", of__plant_uptake);

  if (ctrl.report__deni_soil==1)  report_create(ctrl.path_ResultsFolder+"deni_soil_TS.bin", of__deni_soil);
  else if (ctrl.report__deni_soil==2)  report_create(ctrl.path_ResultsFolder+"deni_soil_map.bin", of__deni_soil);

  if (ctrl.report__minerl_soil==1)  report_create(ctrl.path_ResultsFolder+"minerl_soil_TS.bin", of__minerl_soil);
  else if (ctrl.report__minerl_soil==2)  report_create(ctrl.path_ResultsFolder+"minerl_soil_map.bin", of__minerl_soil);

  if (ctrl.report__degrad_soil==1)  report_create(ctrl.path_ResultsFolder+"degrad_soil_TS.bin", of__degrad_soil);
  else if (ctrl.report__degrad_soil==2)  report_create(ctrl.path_ResultsFolder+"degrad_soil_map.bin", of__degrad_soil);

  if (ctrl.report__deni_river==1)  report_create(ctrl.path_ResultsFolder+"deni_river_TS.bin", of__deni_river);
  else if (ctrl.report__deni_river==2)  report_create(ctrl.path_ResultsFolder+"deni_river_map.bin", of__deni_river);

  /* end of Init Report */
  return EXIT_SUCCESS;
}







int Report::Report_to_Ts(Control &ctrl, Basin &Bsn){
  
  /* Report to time series */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==1) {reportTS(ctrl, Bsn._I, of__I);}
  if (ctrl.report__snow==1) {reportTS(ctrl, Bsn._snow, of__snow);}
  if (ctrl.report__pond==1) {reportTS(ctrl, Bsn._pond, of__pond);}
  if (ctrl.report__theta1==1) {reportTS(ctrl, Bsn._theta1, of__theta1);}
  if (ctrl.report__theta2==1) {reportTS(ctrl, Bsn._theta2, of__theta2);}
  if (ctrl.report__theta3==1) {reportTS(ctrl, Bsn._theta3, of__theta3);}
  if (ctrl.report__GW==1) {reportTS(ctrl, Bsn._GW, of__GW);}
  if (ctrl.report__Th==1) {reportTS(ctrl, Bsn._Th, of__Th);}
  if (ctrl.report__snowmelt==1) {reportTS(ctrl, Bsn._snowmelt, of__snowmelt);}
  if (ctrl.report__infilt==1) {reportTS(ctrl, Bsn._infilt, of__infilt);}
  if (ctrl.report__Perc1==1) {reportTS(ctrl, Bsn._Perc1, of__Perc1);}
  if (ctrl.report__Perc2==1) {reportTS(ctrl, Bsn._Perc2, of__Perc2);}
  if (ctrl.report__Perc3==1) {reportTS(ctrl, Bsn._Perc3, of__Perc3);}
  if (ctrl.report__rinfilt==1) {reportTS(ctrl, Bsn._rinfilt, of__rinfilt);}
  if (ctrl.report__rPerc1==1) {reportTS(ctrl, Bsn._rPerc1, of__rPerc1);}
  if (ctrl.report__rPerc2==1) {reportTS(ctrl, Bsn._rPerc2, of__rPerc2);}
  if (ctrl.report__rPerc3==1) {reportTS(ctrl, Bsn._rPerc3, of__rPerc3);}
  if (ctrl.report__rrPerc3==1) {reportTS(ctrl, Bsn._rrPerc3, of__rrPerc3);}
  if (ctrl.report__Ei==1) {reportTS(ctrl, Bsn._Ei, of__Ei);}
  if (ctrl.report__Es==1) {reportTS(ctrl, Bsn._Es, of__Es);}
  if (ctrl.report__Tr==1) {reportTS(ctrl, Bsn._Tr, of__Tr);}
  if (ctrl.report__Tr1==1) {reportTS(ctrl, Bsn._Tr1, of__Tr1);}
  if (ctrl.report__Tr2==1) {reportTS(ctrl, Bsn._Tr2, of__Tr2);}
  if (ctrl.report__Tr3==1) {reportTS(ctrl, Bsn._Tr3, of__Tr3);}
  if (ctrl.report__irrigation_from_river==1) {reportTS(ctrl, Bsn._irrigation_from_river, of__irrigation_from_river);}
  if (ctrl.report__irrigation_from_GW==1) {reportTS(ctrl, Bsn._irrigation_from_GW, of__irrigation_from_GW);}
  if (ctrl.report__ovf_in==1) {reportTS(ctrl, Bsn._ovf_in, of__ovf_in);}
  if (ctrl.report__ovf_out==1) {reportTS(ctrl, Bsn._ovf_out, of__ovf_out);}
  if (ctrl.report__ovf_toChn==1) {reportTS(ctrl, Bsn._ovf_toChn, of__ovf_toChn);}
  if (ctrl.report__interf_in==1) {reportTS(ctrl, Bsn._interf_in, of__interf_in);}
  if (ctrl.report__interf_out==1) {reportTS(ctrl, Bsn._interf_out, of__interf_out);}
  if (ctrl.report__interf_toChn==1) {reportTS(ctrl, Bsn._interf_toChn, of__interf_toChn);}
  if (ctrl.report__GWf_in==1) {reportTS(ctrl, Bsn._GWf_in, of__GWf_in);}
  if (ctrl.report__GWf_out==1) {reportTS(ctrl, Bsn._GWf_out, of__GWf_out);}
  if (ctrl.report__GWf_toChn==1) {reportTS(ctrl, Bsn._GWf_toChn, of__GWf_toChn);}
  if (ctrl.report__Q==1) {reportTS(ctrl, Bsn._Q, of__Q);}
  if (ctrl.report__Echan==1) {reportTS(ctrl, Bsn._Echan, of__Echan);}
  if (ctrl.report__d18o_I==1) {reportTS(ctrl, Bsn._d18o_I, of__d18o_I);}
  if (ctrl.report__d18o_snow==1) {reportTS(ctrl, Bsn._d18o_snow, of__d18o_snow);}
  if (ctrl.report__d18o_pond==1) {reportTS(ctrl, Bsn._d18o_pond, of__d18o_pond);}
  if (ctrl.report__d18o_layer1==1) {reportTS(ctrl, Bsn._d18o_layer1, of__d18o_layer1);}
  if (ctrl.report__d18o_layer2==1) {reportTS(ctrl, Bsn._d18o_layer2, of__d18o_layer2);}
  if (ctrl.report__d18o_layer3==1) {reportTS(ctrl, Bsn._d18o_layer3, of__d18o_layer3);}
  if (ctrl.report__d18o_GW==1) {reportTS(ctrl, Bsn._d18o_GW, of__d18o_GW);}
  if (ctrl.report__d18o_chanS==1) {reportTS(ctrl, Bsn._d18o_chanS, of__d18o_chanS);}
  if (ctrl.report__age_I==1) {reportTS(ctrl, Bsn._age_I, of__age_I);}
  if (ctrl.report__age_snow==1) {reportTS(ctrl, Bsn._age_snow, of__age_snow);}
  if (ctrl.report__age_pond==1) {reportTS(ctrl, Bsn._age_pond, of__age_pond);}
  if (ctrl.report__age_layer1==1) {reportTS(ctrl, Bsn._age_layer1, of__age_layer1);}
  if (ctrl.report__age_layer2==1) {reportTS(ctrl, Bsn._age_layer2, of__age_layer2);}
  if (ctrl.report__age_layer3==1) {reportTS(ctrl, Bsn._age_layer3, of__age_layer3);}
  if (ctrl.report__age_GW==1) {reportTS(ctrl, Bsn._age_GW, of__age_GW);}
  if (ctrl.report__age_chanS==1) {reportTS(ctrl, Bsn._age_chanS, of__age_chanS);}
  if (ctrl.report__no3_I==1) {reportTS(ctrl, Bsn._no3_I, of__no3_I);}
  if (ctrl.report__no3_snow==1) {reportTS(ctrl, Bsn._no3_snow, of__no3_snow);}
  if (ctrl.report__no3_pond==1) {reportTS(ctrl, Bsn._no3_pond, of__no3_pond);}
  if (ctrl.report__no3_layer1==1) {reportTS(ctrl, Bsn._no3_layer1, of__no3_layer1);}
  if (ctrl.report__no3_layer2==1) {reportTS(ctrl, Bsn._no3_layer2, of__no3_layer2);}
  if (ctrl.report__no3_layer3==1) {reportTS(ctrl, Bsn._no3_layer3, of__no3_layer3);}
  if (ctrl.report__no3_GW==1) {reportTS(ctrl, Bsn._no3_GW, of__no3_GW);}
  if (ctrl.report__no3_chanS==1) {reportTS(ctrl, Bsn._no3_chanS, of__no3_chanS);}
  if (ctrl.report__nitrogen_add==1) {reportTS(ctrl, Bsn._nitrogen_add, of__nitrogen_add);}
  if (ctrl.report__plant_uptake==1) {reportTS(ctrl, Bsn._plant_uptake, of__plant_uptake);}
  if (ctrl.report__deni_soil==1) {reportTS(ctrl, Bsn._deni_soil, of__deni_soil);}
  if (ctrl.report__minerl_soil==1) {reportTS(ctrl, Bsn._minerl_soil, of__minerl_soil);}
  if (ctrl.report__degrad_soil==1) {reportTS(ctrl, Bsn._degrad_soil, of__degrad_soil);}
  if (ctrl.report__deni_river==1) {reportTS(ctrl, Bsn._deni_river, of__deni_river);}
  /* end of Report to time series */
  return EXIT_SUCCESS;
  }


int Report::Report_to_maps(Control &ctrl){
  /* Report to maps */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==2) {reportMap(ctrl, _I_acc, ctrl._sortedGrid, of__I);}
  if (ctrl.report__snow==2) {reportMap(ctrl, _snow_acc, ctrl._sortedGrid, of__snow);}
  if (ctrl.report__pond==2) {reportMap(ctrl, _pond_acc, ctrl._sortedGrid, of__pond);}
  if (ctrl.report__theta1==2) {reportMap(ctrl, _theta1_acc, ctrl._sortedGrid, of__theta1);}
  if (ctrl.report__theta2==2) {reportMap(ctrl, _theta2_acc, ctrl._sortedGrid, of__theta2);}
  if (ctrl.report__theta3==2) {reportMap(ctrl, _theta3_acc, ctrl._sortedGrid, of__theta3);}
  if (ctrl.report__GW==2) {reportMap(ctrl, _GW_acc, ctrl._sortedGrid, of__GW);}
  if (ctrl.report__Th==2) {reportMap(ctrl, _Th_acc, ctrl._sortedGrid, of__Th);}
  if (ctrl.report__snowmelt==2) {reportMap(ctrl, _snowmelt_acc, ctrl._sortedGrid, of__snowmelt);}
  if (ctrl.report__infilt==2) {reportMap(ctrl, _infilt_acc, ctrl._sortedGrid, of__infilt);}
  if (ctrl.report__Perc1==2) {reportMap(ctrl, _Perc1_acc, ctrl._sortedGrid, of__Perc1);}
  if (ctrl.report__Perc2==2) {reportMap(ctrl, _Perc2_acc, ctrl._sortedGrid, of__Perc2);}
  if (ctrl.report__Perc3==2) {reportMap(ctrl, _Perc3_acc, ctrl._sortedGrid, of__Perc3);}
  if (ctrl.report__rinfilt==2) {reportMap(ctrl, _rinfilt_acc, ctrl._sortedGrid, of__rinfilt);}
  if (ctrl.report__rPerc1==2) {reportMap(ctrl, _rPerc1_acc, ctrl._sortedGrid, of__rPerc1);}
  if (ctrl.report__rPerc2==2) {reportMap(ctrl, _rPerc2_acc, ctrl._sortedGrid, of__rPerc2);}
  if (ctrl.report__rPerc3==2) {reportMap(ctrl, _rPerc3_acc, ctrl._sortedGrid, of__rPerc3);}
  if (ctrl.report__rrPerc3==2) {reportMap(ctrl, _rrPerc3_acc, ctrl._sortedGrid, of__rrPerc3);}
  if (ctrl.report__Ei==2) {reportMap(ctrl, _Ei_acc, ctrl._sortedGrid, of__Ei);}
  if (ctrl.report__Es==2) {reportMap(ctrl, _Es_acc, ctrl._sortedGrid, of__Es);}
  if (ctrl.report__Tr==2) {reportMap(ctrl, _Tr_acc, ctrl._sortedGrid, of__Tr);}
  if (ctrl.report__Tr1==2) {reportMap(ctrl, _Tr1_acc, ctrl._sortedGrid, of__Tr1);}
  if (ctrl.report__Tr2==2) {reportMap(ctrl, _Tr2_acc, ctrl._sortedGrid, of__Tr2);}
  if (ctrl.report__Tr3==2) {reportMap(ctrl, _Tr3_acc, ctrl._sortedGrid, of__Tr3);}
  if (ctrl.report__irrigation_from_river==2) {reportMap(ctrl, _irrigation_from_river_acc, ctrl._sortedGrid, of__irrigation_from_river);}
  if (ctrl.report__irrigation_from_GW==2) {reportMap(ctrl, _irrigation_from_GW_acc, ctrl._sortedGrid, of__irrigation_from_GW);}
  if (ctrl.report__ovf_in==2) {reportMap(ctrl, _ovf_in_acc, ctrl._sortedGrid, of__ovf_in);}
  if (ctrl.report__ovf_out==2) {reportMap(ctrl, _ovf_out_acc, ctrl._sortedGrid, of__ovf_out);}
  if (ctrl.report__ovf_toChn==2) {reportMap(ctrl, _ovf_toChn_acc, ctrl._sortedGrid, of__ovf_toChn);}
  if (ctrl.report__interf_in==2) {reportMap(ctrl, _interf_in_acc, ctrl._sortedGrid, of__interf_in);}
  if (ctrl.report__interf_out==2) {reportMap(ctrl, _interf_out_acc, ctrl._sortedGrid, of__interf_out);}
  if (ctrl.report__interf_toChn==2) {reportMap(ctrl, _interf_toChn_acc, ctrl._sortedGrid, of__interf_toChn);}
  if (ctrl.report__GWf_in==2) {reportMap(ctrl, _GWf_in_acc, ctrl._sortedGrid, of__GWf_in);}
  if (ctrl.report__GWf_out==2) {reportMap(ctrl, _GWf_out_acc, ctrl._sortedGrid, of__GWf_out);}
  if (ctrl.report__GWf_toChn==2) {reportMap(ctrl, _GWf_toChn_acc, ctrl._sortedGrid, of__GWf_toChn);}
  if (ctrl.report__Q==2) {reportMap(ctrl, _Q_acc, ctrl._sortedGrid, of__Q);}
  if (ctrl.report__Echan==2) {reportMap(ctrl, _Echan_acc, ctrl._sortedGrid, of__Echan);}
  if (ctrl.report__d18o_I==2) {reportMap(ctrl, _d18o_I_acc, ctrl._sortedGrid, of__d18o_I);}
  if (ctrl.report__d18o_snow==2) {reportMap(ctrl, _d18o_snow_acc, ctrl._sortedGrid, of__d18o_snow);}
  if (ctrl.report__d18o_pond==2) {reportMap(ctrl, _d18o_pond_acc, ctrl._sortedGrid, of__d18o_pond);}
  if (ctrl.report__d18o_layer1==2) {reportMap(ctrl, _d18o_layer1_acc, ctrl._sortedGrid, of__d18o_layer1);}
  if (ctrl.report__d18o_layer2==2) {reportMap(ctrl, _d18o_layer2_acc, ctrl._sortedGrid, of__d18o_layer2);}
  if (ctrl.report__d18o_layer3==2) {reportMap(ctrl, _d18o_layer3_acc, ctrl._sortedGrid, of__d18o_layer3);}
  if (ctrl.report__d18o_GW==2) {reportMap(ctrl, _d18o_GW_acc, ctrl._sortedGrid, of__d18o_GW);}
  if (ctrl.report__d18o_chanS==2) {reportMap(ctrl, _d18o_chanS_acc, ctrl._sortedGrid, of__d18o_chanS);}
  if (ctrl.report__age_I==2) {reportMap(ctrl, _age_I_acc, ctrl._sortedGrid, of__age_I);}
  if (ctrl.report__age_snow==2) {reportMap(ctrl, _age_snow_acc, ctrl._sortedGrid, of__age_snow);}
  if (ctrl.report__age_pond==2) {reportMap(ctrl, _age_pond_acc, ctrl._sortedGrid, of__age_pond);}
  if (ctrl.report__age_layer1==2) {reportMap(ctrl, _age_layer1_acc, ctrl._sortedGrid, of__age_layer1);}
  if (ctrl.report__age_layer2==2) {reportMap(ctrl, _age_layer2_acc, ctrl._sortedGrid, of__age_layer2);}
  if (ctrl.report__age_layer3==2) {reportMap(ctrl, _age_layer3_acc, ctrl._sortedGrid, of__age_layer3);}
  if (ctrl.report__age_GW==2) {reportMap(ctrl, _age_GW_acc, ctrl._sortedGrid, of__age_GW);}
  if (ctrl.report__age_chanS==2) {reportMap(ctrl, _age_chanS_acc, ctrl._sortedGrid, of__age_chanS);}
  if (ctrl.report__no3_I==2) {reportMap(ctrl, _no3_I_acc, ctrl._sortedGrid, of__no3_I);}
  if (ctrl.report__no3_snow==2) {reportMap(ctrl, _no3_snow_acc, ctrl._sortedGrid, of__no3_snow);}
  if (ctrl.report__no3_pond==2) {reportMap(ctrl, _no3_pond_acc, ctrl._sortedGrid, of__no3_pond);}
  if (ctrl.report__no3_layer1==2) {reportMap(ctrl, _no3_layer1_acc, ctrl._sortedGrid, of__no3_layer1);}
  if (ctrl.report__no3_layer2==2) {reportMap(ctrl, _no3_layer2_acc, ctrl._sortedGrid, of__no3_layer2);}
  if (ctrl.report__no3_layer3==2) {reportMap(ctrl, _no3_layer3_acc, ctrl._sortedGrid, of__no3_layer3);}
  if (ctrl.report__no3_GW==2) {reportMap(ctrl, _no3_GW_acc, ctrl._sortedGrid, of__no3_GW);}
  if (ctrl.report__no3_chanS==2) {reportMap(ctrl, _no3_chanS_acc, ctrl._sortedGrid, of__no3_chanS);}
  if (ctrl.report__nitrogen_add==2) {reportMap(ctrl, _nitrogen_add_acc, ctrl._sortedGrid, of__nitrogen_add);}
  if (ctrl.report__plant_uptake==2) {reportMap(ctrl, _plant_uptake_acc, ctrl._sortedGrid, of__plant_uptake);}
  if (ctrl.report__deni_soil==2) {reportMap(ctrl, _deni_soil_acc, ctrl._sortedGrid, of__deni_soil);}
  if (ctrl.report__minerl_soil==2) {reportMap(ctrl, _minerl_soil_acc, ctrl._sortedGrid, of__minerl_soil);}
  if (ctrl.report__degrad_soil==2) {reportMap(ctrl, _degrad_soil_acc, ctrl._sortedGrid, of__degrad_soil);}
  if (ctrl.report__deni_river==2) {reportMap(ctrl, _deni_river_acc, ctrl._sortedGrid, of__deni_river);}
  /* end of Report to maps */
  advance_report = 0;
  return EXIT_SUCCESS;
  }

int Report::report_create(string fname, ofstream &ofHandle){
      // Delete the report files from last iteration
      ifstream file(fname);
        if (file.good()) {
          file.close();
          remove(fname.c_str());
        }
      
      // Open report file
      ofHandle.open(fname, ios::binary|ios::app);
      if (!ofHandle.good()){
        throw runtime_error("file not found    :" + fname);
      }
      return EXIT_SUCCESS;
    }


int Report::reportTS(Control &ctrl, const svector *input, ofstream &ofHandle){
  int length = ctrl._Tsmask.cell.size();
  double outdata[length];
  string filename;
  for (int i = 0; i<length; i++){
      outdata[i] = input->val[ctrl._Tsmask.cell[i]];
  }
  
  ofHandle.write((char*)&outdata, sizeof(double)*length);

  return EXIT_SUCCESS;
  }


int Report::reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, ofstream &ofHandle){
  int r, c;
  int _rowNum = ctrl._rowNum;
  int _colNum = ctrl._colNum;
  double outdata[_rowNum*_colNum];
  string filename;

  for(int i = 0; i < _rowNum*_colNum; i++){
      outdata[i] = ctrl._nodata;
  }
  for(int j = 0; j < _sortedGrid.size; j++){
    r = _sortedGrid.row[j];
    c = _sortedGrid.col[j];
    outdata[r*_colNum + c] = input->val[j] / advance_report * ctrl.Simul_tstep;
    input->val[j] = 0.0;  // reset accumulated maps
  }  
  ofHandle.write((char*)&outdata, sizeof(double)*_rowNum*_colNum);
  return EXIT_SUCCESS;
  }