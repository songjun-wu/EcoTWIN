#include "Report.h"

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

  /* end of Init Report */
  return EXIT_SUCCESS;
}

int Report::report(Control &ctrl, Basin &Bsn){
  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==1) {reportTS(ctrl, Bsn._I, of__I);}
  else if (ctrl.report__I==2) {reportMap(ctrl, Bsn._I, ctrl._sortedGrid, of__I);}

  if (ctrl.report__snow==1) {reportTS(ctrl, Bsn._snow, of__snow);}
  else if (ctrl.report__snow==2) {reportMap(ctrl, Bsn._snow, ctrl._sortedGrid, of__snow);}

  if (ctrl.report__pond==1) {reportTS(ctrl, Bsn._pond, of__pond);}
  else if (ctrl.report__pond==2) {reportMap(ctrl, Bsn._pond, ctrl._sortedGrid, of__pond);}

  if (ctrl.report__theta1==1) {reportTS(ctrl, Bsn._theta1, of__theta1);}
  else if (ctrl.report__theta1==2) {reportMap(ctrl, Bsn._theta1, ctrl._sortedGrid, of__theta1);}

  if (ctrl.report__theta2==1) {reportTS(ctrl, Bsn._theta2, of__theta2);}
  else if (ctrl.report__theta2==2) {reportMap(ctrl, Bsn._theta2, ctrl._sortedGrid, of__theta2);}

  if (ctrl.report__theta3==1) {reportTS(ctrl, Bsn._theta3, of__theta3);}
  else if (ctrl.report__theta3==2) {reportMap(ctrl, Bsn._theta3, ctrl._sortedGrid, of__theta3);}

  if (ctrl.report__GW==1) {reportTS(ctrl, Bsn._GW, of__GW);}
  else if (ctrl.report__GW==2) {reportMap(ctrl, Bsn._GW, ctrl._sortedGrid, of__GW);}

  if (ctrl.report__Th==1) {reportTS(ctrl, Bsn._Th, of__Th);}
  else if (ctrl.report__Th==2) {reportMap(ctrl, Bsn._Th, ctrl._sortedGrid, of__Th);}

  if (ctrl.report__snowmelt==1) {reportTS(ctrl, Bsn._snowmelt, of__snowmelt);}
  else if (ctrl.report__snowmelt==2) {reportMap(ctrl, Bsn._snowmelt, ctrl._sortedGrid, of__snowmelt);}

  if (ctrl.report__infilt==1) {reportTS(ctrl, Bsn._infilt, of__infilt);}
  else if (ctrl.report__infilt==2) {reportMap(ctrl, Bsn._infilt, ctrl._sortedGrid, of__infilt);}

  if (ctrl.report__Perc1==1) {reportTS(ctrl, Bsn._Perc1, of__Perc1);}
  else if (ctrl.report__Perc1==2) {reportMap(ctrl, Bsn._Perc1, ctrl._sortedGrid, of__Perc1);}

  if (ctrl.report__Perc2==1) {reportTS(ctrl, Bsn._Perc2, of__Perc2);}
  else if (ctrl.report__Perc2==2) {reportMap(ctrl, Bsn._Perc2, ctrl._sortedGrid, of__Perc2);}

  if (ctrl.report__Perc3==1) {reportTS(ctrl, Bsn._Perc3, of__Perc3);}
  else if (ctrl.report__Perc3==2) {reportMap(ctrl, Bsn._Perc3, ctrl._sortedGrid, of__Perc3);}

  if (ctrl.report__rinfilt==1) {reportTS(ctrl, Bsn._rinfilt, of__rinfilt);}
  else if (ctrl.report__rinfilt==2) {reportMap(ctrl, Bsn._rinfilt, ctrl._sortedGrid, of__rinfilt);}

  if (ctrl.report__rPerc1==1) {reportTS(ctrl, Bsn._rPerc1, of__rPerc1);}
  else if (ctrl.report__rPerc1==2) {reportMap(ctrl, Bsn._rPerc1, ctrl._sortedGrid, of__rPerc1);}

  if (ctrl.report__rPerc2==1) {reportTS(ctrl, Bsn._rPerc2, of__rPerc2);}
  else if (ctrl.report__rPerc2==2) {reportMap(ctrl, Bsn._rPerc2, ctrl._sortedGrid, of__rPerc2);}

  if (ctrl.report__rPerc3==1) {reportTS(ctrl, Bsn._rPerc3, of__rPerc3);}
  else if (ctrl.report__rPerc3==2) {reportMap(ctrl, Bsn._rPerc3, ctrl._sortedGrid, of__rPerc3);}

  if (ctrl.report__Ei==1) {reportTS(ctrl, Bsn._Ei, of__Ei);}
  else if (ctrl.report__Ei==2) {reportMap(ctrl, Bsn._Ei, ctrl._sortedGrid, of__Ei);}

  if (ctrl.report__Es==1) {reportTS(ctrl, Bsn._Es, of__Es);}
  else if (ctrl.report__Es==2) {reportMap(ctrl, Bsn._Es, ctrl._sortedGrid, of__Es);}

  if (ctrl.report__Tr==1) {reportTS(ctrl, Bsn._Tr, of__Tr);}
  else if (ctrl.report__Tr==2) {reportMap(ctrl, Bsn._Tr, ctrl._sortedGrid, of__Tr);}

  if (ctrl.report__Tr1==1) {reportTS(ctrl, Bsn._Tr1, of__Tr1);}
  else if (ctrl.report__Tr1==2) {reportMap(ctrl, Bsn._Tr1, ctrl._sortedGrid, of__Tr1);}

  if (ctrl.report__Tr2==1) {reportTS(ctrl, Bsn._Tr2, of__Tr2);}
  else if (ctrl.report__Tr2==2) {reportMap(ctrl, Bsn._Tr2, ctrl._sortedGrid, of__Tr2);}

  if (ctrl.report__Tr3==1) {reportTS(ctrl, Bsn._Tr3, of__Tr3);}
  else if (ctrl.report__Tr3==2) {reportMap(ctrl, Bsn._Tr3, ctrl._sortedGrid, of__Tr3);}

  if (ctrl.report__ovf_in==1) {reportTS(ctrl, Bsn._ovf_in, of__ovf_in);}
  else if (ctrl.report__ovf_in==2) {reportMap(ctrl, Bsn._ovf_in, ctrl._sortedGrid, of__ovf_in);}

  if (ctrl.report__ovf_out==1) {reportTS(ctrl, Bsn._ovf_out, of__ovf_out);}
  else if (ctrl.report__ovf_out==2) {reportMap(ctrl, Bsn._ovf_out, ctrl._sortedGrid, of__ovf_out);}

  if (ctrl.report__ovf_toChn==1) {reportTS(ctrl, Bsn._ovf_toChn, of__ovf_toChn);}
  else if (ctrl.report__ovf_toChn==2) {reportMap(ctrl, Bsn._ovf_toChn, ctrl._sortedGrid, of__ovf_toChn);}

  if (ctrl.report__interf_in==1) {reportTS(ctrl, Bsn._interf_in, of__interf_in);}
  else if (ctrl.report__interf_in==2) {reportMap(ctrl, Bsn._interf_in, ctrl._sortedGrid, of__interf_in);}

  if (ctrl.report__interf_out==1) {reportTS(ctrl, Bsn._interf_out, of__interf_out);}
  else if (ctrl.report__interf_out==2) {reportMap(ctrl, Bsn._interf_out, ctrl._sortedGrid, of__interf_out);}

  if (ctrl.report__interf_toChn==1) {reportTS(ctrl, Bsn._interf_toChn, of__interf_toChn);}
  else if (ctrl.report__interf_toChn==2) {reportMap(ctrl, Bsn._interf_toChn, ctrl._sortedGrid, of__interf_toChn);}

  if (ctrl.report__GWf_in==1) {reportTS(ctrl, Bsn._GWf_in, of__GWf_in);}
  else if (ctrl.report__GWf_in==2) {reportMap(ctrl, Bsn._GWf_in, ctrl._sortedGrid, of__GWf_in);}

  if (ctrl.report__GWf_out==1) {reportTS(ctrl, Bsn._GWf_out, of__GWf_out);}
  else if (ctrl.report__GWf_out==2) {reportMap(ctrl, Bsn._GWf_out, ctrl._sortedGrid, of__GWf_out);}

  if (ctrl.report__GWf_toChn==1) {reportTS(ctrl, Bsn._GWf_toChn, of__GWf_toChn);}
  else if (ctrl.report__GWf_toChn==2) {reportMap(ctrl, Bsn._GWf_toChn, ctrl._sortedGrid, of__GWf_toChn);}

  if (ctrl.report__Q==1) {reportTS(ctrl, Bsn._Q, of__Q);}
  else if (ctrl.report__Q==2) {reportMap(ctrl, Bsn._Q, ctrl._sortedGrid, of__Q);}

  if (ctrl.report__d18o_I==1) {reportTS(ctrl, Bsn._d18o_I, of__d18o_I);}
  else if (ctrl.report__d18o_I==2) {reportMap(ctrl, Bsn._d18o_I, ctrl._sortedGrid, of__d18o_I);}

  if (ctrl.report__d18o_snow==1) {reportTS(ctrl, Bsn._d18o_snow, of__d18o_snow);}
  else if (ctrl.report__d18o_snow==2) {reportMap(ctrl, Bsn._d18o_snow, ctrl._sortedGrid, of__d18o_snow);}

  if (ctrl.report__d18o_pond==1) {reportTS(ctrl, Bsn._d18o_pond, of__d18o_pond);}
  else if (ctrl.report__d18o_pond==2) {reportMap(ctrl, Bsn._d18o_pond, ctrl._sortedGrid, of__d18o_pond);}

  if (ctrl.report__d18o_layer1==1) {reportTS(ctrl, Bsn._d18o_layer1, of__d18o_layer1);}
  else if (ctrl.report__d18o_layer1==2) {reportMap(ctrl, Bsn._d18o_layer1, ctrl._sortedGrid, of__d18o_layer1);}

  if (ctrl.report__d18o_layer2==1) {reportTS(ctrl, Bsn._d18o_layer2, of__d18o_layer2);}
  else if (ctrl.report__d18o_layer2==2) {reportMap(ctrl, Bsn._d18o_layer2, ctrl._sortedGrid, of__d18o_layer2);}

  if (ctrl.report__d18o_layer3==1) {reportTS(ctrl, Bsn._d18o_layer3, of__d18o_layer3);}
  else if (ctrl.report__d18o_layer3==2) {reportMap(ctrl, Bsn._d18o_layer3, ctrl._sortedGrid, of__d18o_layer3);}

  if (ctrl.report__d18o_GW==1) {reportTS(ctrl, Bsn._d18o_GW, of__d18o_GW);}
  else if (ctrl.report__d18o_GW==2) {reportMap(ctrl, Bsn._d18o_GW, ctrl._sortedGrid, of__d18o_GW);}

  if (ctrl.report__d18o_chanS==1) {reportTS(ctrl, Bsn._d18o_chanS, of__d18o_chanS);}
  else if (ctrl.report__d18o_chanS==2) {reportMap(ctrl, Bsn._d18o_chanS, ctrl._sortedGrid, of__d18o_chanS);}

  /* end of Report */
  return 0;
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
    outdata[r*_colNum + c] = input->val[j];
  }

  

  ofHandle.write((char*)&outdata, sizeof(double)*_rowNum*_colNum);

  return EXIT_SUCCESS;
  }