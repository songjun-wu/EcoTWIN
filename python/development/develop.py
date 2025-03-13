import os
import config_build
import linux_build
import define_variables
import numpy as np
from def_develop import *


Options = [['opt_climate_input_format', 'how is climate inputs orgainsed? 1 = raster; 2 = aggregated binary file (climate_zone file should be specified)'],
            ['opt_tracking_isotope', 'if enable isotopic tracking?'],
            ['opt_canopy', 'Which canopy process to use?']
            ]
colNum = 5
                #var_name, if_relies_on_setting, comments, datatype, data source,
Climate = [ ['_P', Opt.cond['none'], 'precipitation [m]', 'grid', 'spatial_TS', 'Precipitation'],
            ['_Ta', Opt.cond['none'], 'air temperature [degree C]', 'grid', 'spatial_TS', 'Air_temperature'],
            ['_Tmin', Opt.cond['none'], 'minimum air temperature [degree C]', 'grid', 'spatial_TS', 'Minimal_air_temperature'],
            ['_Tmax', Opt.cond['none'], 'maximum air temperature [degree C]', 'grid', 'spatial_TS', 'Maximum_air_temperature'],
            ['_RH', Opt.cond['none'], 'relative humidity [decimal]', 'grid', 'spatial_TS', 'Relative_humidity'],
            #['_PET', Opt.cond['none'], 'potential evapotranspiration [m]', 'grid', 'spatial_TS', 'PET'],
            ['_LAI', Opt.cond['none'], 'leaf area index [decimal]', 'grid', 'spatial_TS', 'LAI']
        ]
        
GIS = [ ['_dem', Opt.cond['none'], 'surface evelation [m]', 'grid', 'spatial', 'Ground_elevation'],
        ['_fdir', Opt.cond['none'], 'flow direction [d8 method]', 'grid', 'spatial', 'flow_direction'],
        ['_chnwidth', Opt.cond['none'], 'channel width [m]', 'grid', 'spatial', 'Channel_width'],
        ['_chndepth', Opt.cond['none'], 'channel depth [m]', 'grid', 'spatial', 'Channel_depth'],
        ['_chnlength', Opt.cond['none'], 'channel length [m]', 'grid', 'spatial', 'Channel_length'],
        ['_depth1', Opt.cond['none'], 'depth of soil layer 1 [m]', 'grid', 'spatial', 'Soil_depth1'],
        ['_depth2', Opt.cond['none'], 'depth of soil layer 2 [m]', 'grid', 'spatial', 'Soil_depth2'],
        ['_depth3', Opt.cond['none'], 'depth of soil layer 3 [m]', 'grid', 'spatial', 'Soil_depth3'],
        ['_Gauge_to_Report', Opt.cond['none'], 'Gauges that require outputs', 'grid', 'spatial', 'Gauge_mask'],
        ]


Storages = [['_I',       Opt.cond['none'], 'interception/canopy storage [m]', 'grid', 'spatial', 'inteception_storage'],
            ['_snow',    Opt.cond['none'], 'snow depth in [m]', 'grid', 'spatial', 'snow_depth'],
            ['_theta1',  Opt.cond['none'], 'soil moisture in layer 1 [decimal]', 'grid', 'spatial', 'SMC_layer1'],
            ['_theta2',  Opt.cond['none'], 'soil moisture in layer 2 [decimal]', 'grid', 'spatial', 'SMC_layer2'],
            ['_theta3',  Opt.cond['none'], 'soil moisture in layer 3 [decimal]', 'grid', 'spatial', 'SMC_layer3'],
            ['_I_old',   Opt.cond['none'], 'interception/canopy storage in previous timestep in [m]', 'grid', 'new', 'none'],
            #['_snow_old',    Opt.cond['none'], 'snow pack in previous timestep in [m]', 'grid', 'new', 'none'],
            #['_theta1_old',  Opt.cond['none'], 'soil moisture in layer 1 in previous timestep [decimal]', 'grid', 'new', 'none'],
            #['_theta2_old',  Opt.cond['none'], 'soil moisture in layer 2 in previous timestep [decimal]', 'grid', 'new', 'none'],
            #['_theta3_old',  Opt.cond['none'], 'soil moisture in layer 3 in previous timestep [decimal]', 'grid', 'new', 'none']                            
            ]

Fluxes   = [['_D', Opt.cond['none'], 'interception [m]', 'grid', 'new', 'interception'],
            ['_Th', Opt.cond['none'], 'throughfall [m]', 'grid', 'new', 'throufall'],
            ['_snowmelt', Opt.cond['none'], 'snow melt [m]', 'grid', 'new', 'snowmelt'],
            ['_Qs', Opt.cond['none'], 'overland flow [m]', 'grid', 'new', 'overland_flow'],
            ['_infilt', Opt.cond['none'], 'inflitration into soil layer 1 [m]', 'grid', 'new', 'infiltration'],
            ['_preferential2', Opt.cond['none'], 'preferential flow to layer 2 [m]', 'grid', 'new', 'preferential_flow_layer2'],
            ['_preferential3', Opt.cond['none'], 'preferential flow to layer 3 [m]', 'grid', 'new', 'preferential_flow_layer3'],
            ['_Perc1', Opt.cond['none'], 'percolation into layer 2 [m]', 'grid', 'new', 'perc_layer1'],
            ['_Perc2', Opt.cond['none'], 'percolation into layer 3 [m]', 'grid', 'new', 'perc_layer2'],
            ['_Perc3', Opt.cond['none'], 'percolation into gw reservior [m]', 'grid', 'new', 'perc_layer3'],
            ['_Ei', Opt.cond['none'], 'canopy evaporation [m]', 'grid', 'new', 'canopy_evap'],
            ['_Es', Opt.cond['none'], 'soil evaporation [m]', 'grid', 'new', 'soil_evap'],
            ['_Tr', Opt.cond['none'], 'total transpiration in three layers [m]', 'grid', 'new', 'transp'],
            ['_Tr1', Opt.cond['none'], 'transpiration in layer 1 [m]', 'grid', 'new', 'transp_layer1'],
            ['_Tr2', Opt.cond['none'], 'transpiration in layer 2 [m]', 'grid', 'new', 'transp_layer2'],
            ['_Tr3', Opt.cond['none'], 'transpiration in layer 3 [m]', 'grid', 'new', 'transp_layer3']
            ]


Reports = [Storages[j] for j in (np.squeeze(np.argwhere([i[4]=='spatial' for i in Storages])))]
Reports.extend(Fluxes) 


homepath = '/home/wusongj/GEM/'
path = homepath + 'codes/'
release_path = homepath + 'release_linux/'
archive_path = '/home/wusongj/GEM/archive_codes/'


signs_atmos = ['Climate']
datas_atmos = [Climate]

signs_basin = ['GIS', 'Storages', 'Fluxes']
datas_basin = [GIS, Storages, Fluxes]

signs_control = np.copy(signs_atmos).tolist()
datas_control = np.copy(datas_atmos).tolist()
signs_control.extend(signs_basin)
datas_control.extend(datas_basin)


""""""
define_variables.includes(fname=path + 'includes/Atmosphere.h', signs=signs_atmos, datas=datas_atmos)

define_variables.destructor(fname=path + 'Destructors/AtmosphereDestruct.cpp', signs=signs_atmos, datas=datas_atmos)

define_variables.constructor(fname=path + 'Constructors/AtmosphereConstruct.cpp', signs=signs_atmos, datas=datas_atmos)

define_variables.atmos_read_climate_maps(fname=path + 'Atmosphere/read_climate_maps.cpp', signs=signs_atmos, datas=datas_atmos)


define_variables.includes(fname=path + 'includes/Basin.h', signs=signs_basin, datas=datas_basin)

define_variables.constructor(fname=path + 'Constructors/BasinConstruct.cpp', signs=signs_basin, datas=datas_basin)

define_variables.destructor(fname=path + 'Destructors/BasinDestruct.cpp', signs=signs_basin, datas=datas_basin)

define_variables.control_includes(fname=path + 'includes/Control.h', options=Options, signs=signs_control, datas=datas_control, reports=Reports)
config_build.read_configs(fname=path+'Control/readConfigFile.cpp', options=Options, signs=signs_control, datas=datas_control, reports=Reports)
config_build.gen_config_template(homepath, signs=signs_control, options=Options, datas=datas_control, reports=Reports)
config_build.report_build(fname=path+'Control/report.cpp', reports=Reports)

linux_build.release_linux(path, release_path)
linux_build.linux_make(release_path)


