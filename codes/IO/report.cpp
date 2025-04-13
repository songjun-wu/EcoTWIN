#include "Report.h"

int Report::Report_Initialisation(Control &ctrl){
  /* Init Report */
  // Create files for report
  if (ctrl.report__I>0)  report_create("canopy_storage", ctrl.path_ResultsFolder, ctrl.report__I);
  if (ctrl.report__snow>0)  report_create("snow_depth", ctrl.path_ResultsFolder, ctrl.report__snow);
  if (ctrl.report__pond>0)  report_create("pond", ctrl.path_ResultsFolder, ctrl.report__pond);
  if (ctrl.report__theta1>0)  report_create("SMC_layer1", ctrl.path_ResultsFolder, ctrl.report__theta1);
  if (ctrl.report__theta2>0)  report_create("SMC_layer2", ctrl.path_ResultsFolder, ctrl.report__theta2);
  if (ctrl.report__theta3>0)  report_create("SMC_layer3", ctrl.path_ResultsFolder, ctrl.report__theta3);
  if (ctrl.report__GW>0)  report_create("groundwater_storage", ctrl.path_ResultsFolder, ctrl.report__GW);
  if (ctrl.report__Th>0)  report_create("throufall", ctrl.path_ResultsFolder, ctrl.report__Th);
  if (ctrl.report__snowmelt>0)  report_create("snowmelt", ctrl.path_ResultsFolder, ctrl.report__snowmelt);
  if (ctrl.report__infilt>0)  report_create("infiltration", ctrl.path_ResultsFolder, ctrl.report__infilt);
  if (ctrl.report__Perc1>0)  report_create("perc_layer1", ctrl.path_ResultsFolder, ctrl.report__Perc1);
  if (ctrl.report__Perc2>0)  report_create("perc_layer2", ctrl.path_ResultsFolder, ctrl.report__Perc2);
  if (ctrl.report__Perc3>0)  report_create("perc_layer3", ctrl.path_ResultsFolder, ctrl.report__Perc3);
  if (ctrl.report__rinfilt>0)  report_create("rinfiltration", ctrl.path_ResultsFolder, ctrl.report__rinfilt);
  if (ctrl.report__rPerc1>0)  report_create("rperc_layer1", ctrl.path_ResultsFolder, ctrl.report__rPerc1);
  if (ctrl.report__rPerc2>0)  report_create("rperc_layer2", ctrl.path_ResultsFolder, ctrl.report__rPerc2);
  if (ctrl.report__rPerc3>0)  report_create("rperc_layer3", ctrl.path_ResultsFolder, ctrl.report__rPerc3);
  if (ctrl.report__Ei>0)  report_create("canopy_evap", ctrl.path_ResultsFolder, ctrl.report__Ei);
  if (ctrl.report__Es>0)  report_create("soil_evap", ctrl.path_ResultsFolder, ctrl.report__Es);
  if (ctrl.report__Tr>0)  report_create("transp", ctrl.path_ResultsFolder, ctrl.report__Tr);
  if (ctrl.report__Tr1>0)  report_create("transp_layer1", ctrl.path_ResultsFolder, ctrl.report__Tr1);
  if (ctrl.report__Tr2>0)  report_create("transp_layer2", ctrl.path_ResultsFolder, ctrl.report__Tr2);
  if (ctrl.report__Tr3>0)  report_create("transp_layer3", ctrl.path_ResultsFolder, ctrl.report__Tr3);
  if (ctrl.report__ovf_in>0)  report_create("overland_flow_input", ctrl.path_ResultsFolder, ctrl.report__ovf_in);
  if (ctrl.report__ovf_out>0)  report_create("overland_flow_output", ctrl.path_ResultsFolder, ctrl.report__ovf_out);
  if (ctrl.report__ovf_toChn>0)  report_create("overland_flow_toChn", ctrl.path_ResultsFolder, ctrl.report__ovf_toChn);
  if (ctrl.report__interf_in>0)  report_create("interflow_input", ctrl.path_ResultsFolder, ctrl.report__interf_in);
  if (ctrl.report__interf_out>0)  report_create("interflow_output", ctrl.path_ResultsFolder, ctrl.report__interf_out);
  if (ctrl.report__interf_toChn>0)  report_create("interflow_toChn", ctrl.path_ResultsFolder, ctrl.report__interf_toChn);
  if (ctrl.report__GWf_in>0)  report_create("GWflow_input", ctrl.path_ResultsFolder, ctrl.report__GWf_in);
  if (ctrl.report__GWf_out>0)  report_create("GWflow_output", ctrl.path_ResultsFolder, ctrl.report__GWf_out);
  if (ctrl.report__GWf_toChn>0)  report_create("GWflow_toChn", ctrl.path_ResultsFolder, ctrl.report__GWf_toChn);
  if (ctrl.report__Q>0)  report_create("discharge", ctrl.path_ResultsFolder, ctrl.report__Q);
  /* end of Init Report */
  return EXIT_SUCCESS;
}

int Report::report(Control &ctrl, Basin &Bsn){
  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==1) {reportTS(ctrl, Bsn._I, "canopy_storage", ctrl.path_ResultsFolder);}
  else if (ctrl.report__I==2) {reportMap(ctrl, Bsn._I, ctrl._sortedGrid, "canopy_storage", ctrl.path_ResultsFolder);}

  if (ctrl.report__snow==1) {reportTS(ctrl, Bsn._snow, "snow_depth", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snow==2) {reportMap(ctrl, Bsn._snow, ctrl._sortedGrid, "snow_depth", ctrl.path_ResultsFolder);}

  if (ctrl.report__pond==1) {reportTS(ctrl, Bsn._pond, "pond", ctrl.path_ResultsFolder);}
  else if (ctrl.report__pond==2) {reportMap(ctrl, Bsn._pond, ctrl._sortedGrid, "pond", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta1==1) {reportTS(ctrl, Bsn._theta1, "SMC_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta1==2) {reportMap(ctrl, Bsn._theta1, ctrl._sortedGrid, "SMC_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta2==1) {reportTS(ctrl, Bsn._theta2, "SMC_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta2==2) {reportMap(ctrl, Bsn._theta2, ctrl._sortedGrid, "SMC_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta3==1) {reportTS(ctrl, Bsn._theta3, "SMC_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta3==2) {reportMap(ctrl, Bsn._theta3, ctrl._sortedGrid, "SMC_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__GW==1) {reportTS(ctrl, Bsn._GW, "groundwater_storage", ctrl.path_ResultsFolder);}
  else if (ctrl.report__GW==2) {reportMap(ctrl, Bsn._GW, ctrl._sortedGrid, "groundwater_storage", ctrl.path_ResultsFolder);}

  if (ctrl.report__Th==1) {reportTS(ctrl, Bsn._Th, "throufall", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Th==2) {reportMap(ctrl, Bsn._Th, ctrl._sortedGrid, "throufall", ctrl.path_ResultsFolder);}

  if (ctrl.report__snowmelt==1) {reportTS(ctrl, Bsn._snowmelt, "snowmelt", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snowmelt==2) {reportMap(ctrl, Bsn._snowmelt, ctrl._sortedGrid, "snowmelt", ctrl.path_ResultsFolder);}

  if (ctrl.report__infilt==1) {reportTS(ctrl, Bsn._infilt, "infiltration", ctrl.path_ResultsFolder);}
  else if (ctrl.report__infilt==2) {reportMap(ctrl, Bsn._infilt, ctrl._sortedGrid, "infiltration", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc1==1) {reportTS(ctrl, Bsn._Perc1, "perc_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc1==2) {reportMap(ctrl, Bsn._Perc1, ctrl._sortedGrid, "perc_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc2==1) {reportTS(ctrl, Bsn._Perc2, "perc_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc2==2) {reportMap(ctrl, Bsn._Perc2, ctrl._sortedGrid, "perc_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc3==1) {reportTS(ctrl, Bsn._Perc3, "perc_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc3==2) {reportMap(ctrl, Bsn._Perc3, ctrl._sortedGrid, "perc_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__rinfilt==1) {reportTS(ctrl, Bsn._rinfilt, "rinfiltration", ctrl.path_ResultsFolder);}
  else if (ctrl.report__rinfilt==2) {reportMap(ctrl, Bsn._rinfilt, ctrl._sortedGrid, "rinfiltration", ctrl.path_ResultsFolder);}

  if (ctrl.report__rPerc1==1) {reportTS(ctrl, Bsn._rPerc1, "rperc_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__rPerc1==2) {reportMap(ctrl, Bsn._rPerc1, ctrl._sortedGrid, "rperc_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__rPerc2==1) {reportTS(ctrl, Bsn._rPerc2, "rperc_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__rPerc2==2) {reportMap(ctrl, Bsn._rPerc2, ctrl._sortedGrid, "rperc_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__rPerc3==1) {reportTS(ctrl, Bsn._rPerc3, "rperc_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__rPerc3==2) {reportMap(ctrl, Bsn._rPerc3, ctrl._sortedGrid, "rperc_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__Ei==1) {reportTS(ctrl, Bsn._Ei, "canopy_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Ei==2) {reportMap(ctrl, Bsn._Ei, ctrl._sortedGrid, "canopy_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Es==1) {reportTS(ctrl, Bsn._Es, "soil_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Es==2) {reportMap(ctrl, Bsn._Es, ctrl._sortedGrid, "soil_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr==1) {reportTS(ctrl, Bsn._Tr, "transp", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr==2) {reportMap(ctrl, Bsn._Tr, ctrl._sortedGrid, "transp", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr1==1) {reportTS(ctrl, Bsn._Tr1, "transp_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr1==2) {reportMap(ctrl, Bsn._Tr1, ctrl._sortedGrid, "transp_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr2==1) {reportTS(ctrl, Bsn._Tr2, "transp_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr2==2) {reportMap(ctrl, Bsn._Tr2, ctrl._sortedGrid, "transp_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr3==1) {reportTS(ctrl, Bsn._Tr3, "transp_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr3==2) {reportMap(ctrl, Bsn._Tr3, ctrl._sortedGrid, "transp_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_in==1) {reportTS(ctrl, Bsn._ovf_in, "overland_flow_input", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_in==2) {reportMap(ctrl, Bsn._ovf_in, ctrl._sortedGrid, "overland_flow_input", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_out==1) {reportTS(ctrl, Bsn._ovf_out, "overland_flow_output", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_out==2) {reportMap(ctrl, Bsn._ovf_out, ctrl._sortedGrid, "overland_flow_output", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_toChn==1) {reportTS(ctrl, Bsn._ovf_toChn, "overland_flow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_toChn==2) {reportMap(ctrl, Bsn._ovf_toChn, ctrl._sortedGrid, "overland_flow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_in==1) {reportTS(ctrl, Bsn._interf_in, "interflow_input", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_in==2) {reportMap(ctrl, Bsn._interf_in, ctrl._sortedGrid, "interflow_input", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_out==1) {reportTS(ctrl, Bsn._interf_out, "interflow_output", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_out==2) {reportMap(ctrl, Bsn._interf_out, ctrl._sortedGrid, "interflow_output", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_toChn==1) {reportTS(ctrl, Bsn._interf_toChn, "interflow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_toChn==2) {reportMap(ctrl, Bsn._interf_toChn, ctrl._sortedGrid, "interflow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__GWf_in==1) {reportTS(ctrl, Bsn._GWf_in, "GWflow_input", ctrl.path_ResultsFolder);}
  else if (ctrl.report__GWf_in==2) {reportMap(ctrl, Bsn._GWf_in, ctrl._sortedGrid, "GWflow_input", ctrl.path_ResultsFolder);}

  if (ctrl.report__GWf_out==1) {reportTS(ctrl, Bsn._GWf_out, "GWflow_output", ctrl.path_ResultsFolder);}
  else if (ctrl.report__GWf_out==2) {reportMap(ctrl, Bsn._GWf_out, ctrl._sortedGrid, "GWflow_output", ctrl.path_ResultsFolder);}

  if (ctrl.report__GWf_toChn==1) {reportTS(ctrl, Bsn._GWf_toChn, "GWflow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__GWf_toChn==2) {reportMap(ctrl, Bsn._GWf_toChn, ctrl._sortedGrid, "GWflow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__Q==1) {reportTS(ctrl, Bsn._Q, "discharge", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Q==2) {reportMap(ctrl, Bsn._Q, ctrl._sortedGrid, "discharge", ctrl.path_ResultsFolder);}

  /* end of Report */

  return 0;
  }

  int Report::report_create(string varname, string filepath, int Ts_or_map){
    string filename;

    if (Ts_or_map == 1){
      filename =  filepath + varname.c_str() + "_TS.bin";
    } else if (Ts_or_map == 2){
      filename =  filepath + varname.c_str() + "_map.bin";
    }
    
    ifstream file(filename);
    if (file.good()) {
      file.close();
      remove(filename.c_str());
    }
    return 0;
    }


int Report::reportTS(Control &ctrl, const svector *input, string varname, string filepath){
  fstream ofOutput;
  int length = ctrl._Tsmask.cell.size();
  double outdata[length];
  string filename;
  for (int i = 0; i<length; i++){
      outdata[i] = input->val[ctrl._Tsmask.cell[i]];
  }
  
  filename =  filepath + varname.c_str() + "_TS.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*length);
  ofOutput.close();
  return 0;
  }


int Report::reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, string varname, string filepath){

  int r, c;

  int _rowNum = ctrl._rowNum;
  int _colNum = ctrl._colNum;


  fstream ofOutput;
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

  
  filename =  filepath + varname.c_str() + "_map.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*_rowNum*_colNum);
  ofOutput.close();
  return 0;
  }