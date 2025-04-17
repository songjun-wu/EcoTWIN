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
  if (of__Ei.is_open())  of__Ei.close();
  if (of__Es.is_open())  of__Es.close();
  if (of__Tr.is_open())  of__Tr.close();
  if (of__Tr1.is_open())  of__Tr1.close();
  if (of__Tr2.is_open())  of__Tr2.close();
  if (of__Tr3.is_open())  of__Tr3.close();
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
  if (of__d18o_I.is_open())  of__d18o_I.close();
  if (of__d18o_snow.is_open())  of__d18o_snow.close();
  if (of__d18o_pond.is_open())  of__d18o_pond.close();
  if (of__d18o_layer1.is_open())  of__d18o_layer1.close();
  if (of__d18o_layer2.is_open())  of__d18o_layer2.close();
  if (of__d18o_layer3.is_open())  of__d18o_layer3.close();
  if (of__d18o_GW.is_open())  of__d18o_GW.close();
  if (of__d18o_chanS.is_open())  of__d18o_chanS.close();
  /* end of Report */

  return EXIT_SUCCESS;

}