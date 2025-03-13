#include "Control.h"

Control::Control(){
  string confilename = "config.ini";

  ReadConfigFile(confilename);
  
  getAsciiHeader(path_BasinFolder+fn__dem);
  
}