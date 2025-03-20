#include "Report.h"

int Report::report(Control &ctrl, Basin &Bsn){

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==1) {reportTS(ctrl, Bsn._I, "inteception_storage", ctrl.path_ResultsFolder);}
  else if (ctrl.report__I==2) {reportMap(ctrl, Bsn._I, "inteception_storage", ctrl.path_ResultsFolder);}

  if (ctrl.report__snow==1) {reportTS(ctrl, Bsn._snow, "snow_depth", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snow==2) {reportMap(ctrl, Bsn._snow, "snow_depth", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta1==1) {reportTS(ctrl, Bsn._theta1, "SMC_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta1==2) {reportMap(ctrl, Bsn._theta1, "SMC_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta2==1) {reportTS(ctrl, Bsn._theta2, "SMC_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta2==2) {reportMap(ctrl, Bsn._theta2, "SMC_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta3==1) {reportTS(ctrl, Bsn._theta3, "SMC_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta3==2) {reportMap(ctrl, Bsn._theta3, "SMC_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__D==1) {reportTS(ctrl, Bsn._D, "interception", ctrl.path_ResultsFolder);}
  else if (ctrl.report__D==2) {reportMap(ctrl, Bsn._D, "interception", ctrl.path_ResultsFolder);}

  if (ctrl.report__Th==1) {reportTS(ctrl, Bsn._Th, "throufall", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Th==2) {reportMap(ctrl, Bsn._Th, "throufall", ctrl.path_ResultsFolder);}

  if (ctrl.report__snowmelt==1) {reportTS(ctrl, Bsn._snowmelt, "snowmelt", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snowmelt==2) {reportMap(ctrl, Bsn._snowmelt, "snowmelt", ctrl.path_ResultsFolder);}

  if (ctrl.report__Qs==1) {reportTS(ctrl, Bsn._Qs, "overland_flow", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Qs==2) {reportMap(ctrl, Bsn._Qs, "overland_flow", ctrl.path_ResultsFolder);}

  if (ctrl.report__infilt==1) {reportTS(ctrl, Bsn._infilt, "infiltration", ctrl.path_ResultsFolder);}
  else if (ctrl.report__infilt==2) {reportMap(ctrl, Bsn._infilt, "infiltration", ctrl.path_ResultsFolder);}

  if (ctrl.report__preferential2==1) {reportTS(ctrl, Bsn._preferential2, "preferential_flow_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__preferential2==2) {reportMap(ctrl, Bsn._preferential2, "preferential_flow_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__preferential3==1) {reportTS(ctrl, Bsn._preferential3, "preferential_flow_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__preferential3==2) {reportMap(ctrl, Bsn._preferential3, "preferential_flow_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc1==1) {reportTS(ctrl, Bsn._Perc1, "perc_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc1==2) {reportMap(ctrl, Bsn._Perc1, "perc_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc2==1) {reportTS(ctrl, Bsn._Perc2, "perc_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc2==2) {reportMap(ctrl, Bsn._Perc2, "perc_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc3==1) {reportTS(ctrl, Bsn._Perc3, "perc_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc3==2) {reportMap(ctrl, Bsn._Perc3, "perc_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__Ei==1) {reportTS(ctrl, Bsn._Ei, "canopy_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Ei==2) {reportMap(ctrl, Bsn._Ei, "canopy_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Es==1) {reportTS(ctrl, Bsn._Es, "soil_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Es==2) {reportMap(ctrl, Bsn._Es, "soil_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr==1) {reportTS(ctrl, Bsn._Tr, "transp", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr==2) {reportMap(ctrl, Bsn._Tr, "transp", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr1==1) {reportTS(ctrl, Bsn._Tr1, "transp_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr1==2) {reportMap(ctrl, Bsn._Tr1, "transp_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr2==1) {reportTS(ctrl, Bsn._Tr2, "transp_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr2==2) {reportMap(ctrl, Bsn._Tr2, "transp_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr3==1) {reportTS(ctrl, Bsn._Tr3, "transp_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr3==2) {reportMap(ctrl, Bsn._Tr3, "transp_layer3", ctrl.path_ResultsFolder);}

  /* end of Report */

  return 0;
  }


int Report::reportTS(Control &ctrl, const grid *input, string varname, string filepath){
  fstream ofOutput;
  double outdata[ctrl._Tsmask.row.size()];
  string filename;
  for (int i = 0; i<ctrl._Tsmask.row.size(); i++){
      outdata[i] = input->matrix[ctrl._Tsmask.row[i]][ctrl._Tsmask.col[i]];
  }
  
  filename =  filepath + varname.c_str() + "_TS.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*ctrl._Tsmask.row.size());
  ofOutput.close();
  return 0;
  }


int Report::reportMap(Control &ctrl, const grid *input, string varname, string filepath){

  int _rowNum = ctrl._rowNum;
  int _colNum = ctrl._colNum;

  fstream ofOutput;
  double outdata[_rowNum*_colNum];
  string filename;
  for(int i = 0; i < _rowNum; i++){
      for(int j = 0; j < _colNum; j++){
        outdata[i*_colNum + j] = input->matrix[i][j];
      }
  }
  
  filename =  filepath + varname.c_str() + "_map.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*_rowNum*_colNum);
  ofOutput.close();
  return 0;
  }