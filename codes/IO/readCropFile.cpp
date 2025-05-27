/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* readCropFile.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::ReadCropFile(Control &ctrl, Param &par, string fname){
    ifstream input;
    vector<string> lines;
    vector<double> is_landuse;
    string s;
    
    // read all text in config file into string-based vector
    input.open(fname.c_str());
    if (!input.good()){
      throw runtime_error(string("file not found: ") + fname.c_str());
    }
  
    while (!input.eof()){
      input >> s;
      lines.push_back(s);
    }

    // Get the number of land use types, and the location of each land use type
    par.readIntoParam(is_landuse, "is_landuse", lines);
    num_landuse = 0;
    for (int i=0; i<is_landuse.size(); i++) {
      if (is_landuse[i] == 1){
        num_landuse += 1;
        landuse_idx.push_back(int(i));
      }
    }

    if (ctrl.opt_nitrogen_sim==1){
    /* Nitrogen addition */
    par.readIntoParam(fert_add, "fert_add", lines);
    par.readIntoParam(fert_day, "fert_day", lines);
    par.readIntoParam(fert_down, "fert_down", lines);
    par.readIntoParam(fert_period, "fert_period", lines);
    par.readIntoParam(fert_IN, "fert_IN", lines);
    par.readIntoParam(manure_add, "manure_add", lines);
    par.readIntoParam(manure_day, "manure_day", lines);
    par.readIntoParam(manure_down, "manure_down", lines);
    par.readIntoParam(manure_period, "manure_period", lines);
    par.readIntoParam(manure_IN, "manure_IN", lines);
    par.readIntoParam(residue_add, "residue_add", lines);
    par.readIntoParam(residue_day, "residue_day", lines);
    par.readIntoParam(residue_down, "residue_down", lines);
    par.readIntoParam(residue_period, "residue_period", lines);
    par.readIntoParam(residue_fastN, "residue_fastN", lines);
    par.readIntoParam(up1, "up1", lines);
    par.readIntoParam(up2, "up2", lines);
    par.readIntoParam(up3, "up3", lines);
    par.readIntoParam(upper_uptake, "upper_uptake", lines);
    par.readIntoParam(plant_day, "plant_day", lines);
    par.readIntoParam(harvest_day, "harvest_day", lines);
    /* end of Nitrogen addition */
    }

    if (ctrl.opt_irrigation==1){
    /* Irrigation */
    par.readIntoParam(irrigation_thres, "irrigation_thres", lines);
    /* end of Irrigation */
    }

  input.close();

  return EXIT_SUCCESS;
}
