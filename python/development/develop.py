import os
import config_build
import linux_build
import define_variables
import parameterisation_build
import numpy as np
from def_develop import *


# new: array will be created internally
# spatial: array will be created based on external raster
# spatial_Ts: array will be created and updated (at each timestep) based on external binary
# spatial param: only parameter for each land use / soil type / climate type will be assigned


colNum = 5
                #var_name, if_relies_on_setting, comments, datatype, data source,
Climate = [ ['_P', [Opt.cond['none']], 'Precipitation [m]', 'grid', 'spatial_TS', 'Precipitation'],
            ['_Ta', [Opt.cond['none']], 'Air temperature [degree C]', 'grid', 'spatial_TS', 'Air_temperature'],
            #['_Tmin', [Opt.cond['none']], 'Minimum air temperature [degree C]', 'grid', 'spatial_TS', 'Minimal_air_temperature'],
            #['_Tmax', [Opt.cond['none']], 'Maximum air temperature [degree C]', 'grid', 'spatial_TS', 'Maximum_air_temperature'],
            ['_RH', [Opt.cond['none']], 'Relative humidity [decimal]', 'grid', 'spatial_TS', 'Relative_humidity'],
            ['_PET', [Opt.cond['evap_1']], 'Potential evapotranspiration [m]', 'grid', 'spatial_TS', 'Potential_evapotranspiration'],
            ['_LAI', [Opt.cond['none']], 'Leaf area index [decimal]', 'grid', 'spatial_TS', 'Leaf_area_index']
        ]
        
GIS = [ #['_dem', [Opt.cond['none']], 'Surface evelation [m]', 'grid', 'spatial', 'Ground_elevation'],
        #['_fdir', [Opt.cond['none']], 'Flow direction [d8 method]', 'grid', 'spatial', 'flow_direction'],
        ['_chnwidth', [Opt.cond['none']], 'Channel width [m]', 'grid', 'spatial', 'Channel_width'],
        ['_chndepth', [Opt.cond['none']], 'Channel depth [m]', 'grid', 'spatial', 'Channel_depth'],
        ['_chnlength', [Opt.cond['none']], 'Channel length [m]', 'grid', 'spatial', 'Channel_length'],
        ['_slope', [Opt.cond['none']], 'Slope [m/m]', 'grid', 'spatial', 'slope'],
        ['_depth1', [Opt.cond['none']], 'Depth of soil layer 1 [m]', 'grid', 'spatial', 'Soil_depth1'],
        ['_depth2', [Opt.cond['none']], 'Depth of soil layer 2 [m]', 'grid', 'spatial', 'Soil_depth2'],
        #['_Gauge_to_Report', [Opt.cond['none']], 'Gauges that require outputs', 'grid', 'spatial', 'Gauge_mask'],
        ['_sand1', [Opt.cond['none']], 'Sand content of layer 1 [decimal]', 'grid', 'spatial', 'sand1'],
        ['_sand2', [Opt.cond['depthprofile_3']], 'Sand content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'sand2'],
        ['_sand3', [Opt.cond['depthprofile_3']], 'Sand content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'sand3'],
        ['_clay1', [Opt.cond['none']], 'Clay content of layer 1 [decimal]', 'grid', 'spatial', 'clay1'],
        ['_clay2', [Opt.cond['depthprofile_3']], 'Clay content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'clay2'],
        ['_clay3', [Opt.cond['depthprofile_3']], 'Clay content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'clay3'],
        ['_silt1', [Opt.cond['pedotransf_1'], Opt.cond['pedotransf_2']], 'Silt content of layer 1 [decimal], only needed when opt_pedotransf = 1 or 2', 'grid', 'spatial', 'silt1'],
        ['_silt2', [Opt.cond['depthprofile_3']], 'Silt content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'silt2'],
        ['_silt3', [Opt.cond['depthprofile_3'], Opt.cond['pedotransf_2']], 'Silt content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'silt3'],
        ['_organic1', [Opt.cond['none']], 'Organic content of layer 1 [decimal]', 'grid', 'spatial', 'organic1'],
        ['_organic2', [Opt.cond['depthprofile_3']], 'Organic content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'organic2'],
        ['_organic3', [Opt.cond['depthprofile_3']], 'Organic content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'organic3'],
        ['_bulkdensity1', [Opt.cond['none']], 'Bulk density of layer 1 [g/cm3]', 'grid', 'spatial', 'bulk_density1'],
        ['_bulkdensity2', [Opt.cond['depthprofile_3']], 'Bulk density of layer 2 [g/cm3], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'bulk_density2'],
        ['_bulkdensity3', [Opt.cond['depthprofile_3']], 'Bulk density of layer 3 [g/cm3], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'bulk_density3'],
        ]


Storages = [['_I',       [Opt.cond['none']], 'Canopy storage [m]', 'grid', 'spatial', 'canopy_storage'], 
            ['_snow',    [Opt.cond['none']], 'Snow depth in [m]', 'grid', 'spatial', 'snow_depth'],
            ['_pond',    [Opt.cond['none']], 'Ponding water in [m]', 'grid', 'spatial', 'pond'],
            ['_theta1',  [Opt.cond['none']], 'Soil moisture in layer 1 [decimal]', 'grid', 'spatial', 'SMC_layer1'],
            ['_theta2',  [Opt.cond['none']], 'Soil moisture in layer 2 [decimal]', 'grid', 'spatial', 'SMC_layer2'],
            ['_theta3',  [Opt.cond['none']], 'Soil moisture in layer 3 [decimal]', 'grid', 'spatial', 'SMC_layer3'], 
            ['_GW',  [Opt.cond['none']], 'Groundwater storage [m]', 'grid', 'spatial', 'groundwater_storage'],
            ['_chanS',  [Opt.cond['none']], 'Channel storage [m3]', 'grid', 'new', None],                       
            ]

Fluxes   = [['_D', [Opt.cond['none']], 'Interception [m]', 'grid', 'new', 'interception'],
            ['_Th', [Opt.cond['none']], 'Throughfall [m]', 'grid', 'new', 'throufall'],
            ['_snowmelt', [Opt.cond['none']], 'Snow melt [m]', 'grid', 'new', 'snowmelt'],
            ['_infilt', [Opt.cond['none']], 'Inflitration into soil layer 1 [m]', 'grid', 'new', 'infiltration'],
            ['_Perc1', [Opt.cond['none']], 'Percolation into layer 2 [m]', 'grid', 'new', 'perc_layer1'],
            ['_Perc2', [Opt.cond['none']], 'Percolation into layer 3 [m]', 'grid', 'new', 'perc_layer2'],
            ['_Perc3', [Opt.cond['none']], 'Percolation into gw reservior [m]', 'grid', 'new', 'perc_layer3'],
            ['_Ei', [Opt.cond['none']], 'Canopy evaporation [m]', 'grid', 'new', 'canopy_evap'],
            ['_Es', [Opt.cond['none']], 'Soil evaporation [m]', 'grid', 'new', 'soil_evap'],
            ['_Tr', [Opt.cond['none']], 'Total transpiration in three layers [m]', 'grid', 'new', 'transp'],
            ['_Tr1', [Opt.cond['none']], 'Transpiration in layer 1 [m]', 'grid', 'new', 'transp_layer1'],
            ['_Tr2', [Opt.cond['none']], 'Transpiration in layer 2 [m]', 'grid', 'new', 'transp_layer2'],
            ['_Tr3', [Opt.cond['none']], 'Transpiration in layer 3 [m]', 'grid', 'new', 'transp_layer3'],

            


            ['_froot_soil', [Opt.cond['evap_1']], 'froot coefficient for all soil profile', 'grid', 'new', None],
            ['_froot_layer2', [Opt.cond['evap_1']], 'froot coefficient for layer 2', 'grid', 'new', None],
            ['_froot_layer3', [Opt.cond['evap_1']], 'froot coefficient for layer 3', 'grid', 'new', None],

            ['_Ks1', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 1', 'grid', 'new', None],
            ['_Ks2', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 2', 'grid', 'new', None],
            ['_Ks3', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 3', 'grid', 'new', None],
            ['_thetaS1', [Opt.cond['none']], 'Saturated soil moisture in layer 1', 'grid', 'new', None],
            ['_thetaS2', [Opt.cond['none']], 'Saturated soil moisture in layer 2', 'grid', 'new', None],
            ['_thetaS3', [Opt.cond['none']], 'Saturated soil moisture in layer 3', 'grid', 'new', None],
            ['_thetaFC1', [Opt.cond['none']], 'Field capacity in layer 1', 'grid', 'new', None],
            ['_thetaFC2', [Opt.cond['none']], 'Field capacity in layer 2', 'grid', 'new', None],
            ['_thetaFC3', [Opt.cond['none']], 'Field capacity in layer 3', 'grid', 'new', None],
            ['_thetaWP1', [Opt.cond['none']], 'Wilting point in layer 1', 'grid', 'new', None],
            ['_thetaWP2', [Opt.cond['none']], 'Wilting point in layer 2', 'grid', 'new', None],
            ['_thetaWP3', [Opt.cond['none']], 'Wilting point in layer 3', 'grid', 'new', None],

            ['_p_perc1', [Opt.cond['perc_1']], 'Percolation proportion in layer 1', 'grid', 'new', None],
            ['_p_perc2', [Opt.cond['perc_1']], 'Percolation proportion in layer 2', 'grid', 'new', None],
            ['_p_perc3', [Opt.cond['perc_1']], 'Percolation proportion in layer 3', 'grid', 'new', None],

            ['_ovf_in', [Opt.cond['none']], 'Overland flow from upstream cell(s) [m]', 'grid', 'new', 'overland_flow_input'],
            ['_ovf_out', [Opt.cond['none']], 'Overland flow to downstream cell [m]', 'grid', 'new', 'overland_flow_output'],
            ['_ovf_toChn', [Opt.cond['none']], 'Overland flow to Channel [m]', 'grid', 'new', 'overland_flow_toChn'],
            ['_interf_in', [Opt.cond['none']], 'Interflow from upstream cell(s) [m]', 'grid', 'new', 'interflow_input'],
            ['_interf_out', [Opt.cond['none']], 'Interflow to downstream cell [m]', 'grid', 'new', 'interflow_output'],
            ['_interf_toChn', [Opt.cond['none']], 'Interflow to Channel [m]', 'grid', 'new', 'interflow_toChn'],

            ['_gwf_toChn', [Opt.cond['none']], 'Groundwater flow to Channel [m]', 'grid', 'new', 'groundwater_flow_toChn'],

            ['_Q', [Opt.cond['none']], 'Discharge [m3/s]', 'grid', 'spatial', 'discharge'],
            ['_Qupstream', [Opt.cond['none']], 'Upstream inflow [m3/s]', 'grid', 'new', None],
            

            ]



Parameters = [['_depth3', [Opt.cond['none']], 'Depth of soil layer 3 [m]', 'grid', 'spatial_param', 'Soil_depth3'],
              ['_alpha', [Opt.cond['none']], 'The weighting parameter that links LAI and maximum canopy storage [-]', 'grid', 'spatial_param', 'alpha'],
              ['_rE', [Opt.cond['intecept_2'], Opt.cond['evap_1']], 'Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)', 'grid', 'spatial_param', 'rE'],
              ['_snow_rain_thre', [Opt.cond['snow_1']], 'The temperature for snow melt  [m]', 'grid', 'spatial_param', 'snow_rain_threshold'],
              ['_deg_day_min', [Opt.cond['snow_1']], 'Degree-day factor with no precipitation [m-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_min'],
              ['_deg_day_max', [Opt.cond['snow_1']], 'Maximum Degree-day factor [m-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_max'],
              ['_deg_day_increase', [Opt.cond['snow_1']], 'Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_increase'],
              
              ['_froot_coeff', [Opt.cond['evap_1']], 'Root fraction coefficient [-]', 'grid', 'spatial_param', 'froot_coeff'],

              ['_ref_thetaS', [Opt.cond['pedotransf_1']], 'Reference saturated soil moisture [-]', 'grid', 'spatial_param', 'ref_thetaS'],
              ['_PTF_VG_clay', [Opt.cond['pedotransf_1']], 'Pedotransfer function for parameter estimation of Van Genuchten Model [-]', 'grid', 'spatial_param', 'PTF_VG_clay'],
              ['_PTF_VG_Db', [Opt.cond['pedotransf_1']], 'Pedotransfer function for parameter estimation of Van Genuchten Model [-]', 'grid', 'spatial_param', 'PTF_VG_Db'],
              
              ['_PTF_Ks_const', [Opt.cond['pedotransf_1']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_Db'],
              ['_PTF_Ks_sand', [Opt.cond['pedotransf_1']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_sand'],
              ['_PTF_Ks_clay', [Opt.cond['pedotransf_1']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_clay'],
              ['_PTF_Ks_slope', [Opt.cond['pedotransf_1']], 'Slope correction for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_Ks_slope'],

              ['_SWP', [Opt.cond['fc_1']], 'Soil water potentail for field capacity estimation [-], only needed when opt_fieldcapacity = 1', 'grid', 'spatial_param', 'SWP'],

              ['_KvKh', [Opt.cond['infil_1'], Opt.cond['depthprofile_2']], 'The coefficient to transform Ks to effective Ks [-], only needed when opt_infil = 1', 'grid', 'spatial_param', 'KvKh'],
              ['_psiAE', [Opt.cond['infil_1'], Opt.cond['depthprofile_2']], 'The wetting front potential for Green-Ampt model [mm], only needed when opt_infil = 1', 'grid', 'spatial_param', 'psiAE'],

              ['_KKs', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent saturated hydraulic conductivity [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'Ksat'],
              ['_Ksat', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent saturated moisture content  [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'Kporos'],
              ['_BClambda', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent field capacity  [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'BClambda'],

              ['_pOvf_toChn', [Opt.cond['routinterf_1']], 'The weighting linear parameter for overland flow routing towards channel  [-]', 'grid', 'spatial_param', 'pOvf_toChn'],
              ['_interfExp', [Opt.cond['routinterf_1']], 'The exponetial weighting parameter for interflow flow routing towards channel  [-]', 'grid', 'spatial_param', 'interfExp'],
              ['_winterf', [Opt.cond['routinterf_1']], 'The weight parameter in kinematic wave solution  [-]', 'grid', 'spatial_param', 'winterf'],
              ['_GWfExp', [Opt.cond['routGWf_1']], 'The exponetial weighting parameter for GW flow routing towards channel  [-]', 'grid', 'spatial_param', 'GWfExp'],
              #['_wGWf', [Opt.cond['routinterf_1']], 'The weight parameter in kinematic wave solution  [-]', 'grid', 'spatial_param', 'wGWf'],
              ['_pActiveGW', [Opt.cond['routGWf_1']], 'The active proportion of GW storage that contributes to channel recharge  [-]', 'grid', 'spatial_param', 'pActiveGW'],

              ['_Manningn', [Opt.cond['routQ_1']], 'Manning N for stream routing [-], only needed when opt_routQ = 1', 'grid', 'spatial_param', 'Manningn'],
              

            ]
              


Reports = [Storages[j] for j in (np.squeeze(np.argwhere([i[4]=='spatial' for i in Storages])))]
Reports.extend(Fluxes) 


homepath = '/home/wusongj/GEM/GEM_generic_ecohydrological_model/'
path = homepath + 'codes/'
release_path = homepath + 'release_linux/'
archive_path = '/home/wusongj/GEM/archive_codes/'


signs_atmos = ['Climate']
datas_atmos = [Climate]

signs_basin = ['GIS', 'Storages', 'Fluxes']
datas_basin = [GIS, Storages, Fluxes]

signs_param = ['Parameters']
datas_param = [Parameters]

signs_control = signs_atmos + signs_basin + signs_param
datas_control = datas_atmos + datas_basin + datas_param




define_variables.includes(fname=path + 'includes/Atmosphere.h', signs=signs_atmos, datas=datas_atmos, max_category=setting.max_category)
define_variables.destructor(fname=path + 'Destructors/AtmosphereDestruct.cpp', signs=signs_atmos, datas=datas_atmos)


define_variables.constructor(fname=path + 'Constructors/AtmosphereConstruct.cpp', signs=signs_atmos, datas=datas_atmos)

define_variables.atmos_read_climate_maps(fname=path + 'Atmosphere/read_climate_maps.cpp', signs=signs_atmos, datas=datas_atmos)


define_variables.includes(fname=path + 'includes/Basin.h', signs=signs_basin, datas=datas_basin, max_category=setting.max_category)

define_variables.constructor(fname=path + 'Constructors/BasinConstruct.cpp', signs=signs_basin, datas=datas_basin)

define_variables.destructor(fname=path + 'Destructors/BasinDestruct.cpp', signs=signs_basin, datas=datas_basin)

define_variables.control_includes(fname=path + 'includes/Control.h', options=Opt.cond, signs=signs_control, datas=datas_control, reports=Reports)
config_build.read_configs(fname=path+'IO/readConfigFile.cpp', options=Opt.cond, signs=signs_control, datas=datas_control, reports=Reports)
config_build.gen_config_template(homepath, signs=signs_control, options=Opt.cond, datas=datas_control, reports=Reports, parameters=Parameters, max_category=setting.max_category)
config_build.report_build(fname=path+'IO/report.cpp', reports=Reports)


define_variables.includes(fname=path + 'includes/Param.h', signs=signs_param, datas=datas_param, max_category=setting.max_category)
define_variables.constructor(fname=path + 'Constructors/ParamConstruct.cpp', signs=signs_param, datas=datas_param)
config_build.read_param(fname=path+'IO/readParamFile.cpp', parameters=Parameters)
define_variables.destructor(fname=path + 'Destructors/ParamDestruct.cpp', signs=signs_param, datas=datas_param)
parameterisation_build.parameterisation_build(fname=path + 'Spatial/parameterisation.cpp', parameters=Parameters)




linux_build.release_linux(path, release_path)
linux_build.linux_make(release_path)


