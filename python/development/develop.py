import os
import sys
import config_build
import linux_build
import define_variables
import parameterisation_build
import numpy as np
from def_develop import *

# Get the directory containing script_a.py
current_dir = os.path.dirname(__file__)
# Go up one level to the project root
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# Add the sibling directory (dir_b) to sys.path
sys.path.insert(0, os.path.join(project_root, 'run_model'))


from def_GEM import Cali



# new: array will be created internally
# spatial: array will be created based on external raster
# spatial_Ts: array will be created and updated (at each timestep) based on external binary
# spatial param: only parameter for each land use / soil type / climate type will be assigned


colNum = 5
                #var_name, if_relies_on_setting, comments, datatype, data source,
Climate = [ ['_P', [Opt.cond['none']], 'Precipitation [m]', 'grid', 'spatial_TS', 'Precipitation', 0],
            ['_Ta', [Opt.cond['none']], 'Air temperature [degree C]', 'grid', 'spatial_TS', 'Air_temperature', 0],
            #['_Tmin', [Opt.cond['none']], 'Minimum air temperature [degree C]', 'grid', 'spatial_TS', 'Minimal_air_temperature', 0],
            #['_Tmax', [Opt.cond['none']], 'Maximum air temperature [degree C]', 'grid', 'spatial_TS', 'Maximum_air_temperature', 0],
            ['_RH', [Opt.cond['none']], 'Relative humidity [decimal]', 'grid', 'spatial_TS', 'Relative_humidity', 0],
            ['_PET', [Opt.cond['evap_1']], 'Potential evapotranspiration [m]', 'grid', 'spatial_TS', 'Potential_evapotranspiration', 0],

            ['_airpressure', [Opt.cond['chanE_1'], Opt.cond['chanE_2']], 'Air pressure [Pa]', 'grid', 'spatial_TS', 'Air_pressure', 0],
            ['_windspeed', [Opt.cond['chanE_1']], 'Wind speed at 2 m [m/s]', 'grid', 'spatial_TS', 'Wind_speed', 0],
            ['_Rnet', [Opt.cond['chanE_1'], Opt.cond['chanE_2']], 'Net radiation [W/m2]', 'grid', 'spatial_TS', 'Net_radiation', 0],
            ['_d18o_P', [Opt.cond['tracking_isotope_1']], 'd18O in precipitation [‰]', 'grid', 'spatial_TS', 'd18O_Precipitation', 0],
            
        ]

GroundTs = [
            ['_LAI', [Opt.cond['none']], 'Leaf area index [decimal]', 'grid', 'spatial_TS', 'Leaf_area_index', 0],
        ]
        
GIS = [ #['_dem', [Opt.cond['none']], 'Surface evelation [m]', 'grid', 'spatial', 'Ground_elevation', 0],
        #['_fdir', [Opt.cond['none']], 'Flow direction [d8 method]', 'grid', 'spatial', 'flow_direction', 0],
        ['_chnwidth', [Opt.cond['none']], 'Channel width [m]', 'grid', 'spatial', 'Channel_width', 0],
        ['_chndepth', [Opt.cond['none']], 'Channel depth [m]', 'grid', 'spatial', 'Channel_depth', 0],
        ['_chnlength', [Opt.cond['none']], 'Channel length [m]', 'grid', 'spatial', 'Channel_length', 0],
        ['_slope', [Opt.cond['none']], 'Slope [m/m]', 'grid', 'spatial', 'slope', 0],
        ['_depth1', [Opt.cond['none']], 'Depth of soil layer 1 [m]', 'grid', 'spatial', 'Soil_depth1', 0],
        ['_depth2', [Opt.cond['none']], 'Depth of soil layer 2 [m]', 'grid', 'spatial', 'Soil_depth2', 0],
        #['_Gauge_to_Report', [Opt.cond['none']], 'Gauges that require outputs', 'grid', 'spatial', 'Gauge_mask', 0],
        ['_sand1', [Opt.cond['none']], 'Sand content of layer 1 [decimal]', 'grid', 'spatial', 'sand1', 0],
        ['_sand2', [Opt.cond['depthprofile_3']], 'Sand content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'sand2', 0],
        ['_sand3', [Opt.cond['depthprofile_3']], 'Sand content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'sand3', 0],
        ['_clay1', [Opt.cond['none']], 'Clay content of layer 1 [decimal]', 'grid', 'spatial', 'clay1', 0],
        ['_clay2', [Opt.cond['depthprofile_3']], 'Clay content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'clay2', 0],
        ['_clay3', [Opt.cond['depthprofile_3']], 'Clay content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'clay3', 0],
        ['_silt1', [Opt.cond['pedotransf_1'], Opt.cond['pedotransf_2']], 'Silt content of layer 1 [decimal], only needed when opt_pedotransf = 1 or 2', 'grid', 'spatial', 'silt1', 0],
        ['_silt2', [Opt.cond['depthprofile_3']], 'Silt content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'silt2', 0],
        ['_silt3', [Opt.cond['depthprofile_3']], 'Silt content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'silt3', 0],
        ['_organic1', [Opt.cond['none']], 'Organic content of layer 1 [decimal]', 'grid', 'spatial', 'organic1', 0],
        ['_organic2', [Opt.cond['depthprofile_3']], 'Organic content of layer 2 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'organic2', 0],
        ['_organic3', [Opt.cond['depthprofile_3']], 'Organic content of layer 3 [decimal], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'organic3', 0],
        ['_bulkdensity1', [Opt.cond['none']], 'Bulk density of layer 1 [g/cm3]', 'grid', 'spatial', 'bulk_density1', 0],
        ['_bulkdensity2', [Opt.cond['depthprofile_3']], 'Bulk density of layer 2 [g/cm3], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'bulk_density2', 0],
        ['_bulkdensity3', [Opt.cond['depthprofile_3']], 'Bulk density of layer 3 [g/cm3], only needed when opt_depthprofile = 3', 'grid', 'spatial', 'bulk_density3', 0],
        ]


Storages = [['_I',       [Opt.cond['none']], 'Canopy storage [m]', 'grid', 'spatial', 'canopy_storage', 1], 
            ['_snow',    [Opt.cond['none']], 'Snow depth in [m]', 'grid', 'spatial', 'snow_depth', 1],
            ['_pond',    [Opt.cond['none']], 'Ponding water in [m]', 'grid', 'spatial', 'pond', 1],
            ['_theta1',  [Opt.cond['none']], 'Soil moisture in layer 1 [decimal]', 'grid', 'spatial', 'SMC_layer1', 1],
            ['_theta2',  [Opt.cond['none']], 'Soil moisture in layer 2 [decimal]', 'grid', 'spatial', 'SMC_layer2', 1],
            ['_theta3',  [Opt.cond['none']], 'Soil moisture in layer 3 [decimal]', 'grid', 'spatial', 'SMC_layer3', 1], 
            ['_GW',  [Opt.cond['none']], 'Groundwater storage [m]', 'grid', 'spatial', 'groundwater_storage', 1],
            ['_chanS',  [Opt.cond['none']], 'Channel storage [m3]', 'grid', 'new', None, 0],

            ['_I_old',       [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Canopy storage [m]', 'grid', 'new', None, 0], 
            ['_snow_old',    [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Snow depth in [m]', 'grid', 'new', None, 0],
            ['_pond_old',    [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Ponding water in [m]', 'grid', 'new', None, 0],
            ['_theta1_old',  [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Soil moisture in layer 1 [decimal]', 'grid', 'new', None, 0],
            ['_theta2_old',  [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Soil moisture in layer 2 [decimal]', 'grid', 'new', None, 0],
            ['_theta3_old',  [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Soil moisture in layer 3 [decimal]', 'grid', 'new', None, 0], 
            ['_GW_old',  [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Groundwater storage [m]', 'grid', 'new', None, 0],
            ['_chanS_old',  [Opt.cond['tracking_isotope_1'], Opt.cond['tracking_age_1'], Opt.cond['nitrogen_sim_1']], 'Channel storage [m3]', 'grid', 'new', None, 0],                      
            ]

Tracking = [['_d18o_I',   [Opt.cond['tracking_isotope_1']], 'd18o in Canopy storage [‰]', 'grid', 'spatial', 'd18o_canopy_storage', 1],
            ['_d18o_snow',    [Opt.cond['tracking_isotope_1']], 'd18o in Snow depth in [‰]', 'grid', 'spatial', 'd18o_snow_depth', 1],
            ['_d18o_pond',    [Opt.cond['tracking_isotope_1']], 'd18o in Ponding water in [‰]', 'grid', 'spatial', 'd18o_pond', 1],
            ['_d18o_layer1',  [Opt.cond['tracking_isotope_1']], 'd18o in Soil moisture in layer 1 [‰]', 'grid', 'spatial', 'd18o_SMC_layer1', 1],
            ['_d18o_layer2',  [Opt.cond['tracking_isotope_1']], 'd18o in Soil moisture in layer 2 [‰]', 'grid', 'spatial', 'd18o_SMC_layer2', 1],
            ['_d18o_layer3',  [Opt.cond['tracking_isotope_1']], 'd18o in Soil moisture in layer 3 [‰]', 'grid', 'spatial', 'd18o_SMC_layer3', 1], 
            ['_d18o_GW',  [Opt.cond['tracking_isotope_1']], 'd18o in Groundwater storage [‰]', 'grid', 'spatial', 'd18o_groundwater_storage', 1],
            ['_d18o_chanS',  [Opt.cond['tracking_isotope_1']], 'd18o in Channel storage [‰]', 'grid', 'spatial', 'd18o_chanS', 1],

            ['_d18o_ovf_in_acc',  [Opt.cond['tracking_isotope_1']], 'Total amount of 18o in overland inflow [‰ * m]', 'grid', 'new', None, 0],
            ['_d18o_interf_in_acc',  [Opt.cond['tracking_isotope_1']], 'Total amount of 18o in inter-inflow [‰ * m]', 'grid', 'new', None, 0],
            ['_d18o_GWf_in_acc',  [Opt.cond['tracking_isotope_1']], 'Total amount of 18o in GW inflow [‰ * m]', 'grid', 'new', None, 0],
            ['_d18o_Qupstream_acc', [Opt.cond['tracking_isotope_1']], 'Total amount of 18o in upstream inflow to channel storage [‰ * m]', 'grid', 'new', None, 0]
            ]



Fluxes   = [#['_D', [Opt.cond['none']], 'Interception [m]', 'grid', 'new', 'interception'],
            ['_Th', [Opt.cond['none']], 'Throughfall [m]', 'grid', 'new', 'throufall', 1],
            ['_snowmelt', [Opt.cond['none']], 'Snow melt [m]', 'grid', 'new', 'snowmelt', 1],
            ['_infilt', [Opt.cond['none']], 'Inflitration into soil layer 1 [m]', 'grid', 'new', 'infiltration', 1],
            ['_Perc1', [Opt.cond['none']], 'Percolation into layer 2 [m]', 'grid', 'new', 'perc_layer1', 1],
            ['_Perc2', [Opt.cond['none']], 'Percolation into layer 3 [m]', 'grid', 'new', 'perc_layer2', 1],
            ['_Perc3', [Opt.cond['none']], 'Percolation into gw reservior [m]', 'grid', 'new', 'perc_layer3', 1],

            ['_rinfilt', [Opt.cond['reinfil_1']], 'Reinflitration into soil layer 1 [m]', 'grid', 'new', 'rinfiltration', 1],
            ['_rPerc1', [Opt.cond['reinfil_1']], 'Repercolation into layer 2 due to overland flow routing [m]', 'grid', 'new', 'rperc_layer1', 1],
            ['_rPerc2', [Opt.cond['reinfil_1']], 'Repercolation into layer 3 due to overland flow routing [m]', 'grid', 'new', 'rperc_layer2', 1],
            ['_rPerc3', [Opt.cond['reinfil_1']], 'Repercolation into gw reservior due to overland flow routing [m]', 'grid', 'new', 'rperc_layer3', 1],
            ['_rrPerc3', [Opt.cond['none']], 'Repercolation into gw reservior due to interflow routing [m]', 'grid', 'new', 'rrperc_layer3', 1],


            
            ['_Ei', [Opt.cond['none']], 'Canopy evaporation [m]', 'grid', 'new', 'canopy_evap', 1],
            ['_Es', [Opt.cond['none']], 'Soil evaporation [m]', 'grid', 'new', 'soil_evap', 1],
            ['_Tr', [Opt.cond['none']], 'Total transpiration in three layers [m]', 'grid', 'new', 'transp', 1],
            ['_Tr1', [Opt.cond['none']], 'Transpiration in layer 1 [m]', 'grid', 'new', 'transp_layer1', 1],
            ['_Tr2', [Opt.cond['none']], 'Transpiration in layer 2 [m]', 'grid', 'new', 'transp_layer2', 1],
            ['_Tr3', [Opt.cond['none']], 'Transpiration in layer 3 [m]', 'grid', 'new', 'transp_layer3', 1],

            


            ['_froot_layer1', [Opt.cond['evap_1']], 'froot coefficient for all soil profile', 'grid', 'new', None, 0],
            ['_froot_layer2', [Opt.cond['evap_1']], 'froot coefficient for layer 2', 'grid', 'new', None, 0],
            ['_froot_layer3', [Opt.cond['evap_1']], 'froot coefficient for layer 3', 'grid', 'new', None, 0],

            ['_Ks1', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 1', 'grid', 'new', None, 0],
            ['_Ks2', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 2', 'grid', 'new', None, 0],
            ['_Ks3', [Opt.cond['none']], 'Saturated hydraulic conductivity in layer 3', 'grid', 'new', None, 0],
            ['_thetaS1', [Opt.cond['none']], 'Saturated soil moisture in layer 1', 'grid', 'new', None, 0],
            ['_thetaS2', [Opt.cond['none']], 'Saturated soil moisture in layer 2', 'grid', 'new', None, 0],
            ['_thetaS3', [Opt.cond['none']], 'Saturated soil moisture in layer 3', 'grid', 'new', None, 0],
            ['_thetaFC1', [Opt.cond['none']], 'Field capacity in layer 1', 'grid', 'new', None, 0],
            ['_thetaFC2', [Opt.cond['none']], 'Field capacity in layer 2', 'grid', 'new', None, 0],
            ['_thetaFC3', [Opt.cond['none']], 'Field capacity in layer 3', 'grid', 'new', None, 0],
            ['_thetaWP1', [Opt.cond['none']], 'Wilting point in layer 1', 'grid', 'new', None, 0],
            ['_thetaWP2', [Opt.cond['none']], 'Wilting point in layer 2', 'grid', 'new', None, 0],
            ['_thetaWP3', [Opt.cond['none']], 'Wilting point in layer 3', 'grid', 'new', None, 0],

            ['_p_perc1', [Opt.cond['perc_1']], 'Percolation proportion in layer 1', 'grid', 'new', None, 0],
            ['_p_perc2', [Opt.cond['perc_1']], 'Percolation proportion in layer 2', 'grid', 'new', None, 0],
            ['_p_perc3', [Opt.cond['perc_1']], 'Percolation proportion in layer 3', 'grid', 'new', None, 0],

            ['_ovf_in', [Opt.cond['none']], 'Overland flow from upstream cell(s) [m]', 'grid', 'new', 'overland_flow_input', 1],
            ['_ovf_out', [Opt.cond['none']], 'Overland flow to downstream cell [m]', 'grid', 'new', 'overland_flow_output', 1],
            ['_ovf_toChn', [Opt.cond['none']], 'Overland flow to Channel [m]', 'grid', 'new', 'overland_flow_toChn', 1],
            ['_interf_in', [Opt.cond['none']], 'Interflow from upstream cell(s) [m]', 'grid', 'new', 'interflow_input', 1],
            ['_interf_out', [Opt.cond['none']], 'Interflow to downstream cell [m]', 'grid', 'new', 'interflow_output', 1],
            ['_interf_toChn', [Opt.cond['none']], 'Interflow to Channel [m]', 'grid', 'new', 'interflow_toChn', 1],
            ['_GWf_in', [Opt.cond['none']], 'GW flow from upstream cell(s) [m]', 'grid', 'new', 'GWflow_input', 1],
            ['_GWf_out', [Opt.cond['none']], 'GW flow to downstream cell [m]', 'grid', 'new', 'GWflow_output', 1],
            ['_GWf_toChn', [Opt.cond['none']], 'Groundwater flow to Channel [m]', 'grid', 'new', 'GWflow_toChn', 1],

            ['_Q', [Opt.cond['none']], 'Discharge [m3/s]', 'grid', 'spatial', 'discharge', 1],
            ['_Qupstream', [Opt.cond['none']], 'Upstream inflow [m3/s]', 'grid', 'new', None, 0],

            ['_Echan', [Opt.cond['none']], 'Channel evaporation [m]', 'grid', 'new', 'channel_evaporation', 1],


            
            # internal variables
            ['_PE', [Opt.cond['evap_1']], 'Potential evaporation [m]', 'grid', 'new', None, 0],
            ['_PT', [Opt.cond['evap_1']], 'Potential transpiration [m]', 'grid', 'new', None, 0],
            ['_tmp', [Opt.cond['none']], 'Temporal variable for testing [-]', 'grid', 'new', None, 0],
            ['_snowacc', [Opt.cond['none']], 'Snow accumulation for testing [m]', 'grid', 'new', None, 0],
            ['_TchanS', [Opt.cond['none']], "Instream temperature conceptualised as 20-day's average of air temperature [degree C]", 'grid', 'new', None, 0],

            ]



Parameters = [['_depth3', [Opt.cond['none']], 'Depth of soil layer 3 [m]', 'grid', 'spatial_param', 'Soil_depth3', 0],
              ['_alpha', [Opt.cond['none']], 'The weighting parameter that links LAI and maximum canopy storage [-]', 'grid', 'spatial_param', 'alpha', 0],
              ['_rE', [Opt.cond['intecept_2'], Opt.cond['evap_1']], 'Parameter regulates the surface cover fraction, rExtinct = -0.463 Rutter (1972)', 'grid', 'spatial_param', 'rE', 0],
              ['_snow_rain_thre', [Opt.cond['snow_1']], 'The temperature for snow melt  [m]', 'grid', 'spatial_param', 'snow_rain_threshold', 0],
              ['_deg_day_min', [Opt.cond['snow_1']], 'Degree-day factor with no precipitation [m-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_min', 0],
              ['_deg_day_max', [Opt.cond['snow_1']], 'Maximum Degree-day factor [m-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_max', 0],
              ['_deg_day_increase', [Opt.cond['snow_1']], 'Increase of the Degree-day factor per mm of increase in precipitation precipitation [s-1 degreeC-1]', 'grid', 'spatial_param', 'deg_day_increase', 0],
              
              ['_froot_coeff', [Opt.cond['evap_1']], 'Root fraction coefficient [-]', 'grid', 'spatial_param', 'froot_coeff', 0],
              # Pedotransfer function
              ['_ref_thetaS', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Reference saturated soil moisture [-]', 'grid', 'spatial_param', 'ref_thetaS', 0],
              ['_PTF_VG_clay', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Pedotransfer function for parameter estimation of Van Genuchten Model [-]', 'grid', 'spatial_param', 'PTF_VG_clay', 0],
              ['_PTF_VG_Db', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Pedotransfer function for parameter estimation of Van Genuchten Model [-]', 'grid', 'spatial_param', 'PTF_VG_Db', 0],
              
              ['_PTF_Ks_const', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_Db', 0],
              ['_PTF_Ks_sand', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_sand', 0],
              ['_PTF_Ks_clay', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Pedotransfer parameter for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_clay', 0],
              ['_PTF_Ks_slope', [Opt.cond['pedotransf_1'],Opt.cond['pedotransf_2'],Opt.cond['pedotransf_3']], 'Slope correction for estimation of saturated hydraulic conductivity [-]', 'grid', 'spatial_param', 'PTF_Ks_slope', 0],

              ['_SWP', [Opt.cond['fc_1']], 'Soil water potentail for field capacity estimation [-], only needed when opt_fieldcapacity = 1', 'grid', 'spatial_param', 'SWP', 0],
              # Infiltration
              ['_KvKh', [Opt.cond['infil_1'], Opt.cond['depthprofile_2']], 'The coefficient to transform Ks to effective Ks [-], only needed when opt_infil = 1', 'grid', 'spatial_param', 'KvKh', 0],
              ['_psiAE', [Opt.cond['infil_1'], Opt.cond['depthprofile_2']], 'The wetting front potential for Green-Ampt model [mm], only needed when opt_infil = 1', 'grid', 'spatial_param', 'psiAE', 0],
              ['_KKs', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent saturated hydraulic conductivity [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'Ksat', 0],
              ['_Ksat', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent saturated moisture content  [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'Kporos', 0],
              ['_BClambda', [Opt.cond['depthprofile_2']], 'The exponential parameter for depth-dependent field capacity  [-], only needed when opt_depthprofile = 2', 'grid', 'spatial_param', 'BClambda', 0],
              
              # Percolation
              ['_percExp', [Opt.cond['perc_2']], 'The exponential parameter for percolation [-], only needed when opt_percolation = 2', 'grid', 'spatial_param', 'percExp', 0],

              # GW
              
              ['_init_GW', [Opt.cond['init_GW_1']], 'The initial GW storage [m], only needed when opt_init_GW = 1', 'grid', 'spatial_param', 'init_GW', 0],
              ['_wRecharge', [Opt.cond['none']], 'The weighting parameter for GW recharge [-], only needed when opt_recharge = 1', 'grid', 'spatial_param', 'wRecharge', 0],

              
              # Routing
              ['_pOvf_toChn', [Opt.cond['routinterf_1']], 'The weighting linear parameter for overland flow routing towards channel  [-]', 'grid', 'spatial_param', 'pOvf_toChn', 0],
              ['_interfExp', [Opt.cond['routinterf_1']], 'The exponetial weighting parameter for interflow flow routing towards channel  [-]', 'grid', 'spatial_param', 'interfExp', 0],
              ['_winterf', [Opt.cond['routinterf_1']], 'The weight parameter in kinematic wave solution  [-]', 'grid', 'spatial_param', 'winterf', 0],
              ['_GWfExp', [Opt.cond['routGWf_1']], 'The exponetial weighting parameter for GW flow routing towards channel  [-]', 'grid', 'spatial_param', 'GWfExp', 0],
              #['_wGWf', [Opt.cond['routGWf_1']], 'The weight parameter in kinematic wave solution  [-]', 'grid', 'spatial_param', 'wGWf', 0],
              ['_wGWf', [Opt.cond['routGWf_1']], 'The active proportion of GW storage that contributes to channel recharge  [-]', 'grid', 'spatial_param', 'wGWf', 0],
              ['_Manningn', [Opt.cond['routQ_1']], 'Manning N for stream routing [-], only needed when opt_routQ = 1', 'grid', 'spatial_param', 'Manningn', 0],

              # Channel 
              ['_Echan_alpha', [Opt.cond['chanE_1'], Opt.cond['chanE_2']], 'orrection factor in Priestley-Taylor equation [-], only needed when opt_chanE = 1 or 2', 'grid', 'spatial_param', 'Echan_alpha', 0],

              # Mixing
              ['_nearsurface_mixing', [Opt.cond['none']], 'The proportion of pond to mix with layer1  [decimal]', 'grid', 'spatial_param', 'nearsurface_mixing', 0],
              ['_ratio_to_interf', [Opt.cond['none']], 'The proportion of excess storage in layer 1 that routs as interflow (otherwise percolate to GW) [decimal]', 'grid', 'spatial_param', 'ratio_to_interf', 0],

              # Tracking
              ['_CG_n_soil', [Opt.cond['tracking_isotope_1']], 'Parameter N in CG model for soil water fractionation [-]', 'grid', 'spatial_param', 'CG_n_soil', 0],
              ['_d18o_init_GW', [Opt.cond['tracking_isotope_1']], 'Initial d18O of GW storage [‰]', 'grid', 'spatial_param', 'd18o_init_GW', 0],
              
              

              # Nitrogen
              ['_denitrification_river', [Opt.cond['nitrogen_sim_1']], 'Reference rates of aquatic denitrification [-]', 'grid', 'spatial_param', 'denitrification_river', 0],
              #['_autotrophic_uptake_aquatic', [Opt.cond['nitrogen_sim_1']], 'Reference rates of aquatic autotrophic uptake [-]', 'grid', 'spatial_param', 'autotrophic_uptake_aquatic', 0],
              #['_primary_production_aquatic', [Opt.cond['nitrogen_sim_1']], 'Reference rates of aquatic primary production [-]', 'grid', 'spatial_param', 'primary_production_aquatic', 0],
              ['_denitrification_soil', [Opt.cond['nitrogen_sim_1']], 'Reference rates of soil denitrification [kg/ha]', 'grid', 'spatial_param', 'denitrification_soil', 0],
              ['_degradation_soil', [Opt.cond['nitrogen_sim_1']], 'Reference rates of soil degradation [kg/ha]', 'grid', 'spatial_param', 'degradation_soil', 0],
              ['_mineralisation_soil', [Opt.cond['nitrogen_sim_1']], 'Reference rates of soil mineralisation [kg/ha]', 'grid', 'spatial_param', 'mineralisation_soil', 0],
              #['_dissolution_soil', [Opt.cond['nitrogen_sim_1']], 'Reference rates of soil dissolution [kg/ha]', 'grid', 'spatial_param', 'dissolution_soil', 0],              
            ]

Nitrogen = [['_no3_I',   [Opt.cond['nitrogen_sim_1']], 'no3 in Canopy storage [mgN/L]', 'grid', 'spatial', 'no3_canopy_storage', 1],
            ['_no3_snow',    [Opt.cond['nitrogen_sim_1']], 'no3 in Snow depth in [mgN/L]', 'grid', 'spatial', 'no3_snow_depth', 1],
            ['_no3_pond',    [Opt.cond['nitrogen_sim_1']], 'no3 in Ponding water in [mgN/L]', 'grid', 'spatial', 'no3_pond', 1],
            ['_no3_layer1',  [Opt.cond['nitrogen_sim_1']], 'no3 in Soil moisture in layer 1 [mgN/L]', 'grid', 'spatial', 'no3_SMC_layer1', 1],
            ['_no3_layer2',  [Opt.cond['nitrogen_sim_1']], 'no3 in Soil moisture in layer 2 [mgN/L]', 'grid', 'spatial', 'no3_SMC_layer2', 1],
            ['_no3_layer3',  [Opt.cond['nitrogen_sim_1']], 'no3 in Soil moisture in layer 3 [mgN/L]', 'grid', 'spatial', 'no3_SMC_layer3', 1], 
            ['_no3_GW',  [Opt.cond['nitrogen_sim_1']], 'no3 in Groundwater storage [mgN/L]', 'grid', 'spatial', 'no3_groundwater_storage', 1],
            ['_no3_chanS',  [Opt.cond['nitrogen_sim_1']], 'no3 in Channel storage [mgN/L]', 'grid', 'spatial', 'no3_chanS', 1],

            # Nitrogen
            ['_nitrogen_add', [Opt.cond['nitrogen_sim_1']], 'Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]', 'grid', 'new', 'nitrogen_addition', 1],
            ['_plant_uptake', [Opt.cond['nitrogen_sim_1']], 'Plant uptake [mgN/L*m = gN/m2]', 'grid', 'new', 'plant_uptake', 1],
            ['_deni_soil', [Opt.cond['nitrogen_sim_1']], 'Soil denitrification [mgN/L*m = gN/m2]', 'grid', 'new', 'deni_soil', 1],
            ['_minerl_soil', [Opt.cond['nitrogen_sim_1']], 'Soil mineralisation [mgN/L*m = gN/m2]', 'grid', 'new', 'minerl_soil', 1],
            ['_degrad_soil', [Opt.cond['nitrogen_sim_1']], 'Soil degradation [mgN/L*m = gN/m2]', 'grid', 'new', 'degrad_soil', 1],
            ['_deni_river', [Opt.cond['nitrogen_sim_1']], 'Aquatic denitrification [mgN/L*m = gN/m2]', 'grid', 'new', 'deni_river', 1],

            # Internal fluxes
            ['_humusN1',  [Opt.cond['nitrogen_sim_1']], 'Humus nitrogen storage in layer 1 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'humusN1', 0],
            ['_humusN2',  [Opt.cond['nitrogen_sim_1']], 'Humus nitrogen storage in layer 2 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'humusN2', 0],
            ['_humusN3',  [Opt.cond['nitrogen_sim_1']], 'Humus nitrogen storage in layer 3 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'humusN3', 0],

            ['_fastN1',  [Opt.cond['nitrogen_sim_1']], 'Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'fastN1', 0],
            ['_fastN2',  [Opt.cond['nitrogen_sim_1']], 'Fast nitrogen storage in layer 2 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'fastN2', 0],
            ['_fastN3',  [Opt.cond['nitrogen_sim_1']], 'Fast nitrogen storage in layer 3 [mgN/L*m = gN/m2]', 'grid', 'spatial', 'fastN3', 0],


            ['_no3_ovf_in_acc',  [Opt.cond['nitrogen_sim_1']], 'Total amount of 18o in overland inflow [mgN/L*m = gN/m2]', 'grid', 'new', None, 0],
            ['_no3_interf_in_acc',  [Opt.cond['nitrogen_sim_1']], 'Total amount of 18o in inter-inflow [mgN/L*m = gN/m2]', 'grid', 'new', None, 0],
            ['_no3_GWf_in_acc',  [Opt.cond['nitrogen_sim_1']], 'Total amount of 18o in GW inflow [mgN/L*m = gN/m2]', 'grid', 'new', None, 0],
            ['_no3_Qupstream_acc', [Opt.cond['nitrogen_sim_1']], 'Total amount of 18o in upstream inflow to channel storage [mgN/L*m = gN/m2]', 'grid', 'new', None, 0]
            ]

Nitrogen_addition = [['fert_add', [Opt.cond['nitrogen_sim_1']], 'Fertilizer addition [mgN/L*m = gN/m2]', 'vector', 'vector', None, 0],
                     ['fert_day', [Opt.cond['nitrogen_sim_1']], 'Day of year to start fertilization [day]', 'vector', 'vector', None, 0],
                     ['fert_down', [Opt.cond['nitrogen_sim_1']], 'The proportion of fertilizer reaching deep soil [decimal]', 'vector', 'vector', None, 0],
                     ['fert_period', [Opt.cond['nitrogen_sim_1']], 'The duration of fertilization [day]', 'vector', 'vector', None, 0],
                     ['fert_IN', [Opt.cond['nitrogen_sim_1']], 'The proportion of fertilization that goes to IN pool [decimal]', 'vector', 'vector', None, 0],
                     

                     ['manure_add', [Opt.cond['nitrogen_sim_1']], 'Manure addition [mgN/L*m = gN/m2]', 'gvectorrid', 'vector', None, 0],
                     ['manure_day', [Opt.cond['nitrogen_sim_1']], 'Day of year to start manure addtion [day]', 'vector', 'vector', None, 0],
                     ['manure_down', [Opt.cond['nitrogen_sim_1']], 'The proportion of manure reaching deep soil [decimal]', 'vector', 'vector', None, 0],
                     ['manure_period', [Opt.cond['nitrogen_sim_1']], 'The duration of manure addition [day]', 'vector', 'vector', None, 0],
                     ['manure_IN', [Opt.cond['nitrogen_sim_1']], 'The proportion of manure that goes to IN pool [decimal]', 'vector', 'vector', None, 0],

                     ['residue_add', [Opt.cond['nitrogen_sim_1']], 'Residue addition [mgN/L*m = gN/m2]', 'vector', 'vector', None, 0],
                     ['residue_day', [Opt.cond['nitrogen_sim_1']], 'Day of year to start residue addtion [day]', 'vector', 'vector', None, 0],
                     ['residue_down', [Opt.cond['nitrogen_sim_1']], 'The proportion of residue reaching deep soil [decimal]', 'vector', 'vector', None, 0],
                     ['residue_period', [Opt.cond['nitrogen_sim_1']], 'The duration of residue addition [day]', 'vector', 'vector', None, 0],
                     ['residue_fastN', [Opt.cond['nitrogen_sim_1']], 'The proportion of residue that goes to fastN pool [decimal]', 'vector', 'vector', None, 0],

                     ['up1', [Opt.cond['nitrogen_sim_1']], '  ', 'vector', 'vector', None, 0],
                     ['up2', [Opt.cond['nitrogen_sim_1']], '  ', 'vector', 'vector', None, 0],
                     ['up3', [Opt.cond['nitrogen_sim_1']], '  ', 'vector', 'vector', None, 0],

                     ['upper_uptake', [Opt.cond['nitrogen_sim_1']], 'Proportion of IN uptook from upper soil [decimal]', 'vector', 'vector', None, 0],
                     

                     ['plant_day', [Opt.cond['nitrogen_sim_1']], 'Day of year for vegetation planting [day]', 'vector', 'vector', None, 0],
                     ['harvest_day', [Opt.cond['nitrogen_sim_1']], 'Day of year for vegetation harvest [day]', 'vector', 'vector', None, 0],
                    ]


Reports = [Storages[j] for j in (np.squeeze(np.argwhere([i[4]=='spatial' for i in Storages])))]
Reports.extend(Fluxes)
Reports.extend(Tracking)
Reports.extend(Nitrogen)


homepath = '/home/wusongj/GEM/GEM_generic_ecohydrological_model/'
path = homepath + 'codes/'
release_path = homepath + 'release_linux/'
archive_path = '/home/wusongj/GEM/archive_codes/'


signs_atmos = ['Climate']
datas_atmos = [Climate]

signs_groundTs = ['GroundTs']
datas_groundTs = [GroundTs]

signs_basin = ['GIS', 'Storages', 'Fluxes', 'Tracking', 'Nitrogen']
datas_basin = [GIS, Storages, Fluxes, Tracking, Nitrogen]

signs_param = ['Parameters']
datas_param = [Parameters]

signs_control = signs_atmos + signs_groundTs + signs_basin + signs_param
datas_control = datas_atmos + datas_groundTs + datas_basin + datas_param




define_variables.includes(fname=path + 'includes/Atmosphere.h', signs=signs_atmos, datas=datas_atmos, max_category=setting.max_category)
define_variables.destructor(fname=path + 'Destructors/AtmosphereDestruct.cpp', signs=signs_atmos, datas=datas_atmos)


define_variables.constructor(fname=path + 'Constructors/AtmosphereConstruct.cpp', signs=signs_atmos, datas=datas_atmos)

define_variables.atmos_read_climate_maps(fname=path + 'Atmosphere/read_climate_maps.cpp', signs=signs_atmos, datas=datas_atmos)


define_variables.includes(fname=path + 'includes/Basin.h', signs=signs_groundTs+signs_basin, datas=datas_groundTs+datas_basin, max_category=setting.max_category)
define_variables.constructor(fname=path + 'Constructors/BasinConstruct.cpp', signs=signs_groundTs+signs_basin, datas=datas_groundTs+datas_basin)
define_variables.destructor(fname=path + 'Destructors/BasinDestruct.cpp', signs=signs_groundTs+signs_basin, datas=datas_groundTs+datas_basin)
define_variables.basin_read_groundTs_maps(fname=path + 'Atmosphere/read_groundTs_maps.cpp', signs=signs_groundTs, datas=datas_groundTs)

define_variables.control_includes(fname=path + 'includes/Control.h', options=Opt.cond, signs=signs_control, datas=datas_control, reports=Reports, static_config=Cali.static_config)
config_build.read_configs(fname=path+'IO/readConfigFile.cpp', options=Opt.cond, signs=signs_control, datas=datas_control, reports=Reports, static_config=Cali.static_config)
config_build.gen_config_template(homepath, signs=signs_control, options=Opt.cond, datas=datas_control, reports=Reports, parameters=Parameters, max_category=setting.max_category)



define_variables.includes(fname=path + 'includes/Param.h', signs=signs_param, datas=datas_param, max_category=setting.max_category)
define_variables.constructor(fname=path + 'Constructors/ParamConstruct.cpp', signs=signs_param, datas=datas_param)
config_build.read_param(fname=path+'IO/readParamFile.cpp', parameters=Parameters)
define_variables.destructor(fname=path + 'Destructors/ParamDestruct.cpp', signs=signs_param, datas=datas_param)
parameterisation_build.parameterisation_build(fname=path + 'Spatial/parameterisation.cpp', parameters=Parameters)


define_variables.report_includes(fname=path + 'includes/Report.h', reports=Reports)
define_variables.report_destructor(fname=path + 'Destructors/ReportDestruct.cpp', reports=Reports)
config_build.report_build(fname=path+'IO/report.cpp', reports=Reports)

define_variables.includes(fname=path + 'includes/Basin.h', signs=['Nitrogen addition'], datas=[Nitrogen_addition], max_category=setting.max_category)
config_build.read_nitrogen(fname=path+'IO/readNitrogenFile.cpp', Nitrogen_inputs=Nitrogen_addition)

linux_build.release_linux(path, release_path)
linux_build.linux_make(release_path)


