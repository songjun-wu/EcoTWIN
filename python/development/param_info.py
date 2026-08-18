import numpy as np


class Info:
    nodata = -9999.0 # nodata value for param.ini and all spatial maps
    soil_index = [1,2,3,4,5,6,7]  # Column index in param.ini
    landuse_index = [8,9,10,11,12,13,14]  # Column index in param.ini
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
    # 5 :           cat4, organic soils in north-eastern Europe ['PZ_HR', 'AN']
    # 6 :           cat5, rocks/mountainous areas (low elevation excluded): High soil moisture, low inflitration capacity, more overland flow, older age ['FL_LP_RG_Rocks', 'CR', 'Glacier_Snow', 'InlandWater']
    # 7 :           cat6, Peat
    # === Land use types === 
    # 8 : Crop
    # 9 : Pasture
    # 10: Grassland
    # 11: Forest
    # 12: Sparse vegetation/bare soil
    # 13: Urban
    # 14: Wetland

    ### Crop info ###
    # Crop, pasture, grass, forest, sparse/bare soil, urban, wetland
    nadd = {}
    nadd['is_crop'] = {'value':[1, 0, 0, 0, 0, 0, 0]}
    nadd['fert_add'] = {'value':[12, 0, 0, 0, 0, 0, 0]}
    nadd['fert_day'] = {'value':[87, 87, 87, 87, 87, 87, 87]}
    nadd['fert_down'] = {'value':[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    nadd['fert_period'] = {'value':[30, 30, 30, 30, 30, 30, 30]}
    nadd['fert_IN'] = {'value':[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]}

    nadd['manure_add'] = {'value':[0, 0, 0, 0, 0, 0, 0]}
    nadd['manure_day'] = {'value':[110, 110, 110, 110, 110, 110, 110]}
    nadd['manure_down'] = {'value':[0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['manure_period'] = {'value':[30, 30, 30, 30, 30, 30, 30]}
    nadd['manure_IN'] = {'value':[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}

    nadd['residue_add'] = {'value':[1, 1, 1, 1, 0, 0, 0]}
    nadd['residue_day'] = {'value':[242, 260, 260, 290, 290, 290, 290]}
    nadd['residue_down'] = {'value':[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]}
    nadd['residue_period'] = {'value':[30, 30, 30, 30, 30, 30, 30]}
    nadd['residue_fast_NP'] = {'value':[0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]}

    nadd['up1'] = {'value':[10, 8, 7, 5, 3, 2, 10]}
    nadd['up2'] = {'value':[0.6, 0.3, 0.3, 0.6, 0.5, 0.2, 0.6]}
    nadd['up3'] = {'value':[0.04, 0.03, 0.03, 0.018, 0.018, 0.018, 0.04]}
    nadd['upper_uptake'] = {'value':[0.99, 0.99, 0.99, 0.85, 0.99, 0.95, 0.95]}
    nadd['plant_day'] = {'value':[85, 55, 55, 55, 55, 55, 55]}  
    nadd['harvest_day'] = {'value':[190, 190, 190, 190, 190, 190, 190]}  # The harvest day has to be consistent across all vegetation types
    nadd['harvest_period'] = {'value':[110, 110, 110, 110, 110, 110, 110]}  # The harvest period has to be consistent across all vegetation types
    nadd['harvest_coeff'] = {'value':[0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}  # The harvest coefficient has to be consistent across all vegetation types


    nadd['irrigation_thres'] = {'value':[0.6,0.0,0,0,0,0,0]}  # The threshold (soil moisture/field capacity) below which irrigation is needed




class Param:
    ### === parameters to calibrate === 
    ref = {}    

    ref['depth3']   =           {'type':'global',  'log':0, 'file':'depth3',   'min':[0.8], 'max':[2.0], 'fix_value':None,}

    # === PET seperation and Max canopy storage === 
    ref['alpha']   =            {'type':'global',  'log':1, 'file':'alpha',   'min':[1e-5], 'max':[5e-2], 'fix_value':None,}  # Maximum canopy storage = alpha * LAI
    ref['rE']   =               {'type':'global',  'log':0, 'file':'rE',   'min':[-5], 'max':[-0.1], 'fix_value':None,}  # the more negative the more transpiration

    # === Management ===
    ref['irrigation_FC_thres']   =   {'type':'global',  'log':1, 'file':'irrigation_FC_thres',   'min':[0.01], 'max':[0.1], 'fix_value':[0.1],}  # The soil moisture threshold for irrigation
    ref['irrigation_coeff']   = {'type':'global',   'log':1, 'file':'irrigation_coeff',   'min':[0.01], 'max':[0.2], 'fix_value':[0.0],}  # Irrigation coefficient to determine the actual water demand from water deficit [-]
    ref['drainage_intensity']   = {'type':'global_landuse',  'log':0, 'file':'drainage_intensity',   'min':[0.0], 'max':[0.99], 'fix_value':None, 'weights':[1,0,0,0,0,0,0],}  # The intensity of drainage based on the density of drainage network [-], only needed when drainage is enabled
    ref['herbivory_uptake_coeff']   = {'type':'global',  'log':0, 'file':'herbivory_uptake_coeff',   'min':[2e-4], 'max':[2e-3], 'fix_value':[0.0],}  # The coefficient for herbivory uptake [-]

    # Snow
    ref['snow_rain_thre']   =   {'type':'global',   'log':0, 'file':'snow_rain_thre',   'min':[-5], 'max':[5], 'fix_value':None,}
    ref['deg_day_min']   =      {'type':'global',   'log':0, 'file':'deg_day_min',   'min':[0], 'max':[2e-3], 'fix_value':None,}
    ref['deg_day_max']   =      {'type':'global',   'log':0, 'file':'deg_day_max',   'min':[2e-3], 'max':[1e-2], 'fix_value':None,}
    ref['deg_day_increase']   = {'type':'global',   'log':0, 'file':'deg_day_increase',   'min':[0.1], 'max':[0.9], 'fix_value':None,}

    
    # === Pedotransfer function ===
    # Soil proporties (field capacity, wilting point, hydraulic conductivity)
    ref['ref_thetaS']   = {'type':'global',   'log':0, 'file':'ref_thetaS',   'min':[0.4], 'max':[0.9], 'fix_value':None,} # 'min':[0.5], 'max':[0.99]
    ref['PTF_VG_clay']   = {'type':'global',   'log':1, 'file':'PTF_VG_clay',   'min':[5e-8], 'max':[5e-3], 'fix_value':None,}
    ref['PTF_VG_Db']   = {'type':'global',   'log':1, 'file':'PTF_VG_Db',   'min':[5e-4], 'max':[5e-1], 'fix_value':None,}
    ref['PTF_Ks_const']   = {'type':'global_landuse',   'log':0, 'file':'PTF_Ks_const',   'min':[-1.2], 'max':[-0.3], 'fix_value':None, 'weights':[1,1,1,1,1,2,1],} # [-1.2, -0.29]
    ref['PTF_Ks_sand']   = {'type':'global',   'log':0, 'file':'PTF_Ks_sand',   'min':[0.006], 'max':[0.026], 'fix_value':None,}
    ref['PTF_Ks_clay']   = {'type':'global',   'log':0, 'file':'PTF_Ks_clay',   'min':[0.003], 'max':[0.013], 'fix_value':None,}
    

    # Field capacity
    #ref['SWP']   = {'type':'soil',   'log':0, 'file':'SWP',   'min':[10]*Info.N_soil, 'max':[33]*Info.N_soil, 'fix_value':[33]*Info.N_soil,}
    #

    # === Infiltration === 
    ref['KvKh']   = {'type':'global',   'log':0, 'file':'KvKh',   'min':[1e-2], 'max':[0.5], 'fix_value':None,}  # Vertical to horizontal ksat anisotropy ratio
    ref['psiAE']   = {'type':'global',   'log':0, 'file':'psiAE',   'min':[1e-2], 'max':[1.3], 'fix_value':None,}

    # === Distrituted soil proporties to different layers === 
    # Deactivated because soil proporties are calculated in each layer based on depth-dependent soil data
    #ref['KKs']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None,}  
    #ref['Ksat']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None,}
    #ref['BClambda']   = {'type':'soil',   'log':0, 'file':'KKs',   'min':[2]*Info.N_soil, 'max':[15]*Info.N_soil, 'fix_value':None,}
    ref['preferential_flow_coeff']   = {'type':'global_soil',   'log':0, 'file':'preferential_flow_coeff',   'min':[1e-3], 'max':[1e-1], 'fix_value':None, 'weights':[0,0,0,0,0,1,0],}  # The coefficient parameter for preferential flow [-]

    # === Percolation === 
    # Only needed for opt_percolation == 2
    ref['perc_optimal_theta']   = {'type':'landuse',   'log':0, 'file':'perc_optimal_theta',   'min':[0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'max':[1.0,1.0,1.0,1.0,1.0,1.0,1.0], 'fix_value':[0.2, 0.5, 0.5, 0.5, 0.5, 0.2, 1.0],}
    #ref['percExp']   = {'type':'soil',   'log':0, 'file':'percExp',   'min':[1]*Info.N_soil, 'max':[50]*Info.N_soil, 'fix_value':None,}

    # === Capillary flow === 
    ref['capillary_flow_rate']   = {'type':'global_landuse',   'log':0, 'file':'capillary_flow_rate',   'min':[0.5], 'max':[1], 'fix_value':None, 'weights':[0.01, 0.1, 0.1, 0.1, 0.1, 0.0, 1.0],}  # The reference conductivity of capillary flow from shallow GW zone to bottom soil layer [m/s]
    
    # === Evapotranspiration === 
    #ref['froot_coeff']   = {'type':'landuse',   'log':1, 'file':'froot_coeff',   'min':[0.8]*Info.N_landuse, 'max':[0.95, 0.95, 0.95, 0.999, 0.92, 0.81, 0.95], 'fix_value':None,} # The higher the more deeper roots [max for crops: 0.95, for forest: 0.999]
    ref['froot_coeff']   = {'type':'landuse',   'log':1, 'file':'froot_coeff',   'min':[0.91]*Info.N_landuse, 'max':[0.98]*Info.N_landuse, 'fix_value':[0.95, 0.95, 0.94, 0.965, 0.95, 0.95, 0.95],} # The higher the more deeper roots [max for crops: 0.95, for forest: 0.999]
    ref['ET_weight'] = {'type':'global_soil',   'log':0, 'file':'ET_weight',   'min':[1.0], 'max':[3.0], 'fix_value':None, 'weights':[1,1,1,1,1,0.8,1],} # Evaporation and Transpiration should be adjusted due to potential underestimation of daily simulaton compared to integral of hourly simulatont [-]

    # === GW recharge === 
    ref['perc_vadose_coeff']   = {'type':'global',   'log':1, 'file':'perc_vadose_coeff',   'min':[1e-3], 'max':[1], 'fix_value':None,} # Coefficient parameter for GW recharge [1e-5, 1]
    ref['init_GW'] = {'type':'global',   'log':0, 'file':'init_GW',   'min':[1], 'max':[50], 'fix_value':None,} # Initial GW storage in m

    # === Routing === 
    ref['pOvf_toChn']   = {'type':'global',   'log':1, 'file':'pOvf_toChn',   'min':[1e-3], 'max':[1], 'fix_value':[1],}  # Proportion of overland flow routed to stream (corrected by channel lenght and cell size) [1e-3, 1]
    ref['Ks_surface']   = {'type':'landuse',   'log':0, 'file':'Ks_surface',   'min':[1e-1]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':[0.9, 0.9, 0.9, 0.8, 1.0, 1.0, 0.5],}  # The reference conductivity of surface for overland flow routing [m/day] [1e-3, 1]
    ref['Ks_vadose']   = {'type':'global',   'log':1, 'file':'Ks_vadose',   'min':[1e-3], 'max':[1], 'fix_value':None,}  # The reference conductivity of vadose zone for interflow routing [m/day] [1e-3, 1]
    ref['Ks_GW']   = {'type':'global',   'log':1, 'file':'Ks_GW',   'min':[1e-9], 'max':[1e-3], 'fix_value':None,}  # The reference conductivity of GW zone for interflow routing [m/day]
    ref['lat_to_Chn_vadose']   = {'type':'global',   'log':1, 'file':'lat_to_Chn_vadose',   'min':[0.1]*Info.N_landuse, 'max':[15]*Info.N_landuse, 'fix_value':None,} # The ratio between conductivities of lateral flow and channel recharge in vadose zone [-]  [0.1,10]
    ref['lat_to_Chn_GW']   = {'type':'global',   'log':1, 'file':'lat_to_Chn_GW',   'min':[1e-3]*Info.N_landuse, 'max':[1e1]*Info.N_landuse, 'fix_value':None,} # The ratio between conductivities of lateral flow and channel recharge in GW zone [-]
    ref['interfExp']   = {'type':'global',   'log':1, 'file':'interfExp',   'min':[1e-2]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None,}
    ref['GWfExp']   = {'type':'global',   'log':1, 'file':'GWfExp',   'min':[1e-5]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None,}
    ref['Manningn']   = {'type':'global',   'log':1, 'file':'Manningn',   'min':[1e-4]*Info.N_landuse, 'max':[10]*Info.N_landuse, 'fix_value':None,}
    ref['ratio_to_interf'] = {'type':'global',   'log':0, 'file':'ratio_to_interf',   'min':[0], 'max':[1], 'fix_value':None,}  #[0,1]

    # === Channel === 
    ref['Echan_alpha']   = {'type':'global',   'log':1, 'file':'Echan_alpha',   'min':[0.1], 'max':[10], 'fix_value':[1],}  # Correction factor in Priestley-Taylor equation

    # === Mixing === 
    ref['nearsurface_mixing']   = {'type':'global',   'log':0, 'file':'nearsurface_mixing',   'min':[0], 'max':[1], 'fix_value':None,} 
    ref['diffuse_molecular_coefficient']   = {'type':'global',   'log':1, 'file':'diffuse_molecular_coefficient',   'min':np.array([1.06e-5]), 'max':np.array([1.06e-5]), 'fix_value':[1.06e-5],}  # The coefficient for Fickian diffusion [m2/s]
    

    # === Tracking ===      
    ref['CG_n_soil'] = {'type':'global',   'log':0, 'file':'CG_n_soil',   'min':[0.5], 'max':[1], 'fix_value':None,}
    #ref['delta_d18o_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_d18o_init_GW',   'min':[-5]*Info.N_soil, 'max':[5]*Info.N_soil, 'fix_value':None,} # The adjustment of initial d18o composition


    # === Carbon module ===
   


    # === Carbon simulation ===
    # Initialization
    ref['delta_doc_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_doc_init_GW',   'min':[-1]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None,} # The adjustment of initial doc composition
    #ref['carboxylation_rate'] = {'type':'landuse',   'log':0, 'file':'carboxylation_rate',   'min':np.array([95,75,75,35,0,0])*1e-6, 'max':np.array([105,85,85,65,30,30])*1e-6, 'fix_value':None,} # Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]
    #ref['ETransport'] = {'type':'landuse',   'log':0, 'file':'ETransport',   'min':np.array([180,130,130,100,20,20])*1e-6, 'max':np.array([200,160,160,120,80,80])*1e-6, 'fix_value':None,} # Maximum electron transport rate at 25 Celsius [1.E-6 * Mol/m^2 leafarea/s] (Jmax=1.9*V_max^25 for C3 plants)
    # Assimilation
    ref['carboxylation_rate'] = {'type':'global_landuse',   'log':0, 'file':'carboxylation_rate',   'min':[0.8], 'max':[1.2], 'fix_value':None, 'weights':np.array([80,80,80,80,70,15,80])*1e-6,} # Carboxylation rate at 25 degree celcius [mol(CO2)/(m2*s)]; np.array([100,80,80,50,70,70])*1e-6
    ref['ETransport'] = {'type':'global_landuse',   'log':0, 'file':'ETransport',   'min':[0.8], 'max':[1.2], 'fix_value':None, 'weights':np.array([145,145,145,145,130,30,145])*1e-6,} # Maximum electron transport rate at 25 Celsius [1.E-6 * Mol/m^2 leafarea/s] (Jmax=1.9*V_max^25 for C3 plants); np.array([190,145,145,110,130,130])*1e-6
    # Plant phenology
    ref['C_in_LeafArea'] = {'type':'landuse',   'log':0, 'file':'C_in_LeafArea',   'min':[], 'max':[], 'fix_value':np.array([0.45, 0.45, 0.45, 0.25, 0.3, 0.3, 0.3])/12,} # Carbon content per leaf area in [m2(leaf)/gC] <== [m2(leaf)/mol(Carbon)/12]
    ref['LAI_shed_coef'] = {'type':'landuse',   'log':0, 'file':'LAI_shed_coef',   'min':[], 'max':[], 'fix_value':np.array([0.0055, 0.0055, 0.0055, 0.0027, 0.0027, 0.0027, 0.0055]),} # Leaf shedding coefficient related to LAI; Time in which leaves are constantly shedded [days-1]
    ref['tau_wood_C'] = {'type':'landuse',   'log':0, 'file':'tau_wood_C',   'min':[], 'max':[], 'fix_value':np.array([1,1,1,60,1,1,1])*365,} # Life time scale of the wood pool and vegetation dynamics [days]
    ref['plant_wood_CP_max'] = {'type':'landuse',   'log':0, 'file':'plant_wood_CP_max',   'min':[], 'max':[], 'fix_value':[0,0,0,1,0.05,0.05,0.01],} # The maximum carbon content in wood pool relative to the maximum carbon content in wood pool for forest [decimal] <== [molC/m2]; the global maximum should be ~2000*12 gC/m2, here we set to 15,000 given the lower carbon biomass in Europe
    ref['plant_reserve_CP_max'] = {'type':'landuse',   'log':0, 'file':'plant_reserve_CP_max',   'min':[], 'max':[], 'fix_value':[4*4,4*3,4*3,2*6,3*4.5,3*4.5,4*4],} # Term to calculate maximum carbon content in reserve pool at optimal conditions [-]: first term is the ratio of ratio of vegetation green pool to reserve pool at maximum LAI, while second term is maximum LAI
    
    # Distribute NPP to vegetation pools
    ref['frac_NPP_to_green'] = {'type':'landuse',   'log':0, 'file':'frac_NPP_to_green',   'min':[], 'max':[], 'fix_value':[0.8,0.8,0.8,0.6,0.8,0.8,0.55],} # The fraction of NPP addition to vegetation green pool [-]
    ref['frac_NPP_to_wood'] = {'type':'landuse',   'log':0, 'file':'frac_NPP_to_wood',   'min':[], 'max':[], 'fix_value':[0.05,0.05,0.05,0.3,0.05,0.05,0.3],} # The fraction of NPP addition to wood green pool [-]

    # Distribute litter to soil carbon pools
    ref['alpha_litter_distribution_nonwood'] = {'type':'landuse',   'log':0, 'file':'alpha_litter_distribution_nonwood',   'min':[0.25], 'max':[1.44], 'fix_value':[1.5, 1.1, 0.87, 0.45, 0.7, 0.7, 0.87],} # The fraction of non-wood plant materials going to decomposable plant material litter pool [-]
    ref['frac_leaf_in_litter'] = {'type':'global',   'log':0, 'file':'frac_leaf_in_litter',   'min':[0.1], 'max':[1], 'fix_value':[0.5],} # The fraction of leaf in non-woody plant materials (compared to fine root) going to decomposable plant material litter pool [-]

    # Carbon decomposition
    ref['frac_DOC_production_from_litter_CP'] = {'type':'global',   'log':0, 'file':'frac_DOC_production_from_litter_CP',   'min':[2e-3], 'max':[1e-1], 'fix_value':None,} # The fraction of DOC production from decomposition of litter carbon pool [-]  # 2e-3 in literature
    ref['frac_DOC_production_from_soil_CP'] = {'type':'global',   'log':0, 'file':'frac_DOC_production_from_soil_CP',   'min':[2e-3], 'max':[2e-1], 'fix_value':None,} # The fraction of DOC production from decomposition of soil carbon pool [-]  # 1e-2 in literature
    ref['ref_frac_soluble_to_doc'] = {'type':'landuse',   'log':1, 'file':'ref_frac_soluble_to_doc',   'min':[5e-4]*Info.N_landuse, 'max':[1e-1]*Info.N_landuse, 'fix_value':None,'weights':None} # Reference fraction of soluble carbon going to DOC pool [-]
    

    # Reference decomposition rates of carbon pools
    ref['f_groundwater_depth_decay_exp_base'] = {'type':'global',   'log':0, 'file':'f_groundwater_depth_decay_exp_base',   'min':[0.1], 'max':[2], 'fix_value':None,} # Exponential base for depth function of groundwater table [-]; this parameter determines how dissolution of DOC is affected by the depth of groundwater table
    #ref['transformation_exp_base'] = {'type':'global',   'log':0, 'file':'transformation_exp_base',   'min':[0.08], 'max':[0.2], 'fix_value':None,} # Exponential base for temperature function of soil decomposition and denitrification; the higher the more sensitive to temperature changes [-]
    ref['fdepth_decay_Exp'] = {'type':'global',   'log':1, 'file':'fdepth_decay_Exp',   'min':[0.5]*Info.N_soil, 'max':[10]*Info.N_soil, 'fix_value':None,} # Exponential decay function for soil decomposition based on depth [-]
    ref['ref_decomp_rate_doc'] = {'type':'spatial_distributed_global_landuse',   'log':0, 'file':'ref_decomp_rate_doc',   'min':[1e-4], 'max':[1e-1], 'fix_value':None, 'weights':[1,1,1,1,1,1,0.9],} # Reference decomposition rate of DOC pool [day-1]
    ref['respiration_river'] = {'type':'global',   'log':1, 'file':'respiration_river',   'min':[1e-3], 'max':[1e-1], 'fix_value':None,} # Reference rates of aquatic heterotrophic respiration [gC m-2 day-1]

    # === Nitrogen simulation ===
    ref['delta_no3_init_GW'] = {'type':'landuse',   'log':0, 'file':'delta_no3_init_GW',   'min':[-2,-1,-1,-1,-1,-1,-1], 'max':[2,1,1,1,1,1,1], 'fix_value':None,} # The adjustment of initial no3 composition
    
    ref['denitrification_river']   = {'type':'global_landuse',   'log':1, 'file':'denitrification_river',   'min':[1e-3], 'max':[1e-1], 'fix_value':None, 'weights':[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 1.0],} # Reference rates of aquatic denitrification [gN m-2 day-1]
    #ref['autotrophic_uptake_aquatic']   = {'type':'landuse',   'log':0, 'file':'autotrophic_uptake_aquatic',   'min':[1e2]*Info.N_landuse, 'max':[5e2]*Info.N_landuse, 'fix_value':None,}
    #ref['primary_production_aquatic']   = {'type':'landuse',   'log':0, 'file':'primary_production_aquatic',   'min':[1e-1]*Info.N_landuse, 'max':[1]*Info.N_landuse, 'fix_value':None,}
    ref['denitrification_soil']   = {'type':'spatial_distributed_global_landuse',   'log':1, 'file':'denitrification_soil',   'min':[1e-5], 'max':[5e-2], 'fix_value':None, 'weights':[1,1,1,1,1,1,1.3],}
    #ref['degradation_soil']   = {'type':'landuse',   'log':1, 'file':'degradation_soil',   'min':[1e-6]*Info.N_landuse, 'max':[1e-4,1e-4,1e-4,1e-4,1e-5,1e-5], 'fix_value':None,}
    #ref['mineralisation_soil']   = {'type':'landuse',   'log':1, 'file':'mineralisation_soil',   'min':[1e-5]*Info.N_landuse, 'max':[0.4,0.4,0.3,0.2,0.1,0.01], 'fix_value':None,}
    #ref['dissolution_soil']   = {'type':'landuse',   'log':1, 'file':'dissolution_soil',   'min':[1e-3]*Info.N_landuse, 'max':[200]*Info.N_landuse, 'fix_value':None,}
    ref['deni_soil_moisture_thres']   = {'type':'spatial_distributed_global',   'log':0, 'file':'deni_soil_moisture_thres',   'min':[0.1], 'max':[0.7], 'fix_value':None,}

    #ref['NC_ratio_plant_green'] = {'type':'global',   'log':2, 'file':'NC_ratio_plant_green',   'min':[16], 'max':[70], 'fix_value':None,} # Carbon nitrogen ratio in vegetation green pool  [gC/gN]; log:2 means the parameter values are the inverse of the nitrogen carbon ratio for mathematic simplicity
    #ref['NC_ratio_plant_wood'] = {'type':'global',   'log':2, 'file':'NC_ratio_plant_wood',   'min':[50], 'max':[250], 'fix_value':None,} # Carbon nitrogen ratio in vegetation wood pool  [gC/gN]
    #ref['NC_ratio_fast_pool_nonwood'] = {'type':'global',   'log':2, 'file':'NC_ratio_fast_pool_nonwood',   'min':[30], 'max':[150], 'fix_value':None,} # Carbon nitrogen ratio in non-wood fast (litter) pool (acid, ethanol, and nonsoluble)  [gC/gN]
    #ref['NC_ratio_fast_pool_wood'] = {'type':'global',   'log':2, 'file':'NC_ratio_fast_pool_wood',   'min':[250], 'max':[1400], 'fix_value':None,} # Carbon nitrogen ratio in wood fast (litter) pool (acid, ethanol, and nonsoluble)  [gC/gN]
    #ref['NC_ratio_humus_pool'] = {'type':'global',   'log':2, 'file':'NC_ratio_humus_pool',   'min':[8], 'max':[30], 'fix_value':None,} # Carbon nitrogen ratio in humus pool  [gC/gN]

    ref['NC_ratio_plant_green'] = {'type':'global',   'log':2, 'file':'NC_ratio_plant_green',   'min':[30], 'max':[70], 'fix_value':None,} # Nitrogen carbon ratio in vegetation green pool  [gN/gC]; log:2 means the parameter values are the inverse of the nitrogen carbon ratio for mathematic simplicity
    ref['NC_ratio_plant_wood'] = {'type':'global',   'log':2, 'file':'NC_ratio_plant_wood',   'min':[50], 'max':[250], 'fix_value':None,} # Nitrogen carbon ratio in vegetation wood pool  [gN/gC]
    ref['NC_ratio_dpm_litter'] = {'type':'global',   'log':2, 'file':'NC_ratio_dpm_litter',   'min':[40], 'max':[150], 'fix_value':None,} # Nitrogen carbon ratio in the litter pool of decomposable plant material  [gN/gC]
    ref['NC_ratio_rpm_litter'] = {'type':'global',   'log':2, 'file':'NC_ratio_rpm_litter',   'min':[200], 'max':[1400], 'fix_value':None,} # Nitrogen carbon ratio in the litter pool of resistant plant material  [gN/gC]
    #ref['NC_ratio_humus_pool'] = {'type':'global',   'log':2, 'file':'NC_ratio_humus_pool',   'min':[15], 'max':[15], 'fix_value':[1/15],} # Nitrogen carbon ratio in humus pool  [gN/gC]



    # todo
    # 1_4
    #ref['frac_DOC_production_from_litter_CP'] = {'type':'global',   'log':0, 'file':'frac_DOC_production_from_litter_CP',   'min':[1e-2], 'max':[1e-1], 'fix_value':None,} # The fraction of DOC production from decomposition of litter carbon pool [-]  # 2e-3 in literature
    #ref['ref_frac_soluble_to_doc'] = {'type':'global',   'log':1, 'file':'ref_frac_soluble_to_doc',   'min':np.array([5e-4]), 'max':np.array([2e-3]), 'fix_value':None,} # Reference fraction of soluble carbon going to DOC pool [-]
    #ref['denitrification_soil']   = {'type':'global',   'log':1, 'file':'denitrification_soil',   'min':[1e-5], 'max':[5e-2], 'fix_value':None, 'weights':[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 1.0],}
    #ref['deni_soil_moisture_thres']   = {'type':'global',   'log':0, 'file':'deni_soil_moisture_thres',   'min':[0.1], 'max':[0.7], 'fix_value':None,}

