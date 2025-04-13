###########################################
# Configuration file for model runs
###########################################

from datetime import datetime
import numpy as np

class Path:
    model_path = '/home/wusongj/GEM/stable_release/' # The path for model executable file
    path_EXEC = 'gEcoHydro'
    data_path = '/home/wusongj/GEM/test_dmc/'                   # The path with spatial and climate data
    config_path = '/home/wusongj/GEM/test_dmc/'                 # The path with configuration files (.ini)

    work_path = '/data/scratch/wusongj/paper4/'            # Working directory
    
    run_path = work_path + 'run/'           # The path for model runs
    output_path = run_path + 'outputs/'     # The path for output saving

    result_path = work_path + 'results/'    # The path to save all posterior results



class Info:
    nodata = -9999.0 # nodata value for param.ini and all spatial maps
    soil_index = [1,2,3,4]  # Column index in param.ini
    landuse_index = [5,6,7,8]  # Column index in param.ini
    N_soil = len(soil_index)  # Number of soil types
    N_landuse = len(landuse_index) # Number of land use types

    spin_up = 731  # warming days


class Cali:
    # DREAM calibration
    TASK_name = 'DREAM_cali_DMC'
    ncores = 20
    nchains = 20

    niterations = 500  # Number of iterations for each batch
    nbatchs = 20  # Number of batches

    restart = False   # Whether restart?
    restart_niteration = 0 # restart since which iteration?

    


class Output:
    N_sites         = 1     # The number of sites for outputs (> 0 in Tsmask.asc)
    sim_q_idx       = [0]   # Demnitz Mill
    sim = {}
    sim['q']       = {'sim_file':'discharge_TS.bin' , 'obs_file':'discharge_obs.bin', 'sim_idx':sim_q_idx, 'type':'Ts'}

    



class Param:
    ref = {}
    ### parameters to calibrate
    ref['depth3']   =           {'type':'soil',  'log':0, 'file':'depth3',   'min':[0.6]*Info.N_soil, 'max':[5]*Info.N_soil}
    ref['alpha']   =            {'type':'landuse',  'log':1, 'file':'alpha',   'min':[1e-5]*Info.N_landuse, 'max':[5e-2]*Info.N_landuse}
    ref['rE']   =               {'type':'landuse',  'log':0, 'file':'rE',   'min':[-3]*Info.N_landuse, 'max':[-0.1]*Info.N_landuse}  # PET to PE and PT
    ref['snow_rain_thre']   =   {'type':'global',   'log':0, 'file':'snow_rain_thre',   'min':[-2], 'max':[2]}
    ref['deg_day_min']   =      {'type':'global',   'log':0, 'file':'deg_day_min',   'min':[0], 'max':[2e-3]}
    ref['deg_day_max']   =      {'type':'global',   'log':0, 'file':'deg_day_max',   'min':[2e-3], 'max':[1e-2]}
    ref['deg_day_increase']   = {'type':'global',   'log':0, 'file':'deg_day_increase',   'min':[0.1], 'max':[0.9]}

    
    # Pedotransfer function
    ref['ref_thetaS']   = {'type':'soil',   'log':0, 'file':'ref_thetaS',   'min':[0.5]*Info.N_soil, 'max':[0.99]*Info.N_soil}
    ref['PTF_VG_clay']   = {'type':'soil',   'log':1, 'file':'PTF_VG_clay',   'min':[5e-8]*Info.N_soil, 'max':[5e-3]*Info.N_soil}
    ref['PTF_VG_Db']   = {'type':'soil',   'log':1, 'file':'PTF_VG_Db',   'min':[5e-4]*Info.N_soil, 'max':[5e-1]*Info.N_soil}

    ref['PTF_Ks_const']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_const',   'min':[-1.2]*Info.N_soil, 'max':[-0.2]*Info.N_soil}
    ref['PTF_Ks_sand']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_sand',   'min':[1e-4]*Info.N_soil, 'max':[0.026]*Info.N_soil}
    ref['PTF_Ks_clay']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_clay',   'min':[-1.3e-2]*Info.N_soil, 'max':[-3e-3]*Info.N_soil}
    ref['PTF_Ks_slope']   = {'type':'soil',   'log':0, 'file':'PTF_Ks_slope',   'min':[0.1]*Info.N_soil, 'max':[15]*Info.N_soil}

    ref['SWP']   = {'type':'soil',   'log':0, 'file':'SWP',   'min':[10]*Info.N_soil, 'max':[33]*Info.N_soil}

    ref['KvKh']   = {'type':'soil',   'log':0, 'file':'KvKh',   'min':[1e-2]*Info.N_soil, 'max':[0.5]*Info.N_soil}  # Vertical to horizontal ksat anisotropy ratio
    ref['psiAE']   = {'type':'soil',   'log':0, 'file':'psiAE',   'min':[1e-2]*Info.N_soil, 'max':[1.3]*Info.N_soil}

    # Infiltration
    ref['KKs']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil}
    ref['Ksat']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil}
    ref['BClambda']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[2]*Info.N_soil, 'max':[15]*Info.N_soil}

    # Percolation
    ref['percExp']   = {'type':'soil',   'log':0, 'file':'percExp',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil}

    # Evapotranspiration
    ref['froot_coeff']   = {'type':'landuse',   'log':1, 'file':'froot_coeff',   'min':[0.8]*Info.N_landuse, 'max':[0.999]*Info.N_landuse} # The higher the more deeper roots

    # GW recharge
    ref['wRecharge']   = {'type':'soil',   'log':1, 'file':'wRecharge',   'min':[1e-10]*Info.N_soil, 'max':[1]*Info.N_soil} # Correction factor for GW recharge

    # Routing
    ref['pOvf_toChn']   = {'type':'soil',   'log':1, 'file':'pOvf_toChn',   'min':[1e-3]*Info.N_soil, 'max':[1e3]*Info.N_soil}
    ref['interfExp']   = {'type':'soil',   'log':1, 'file':'interfExp',   'min':[1e-5]*Info.N_soil, 'max':[10]*Info.N_soil}
    ref['winterf']   = {'type':'soil',   'log':1, 'file':'winterf',   'min':[1e-2]*Info.N_soil, 'max':[1e7]*Info.N_soil}  # Correction factor for linear Kinematic waver approximation of interflow
    ref['GWfExp']   = {'type':'soil',   'log':1, 'file':'GWfExp',   'min':[1e-5]*Info.N_soil, 'max':[1]*Info.N_soil}
    ref['wGWf']   = {'type':'soil',   'log':1, 'file':'wGWf',   'min':[1e-15]*Info.N_soil, 'max':[1e-2]*Info.N_soil}  # Proportion of GW storage for routing generation
    ref['Manningn']   = {'type':'soil',   'log':1, 'file':'Manningn',   'min':[0.01]*Info.N_soil, 'max':[0.1]*Info.N_soil}
    


    


"""
Ecoplot:
    paramName = ["param_rE" ,    "param_Ic", "param_snowThreshold",   "param_degreeFactorMin",    "param_degreeFactorMax",    "param_degreeFactorIncrease",   "param_weight_Ei",    "param_weight_Es"] 
    paramMin  = [-0.5,           30/1000,    -2+273.15,              0/1000,                     2/1000,                     0.1,                             0.1,            0.1]
    paramMax  = [-0.1 ,          60/1000,    2+273.15,               2/1000,                     10/1000,                    0.9,                             0.9,            0.9]

    paramName_vegDependent =["param_ks1",   "param_ks2",    "param_ks3",    "param_FC1",    "param_FC2",    "param_FC3",    "param_g1", "param_g2", "param_g3", \
                            "param_PFthreshold", "param_PFscale2", "param_PFscale3"]
    paramMin_vegDependent  =[5/1000,        5/1000,         5/1000,         0.15,           0.15,           0.15,            1,          1,          1, \
                            0/1000,         0,                  0]
    paramMax_vegDependent  =[35/1000,       40/1000,        40/1000,        0.7,            0.7,            0.8,             7,          7,          7, \
                            8/1000,         0.4,                0.4]
"""

"""
EcH2O-iso
    ref['Depth']     = {'soil':0, 'veg':0, 'log':0, 'file':'soildepth',    'min':[1],    'max':[1.01]}
#    ref['HLayer1']   = {'soil':1, 'veg':0, 'log':0, 'file':'soildepth.L1', 'min':[0.15,0.15,0.15,0.15],'max':[0.15,0.15,0.15,0.15]}
#    ref['HLayer2']   = {'soil':1, 'veg':0, 'log':0, 'file':'soildepth.L2', 'min':[0.35,0.35,0.35,0.35],'max':[0.35,0.35,0.35,0.35]}
    ref['Porosity']  = {'soil':1, 'veg':0, 'log':0, 'file':'poros',        'min':[0.33,0.32,0.32,0.32],'max':[0.7,0.7,0.7,0.7]}
    ref['Khoriz']    = {'soil':1, 'veg':0, 'log':1, 'file':'Keff',         'min':[1e-6,1e-6,1e-6,1e-6],'max':[1e-1,1e-1,1e-1,1e-1]}
    ref['Anisotropy']= {'soil':1, 'veg':0, 'log':1, 'file':'KvKh',         'min':[0.01,0.01,0.01,0.01],'max':[0.4,0.4,0.4,0.4]}
    ref['BClambda']  = {'soil':1, 'veg':0, 'log':0, 'file':'BClambda',     'min':[2.5,2.6,2,2.4],      'max':[7,7.1,15,6.5]}
    ref['PsiAE']     = {'soil':1, 'veg':0, 'log':0, 'file':'psi_ae',       'min':[0.05,0.05,0.05,0.05],'max':[0.57,0.47,1.2,0.35]}
#    ref['SMresidual']= {'soil':1, 'veg':0, 'log':0, 'file':'theta_r',      'min':[0.02,0.02,0.02,0.02],'max':[0.05,0.05,0.05,0.05]}
#    ref['kKexp']     = {'soil':1, 'veg':0, 'log':0, 'file':'kKsat',        'min':[1,1,1,1],            'max':[50,50,50,50]};
#    ref['kPorosity'] = {'soil':1, 'veg':0, 'log':0, 'file':'kporos',       'min':[1,1,1,1],            'max':[50,50,50,50]};
#    ref['Wc']        = {'soil':1, 'veg':0, 'log':0, 'file':'Wc',           'min':[0.7,0.7,0.7,0.7],    'max':[0.7,0.7,0.7,0.7]}
#    ref['Wp']        = {'soil':1, 'veg':0, 'log':0, 'file':'Wp',           'min':[9,9,9,9],            'max':[9,9,9,9]}
    ref['leakance']  = {'soil':1, 'veg':0, 'log':1, 'file':'leakance',     'min':[1e-8,1e-8,1e-8,1e-8],'max':[0.1,0.1,0.1,0.1]}
#    ref['dampdepth'] = {'soil':1, 'veg':0, 'log':0, 'file':'dampdepth',    'min':[2.0,2.0,2.0,2.0],    'max':[2.0,2.0,2.0,2.0]}
#    ref['tempdamp']  = {'soil':1, 'veg':0, 'log':0, 'file':'temp_damp',    'min':[8.5,8.5,8.5,8.5],    'max':[8.5,8.5,8.5,8.5]}
#    ref['SthermalK'] = {'soil':1, 'veg':0, 'log':0, 'file':'soilthermalK', 'min':[0.3,0.3,0.11,0.22],  'max':[0.3,0.3,0.11,0.22]}
#    ref['Sheatcap']  = {'soil':1, 'veg':0, 'log':0, 'file':'soilheatcap',  'min':[2.2e6,2.2e6,7.8e5,1.9e6],'max':[2.2e6,2.2e6,7.8e5,1.9e6]}
    ref['albedoS']   = {'soil':1, 'veg':0, 'log':0, 'file':'albedo',       'min':[0.1,0.1,0.1,0.1],    'max':[0.4,0.4,0.4,0.4]}
#    ref['emissS']    = {'soil':1, 'veg':0, 'log':0, 'file':'emissivity',   'min':[0.95,0.95,0.95,0.95],'max':[0.95,0.95,0.95,0.95]}
#    ref['Rugosity']  = {'soil':1, 'veg':0, 'log':0, 'file':'randrough',    'min':[0.01,0.01,0.01,0.01],'max':[0.2,0.2,0.2,0.2]}

    #ref['srfovf_ratio']   = {'soil':1, 'veg':0, 'log':0, 'file':'srfovf_ratio',       'min':[0,0,0,0],    'max':[1,1,1,1]}

    # - uniform channel parameters
    ref['ChanGWSeep']        = {'soil':0, 'veg':0, 'log':1, 'file':'chanparam',    'min':1e-5,    'max':1}
    ref['chanrough_all']     = {'soil':0, 'veg':0, 'log':0, 'file':'chanrough',    'min':10,      'max':30}
    ref['chanrough_wetland'] = {'soil':0, 'veg':0, 'log':0, 'file':'chanrough',    'min':5,       'max':15}
    ref['manningRiv_all']    = {'soil':0, 'veg':0, 'log':0, 'file':'chanmanningn', 'min':0.01,    'max':0.1}
    ref['manningRiv_wetland']= {'soil':0, 'veg':0, 'log':0, 'file':'chanmanningn', 'min':0.01,    'max':0.5}
    ref['snowmeltCo']        = {'soil':0, 'veg':0, 'log':0, 'file':'snowmeltCoeff','min':1e-8,'max':2.0e-7}

    # For extra GW storage
    ref['channel_ExtraGW_transfer_param']= {'soil':0, 'veg':0, 'log':1, 'file':'chanExtraparam',    'min':[1e-5],  'max':[0.1]}
    ref['Fraction_Hydroactive_ExtraGW']= {'soil':0, 'veg':0, 'log':1, 'file':'ExtraGW_hydroFraction',    'min':[1e-8],  'max':[0.01]}
    ref['d2H_ExtraGW']= {'soil':0, 'veg':0, 'log':0, 'file':'d2H_ExtraGW',    'min':[-65],  'max':[-57]}
    #ref['init_concIN'] = {'soil':0, 'veg':1, 'log':0, 'file':'init_concIN',    'min':[1,0.1,0.1,0.1],  'max':[15,1.5,1.5,3]}  #todo

    # - vegetation-dependent
    # vegetation state in maps
#    ref['LAI_Crops'] = {'soil':0, 'veg':0, 'log':0,'min':2,   'max':3,   'file':'lai_0'}
#    ref['LAI_Broad'] = {'soil':0, 'veg':0, 'log':0,'min':4,   'max':5,   'file':'lai_1'}
#    ref['LAI_Conif'] = {'soil':0, 'veg':0, 'log':0,'min':4,   'max':5,   'file':'lai_2'}
#    ref['LAI_Past']  = {'soil':0, 'veg':0, 'log':0,'min':2,   'max':3,   'file':'lai_3'}
#    ref['ntr_Crops'] = {'soil':0, 'veg':0, 'log':1,'min':1e-3,'max':50,  'file':'ntr_0'}
#    ref['bas_Crops'] = {'soil':0, 'veg':0, 'log':1,'min':1e-5,'max':0.1, 'file':'bas_0'}
#    ref['hgt_Crops'] = {'soil':0, 'veg':0, 'log':0,'min':0.1, 'max':2,   'file':'hgt_0'}
#    ref['Rt_Crops']  = {'soil':0, 'veg':0, 'log':0,'min':100, 'max':1000,'file':'root_0'}
     # water use
    ref['Gs_max']    = {'soil':0, 'veg':1, 'log':1,'min':[1e-3,4e-3,4e-3,1e-3],     'max':[1e-2,1e-2,1e-2,1e-2]}
#    ref['CnpQEff']   = {'soil':0, 'veg':1, 'log':1,'min':[1e-7,1e-7,1e-7,1e-7],'max':[1e-5,1e-5,1e-5,1e-5]}
#    ref['Topt']      = {'soil':0, 'veg':1, 'log':0,'min':[5,5,5,5,5],               'max':[25,25,25,25,25]}
#    ref['Tmax']      = {'soil':0, 'veg':1, 'log':0,'min':[25,25,25,25,25],          'max':[40,40,40,40,40]}
#    ref['Tmin']      = {'soil':0, 'veg':1, 'log':0,'min':[-5,-5,-5,-5,-5],          'max':[5,5,5,5,5]}
#    ref['AllocLeaf_a']={'soil':0, 'veg':1, 'log':0,'min':[1.5,1.5,1.5,1.5,1.5],     'max':[3,3,3,3,3]}
#    ref['AllocLeaf_b']={'soil':0, 'veg':1, 'log':1,'min':[1e-3,1e-3,1e-3,1e-3,1e-3],'max':[5e-2,5e-2,5e-2,5e-2,5e-2]}
#    ref['AllocStem_a']={'soil':0, 'veg':1, 'log':0,'min':[2,2,2,2,2],               'max':[4,4,4,4,4]}
#    ref['AllocStem_b']={'soil':0, 'veg':1, 'log':1,'min':[1e-8,1e-8,1e-8,1e-8,1e-8],'max':[9e-6,9e-6,9e-6,9e-6,9e-6]}
    ref['Gs_light']  = {'soil':0, 'veg':1, 'log':0,'min':[0,0,0,0],                 'max':[100,100,100,100]}
    ref['Gs_vpd']    = {'soil':0, 'veg':1, 'log':1,'min':[1e-6,1e-6,1e-6,1e-6],     'max':[1e-2,1e-2,1e-2,1e-2]}
#    ref['LWP_d']     = {'soil':0, 'veg':1, 'log':0,'min':[5,5,5,5,5],               'max':[20,20,20,20,20]}
#    ref['LWP_c']     = {'soil':0, 'veg':1, 'log':1,'min':[1e-2,1e-2,1e-2,1e-2,1e-2],'max':[4,4,4,4,4]}
#    ref['WiltPnt']   = {'soil':0, 'veg':1, 'log':0,'min':[0.01,0.01,0.01,0.01,0.01],'max':[0.15,0.15,0.15,0.15,0.15]}
#    ref['SLA']       = {'soil':0, 'veg':1, 'log':1,'min':[1e-4,1e-4,1e-4,1e-4,1e-4],'max':[0.05,0.05,0.05,0.05,0.05]}
#    ref['SRA']       = {'soil':0, 'veg':1, 'log':1,'min':[1e-4,1e-4,1e-4,1e-4,1e-4],'max':[5e-2,5e-2,5e-2,5e-2,5e-2]}
    #ref['WoodDens']  = {'soil':0, 'veg':1, 'log':0,'min':[],'max':[]}
#    ref['Fhdmax']    = {'soil':0, 'veg':1, 'log':0,'min':[11,11,11,11,11],          'max':[22,22,22,22,22]}
#    ref['Fhdmin']    = {'soil':0, 'veg':1, 'log':0,'min':[1,1,1,1,1],               'max':[10,10,10,10,10]}
#    ref['TurnovL']   = {'soil':0, 'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
#    ref['TurnovL_MWS']= {'soil':0,'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
#    ref['TurnovL_WSc']= {'soil':0,'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
#    ref['TurnovL_MTS']= {'soil':0,'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
#    ref['TurnovL_TSc']= {'soil':0,'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
#    ref['ColdStress_c']= {'soil':0,'veg':1,'log':0,'min':[-5,-5,-5,-5,-5],          'max':[5,5,5,5,5]}
#    ref['TurnovR']   = {'soil':0, 'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[1e-7,1e-7,1e-7,1e-7,1e-7]}
    ref['CWS_max']   = {'soil':0, 'veg':1, 'log':1,'min':[1e-4,2e-4,2e-4,1e-4],     'max':[4e-4,6e-3,6e-3,4e-4]}
    ref['Kroot']     = {'soil':0, 'veg':1, 'log':0,'min':[0.1,0.1,0.1,0.1],         'max':[10,10,10,10]}
    # energy balance
#    ref['Albedo']    = {'soil':0, 'veg':1, 'log':0,'min':[0.1,0.1,0.1,0.1,0.1],     'max':[0.25,0.25,0.25,0.25,0.25]}
#    ref['Emissivity']= {'soil':0, 'veg':1, 'log':0,'min':[0.9,0.9,0.9,0.9,0.9],     'max':[0.99,0.99,0.99,0.99,0.99]}
    ref['KBeers']    = {'soil':0, 'veg':1, 'log':0,'min':[0.4,0.4,0.4,0.4],         'max':[0.7,0.7,0.7,0.7]}
#    ref['WUE_cnp']   = {'soil':0, 'veg':1, 'log':0,'min':[500,500,500,500,500],     'max':[5000,5000,5000,5000,5000]}
#    ref['TurnovL_DGr'] ={'soil':0,'veg':1, 'log':1,'min':[1e-9,1e-9,1e-9,1e-9,1e-9],'max':[2e-6,1e-6,1e-6,1e-6,1e-6]}
#    ref['TurnovL_DGrT']={'soil':0,'veg':1, 'log':0,'min':[10,10,10,10,10],          'max':[20,20,20,20,20]}
    # physiology
    # ref['NPP/GPP']   = {'soil':0, 'veg':1, 'min':0.2,  'max':0.6,   'log':0}
    # ref['CnpQEff']   = {'soil':0, 'veg':1, 'min':1e-06,'max':5e-06, 'log':0}
    # Structure
    #ref['WoodDens']  = {'soil':0, 'veg':1, 'min':1e05, 'max':1e06, 'log':0}
"""