import numpy as np
import pandas as pd
import pcraster
import prep_tools
import os
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_net_radiation(shortwave_down, longwave_down, air_temperature, 
                            albedo=0.23, emissivity=0.96):
    """
    计算净辐射 R_n [W/m²]
    
    参数：
        shortwave_down: array-like, 短波入射辐射 [W/m²]
        longwave_down: array-like, 长波入射辐射 [W/m²]
        air_temperature: array-like, 空气温度 [°C]
        albedo: 地表反照率 (默认草地 0.23)
        emissivity: 地表发射率 (默认 0.96)
        
    返回：
        R_n: array-like, 净辐射 [W/m²]
    """
    # 常数
    sigma = 5.67e-8  # 斯特藩-玻尔兹曼常数 [W m-2 K-4]
    
    # 温度转为开尔文
    T_s_K = np.array(air_temperature) + 273.15
    
    # 计算各分量
    R_ns = (1 - albedo) * np.array(shortwave_down)  # 净短波辐射
    R_l_up = emissivity * sigma * T_s_K**4           # 向上长波
    R_nl = np.array(longwave_down) - R_l_up          # 净长波辐射
    
    R_n = R_ns + R_nl
    return R_n

home_dir = '/home/wusongj/GEM/test_dmc/'
nan_value = -9999


# sort DEM and flow direction
dem = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/DEM.map'), np.nan)
mask = np.logical_not(np.isnan(dem))
chanwidth = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/chanwidth.map'), np.nan)
chanmask = chanwidth>0

unit_soil = np.full(dem.shape, 1.0)
unit_chan = np.full(dem.shape, 1.0)
unit_soil[~mask] = np.nan
unit_chan[~chanmask] = np.nan


fdir = (prep_tools.pcraster_ldd_to_d8(pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/ldd.map'), np.nan))).astype(np.float64)
fdir[~mask] = nan_value
slope = prep_tools.cal_slope(dem, fdir, cellsize=500)

prep_tools.saveToASCII(dem, 'dem', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(fdir, 'fdir', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(slope, 'slope', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

# sort channel proporties
chanlength = unit_soil * 500
chanlength[~chanmask] = np.nan
chandepth = chanwidth / 3
""""""
prep_tools.saveToASCII(chanwidth, 'chnwidth', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(chandepth, 'chndepth', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(chanlength, 'chnlength', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0, 'climate_zones', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0.2, 'depth1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.2, 'depth2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.6, 'depth3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

GaugetoReport = np.full(unit_soil.shape, -9999.0)
GaugetoReport[10, 10] = 1   # 24
GaugetoReport[13, 10] = 1   # 25
GaugetoReport[15, 6] = 1    # 32
GaugetoReport[21, 5] = 1    # 26
GaugetoReport[23, 3] = 1    # 26x
GaugetoReport[26, 4] = 1    # 29a
prep_tools.saveToASCII(GaugetoReport, 'Gauge_to_Report', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0.0, 'I', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.0, 'snow', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.0, 'pond', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*20.0, 'GW', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.0, 'Q', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0.65, 'sand1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.63, 'sand2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.61, 'sand3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.1, 'clay1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.12, 'clay2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.14, 'clay3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.2, 'silt1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.18, 'silt2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.16, 'silt3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.08, 'organic1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.06, 'organic2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.04, 'organic3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*1.2, 'bulkdensity1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*1.4, 'bulkdensity2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*1.6, 'bulkdensity3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

### Tracking
prep_tools.saveToASCII(unit_soil*-8, 'd18o_I', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_snow', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_pond', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_layer1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_layer2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_layer3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_GW', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*-8, 'd18o_chanS', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)


### Nitrogen
prep_tools.saveToASCII(unit_soil*2, 'no3_I', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_snow', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_pond', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_layer1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_layer2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_layer3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_GW', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*2, 'no3_chanS', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

tmp = np.tile((unit_soil*1.0).flatten(), 50)
tmp.tofile(home_dir+'spatial/'+'category_0.bin')

fnames = ['unit.soil_BE', 'unit.soil_GL', 'unit.soil_PE', 'unit.soil_PZ', 'p_0', 'p_1', 'p_2', 'p_3' ]
#fnames = ['p_0', 'p_1', 'p_2', 'p_3', 'p_0', 'p_1', 'p_2', 'p_3' ]
for i in range(len(fnames)):
    tmp = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/'+fnames[i]+'.map'), np.nan).astype(np.float64)
    tmp[~mask] = nan_value
    tmp = np.tile(tmp.flatten(), 50)
    tmp.tofile(home_dir+'spatial/'+'category_'+str(i+1)+'.bin')

    data = tmp.reshape(50, 30, 22)[0,:,:]
    fig, ax = plt.subplots(1,1)
    data[data==nan_value] = np.nan
    im = ax.imshow(data)
    fig.colorbar(im, ax=ax)
    fig.savefig('/home/wusongj/GEM/test_dmc/spatial/2_cat_'+str(i+1)+'.png')


p0 = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/p_0.map'), np.nan).astype(np.float64)
p1 = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/p_1.map'), np.nan).astype(np.float64)
p2 = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/p_2.map'), np.nan).astype(np.float64)
p3 = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/p_3.map'), np.nan).astype(np.float64)

humusN = 8033
fastN = 200

prep_tools.saveToASCII(unit_soil*8033, 'humusN1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*8033, 'humusN2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*8033, 'humusN3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*200, 'fastN1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*200, 'fastN2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*200, 'fastN3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)





df = pd.read_csv('/home/wusongj/dmc/forHydrology/Climate/climate_interpolated_PET.csv')
np.repeat(df['precip_3015']/1000, 1).to_numpy().tofile(home_dir+'climate/P.bin')
np.repeat(df['Tmean_3015'], 1).to_numpy().tofile(home_dir+'climate/Ta.bin')
np.repeat(df['Tmin_3015'], 1).to_numpy().tofile(home_dir+'climate/Tmin.bin')
np.repeat(df['Tmax_3015'], 1).to_numpy().tofile(home_dir+'climate/Tmax.bin')

np.repeat(df['RH_3015']/100, 1).to_numpy().tofile(home_dir+'climate/RH.bin')
np.repeat(df['Tmax_3015'], 1).to_numpy().tofile(home_dir+'climate/Tmax.bin')
np.repeat(df['Tmax_3015'], 1).to_numpy().tofile(home_dir+'climate/Tmax.bin')

np.repeat(df['airPressure_3015']*100, 1).to_numpy().tofile(home_dir+'climate/airpressure.bin')  # hPa to Pa
np.repeat(df['windSpeed_3015'], 1).to_numpy().tofile(home_dir+'climate/windspeed.bin')

Rn = calculate_net_radiation(df['sdown'], df['ldown'], df['Tmean_3015'])
#np.savetxt('/data/scratch/wusongj/paper4/Rn.txt',Rn)
np.repeat(Rn, 1).tofile(home_dir+'climate/Rnet.bin')
np.repeat(df['d2H_14dMV_3015'], 1).to_numpy().tofile(home_dir+'climate/d2h_P.bin')
np.repeat(df['d18O_14dMV_3015'], 1).to_numpy().tofile(home_dir+'climate/d18o_P.bin')

pet = df['PET']/1000 / 1.2
np.repeat(pet, 1).to_numpy().tofile(home_dir+'climate/PET.bin')

print(np.mean(pet)*365)

lai = np.full((len(df['lai_2']), 9), -9999.0)
lai[:,5] = df['lai_0']
lai[:,6] = df['lai_1']
lai[:,7] = df['lai_2']
lai[:,8] = df['lai_3']
lai.flatten().tofile(home_dir+'climate/LAI.bin')


obs_q = np.fromfile('/home/wusongj/paper3_scripts/configs/discharge_obs.bin').reshape(4, -1)
print(obs_q.shape)

df = pd.read_csv('/home/wusongj/paper3_scripts/configs/obs_all.csv', index_col='time')
df.index = pd.to_datetime(df.index)
df = df.loc[datetime(1994,1,1):datetime(2022,1,1), :].loc[:, ['d18o_stream_25', 'd18o_stream_32', 'd18o_stream_26', 'd18o_stream_29a']]
arr = df.to_numpy().T
arr.tofile(home_dir + 'd18o_stream_obs.bin')


"""
os.chdir('/home/wusongj/GEM/test_dmc/spatial/')
fnames = os.listdir()
for fname in fnames:
    if '.asc' in fname and ('.png' not in fname):
        #print(fname)
        data = np.loadtxt(fname, skiprows=6)
        fig, ax = plt.subplots(1,1)
        data[data==nan_value] = np.nan
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax)
        fig.savefig('/home/wusongj/GEM/test_dmc/spatial/2_'+fname+'.png')
"""



