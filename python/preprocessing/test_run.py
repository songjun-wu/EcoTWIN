import numpy as np
import pandas as pd
import pcraster
import GIS_tools
import prep_tools

home_dir = '/home/wusongj/GEM/c1_dmc/'

nan_value = -9999

"""
# sort DEM and flow direction
dem = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/DEM.map'), np.nan)
ldd = GIS_tools.pcraster_ldd_to_d8(pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/ldd.map'), np.nan))
mask = np.logical_not(np.isnan(dem))
chanwidth = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/chanwidth.map'), np.nan)
chanmask = chanwidth>0

unit_soil = np.full(dem.shape, 1.0)
unit_chan = np.full(dem.shape, 1.0)
unit_soil[~mask] = np.nan
unit_chan[~chanmask] = np.nan

sorted_cells = GIS_tools.sort_grid_based_on_fdir(ldd)
dem = GIS_tools.modify_dem_based_on_fdir(dem, ldd, sorted_cells)
#fdir0 = pcraster.lddcreate('/home/wusongj/dmc/forHydrology/Spatial_500m/DEM.map', 1e9,1e9,1e9,1e9)
fdir = GIS_tools.d8_flow_direction(dem)
prep_tools.saveToASCII(dem, 'dem', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(fdir, 'fdir', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

# sort channel proporties

chanlength = unit_soil * 500
chandepth = chanwidth / 3

prep_tools.saveToASCII(chanwidth, 'chnwidth', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(chandepth, 'chndepth', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(chanlength, 'chnlength', home_dir+'spatial/', 'float64', chanmask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0.2, 'depth1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.2, 'depth2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.6, 'depth3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

GaugetoReport = pcraster.pcr2numpy(pcraster.readmap('/home/wusongj/dmc/forHydrology/Spatial_500m/Tsmask.map'), np.nan)
prep_tools.saveToASCII(GaugetoReport, 'GaugetoReport', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)

prep_tools.saveToASCII(unit_soil*0.0, 'I', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.0, 'snow', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta1', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta2', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
prep_tools.saveToASCII(unit_soil*0.3, 'theta3', home_dir+'spatial/', 'float64', mask, xllcorner=442449.229, yllcorner=5798066.25, cellsize=500, nodata=-9999)
"""

df = pd.read_csv('/home/wusongj/dmc/forHydrology/Climate/climate_interpolated.csv')
np.repeat(df['precip_3015'], 30*22).to_numpy().tofile(home_dir+'climate/P.bin')
np.repeat(df['Tmean_3015'], 30*22).to_numpy().tofile(home_dir+'climate/Ta.bin')
np.repeat(df['Tmin_3015'], 30*22).to_numpy().tofile(home_dir+'climate/Tmin.bin')
np.repeat(df['Tmax_3015'], 30*22).to_numpy().tofile(home_dir+'climate/Tmax.bin')

np.repeat(df['RH_3015'], 30*22).to_numpy().tofile(home_dir+'climate/RH.bin')
np.repeat(df['Tmax_3015'], 30*22).to_numpy().tofile(home_dir+'climate/Tmax.bin')
np.repeat(df['Tmax_3015'], 30*22).to_numpy().tofile(home_dir+'climate/Tmax.bin')
np.repeat(df['lai_2'], 30*22).to_numpy().tofile(home_dir+'climate/LAI.bin')
np.repeat(df['d2H_14dMV_3015'], 30*22).to_numpy().tofile(home_dir+'climate/d2h_P.bin')



