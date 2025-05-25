#include "Param.h"

int Param::ReadParamFile(Control &ctrl, string fname){
    ifstream input;
    vector<string> lines;
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

  /* Parameters */
  readIntoParam(depth3, "depth3", lines);
  readIntoParam(alpha, "alpha", lines);
  readIntoParam(rE, "rE", lines);
  readIntoParam(snow_rain_thre, "snow_rain_thre", lines);
  readIntoParam(deg_day_min, "deg_day_min", lines);
  readIntoParam(deg_day_max, "deg_day_max", lines);
  readIntoParam(deg_day_increase, "deg_day_increase", lines);
  readIntoParam(froot_coeff, "froot_coeff", lines);
  readIntoParam(ref_thetaS, "ref_thetaS", lines);
  readIntoParam(PTF_VG_clay, "PTF_VG_clay", lines);
  readIntoParam(PTF_VG_Db, "PTF_VG_Db", lines);
  readIntoParam(PTF_Ks_const, "PTF_Ks_const", lines);
  readIntoParam(PTF_Ks_sand, "PTF_Ks_sand", lines);
  readIntoParam(PTF_Ks_clay, "PTF_Ks_clay", lines);
  readIntoParam(PTF_Ks_slope, "PTF_Ks_slope", lines);
  readIntoParam(SWP, "SWP", lines);
  readIntoParam(KvKh, "KvKh", lines);
  readIntoParam(psiAE, "psiAE", lines);
  readIntoParam(KKs, "KKs", lines);
  readIntoParam(Ksat, "Ksat", lines);
  readIntoParam(BClambda, "BClambda", lines);
  readIntoParam(percExp, "percExp", lines);
  readIntoParam(init_GW, "init_GW", lines);
  readIntoParam(wRecharge, "wRecharge", lines);
  readIntoParam(pOvf_toChn, "pOvf_toChn", lines);
  readIntoParam(interfExp, "interfExp", lines);
  readIntoParam(winterf, "winterf", lines);
  readIntoParam(GWfExp, "GWfExp", lines);
  readIntoParam(wGWf, "wGWf", lines);
  readIntoParam(Manningn, "Manningn", lines);
  readIntoParam(Echan_alpha, "Echan_alpha", lines);
  readIntoParam(irrigation_coeff, "irrigation_coeff", lines);
  readIntoParam(nearsurface_mixing, "nearsurface_mixing", lines);
  readIntoParam(ratio_to_interf, "ratio_to_interf", lines);
  readIntoParam(CG_n_soil, "CG_n_soil", lines);
  readIntoParam(d18o_init_GW, "d18o_init_GW", lines);
  readIntoParam(denitrification_river, "denitrification_river", lines);
  readIntoParam(denitrification_soil, "denitrification_soil", lines);
  readIntoParam(degradation_soil, "degradation_soil", lines);
  readIntoParam(mineralisation_soil, "mineralisation_soil", lines);
  readIntoParam(deni_soil_moisture_thres, "deni_soil_moisture_thres", lines);
  /* end of Parameters */

  input.close();

  return EXIT_SUCCESS;
}


void Param::readIntoParam(vector<double>& param_arr, string key, vector<string> lines){
    for (const auto& row : lines) {
        stringstream ss(row);
        string value;
        if (getline(ss, value, ',')) { // Read the first column as key
            if (value == key) { // Check if it matches the given key
                while (getline(ss, value, ',')) { // Read remaining values
                    try {
                        param_arr.push_back(stod(value)); // Convert string to double
                    } catch (const exception& e) {
                        cerr << "Error: Invalid number format in row." << endl;
                        return;
                    }
                }
                break; // Stop after finding the matching row
            }
         }
    }
}

