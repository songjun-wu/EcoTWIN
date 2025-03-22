import numpy as np
import os
from def_GEM import *
import GEM_tools





spatial_path = Path.data_path + 'spatial/'

nodata = -9999.0

tmp = np.loadtxt(spatial_path + 'dem.asc', skiprows=6)
unit_nodata = np.full(tmp.shape, nodata)
unit_soil = np.full(tmp.shape, nodata)
unit_soil[tmp > 0] = 1

unit_zero = np.copy(unit_soil)
unit_zero[unit_soil==1] = 0


GEM_tools.save_to_ascii(data=unit_zero, path=spatial_path+'climate_zones.asc', ref_path=spatial_path+'dem.asc')

tmpp = np.copy(unit_nodata)
tmpp[200,200] = 0
GEM_tools.save_to_ascii(data=tmpp, path=spatial_path+'Gauge_to_Report.asc', ref_path=spatial_path+'dem.asc')


#for fname in ['chnwidth', 'chndepth', 'chnlength', 'depth1', 'depth2', 'depth3', 'I', 'snow', 'theta1', 'theta2', 'theta3']:
#    GEM_tools.save_to_ascii(data=unit_soil, path=spatial_path+fname+'.asc', ref_path=spatial_path+'dem.asc')

p_cat_list = [1, 0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.06, 0.04]
for i in range(len(p_cat_list)):
    p_cat = p_cat_list[i]
    GEM_tools.save_to_ascii(data=unit_soil*p_cat, path=spatial_path+'category_'+str(i)+'.asc', ref_path=spatial_path+'dem.asc')







