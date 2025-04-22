#include "Basin.h"

int Basin::ReadNitrogenFile(Control &ctrl, Param &par, string fname){
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


    /* Nitrogen addition */
    par.readIntoParam(fert_add, "fert_add", lines);
    par.readIntoParam(fert_day, "fert_day", lines);
    par.readIntoParam(fert_down, "fert_down", lines);
    par.readIntoParam(fert_period, "fert_period", lines);
    par.readIntoParam(manure_add, "manure_add", lines);
    par.readIntoParam(manure_day, "manure_day", lines);
    par.readIntoParam(manure_down, "manure_down", lines);
    par.readIntoParam(manure_period, "manure_period", lines);
    par.readIntoParam(residue_add, "residue_add", lines);
    par.readIntoParam(residue_day, "residue_day", lines);
    par.readIntoParam(residue_down, "residue_down", lines);
    par.readIntoParam(residue_period, "residue_period", lines);
    par.readIntoParam(up1, "up1", lines);
    par.readIntoParam(up2, "up2", lines);
    par.readIntoParam(up3, "up3", lines);
    par.readIntoParam(upper_uptake, "upper_uptake", lines);
    par.readIntoParam(plant_day, "plant_day", lines);
    par.readIntoParam(harvest_day, "harvest_day", lines);
    /* end of Nitrogen addition */

  input.close();

  return EXIT_SUCCESS;
}
