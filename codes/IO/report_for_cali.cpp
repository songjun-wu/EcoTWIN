/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* report_for_cali.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Report_for_cali(Control &ctrl){
  
  // Only report discharge, in-stream d18o, and in-stream nitrate for calibration
  int length = ctrl._Tsmask.cell.size();
  int idx;
  for (int i = 0; i<ctrl._Tsmask.cell.size(); i++){
      idx = ctrl._Tsmask.cell[i];
      vector_Q.push_back(_Q->val[idx]);
      vector_d18o_chanS.push_back(_d18o_chanS->val[idx]);
      vector_no3_chanS.push_back(_no3_chanS->val[idx]);

      //if(ctrl.current_ts/86400 == 1) cout << i << "   "<< idx<<"   "<< _sortedGrid.row[idx] << "   "<<_sortedGrid.col[idx] << "   "<< _no3_layer3->val[idx] << endl;  // todo
  }

  return EXIT_SUCCESS;
}

int Basin::Save_for_cali(Control &ctrl){
  // Save outputs to binary files
  save_vector_to_binary(vector_Q, ctrl.path_ResultsFolder+"discharge_TS.bin");
  save_vector_to_binary(vector_d18o_chanS, ctrl.path_ResultsFolder+"d18o_chanS_TS.bin");
  save_vector_to_binary(vector_no3_chanS, ctrl.path_ResultsFolder+"no3_chanS_TS.bin") ;

  return EXIT_SUCCESS;
}


bool Basin::save_vector_to_binary(const std::vector<double>& vec, const std::string& filename) {
    // Open file in binary mode
    std::ofstream outFile(filename, std::ios::binary);
    
    if (!outFile.is_open()) {
        return false;
    }
    
    // Write the size of the vector first
    size_t size = vec.size();
    //outFile.write(reinterpret_cast<const char*>(&size), sizeof(size));
    
    // Write the vector data
    outFile.write(reinterpret_cast<const char*>(vec.data()), size * sizeof(double));
    
    // Check if writing was successful
    bool success = outFile.good();
    
    // Close the file
    outFile.close();
    
    return success;
}




