###########################################
# Configuration file for model runs
###########################################

from datetime import datetime
import pickle
import numpy as np

class Path:
    model_path = '/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux/' # The path for model executable file
    path_EXEC = 'gEcoHydro'
    data_path = '/data/scratch/wusongj/paper4/data/'                   # The path with spatial and climate data
    config_path = '/data/scratch/wusongj/paper4/data/config/'                 # The path with configuration files (.ini)
    work_path = '/data/scratch/wusongj/paper4/'            # Working directory
    
    #run_path = work_path + 'run/'           # The path for model runs
    #output_path = run_path + 'outputs/'     # The path for output saving
    #result_path = work_path + 'results/'    # The path to save all posterior results



class Info:
    nodata = -9999.0 # nodata value for param.ini and all spatial maps
    soil_index = [1,2,3,4,5,6]  # Column index in param.ini
    landuse_index = [7,8,9,10,11,12]  # Column index in param.ini
    N_soil = len(soil_index)  # Number of soil types
    N_landuse = len(landuse_index) # Number of land use types
    spin_up = 731  # warming days

    # === Global ===
    # 0 : All global grids have value of 1
    # === Soil types ===
    # 1 : Urban
    # 2 : 
    # 3 : 
    # 4 : 
    # 5 : 
    # 6 : 
    # === Land use types === 
    # 7 : Crop
    # 8 : Pasture
    # 9 : Grassland
    # 10 : Forest
    # 11: Sparse vegetation/bare soil
    # 12: Urban

    ### Crop info ###
    # Crop, pasture, grass, forest, sparse/bare soil, urban
    nadd = {}
    nadd['is_crop'] = {'value':[1, 0, 0, 0, 0, 0]}
    nadd['fert_add'] = {'value':[12, 0.5, 0, 0, 0, 0]}
    nadd['fert_day'] = {'value':[87, 87, 87, 87, 87, 87]}
    nadd['fert_down'] = {'value':[0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    nadd['fert_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['fert_IN'] = {'value':[0.7, 0.7, 0.7, 0.7, 0.7, 0.7]}

    nadd['manure_add'] = {'value':[0, 2, 0, 0, 0, 2]}
    nadd['manure_day'] = {'value':[110, 110, 110, 110, 110, 110]}
    nadd['manure_down'] = {'value':[0.4, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['manure_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['manure_IN'] = {'value':[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}

    nadd['residue_add'] = {'value':[2, 2, 1, 1, 0, 0]}
    nadd['residue_day'] = {'value':[242, 260, 260, 290, 290, 290]}
    nadd['residue_down'] = {'value':[0.3, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['residue_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['residue_fastN'] = {'value':[0.6, 0.6, 0.6, 0.6, 0.6, 0.6]}

    nadd['up1'] = {'value':[10, 8, 7, 5, 3, 2]}
    nadd['up2'] = {'value':[0.6, 0.3, 0.3, 0.6, 0.5, 0.2]}
    nadd['up3'] = {'value':[0.04, 0.03, 0.03, 0.018, 0.018, 0.018]}
    nadd['upper_uptake'] = {'value':[0.99, 0.99, 0.99, 0.85, 0.99, 0.95]}
    nadd['plant_day'] = {'value':[85, 55, 55, 55, 55, 55]}  
    nadd['harvest_day'] = {'value':[242, 280, 320, 320, 320, 320]}

    nadd['irrigation_thres'] = {'value':[0.6,0.4,0,0,0,0]}  # The threshold (soil moisture/field capacity) below which irrigation is needed


class Cali:
    # DREAM calibration
    TASK_name = 'DREAM_cali'
    nchains = 50
    cores_for_each_chain = 4

    nbatchs = 5  # Number of batches
    niterations = 100  # Number of iterations for each batch
    

    restart = True   # Whether restart?
    restart_niteration = 100 # restart since which iteration?

    history_thin = 5

    static_config = False  # Whether to define the configs at the beginning to speed up

    


class Output:
    # WOS-ID of each catchment
    Catchment_ID    = ['6_001', '291110_001', '566445_001', '442364_001', '1034751_001', '291111_001', '83811_001', '831616_001', '129489_001', '4_001', '566445_002', '566445_003']
    N_catchments    = len(Catchment_ID)     # Number of catchments
    

    # Site ID in each catchment; shape = (N_catchments, N_sites)
    sim_q_idx       = []
    sim_iso_idx     = []
    sim_no3_idx     = []
    N_sites         = [] # Number of sites in each catchment

    

    catchment_to_cali = pickle.load(open(Path.data_path+'catchment_info/cali/sub_catchment_ID_list','rb'))
    discharge_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/discharge_gauge_list','rb'))
    isotope_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/isotope_gauge_list','rb'))
    nitrate_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/nitrate_gauge_list','rb'))

    

    for i in range(N_catchments):
        
        sim_q_idx.append(discharge_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        sim_iso_idx.append(isotope_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        sim_no3_idx.append(nitrate_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        N_sites.append(len(np.unique(sim_q_idx[i]+sim_iso_idx[i]+sim_no3_idx[i])))

    # Weight for each site in each catchment; shape = (N_catchments, N_sites)
    overall_weights_for_each_var = [0.5, 0.2, 0.3]
    sim_q_weights   = []
    sim_iso_weights = []
    sim_no3_weights = []

    for i in range(N_catchments):
        n_valid_weights =   int((len(sim_q_idx[i])>0))*overall_weights_for_each_var[0] + \
                            int((len(sim_iso_idx[i])>0))*overall_weights_for_each_var[1] + \
                            int((len(sim_no3_idx[i])>0))*overall_weights_for_each_var[2]
        sim_q_weights.append(np.full(len(sim_q_idx[i]), 1)/len(sim_q_idx[i]) * (overall_weights_for_each_var[0] / n_valid_weights) /N_catchments)
        sim_iso_weights.append(np.full(len(sim_iso_idx[i]), 1)/len(sim_iso_idx[i]) * (overall_weights_for_each_var[1] / n_valid_weights) /N_catchments)
        sim_no3_weights.append(np.full(len(sim_no3_idx[i]), 1)/len(sim_no3_idx[i]) * (overall_weights_for_each_var[2] / n_valid_weights) /N_catchments)

  
    sim = {}
    sim['q']       = {'sim_file':'discharge_TS.bin' , 'obs_file':'discharge_obs.bin', 'sim_idx':sim_q_idx, 'weights':sim_q_weights, 'type':'Ts'}
    sim['iso_stream']       = {'sim_file':'d18o_chanS_TS.bin' , 'obs_file':'d18o_stream_obs.bin', 'sim_idx':sim_iso_idx, 'weights':sim_iso_weights, 'type':'Ts'}
    sim['no3']      = {'sim_file':'no3_chanS_TS.bin' , 'obs_file':'no3_stream_obs.bin', 'sim_idx':sim_no3_idx, 'weights':sim_no3_weights, 'type':'Ts'}

    



class Param:
    ### === parameters to calibrate === 
    ref = {}    

    ref['depth3']   =           {'type':'global',  'log':0, 'file':'depth3',   'min':[0.2]*Info.N_soil, 'max':[1]*Info.N_soil, 'fix_value':None}

    # === PET seperation and Max canopy storage === 
    ref['alpha']   =            {'type':'global',  'log':1, 'file':'alpha',   'min':[1e-5]*Info.N_landuse, 'max':[5e-2]*Info.N_landuse, 'fix_value':None}  # Maximum canopy storage = alpha * PET
    ref['rE']   =               {'type':'global',  'log':0, 'file':'rE',   'min':[-3]*Info.N_landuse, 'max':[-0.1]*Info.N_landuse, 'fix_value':None}  # PET to PE and PT

    # Snow
    ref['snow_rain_thre']   =   {'type':'global',   'log':0, 'file':'snow_rain_thre',   'min':[-2], 'max':[2], 'fix_value':None}
    ref['deg_day_min']   =      {'type':'global',   'log':0, 'file':'deg_day_min',   'min':[0], 'max':[2e-3], 'fix_value':None}
    ref['deg_day_max']   =      {'type':'global',   'log':0, 'file':'deg_day_max',   'min':[2e-3], 'max':[1e-2], 'fix_value':None}
    ref['deg_day_increase']   = {'type':'global',   'log':0, 'file':'deg_day_increase',   'min':[0.1], 'max':[0.9], 'fix_value':None}

    
    # === Pedotransfer function ===
    # Soil proporties (field capacity, wilting point, hydraulic conductivity)
    ref['ref_thetaS']   = {'type':'soil',   'log':0, 'file':'ref_thetaS',   'min':[0.5]*Info.N_soil, 'max':[0.99]*Info.N_soil, 'fix_value':None}
    ref['PTF_VG_clay']   = {'type':'soil',   'log':1, 'file':'PTF_VG_clay',   'min':[5e-8]*Info.N_soil, 'max':[5e-3]*Info.N_soil, 'fix_value':None}
    ref['PTF_VG_Db']   = {'type':'soil',   'log':1, 'file':'PTF_VG_Db',   'min':[5e-4]*Info.N_soil, 'max':[5e-1]*Info.N_soil, 'fix_value':None}
    ref['PTF_Ks_const']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_const',   'min':[-3,-1.2,-1.2,-1.2,-1.2,-1.2], 'max':[-2.9,-0.2,-0.2,-0.2,-0.2,-0.2], 'fix_value':None}
    ref['PTF_Ks_sand']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_sand',   'min':[0.006]*Info.N_soil, 'max':[0.026]*Info.N_soil, 'fix_value':None}
    ref['PTF_Ks_clay']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_clay',   'min':[0.003]*Info.N_soil, 'max':[0.013]*Info.N_soil, 'fix_value':None}
    ref['PTF_Ks_slope']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_slope',   'min':[0.1]*Info.N_soil, 'max':[1,15,15,15,15,15], 'fix_value':None}  # Low infiltration capacity in urban areas
    
    # Field capacity
    #ref['SWP']   = {'type':'soil',   'log':0, 'file':'SWP',   'min':[10]*Info.N_soil, 'max':[33]*Info.N_soil, 'fix_value':[33]*Info.N_soil}
    #

    # === Infiltration === 
    ref['KvKh']   = {'type':'soil',   'log':0, 'file':'KvKh',   'min':[1e-2]*Info.N_soil, 'max':[0.5]*Info.N_soil, 'fix_value':None}  # Vertical to horizontal ksat anisotropy ratio
    ref['psiAE']   = {'type':'soil',   'log':0, 'file':'psiAE',   'min':[1e-2]*Info.N_soil, 'max':[1.3]*Info.N_soil, 'fix_value':None}

    # === Distrituted soil proporties to different layers === 
    # Deactivated because soil proporties are calculated in each layer based on depth-dependent soil data
    #ref['KKs']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None}  
    #ref['Ksat']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None}
    #ref['BClambda']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[2]*Info.N_soil, 'max':[15]*Info.N_soil, 'fix_value':None}

    # === Percolation === 
    # Only needed for opt_percolation == 2
    #ref['percExp']   = {'type':'soil',   'log':0, 'file':'percExp',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None}
    
    # === Evapotranspiration === 
    ref['froot_coeff']   = {'type':'landuse',   'log':1, 'file':'froot_coeff',   'min':[0.8]*Info.N_landuse, 'max':[0.95, 0.95, 0.95, 0.999, 0.92, 0.81], 'fix_value':None} # The higher the more deeper roots [max for crops: 0.95, for forest: 0.999]
    ref['ET_reduction'] = {'type':'global',   'log':0, 'file':'ET_reduction',   'min':[0.6], 'max':[1.0], 'fix_value':None} # ET correction weights

    # === GW recharge === 
    ref['wRecharge']   = {'type':'soil',   'log':1, 'file':'wRecharge',   'min':[1e-5]*Info.N_soil, 'max':[1]*Info.N_soil, 'fix_value':None} # Correction factor for GW recharge
    ref['init_GW'] = {'type':'landuse',   'log':0, 'file':'init_GW',   'min':[1]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None} # Initial GW storage in m

    # === Routing === 
    ref['pOvf_toChn']   = {'type':'landuse',   'log':1, 'file':'pOvf_toChn',   'min':[1e-3]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}  # Proportion of overland flow routed to stream (corrected by channel lenght and cell size)
    ref['Ks_vadose']   = {'type':'landuse',   'log':1, 'file':'Ks_vadose',   'min':[1e-3]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}  # The reference conductivity of vadose zone for interflow routing [m/day]
    ref['Ks_GW']   = {'type':'landuse',   'log':1, 'file':'Ks_GW',   'min':[1e-9]*Info.N_landuse, 'max':[1e-2]*Info.N_landuse, 'fix_value':None}  # The reference conductivity of GW zone for interflow routing [m/day]
    ref['lat_to_Chn_vadose']   = {'type':'landuse',   'log':1, 'file':'lat_to_Chn_vadose',   'min':[1e-1]*Info.N_landuse, 'max':[1e1]*Info.N_landuse, 'fix_value':None} # The ratio between conductivities of lateral flow and channel recharge in vadose zone [-]
    ref['lat_to_Chn_GW']   = {'type':'landuse',   'log':1, 'file':'lat_to_Chn_GW',   'min':[1e-3]*Info.N_landuse, 'max':[1e1]*Info.N_landuse, 'fix_value':None} # The ratio between conductivities of lateral flow and channel recharge in GW zone [-]
    ref['interfExp']   = {'type':'landuse',   'log':1, 'file':'interfExp',   'min':[1e-2]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None}
    ref['GWfExp']   = {'type':'landuse',   'log':1, 'file':'GWfExp',   'min':[1e-5]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}
    ref['Manningn']   = {'type':'landuse',   'log':1, 'file':'Manningn',   'min':[1e-4]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None}
    ref['ratio_to_interf'] = {'type':'landuse',   'log':0, 'file':'ratio_to_interf',   'min':[0]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}

    # === Channel === 
    ref['Echan_alpha']   = {'type':'global',   'log':1, 'file':'Echan_alpha',   'min':[0.1]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None}  # Correction factor in Priestley-Taylor equation

    # === Irrigation === 
    ref['irrigation_coeff']   = {'type':'landuse',   'log':0, 'file':'irrigation_coeff',   'min':[0.1,0.01,0,0,0,0], 'max':[2,2,0,0,0,0], 'fix_value':None}  # Irrigation coefficient to determine the actual water demand from water deficit [-]

    # === Mixing === 
    ref['nearsurface_mixing']   = {'type':'landuse',   'log':0, 'file':'nearsurface_mixing',   'min':[0]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None} 
    
    # === Tracking === 
    ref['CG_n_soil'] = {'type':'global',   'log':0, 'file':'CG_n_soil',   'min':[0.5], 'max':[1], 'fix_value':None}
    #ref['delta_d18o_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_d18o_init_GW',   'min':[-5]*Info.N_soil, 'max':[5]*Info.N_soil, 'fix_value':None} # The adjustment of initial d18o composition

    # === Nitrogen simulation ===
    #ref['delta_no3_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_no3_init_GW',   'min':[-5]*Info.N_soil, 'max':[5]*Info.N_soil, 'fix_value':None} # The adjustment of initial no3 composition
    ref['denitrification_river']   = {'type':'landuse',   'log':1, 'file':'denitrification_river',   'min':[1e-5]*Info.N_landuse, 'max':[1e-1]*Info.N_landuse, 'fix_value':None}
    #ref['autotrophic_uptake_aquatic']   = {'type':'landuse',   'log':0, 'file':'autotrophic_uptake_aquatic',   'min':[1e2]*Info.N_landuse, 'max':[5e2]*Info.N_landuse, 'fix_value':None}
    #ref['primary_production_aquatic']   = {'type':'landuse',   'log':0, 'file':'primary_production_aquatic',   'min':[1e-1]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}
    ref['denitrification_soil']   = {'type':'landuse',   'log':1, 'file':'denitrification_soil',   'min':[1e-4,1e-4,1e-4,1e-5,1e-5,1e-5], 'max':[1.1, 1.1, 0.5, 0.3, 0.1, 0.01], 'fix_value':None}
    ref['degradation_soil']   = {'type':'landuse',   'log':1, 'file':'degradation_soil',   'min':[1e-6]*Info.N_landuse, 'max':[1e-4,1e-4,1e-4,1e-4,1e-5,1e-5], 'fix_value':None}
    ref['mineralisation_soil']   = {'type':'landuse',   'log':1, 'file':'mineralisation_soil',   'min':[1e-5]*Info.N_landuse, 'max':[0.4,0.4,0.3,0.2,0.1,0.01], 'fix_value':None}
    #ref['dissolution_soil']   = {'type':'landuse',   'log':1, 'file':'dissolution_soil',   'min':[1e-3]*Info.N_landuse, 'max':[200]*Info.N_landuse, 'fix_value':None}
    ref['deni_soil_moisture_thres']   = {'type':'landuse',   'log':0, 'file':'deni_soil_moisture_thres',   'min':[0.2]*Info.N_landuse, 'max':[0.85]*Info.N_landuse, 'fix_value':None}
