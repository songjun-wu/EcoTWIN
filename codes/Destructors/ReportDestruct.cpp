/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ReportDestruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Report.h"

Report::~Report(){}

int Report::dtor(Control &ctrl){


  /* Report */
  if (of__I.is_open())  of__I.close();
  if (of__snow.is_open())  of__snow.close();
  if (of__pond.is_open())  of__pond.close();
  if (of__theta1.is_open())  of__theta1.close();
  if (of__theta2.is_open())  of__theta2.close();
  if (of__theta3.is_open())  of__theta3.close();
  if (of__GW.is_open())  of__GW.close();
  if (of__Th.is_open())  of__Th.close();
  if (of__snowmelt.is_open())  of__snowmelt.close();
  if (of__infilt.is_open())  of__infilt.close();
  if (of__Perc1.is_open())  of__Perc1.close();
  if (of__Perc2.is_open())  of__Perc2.close();
  if (of__Perc3.is_open())  of__Perc3.close();
  if (of__rinfilt.is_open())  of__rinfilt.close();
  if (of__rPerc1.is_open())  of__rPerc1.close();
  if (of__rPerc2.is_open())  of__rPerc2.close();
  if (of__rPerc3.is_open())  of__rPerc3.close();
  if (of__rrPerc3.is_open())  of__rrPerc3.close();
  if (of__Ei.is_open())  of__Ei.close();
  if (of__Es.is_open())  of__Es.close();
  if (of__Tr.is_open())  of__Tr.close();
  if (of__Tr1.is_open())  of__Tr1.close();
  if (of__Tr2.is_open())  of__Tr2.close();
  if (of__Tr3.is_open())  of__Tr3.close();
  if (of__irrigation_from_river.is_open())  of__irrigation_from_river.close();
  if (of__irrigation_from_GW.is_open())  of__irrigation_from_GW.close();
  if (of__ovf_in.is_open())  of__ovf_in.close();
  if (of__ovf_out.is_open())  of__ovf_out.close();
  if (of__ovf_toChn.is_open())  of__ovf_toChn.close();
  if (of__interf_in.is_open())  of__interf_in.close();
  if (of__interf_out.is_open())  of__interf_out.close();
  if (of__interf_toChn.is_open())  of__interf_toChn.close();
  if (of__GWf_in.is_open())  of__GWf_in.close();
  if (of__GWf_out.is_open())  of__GWf_out.close();
  if (of__GWf_toChn.is_open())  of__GWf_toChn.close();
  if (of__Q.is_open())  of__Q.close();
  if (of__Echan.is_open())  of__Echan.close();
  if (of__d18o_I.is_open())  of__d18o_I.close();
  if (of__d18o_snow.is_open())  of__d18o_snow.close();
  if (of__d18o_pond.is_open())  of__d18o_pond.close();
  if (of__d18o_layer1.is_open())  of__d18o_layer1.close();
  if (of__d18o_layer2.is_open())  of__d18o_layer2.close();
  if (of__d18o_layer3.is_open())  of__d18o_layer3.close();
  if (of__d18o_GW.is_open())  of__d18o_GW.close();
  if (of__d18o_chanS.is_open())  of__d18o_chanS.close();
  if (of__age_I.is_open())  of__age_I.close();
  if (of__age_snow.is_open())  of__age_snow.close();
  if (of__age_pond.is_open())  of__age_pond.close();
  if (of__age_layer1.is_open())  of__age_layer1.close();
  if (of__age_layer2.is_open())  of__age_layer2.close();
  if (of__age_layer3.is_open())  of__age_layer3.close();
  if (of__age_GW.is_open())  of__age_GW.close();
  if (of__age_chanS.is_open())  of__age_chanS.close();
  if (of__no3_I.is_open())  of__no3_I.close();
  if (of__no3_snow.is_open())  of__no3_snow.close();
  if (of__no3_pond.is_open())  of__no3_pond.close();
  if (of__no3_layer1.is_open())  of__no3_layer1.close();
  if (of__no3_layer2.is_open())  of__no3_layer2.close();
  if (of__no3_layer3.is_open())  of__no3_layer3.close();
  if (of__no3_GW.is_open())  of__no3_GW.close();
  if (of__no3_chanS.is_open())  of__no3_chanS.close();
  if (of__nitrogen_add.is_open())  of__nitrogen_add.close();
  if (of__plant_uptake.is_open())  of__plant_uptake.close();
  if (of__deni_soil.is_open())  of__deni_soil.close();
  if (of__minerl_soil.is_open())  of__minerl_soil.close();
  if (of__degrad_soil.is_open())  of__degrad_soil.close();
  if (of__deni_river.is_open())  of__deni_river.close();
  if (ctrl.report__I==2) delete _I_acc;
  if (ctrl.report__snow==2) delete _snow_acc;
  if (ctrl.report__pond==2) delete _pond_acc;
  if (ctrl.report__theta1==2) delete _theta1_acc;
  if (ctrl.report__theta2==2) delete _theta2_acc;
  if (ctrl.report__theta3==2) delete _theta3_acc;
  if (ctrl.report__GW==2) delete _GW_acc;
  if (ctrl.report__Th==2) delete _Th_acc;
  if (ctrl.report__snowmelt==2) delete _snowmelt_acc;
  if (ctrl.report__infilt==2) delete _infilt_acc;
  if (ctrl.report__Perc1==2) delete _Perc1_acc;
  if (ctrl.report__Perc2==2) delete _Perc2_acc;
  if (ctrl.report__Perc3==2) delete _Perc3_acc;
  if (ctrl.report__rinfilt==2) delete _rinfilt_acc;
  if (ctrl.report__rPerc1==2) delete _rPerc1_acc;
  if (ctrl.report__rPerc2==2) delete _rPerc2_acc;
  if (ctrl.report__rPerc3==2) delete _rPerc3_acc;
  if (ctrl.report__rrPerc3==2) delete _rrPerc3_acc;
  if (ctrl.report__Ei==2) delete _Ei_acc;
  if (ctrl.report__Es==2) delete _Es_acc;
  if (ctrl.report__Tr==2) delete _Tr_acc;
  if (ctrl.report__Tr1==2) delete _Tr1_acc;
  if (ctrl.report__Tr2==2) delete _Tr2_acc;
  if (ctrl.report__Tr3==2) delete _Tr3_acc;
  if (ctrl.report__irrigation_from_river==2) delete _irrigation_from_river_acc;
  if (ctrl.report__irrigation_from_GW==2) delete _irrigation_from_GW_acc;
  if (ctrl.report__ovf_in==2) delete _ovf_in_acc;
  if (ctrl.report__ovf_out==2) delete _ovf_out_acc;
  if (ctrl.report__ovf_toChn==2) delete _ovf_toChn_acc;
  if (ctrl.report__interf_in==2) delete _interf_in_acc;
  if (ctrl.report__interf_out==2) delete _interf_out_acc;
  if (ctrl.report__interf_toChn==2) delete _interf_toChn_acc;
  if (ctrl.report__GWf_in==2) delete _GWf_in_acc;
  if (ctrl.report__GWf_out==2) delete _GWf_out_acc;
  if (ctrl.report__GWf_toChn==2) delete _GWf_toChn_acc;
  if (ctrl.report__Q==2) delete _Q_acc;
  if (ctrl.report__Echan==2) delete _Echan_acc;
  if (ctrl.report__d18o_I==2) delete _d18o_I_acc;
  if (ctrl.report__d18o_snow==2) delete _d18o_snow_acc;
  if (ctrl.report__d18o_pond==2) delete _d18o_pond_acc;
  if (ctrl.report__d18o_layer1==2) delete _d18o_layer1_acc;
  if (ctrl.report__d18o_layer2==2) delete _d18o_layer2_acc;
  if (ctrl.report__d18o_layer3==2) delete _d18o_layer3_acc;
  if (ctrl.report__d18o_GW==2) delete _d18o_GW_acc;
  if (ctrl.report__d18o_chanS==2) delete _d18o_chanS_acc;
  if (ctrl.report__age_I==2) delete _age_I_acc;
  if (ctrl.report__age_snow==2) delete _age_snow_acc;
  if (ctrl.report__age_pond==2) delete _age_pond_acc;
  if (ctrl.report__age_layer1==2) delete _age_layer1_acc;
  if (ctrl.report__age_layer2==2) delete _age_layer2_acc;
  if (ctrl.report__age_layer3==2) delete _age_layer3_acc;
  if (ctrl.report__age_GW==2) delete _age_GW_acc;
  if (ctrl.report__age_chanS==2) delete _age_chanS_acc;
  if (ctrl.report__no3_I==2) delete _no3_I_acc;
  if (ctrl.report__no3_snow==2) delete _no3_snow_acc;
  if (ctrl.report__no3_pond==2) delete _no3_pond_acc;
  if (ctrl.report__no3_layer1==2) delete _no3_layer1_acc;
  if (ctrl.report__no3_layer2==2) delete _no3_layer2_acc;
  if (ctrl.report__no3_layer3==2) delete _no3_layer3_acc;
  if (ctrl.report__no3_GW==2) delete _no3_GW_acc;
  if (ctrl.report__no3_chanS==2) delete _no3_chanS_acc;
  if (ctrl.report__nitrogen_add==2) delete _nitrogen_add_acc;
  if (ctrl.report__plant_uptake==2) delete _plant_uptake_acc;
  if (ctrl.report__deni_soil==2) delete _deni_soil_acc;
  if (ctrl.report__minerl_soil==2) delete _minerl_soil_acc;
  if (ctrl.report__degrad_soil==2) delete _degrad_soil_acc;
  if (ctrl.report__deni_river==2) delete _deni_river_acc;
  /* end of Report */

  return EXIT_SUCCESS;

}