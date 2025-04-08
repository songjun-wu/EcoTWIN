import numpy as np
import pandas as pd
import os
import GEM_tools




path = '/home/wusongj/GEM/test/'


row = 7
col = 7


spatial_path = path + 'spatial/'
climate_path = path + 'climate/'

nodata = -9999.0

unit_mask = np.full((row,col), 1.0)
nodata_mask = np.full((row,col), np.nan)
chan_mask = np.full((row,col), np.nan)
chan_mask[:,col//2] = 1

tmp = np.repeat([6,5,4,0,5,7,9], row).reshape(row, col).T.astype(np.float64)
tmp[:, col//2] = np.linspace(0,4, row)
GEM_tools.save_to_ascii(data=GEM_tools.add_edge(tmp), path=spatial_path+'dem.asc', ref_path=spatial_path+'ref.asc')

tmp = np.repeat([1,1,1,4,16,16,16], row).reshape(row, col).T.astype(np.float64)
GEM_tools.save_to_ascii(data=GEM_tools.add_edge(tmp), path=spatial_path+'fdir.asc', ref_path=spatial_path+'ref.asc')

tmp = np.repeat([0.01,0.01,0.01,0.01,0.02,0.02,0.02], row).reshape(row, col).T.astype(np.float64)
GEM_tools.save_to_ascii(data=GEM_tools.add_edge(tmp), path=spatial_path+'slope.asc', ref_path=spatial_path+'ref.asc')

Gauge_to_Report = np.copy(nodata_mask)
Gauge_to_Report[[[0,1,2,3,4,5,6], [0,1,2,3,4,5,6]]] = 1
Gauge_to_Report[np.isnan(Gauge_to_Report)] = nodata
GEM_tools.save_to_ascii(data=GEM_tools.add_edge(Gauge_to_Report), path=spatial_path+'Gauge_to_Report.asc', ref_path=spatial_path+'ref.asc')


chnwidth = chan_mask * 10
chnlength = chan_mask * 100
chndepth = chan_mask * 2


climate_zones = unit_mask


climate_zones = unit_mask * 0

depth1 = unit_mask * 0.2
depth2 = unit_mask * 0.2
depth3 = unit_mask * 0.6

I = unit_mask * 0
snow = unit_mask * 0
pond = unit_mask * 0
theta1 = unit_mask * 0.3
theta2 = unit_mask * 0.3
theta3 = unit_mask * 0.3
GW = unit_mask * 20
sand1 = unit_mask * 0.3
sand2 = unit_mask * 0.25
sand3 = unit_mask * 0.2
clay1 = unit_mask * 0.1
clay2 = unit_mask * 0.15
clay3 = unit_mask * 0.2
silt1 = unit_mask * 0.5
silt2 = unit_mask * 0.55
silt3 = unit_mask * 0.6
organic1 = unit_mask * 0.08
organic2 = unit_mask * 0.06
organic3 = unit_mask * 0.04
bulkdensity1 = unit_mask * 1.2
bulkdensity2 = unit_mask * 1.4
bulkdensity3 = unit_mask * 1.6
Q = chan_mask * 0



fnames = ['climate_zones', 'chnwidth', 'chndepth', 'chnlength', 'depth1', 'depth2', 'I', 'snow', 'pond', 'theta1', 'theta2', 'theta3', 'GW',
          'sand1', 'sand2', 'sand3', 'clay1', 'clay2', 'clay3', 'silt1', 'silt2', 'silt3', 'organic1', 'organic2', 'organic3', 'bulkdensity1', 'bulkdensity2', 'bulkdensity3',
          'Q']
for i in range(len(fnames)):
    fname = fnames[i]
    data = GEM_tools.add_edge(locals()[fname], ext=1, no_data=nodata)
    data[np.isnan(data)] = nodata
    GEM_tools.save_to_ascii(data=data, path=spatial_path+fname+'.asc', ref_path=spatial_path+'ref.asc')

p_cat_list = [1, 0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.06, 0.04]
for i in range(len(p_cat_list)):
    _data = []
    for j in range(5):
        data = GEM_tools.add_edge(np.full((row, col), p_cat_list[i]), ext=1, no_data=nodata)
        _data = np.append(_data, data.flatten())
        data[np.isnan(data)] = nodata
        _data.tofile(spatial_path+'category_'+str(i)+'.bin')





# Climate inputs
df = pd.read_excel('/home/wusongj/dmc/forHydrology/Climate/climate_daily_AM_since2020.xlsx')
df1 = pd.read_csv('/home/wusongj/dmc/forHydrology/Climate/climate_interpolated.csv')
(np.repeat(df['Rain_corr_mm_Tot'], 1).to_numpy() / 1000).tofile(climate_path+'P.bin')
np.repeat(df['AirT_C_Avg'], 1).to_numpy().tofile(climate_path+'Ta.bin')


(np.repeat(df['RelHumid'], 1).to_numpy() / 100).tofile(climate_path+'RH.bin')

np.repeat(df1['lai_2'], 1).to_numpy().tofile(climate_path+'LAI.bin')
(np.repeat(df['pet'], 1).to_numpy()/1000).tofile(climate_path+'PET.bin')
np.repeat(df1['d2H_14dMV_3015'], 1).to_numpy().tofile(climate_path+'d2h_P.bin')




