###########################################
# Configuration file for model runs
###########################################

from datetime import datetime
import pickle
import numpy as np

class Path:
    model_path = '/home/wusongj/EcoTWIN/release_linux/' # The path for model executable file
    path_EXEC = 'EcoTWIN_cali'
    data_path = '/data/scratch/wusongj/paper6/data/'                   # The path with spatial and climate data
    config_path = '/data/scratch/wusongj/paper6/data/config/'                 # The path with configuration files (.ini)
    work_path = '/data/scratch/wusongj/paper6/'            # Working directory
    
    #run_path = work_path + 'run/'           # The path for model runs
    #output_path = run_path + 'outputs/'     # The path for output saving
    #result_path = work_path + 'results/'    # The path to save all posterior results



class Info:
    nodata = -9999.0 # nodata value for param.ini and all spatial maps
    soil_index = [1,2,3,4,5,6,7]  # Column index in param.ini
    landuse_index = [8,9,10,11,12,13]  # Column index in param.ini
    N_soil = len(soil_index)  # Number of soil types
    N_landuse = len(landuse_index) # Number of land use types
    spin_up = 731  # warming days

    # === Global ===
    # 0 : All global grids have value of 1
    # === Soil types ===
    # 1 : Urban     cat0, urban: low infiltration: ['UR']
    # 2 :           cat1, cropland in eastern Europe: dark organic soils, rapid infiltration, high water retention, and deep rooting ['KS_CH_PH', 'Vr']  
    # 3 :           cat2, grassland, including nordic regions: clay, high soil moisture, low infilitration capacity ['LV_AL_PD', 'LX_AC', 'FR_NT_PT', 'NoData']
    # 4 :           cat3, all land use types in central-eastern-southern Europe: sands, low porosity, high infiltration capcity ['CM', 'AR_Dunes', 'AT', 'DU_CA_GY_SC']
    # 5 :           cat4, forest in north-eastern Europe ['PZ_HR', 'AN']
    # 6 :           cat5, rocks/mountainous areas (low elevation excluded): High soil moisture, low inflitration capacity, more overland flow, older age ['FL_LP_RG_Rocks', 'CR', 'Glacier_Snow', 'InlandWater']
    # 7 :           cat6, Peatland
    # === Land use types === 
    # 8 : Crop
    # 9 : Pasture
    # 10: Grassland
    # 11: Forest
    # 12: Sparse vegetation/bare soil
    # 13: Urban

    ### Crop info ###
    # Crop, pasture, grass, forest, sparse/bare soil, urban
    nadd = {}
    nadd['is_crop'] = {'value':[1, 0, 0, 0, 0, 0]}
    nadd['fert_add'] = {'value':[12, 0, 0, 0, 0, 0]}
    nadd['fert_day'] = {'value':[87, 87, 87, 87, 87, 87]}
    nadd['fert_down'] = {'value':[0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    nadd['fert_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['fert_IN'] = {'value':[0.7, 0.7, 0.7, 0.7, 0.7, 0.7]}

    nadd['manure_add'] = {'value':[0, 0, 0, 0, 0, 0]}
    nadd['manure_day'] = {'value':[110, 110, 110, 110, 110, 110]}
    nadd['manure_down'] = {'value':[0.4, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['manure_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['manure_IN'] = {'value':[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}

    nadd['residue_add'] = {'value':[1, 1, 1, 1, 0, 0]}
    nadd['residue_day'] = {'value':[242, 260, 260, 290, 290, 290]}
    nadd['residue_down'] = {'value':[0.3, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['residue_period'] = {'value':[30, 30, 30, 30, 30, 30]}
    nadd['residue_fast_NP'] = {'value':[0.6, 0.6, 0.6, 0.6, 0.6, 0.6]}

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
    nchains = 20
    cores_for_each_chain = 1

    nbatchs = 5  # Number of batches
    niterations = 20000  # Number of iterations for each batch
    

    restart = False   # Whether restart?
    restart_niteration = 0 # restart since which iteration?

    history_thin = 5

    static_config = False  # Whether to define the configs at the beginning to speed up

    


class Output:
    # WOS-ID of each catchment
    Catchment_ID    = ['291110_001', '831616_001']
    N_catchments    = len(Catchment_ID)     # Number of catchments
    

    # Site ID in each catchment; shape = (N_catchments, N_sites)
    sim_q_idx       = []
    sim_iso_idx     = []
    sim_doc_idx     = []
    sim_no3_idx     = []
    N_sites         = [] # Number of sites in each catchment


    catchment_to_cali = pickle.load(open(Path.data_path+'catchment_info/cali/sub_catchment_ID_list','rb'))
    discharge_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/discharge_gauge_list','rb'))
    isotope_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/isotope_gauge_list','rb'))
    doc_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/DOC_gauge_list','rb'))
    nitrate_gauge_list = pickle.load(open(Path.data_path+'catchment_info/cali/nitrate_gauge_list','rb'))
    
    
    for i in range(N_catchments):
        sim_q_idx.append(discharge_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        sim_iso_idx.append(isotope_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        sim_doc_idx.append(doc_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        sim_no3_idx.append(nitrate_gauge_list[np.where(catchment_to_cali==Catchment_ID[i])[0][0]])
        N_sites.append(len(np.unique(sim_q_idx[i]+sim_iso_idx[i]+sim_no3_idx[i]+sim_doc_idx[i])))

    # Weight for each site in each catchment; shape = (N_catchments, N_sites)
    overall_weights_for_each_var = [0.4, 0.2, 0.2, 0.2]
    #overall_weights_for_each_var = [0.5, 0.5, 0.0, 0.0]
    sim_q_weights   = []
    sim_iso_weights = []
    sim_doc_weights = []
    sim_no3_weights = []

    n_q_sites = 0
    n_iso_sites = 0
    n_doc_sites = 0
    n_no3_sites = 0
    for i in range(N_catchments):
        n_q_sites += len(sim_q_idx[i])
        n_iso_sites += len(sim_iso_idx[i])
        n_doc_sites += len(sim_doc_idx[i])
        n_no3_sites += len(sim_no3_idx[i])

    for i in range(N_catchments):
        sim_q_weights.append(np.full(len(sim_q_idx[i]), overall_weights_for_each_var[0] / n_q_sites))
        sim_iso_weights.append(np.full(len(sim_q_idx[i]), overall_weights_for_each_var[1] / n_iso_sites))
        sim_doc_weights.append(np.full(len(sim_q_idx[i]), overall_weights_for_each_var[2] / n_doc_sites))
        sim_no3_weights.append(np.full(len(sim_q_idx[i]), overall_weights_for_each_var[3] / n_no3_sites))

  
    sim = {}
    sim['q']       = {'sim_file':'discharge_TS.bin' , 'obs_file':'discharge_obs.bin', 'sim_idx':sim_q_idx, 'weights':sim_q_weights, 'type':'Ts'}
    sim['iso_stream']       = {'sim_file':'d18o_chanS_TS.bin' , 'obs_file':'d18o_stream_obs.bin', 'sim_idx':sim_iso_idx, 'weights':sim_iso_weights, 'type':'Ts'}
    sim['no3']      = {'sim_file':'no3_chanS_TS.bin' , 'obs_file':'no3_stream_obs.bin', 'sim_idx':sim_no3_idx, 'weights':sim_no3_weights, 'type':'Ts'}
    sim['doc']      = {'sim_file':'doc_chanS_TS.bin' , 'obs_file':'DOC_stream_obs.bin', 'sim_idx':sim_doc_idx, 'weights':sim_doc_weights, 'type':'Ts'}

    



class Param:
    ### === parameters to calibrate === 
    ref = {}    

    ref['depth3']   =           {'type':'global',  'log':0, 'file':'depth3',   'min':[0.2], 'max':[2], 'fix_value':None}

    # === PET seperation and Max canopy storage === 
    ref['alpha']   =            {'type':'global',  'log':1, 'file':'alpha',   'min':[1e-5], 'max':[5e-2], 'fix_value':None}  # Maximum canopy storage = alpha * PET
    ref['rE']   =               {'type':'global',  'log':0, 'file':'rE',   'min':[-3], 'max':[-0.1], 'fix_value':None}  # the more negative the more transpiration

    # === Management ===
    ref['irrigation_FC_thres']   =   {'type':'global',  'log':1, 'file':'irrigation_FC_thres',   'min':[0.01], 'max':[0.1], 'fix_value':None}  # The soil moisture threshold for irrigation
    ref['irrigation_coeff']   = {'type':'global',   'log':1, 'file':'irrigation_coeff',   'min':[0.01], 'max':[0.2], 'fix_value':None}  # Irrigation coefficient to determine the actual water demand from water deficit [-]
    ref['drainage_intensity']   = {'type':'landuse',  'log':0, 'file':'drainage_intensity',   'min':[0.5,0.01,0.01,0.01,0.01,0.5], 'max':[0.99,0.5,0.5,0.5,0.5,0.99], 'fix_value':None}  # The intensity of drainage based on the density of drainage network [-], only needed when drainage is enabled


    # Snow
    ref['snow_rain_thre']   =   {'type':'global',   'log':0, 'file':'snow_rain_thre',   'min':[-5], 'max':[5], 'fix_value':None}
    ref['deg_day_min']   =      {'type':'global',   'log':0, 'file':'deg_day_min',   'min':[0], 'max':[2e-3], 'fix_value':None}
    ref['deg_day_max']   =      {'type':'global',   'log':0, 'file':'deg_day_max',   'min':[2e-3], 'max':[1e-2], 'fix_value':None}
    ref['deg_day_increase']   = {'type':'global',   'log':0, 'file':'deg_day_increase',   'min':[0.1], 'max':[0.9], 'fix_value':None}

    
    # === Pedotransfer function ===
    # Soil proporties (field capacity, wilting point, hydraulic conductivity)
    ref['ref_thetaS']   = {'type':'global',   'log':0, 'file':'ref_thetaS',   'min':[0.4], 'max':[0.9], 'fix_value':None} # 'min':[0.5], 'max':[0.99]
    ref['PTF_VG_clay']   = {'type':'global',   'log':1, 'file':'PTF_VG_clay',   'min':[5e-4], 'max':[3e-3], 'fix_value':None}
    ref['PTF_VG_Db']   = {'type':'global',   'log':1, 'file':'PTF_VG_Db',   'min':[0.25], 'max':[0.35], 'fix_value':None}
    ref['PTF_Ks_const']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_const',   'min':[-3,-1.2,-1.5,-1.3,-1.4,-1.5,-1.5], 'max':[-2.9,-0.3,-0.5,-0.3,-0.3,-0.3,-0.3], 'fix_value':None} # [-1.2, -0.29]
    ref['PTF_Ks_sand']   = {'type':'global',   'log':0, 'file':'PTF_Ks_sand',   'min':[0.006], 'max':[0.026], 'fix_value':None}
    ref['PTF_Ks_clay']   = {'type':'global',   'log':0, 'file':'PTF_Ks_clay',   'min':[0.003], 'max':[0.013], 'fix_value':None}
    

    # Field capacity
    #ref['SWP']   = {'type':'soil',   'log':0, 'file':'SWP',   'min':[10]*Info.N_soil, 'max':[33]*Info.N_soil, 'fix_value':[33]*Info.N_soil}
    #

    # === Infiltration === 
    ref['KvKh']   = {'type':'global',   'log':0, 'file':'KvKh',   'min':[1e-2], 'max':[0.5], 'fix_value':None}  # Vertical to horizontal ksat anisotropy ratio
    ref['psiAE']   = {'type':'global',   'log':0, 'file':'psiAE',   'min':[1e-2], 'max':[1.3], 'fix_value':None}

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
    ref['perc_vadose_coeff']   = {'type':'soil',   'log':1, 'file':'perc_vadose_coeff',   'min':[1e-5,1e-6,1e-5,1e-6,1e-5,1e-3,1e-5], 'max':[1,0.5,1,0.5,1,1,1], 'fix_value':None} # Coefficient parameter for GW recharge [1e-5, 1]
    ref['init_GW'] = {'type':'global',   'log':0, 'file':'init_GW',   'min':[1], 'max':[50], 'fix_value':None} # Initial GW storage in m

    # === Routing === 
    ref['pOvf_toChn']   = {'type':'global',   'log':1, 'file':'pOvf_toChn',   'min':[1e-3], 'max':[1], 'fix_value':None}  # Proportion of overland flow routed to stream (corrected by channel lenght and cell size) [1e-3, 1]
    ref['Ks_vadose']   = {'type':'global',   'log':1, 'file':'Ks_vadose',   'min':[1e-3], 'max':[1], 'fix_value':None}  # The reference conductivity of vadose zone for interflow routing [m/day] [1e-3, 1]
    ref['Ks_GW']   = {'type':'global',   'log':1, 'file':'Ks_GW',   'min':[1e-9], 'max':[1e-2], 'fix_value':None}  # The reference conductivity of GW zone for interflow routing [m/day]
    ref['lat_to_Chn_vadose']   = {'type':'global',   'log':1, 'file':'lat_to_Chn_vadose',   'min':[0.1], 'max':[15], 'fix_value':None} # The ratio between conductivities of lateral flow and channel recharge in vadose zone [-]  [0.1,10]
    ref['lat_to_Chn_GW']   = {'type':'global',   'log':1, 'file':'lat_to_Chn_GW',   'min':[1e-3], 'max':[1e1], 'fix_value':None} # The ratio between conductivities of lateral flow and channel recharge in GW zone [-]
    ref['interfExp']   = {'type':'global',   'log':1, 'file':'interfExp',   'min':[1e-2], 'max':[10], 'fix_value':None}
    ref['GWfExp']   = {'type':'global',   'log':1, 'file':'GWfExp',   'min':[1e-5], 'max':[1], 'fix_value':None}
    ref['Manningn']   = {'type':'global',   'log':1, 'file':'Manningn',   'min':[1e-4], 'max':[10], 'fix_value':None}
    ref['ratio_to_interf'] = {'type':'global',   'log':0, 'file':'ratio_to_interf',   'min':[0], 'max':[1], 'fix_value':None}  #[0,1]

    # === Channel === 
    ref['Echan_alpha']   = {'type':'global',   'log':1, 'file':'Echan_alpha',   'min':[0.1], 'max':[10], 'fix_value':None}  # Correction factor in Priestley-Taylor equation

    # === Mixing === 
    ref['nearsurface_mixing']   = {'type':'global',   'log':0, 'file':'nearsurface_mixing',   'min':[0], 'max':[1], 'fix_value':None} 
    
    # === Tracking === 
    ref['CG_n_soil'] = {'type':'global',   'log':0, 'file':'CG_n_soil',   'min':[0.5], 'max':[1], 'fix_value':None}
    #ref['delta_d18o_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_d18o_init_GW',   'min':[-5]*Info.N_soil, 'max':[5]*Info.N_soil, 'fix_value':None} # The adjustment of initial d18o composition

    # === Carbon simulation ===
    #ref['carboxylation_rate'] = {'type':'landuse',   'log':0, 'file':'carboxylation_rate',   'min':np.array([95,75,75,35,0,0])*1e-6, 'max':np.array([105,85,85,65,30,30])*1e-6, 'fix_value':None} # Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]
    #ref['ETransport'] = {'type':'landuse',   'log':0, 'file':'ETransport',   'min':np.array([180,130,130,100,20,20])*1e-6, 'max':np.array([200,160,160,120,80,80])*1e-6, 'fix_value':None} # Maximum electron transport rate at 25 Celsius [1.E-6 * Mol/m^2 leafarea/s] (Jmax=1.9*V_max^25 for C3 plants)
    # Assimilation
    ref['carboxylation_rate'] = {'type':'landuse',   'log':0, 'file':'carboxylation_rate',   'min':[np.array([100,80,80,50,70,70])*1e-7], 'max':[np.array([100,80,80,50,70,70])*1e-6], 'fix_value':None} # Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]; np.array([100,80,80,50,70,70])*1e-6
    ref['ETransport'] = {'type':'landuse',   'log':0, 'file':'ETransport',   'min':[np.array([190,145,145,110,130,130])*1e-7], 'max':[np.array([190,145,145,110,130,130])*1e-6], 'fix_value':None} # Maximum electron transport rate at 25 Celsius [1.E-6 * Mol/m^2 leafarea/s] (Jmax=1.9*V_max^25 for C3 plants); np.array([190,145,145,110,130,130])*1e-6
    
    ref['C_in_LeafArea'] = {'type':'landuse',   'log':0, 'file':'C_in_LeafArea',   'min':[], 'max':[], 'fix_value':np.array([0.45, 0.45, 0.45, 0.25, 0.3, 0.3])/12} # Carbon content per leaf area in [m2(leaf)/gC] <== [m2(leaf)/mol(Carbon)/12]
    ref['LAI_shed_coef'] = {'type':'landuse',   'log':0, 'file':'LAI_shed_coef',   'min':[], 'max':[], 'fix_value':[0.0027, 0.0037, 0.0055, 0.0, 0.0015, 0.0015]} # Leaf shedding coefficient related to LAI; Time in which leaves are constantly shedded [days-1]
    ref['tau_wood_C'] = {'type':'landuse',   'log':0, 'file':'tau_wood_C',   'min':[], 'max':[], 'fix_value':np.array([1,1,1,60,1,1])*365} # Life time scale of the wood pool and vegetation dynamics [days]
    # Distribute NPP to vegetation pools
    ref['frac_NPP_to_green'] = {'type':'landuse',   'log':0, 'file':'frac_NPP_to_green',   'min':[], 'max':[], 'fix_value':[0.8,0.8,0.8,0.6,0.8,0.8]} # The fraction of NPP addition to vegetation green pool [-]
    ref['frac_NPP_to_wood'] = {'type':'landuse',   'log':0, 'file':'frac_NPP_to_wood',   'min':[], 'max':[], 'fix_value':[0.05,0.05,0.05,0.3,0.05,0.05]} # The fraction of NPP addition to wood green pool [-]
    # Vegetation phenology
    ref['plant_wood_CP_max'] = {'type':'landuse',   'log':0, 'file':'plant_wood_CP_max',   'min':[], 'max':[], 'fix_value':[0,0,0,15000,1000,1000]} # The maximum carbon content in wood pool [gC/m2] <== [molC/m2]; the global maximum should be ~2000*12 gC/m2, here we set to 15,000 given the lower carbon biomass in Europe
    ref['plant_reserve_CP_max'] = {'type':'landuse',   'log':0, 'file':'plant_reserve_CP_max',   'min':[], 'max':[], 'fix_value':[4*4,4*3,4*3,2*6,3*4.5,3*4.5]} # Term to calculate maximum carbon content in reserve pool at optimal conditions [-]: first term is the ratio of ratio of vegetation green pool to reserve pool at maximum LAI, while second term is maximum LAI
    # Distribute litter to soil carbon pools (humus = 1 - soluble - acid - ethanol - nonsoluble)
    ref['frac_litter_to_soluble_nonwood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_soluble_nonwood',   'min':[], 'max':[], 'fix_value':[0.07,0.17,0.17,0.39,0.22,0.22]} # The fraction of nonwood litter going to soil soluble pool (DOC pool)  [-]
    ref['frac_litter_to_acid_nonwood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_acid_nonwood',   'min':[], 'max':[], 'fix_value':[0.74,0.62,0.62,0.40,0.50,0.50]} # The fraction of non-woody litter going to soil acid pool  [-]
    ref['frac_litter_to_ethanol_nonwood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_ethanol_nonwood',   'min':[], 'max':[], 'fix_value':[0.03,0.06,0.06,0.10,0.07,0.07]} # The fraction of non-woody litter going to soil ethano pool  [-]
    ref['frac_litter_to_nonsoluble_nonwood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_nonsoluble_nonwood',   'min':[], 'max':[], 'fix_value':[0.16,0.15,0.15,0.11,0.21,0.21]} # The fraction of non-woody litter going to soil nonsoluble pool  [-]
    ref['frac_litter_to_soluble_wood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_soluble_wood',   'min':[], 'max':[], 'fix_value':[0.02,0.02,0.02,0.02,0.02,0.02]} # The fraction of wood litter going to soil soluble pool (DOC pool)  [-]
    ref['frac_litter_to_acid_wood'] = {'type':'landuse',   'log':0, 'file':'_frac_litter_to_acid_wood',   'min':[], 'max':[], 'fix_value':[0.73,0.73,0.73,0.73,0.73,0.73]} # The fraction of wood litter going to soil acid pool  [-]
    ref['frac_litter_to_ethanol_wood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_ethanol_wood',   'min':[], 'max':[], 'fix_value':[0.02,0.02,0.02,0.02,0.02,0.02]} # The fraction of wood litter going to soil ethano pool  [-]
    ref['frac_litter_to_nonsoluble_wood'] = {'type':'landuse',   'log':0, 'file':'frac_litter_to_nonsoluble_wood',   'min':[], 'max':[], 'fix_value':[0.23,0.23,0.23,0.23,0.23,0.23]} # The fraction of wood litter going to soil nonsoluble pool  [-]
    # Reference decomposition rates of carbon pools
    ref['decomposition_weight_fast_pool'] = {'type':'global',   'log':1, 'file':'decomposition_weight_fast_pool',   'min':[1e-2], 'max':[1e2], 'fix_value':None} # Correction of decomposition rates of past pool based on the magnitudes of carbon storages [-]
    ref['decomposition_weight_humus_pool'] = {'type':'global',   'log':1, 'file':'decomposition_weight_humus_pool',   'min':[1e-2], 'max':[1e2], 'fix_value':None} # Correction of decomposition rates of humus pool based on the magnitudes of carbon storages [-]


    # === Nitrogen simulation ===
    ref['delta_no3_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_no3_init_GW',   'min':[-5,-1,-0.2,-0.2,-0.2,-0.2], 'max':[5,1,0.2,0.2,0.2,0.2], 'fix_value':None} # The adjustment of initial no3 composition
    ref['denitrification_river']   = {'type':'landuse',   'log':1, 'file':'denitrification_river',   'min':[1e-5]*Info.N_landuse, 'max':[1e-1]*Info.N_landuse, 'fix_value':None}
    #ref['autotrophic_uptake_aquatic']   = {'type':'landuse',   'log':0, 'file':'autotrophic_uptake_aquatic',   'min':[1e2]*Info.N_landuse, 'max':[5e2]*Info.N_landuse, 'fix_value':None}
    #ref['primary_production_aquatic']   = {'type':'landuse',   'log':0, 'file':'primary_production_aquatic',   'min':[1e-1]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None}
    ref['denitrification_soil']   = {'type':'landuse',   'log':1, 'file':'denitrification_soil',   'min':[1e-4,1e-4,1e-4,1e-5,1e-5,1e-5], 'max':[0.8, 0.8, 0.5, 0.3, 0.1, 0.01], 'fix_value':None}
    #ref['degradation_soil']   = {'type':'landuse',   'log':1, 'file':'degradation_soil',   'min':[1e-6]*Info.N_landuse, 'max':[1e-4,1e-4,1e-4,1e-4,1e-5,1e-5], 'fix_value':None}
    #ref['mineralisation_soil']   = {'type':'landuse',   'log':1, 'file':'mineralisation_soil',   'min':[1e-5]*Info.N_landuse, 'max':[0.4,0.4,0.3,0.2,0.1,0.01], 'fix_value':None}
    #ref['dissolution_soil']   = {'type':'landuse',   'log':1, 'file':'dissolution_soil',   'min':[1e-3]*Info.N_landuse, 'max':[200]*Info.N_landuse, 'fix_value':None}
    ref['deni_soil_moisture_thres']   = {'type':'global',   'log':0, 'file':'deni_soil_moisture_thres',   'min':[0.2], 'max':[0.85], 'fix_value':None}

    ref['NC_ratio_plant_green'] = {'type':'global',   'log':1, 'file':'NC_ratio_plant_green',   'min':[1/70], 'max':[1/16], 'fix_value':None} # Nitrogen carbon ratio in vegetation green pool  [gN/gC]
    ref['NC_ratio_plant_wood'] = {'type':'global',   'log':1, 'file':'NC_ratio_plant_wood',   'min':[1/250], 'max':[1/50], 'fix_value':None} # Nitrogen carbon ratio in vegetation wood pool  [gN/gC]
    ref['NC_ratio_fast_pool_nonwood'] = {'type':'global',   'log':1, 'file':'NC_ratio_fast_pool_nonwood',   'min':[1/150], 'max':[1/30], 'fix_value':None} # Nitrogen carbon ratio in non-wood fast (litter) pool (acid, ethanol, and nonsoluble)  [gN/gC]
    ref['NC_ratio_fast_pool_wood'] = {'type':'global',   'log':1, 'file':'NC_ratio_fast_pool_wood',   'min':[1/1400], 'max':[1/250], 'fix_value':None} # Nitrogen carbon ratio in wood fast (litter) pool (acid, ethanol, and nonsoluble)  [gN/gC]
    ref['NC_ratio_humus_pool'] = {'type':'global',   'log':1, 'file':'NC_ratio_humus_pool',   'min':[1/30], 'max':[1/8], 'fix_value':None} # Nitrogen carbon ratio in humus pool  [gN/gC]