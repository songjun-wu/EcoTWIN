import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
import multiprocessing
from multiprocessing import Pool, cpu_count
import numpy as np
import time
import post_plot
import GIS_tools
import pandas as pd
import pickle
import subprocess
from def_GEM_forward import *


def clean_directory(path_to_remove):
    if os.path.exists(path_to_remove):
        shutil.rmtree(path_to_remove)

def clean_directory_parallel(catchment_list):
    tasks = []
    for catchment_ID in catchment_list:
        path_to_remove = Path.work_path + mode + '/outputs/cali/yearly/' + str(catchment_ID)
        tasks.append((path_to_remove))
    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 40)) as pool:
        pool.starmap(clean_directory, tasks)

def sort_obs_gauge_index(mode, catchment_list):
    
    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    os.makedirs(Path.work_path + mode +'/outputs/cali_merged/performance/', exist_ok=True)

    
    for kk in range(len(vars)):
        obs_all = np.array([])
        site_info = pd.read_csv(Path.data_path+'catchment_info/site_info_'+vars[kk]+'.csv', index_col='site')
        catchmentID_list = []
        key_list = []

        df = pd.DataFrame([])

        for catchment_ID in catchment_list:
             
            obs_path = Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/obs/'
            keys = pickle.load(open(obs_path+vars[kk]+'_gauge_list', 'rb'))
            sites = pickle.load(open(obs_path+vars[kk]+'_site_list', 'rb'))

            if len(keys) > 0:
                for i in range(len(keys)):
                    _obs = np.fromfile(obs_path+obs_vars[kk]+'_obs.bin').reshape(len(keys), -1)
                    catchmentID_list.append(catchment_ID)
                    key_list.append(keys[i])
                    obs_all = np.append(obs_all, _obs[i,:])

        
        with open(Path.data_path+'catchment_info/gauge_info_forward_'+vars[kk], 'wb') as f:
            pickle.dump([catchmentID_list, key_list, obs_all], f)
        gauge_info = pickle.load(open(Path.data_path+'catchment_info/gauge_info_forward_'+vars[kk], 'rb'))

def get_performance(mode, chainID_list):
    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    

    os.makedirs(Path.work_path + mode +'/outputs/cali_merged/performance/', exist_ok=True)
    for kk in range(len(vars)):
        gauge_info = pickle.load(open(Path.data_path+'catchment_info/gauge_info_forward_'+vars[kk], 'rb'))

        catchment_list = np.array(gauge_info[0]).astype(str)
        catchment_list_unique = np.unique(catchment_list).astype(str)
        key_list = np.array(gauge_info[1])
        obs_all = np.array(gauge_info[2]).reshape(len(catchment_list),-1)

        locals()['kge_'+vars[kk]] = []
        
        for catchment_ID in catchment_list_unique:
                           
  
            counter = 0
            for xx, chainID in enumerate(chainID_list):
                save_path = Path.work_path + mode +'/outputs/cali/' + str(catchment_ID) + '/' + str(chainID) + '/'
                if not os.path.exists(save_path+'age_canopy_storage_map.bin'):
                    continue
                if xx == 0:
                    _sim = np.fromfile(save_path+sim_vars[kk]+'.bin')
                else:
                    _sim += np.fromfile(save_path+sim_vars[kk]+'.bin')
                counter += 1
            _sim = (_sim.reshape(16437, -1).T)[:, Info.spin_up:] / counter
     
            idx = np.where(catchment_list == catchment_ID)[0]
            idx = [idx] if isinstance(idx, int) else idx
            sim_idx = key_list[idx]
            _obs = obs_all[idx,:]
            _sim += 0.1
            _obs += 0.1
            for i in range(len(idx)):
                locals()['kge_'+vars[kk]].append(GEM_tools.kge(_sim[sim_idx[i],:], _obs[i,:]))
            
    return locals()['kge_discharge'], locals()['kge_isotope'], locals()['kge_nitrate']
                
def split_indices(n_tasks, n_cores):
    base = n_tasks // n_cores
    extra = n_tasks % n_cores
    sizes = [base + 1 if i < extra else base for i in range(n_cores)]
    indices = []
    start = 0
    for size in sizes:
        indices.append((start, start + size))
        start += size
    return indices

def forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, Vars=None, replace=False, batch_num=None, batch_ID=None, experiment=None):

    if Vars is None:
        Vars = ['snow_depth', 'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 'channel_storage', \
                'snowmelt', 'infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose', \
                'rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3', 'rperc_vadose', \
                'soil_evap', 'transp', 'irrigation_from_GW', \
                'overland_flow_input', 'overland_flow_output', 'overland_flow_toChn', 'interflow_input', 'interflow_output', 'interflow_toChn', \
                'GWflow_input', 'GWflow_output', 'GWflow_toChn', 'discharge', 'channel_evaporation', \
                'age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_chanS', 'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_chanS', \
                'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_chanS', 'nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'deni_river']


    # Merge results in each catchment to one
    if batch_num is not None:
        indices = split_indices(n_tasks=len(Vars), n_cores=batch_num)
        start = indices[batch_ID][0]
        end = indices[batch_ID][1]
        Vars = Vars[start:end]
        print(batch_ID, start, end, Vars)

    tasks = []
    for var in Vars:
        tasks.append((mode, temp_res, catchment_list, chainID_list, [var], replace, experiment))
    # Use multiprocessing pool to run in parallel
    if experiment is None:
        max_cores = 5
    else:
        max_cores = 2
    with Pool(processes=min(cpu_count(), max_cores)) as pool:          
        pool.starmap(forward_post_catchment_merge_parallel, tasks)


def forward_post_catchment_merge_parallel(mode, temp_res, catchment_list, chainID_list, Vars, replace, experiment):
    post_plot.merge_spatial_results_EU(mode, temp_res, catchment_list, Vars, chainID=None, replace=replace, experiment=experiment)



# Young water fraction
def forward_post_young_water_fraction(mode, catchment_list, batch_num=None, batch_ID=None, experiment=None):
    
    # Merge results of 40 chains for each catchment
    if batch_num is not None:
        indices = split_indices(n_tasks=len(catchment_list), n_cores=batch_num)
        start = indices[batch_ID][0]
        end = indices[batch_ID][1]
        catchment_list_split = catchment_list[start:end]
        print(batch_ID, start, end, len(catchment_list_split))

    # merge spatial results for each chain
    tasks = []
    for catchment_ID in catchment_list_split:
        tasks.append((catchment_ID, 3, experiment))

    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 20)) as pool:          
        pool.starmap(forward_post_young_water_fraction_parallel, tasks)

def forward_post_young_water_fraction_parallel(catchment_ID, young_water_thres, experiment):
    # Young water fraction
    post_plot.young_water_fraction(catchment_ID, young_water_thres=young_water_thres, experiment=experiment)


# Flow path length
def forward_post_flow_path_length(mode, catchment_list, batch_num=None, batch_ID=None, experiment=None):
    
    if batch_num is not None:
        indices = split_indices(n_tasks=len(catchment_list), n_cores=batch_num)
        start = indices[batch_ID][0]
        end = indices[batch_ID][1]
        catchment_list_split = catchment_list[start:end]
        print(batch_ID, start, end, len(catchment_list_split))

    # merge spatial results for each chain
    tasks = []
    for catchment_ID in catchment_list_split:
        tasks.append([catchment_ID, experiment])

    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 20)) as pool:          
        pool.starmap(forward_post_flow_path_length_parallel, tasks)

def forward_post_flow_path_length_parallel(catchment_ID, experiment):
    # Flow path length
    post_plot.flow_path_length(catchment_ID, experiment)





if __name__ == "__main__":
    mode = 'forward_all'
    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainID_list = np.arange(40)
    temp_res = 'monthly'

    #experiment = None
    #experiment = 'ssp585'
    experiment = 'ssp126'


    multiprocessing.set_start_method("spawn", force=True)


    # model performance
    #sort_obs_gauge_index(mode, catchment_list)
    
    #post_plot.merge_performance_EU(mode, catchment_list, chainID=None, chainID_list=chainID_list, temp_res=temp_res)
    #post_plot.plot_performance_EU(mode, chainID=None)

    #post_plot.plot_performance_specific_site(mode, site='IRL00172')

    

    # Merge spatial results
    batch_ID = 0
    batch_num = 1

    # === Merge and average chain-specific results ===
    #forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, Vars=None, replace=True, batch_num=batch_num, batch_ID=batch_ID, experiment=experiment)




    

    # === Young water fraction ===
    #forward_post_young_water_fraction(mode, catchment_list, batch_num=batch_num, batch_ID=batch_ID, experiment=experiment)
    #forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, \
    #                             Vars=['young_water_fraction_chanS', 'young_water_fraction_sm1', 'young_water_fraction_sm2', 'young_water_fraction_sm3'], \
    #                             replace=True, batch_num=batch_num, batch_ID=batch_ID, experiment=experiment)

    # === Length of interflow path ===
    #forward_post_flow_path_length(mode, catchment_list, batch_num=batch_num, batch_ID=batch_ID, experiment=experiment)
    #forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, Vars=['interflow_length'], \
    #                            replace=True, batch_num=batch_num, batch_ID=batch_ID, experiment=experiment)


    # === Additional parameters ==
    #post_plot.calculate_additional_parameters(mode, temp_res, experiment=experiment)

    # === Damkholer Number ===
    #for experiment in [None, 'ssp126', 'ssp585']:
    #for experiment in ['ssp126']:    
    #    post_plot.calculate_monthly_Damkohler(mode, temp_res, experiment=experiment)
    #    post_plot.calculate_yearly_Damkohler(mode, temp_res, experiment=experiment)
    #post_plot.calculate_monthly_Damkohler_debug(mode, temp_res, experiment=experiment)
    
    

    # Plot yearly spatial maps
    Vars = ['young_water_fraction_vadose', 'young_water_fraction_sm1', 'young_water_fraction_sm2', 'young_water_fraction_sm3', 'young_water_fraction_chanS',
    'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'groundwater_storage', 'soil_evap','transp', 
    'infiltration', 'perc_layer1', 'perc_layer3', 'perc_vadose', 'rinfiltration', 'rperc_layer1', 'rperc_layer3', 'rperc_vadose',
    'interflow_toChn', 'GWflow_toChn', 'discharge',
    'age_chanS','age_SMC_layer3',
    'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3',
    'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_chanS', 'nitrogen_addition', 'wet_deposition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'deni_river', 'nitrogen_input', 'nitrogen_uptake', 'nitrogen_storage', 'nitrogen_leaching',
    'damkholer_num', 'young_water_fraction_soil_all_depths', 'trans_age_SMC_soil_all_depths', 'Evapotranspiration_fraction']


    # 'no3_SMC_layer1', 'no3_SMC_layer2', 'interflow_length', 'processing_time'
    # 'Precipitation_npfloat32', 'Potential_evapotranspiration_npfloat32', 'Mean_air_temperature_npfloat32', 'Surface_net_radiation_npfloat32'
    #Vars = ['trans_age_SMC_soil_all_depths']
    #Vars = ['Evapotranspiration_fraction', 'interflow_toChn', 'young_water_fraction_soil_all_depths', 'nitrogen_input', 'nitrogen_uptake', 'nitrogen_storage', 'nitrogen_leaching']
    Vars = ['infiltration',  'Evapotranspiration_fraction', 'young_water_fraction_soil_all_depths', 
            'nitrogen_addition', 'damkholer_num', 'nitrogen_surplus', 'nitrogen_storage']
    Vars = ['trans_age_SMC_soil_all_depths', 'damkholer_num', 'processing_time', 'nitrogen_storage', 'infiltration', 'Evapotranspiration', 'nitrogen_uptake', 'nitrogen_leaching']
    Vars = ['Precipitation_npfloat32', 'infiltration','trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3']
    Vars = [var+'.bin' for var in Vars]


    # === Plot aggregated spatial maps spatial maps ===
    #post_plot.plot_spatial_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)

    # === Plot monthly and annual average of EU  ===
    #post_plot.plot_TS_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)

    # === Plot increasing/decreasing trend  ===
    #post_plot.plot_spatial_TS_trend_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)
    #post_plot.plot_spatial_TS_trend_results_EU_spearman(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)

    # === Plot increasing/decreasing values  ===
    
    #for experiment in ['ssp126']:
    #    post_plot.plot_spatial_results_EU_diff(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False, experiment=experiment)
    
    #post_plot.plot_TS_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False, experiment=experiment)
    #post_plot.plot_TS_results_EU_by_regions(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)
    ['trans_age_SMC_soil_all_depths', 'damkholer_num']
    #post_plot.plot_TS_results_EU_experiments(mode, chainID=None, chainID_list=chainID_list, vars=['trans_age_SMC_soil_all_depths'], temp_res=temp_res, replace=True, yearly_flag=False)


    # == Plot flow paths ==
    #post_plot.plot_interflow_path(mode, catchment_list, chainID=None, chainID_list=chainID_list, vars=None, temp_res=temp_res, replace=True, yearly_flag=False)
    #post_plot.plot_interflow_connection(mode, catchment_list, chainID=None, chainID_list=chainID_list, vars=None, temp_res=temp_res, replace=True, yearly_flag=False)


    # == Plot mass balance == 
    #post_plot.plot_water_balance(mode, temp_res=temp_res, experiment=experiment)
    

    # == Plot by countries ==
    #post_plot.sort_statistics_by_countries(mode, temp_res)

    # == Plot by typical regions
    #post_plot.plot_typical_regions(mode, temp_res)
    #post_plot.plot_typical_regions_Ts(mode, temp_res)
    #post_plot.plot_pdf_by_typical_regions(mode, temp_res)

    
    # === Analysis
    #post_plot.sort_dominant_factor(mode)
    #post_plot.plot_risky_region(mode)

    #post_plot.plot_risky_regions_TS(mode)
    #post_plot.plot_risky_regions(mode)
    #post_plot.plot_risky_regions_scatter(mode)

    post_plot.analysis(mode)
    
   
    # === EXPERIEMTNS ===

    

    Vars = ['SMC_layer1']
    #Vars = [var+'.bin' for var in Vars]
    
    #post_plot.plot_TS_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False, experiment=experiment)
    #post_plot.plot_spatial_results_EU_diff(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False, experiment=experiment)

    #post_plot.merge_spatial_results_EU_debug(mode, temp_res, catchment_list=['831616'], vars=Vars, chainID=None, replace=True, experiment=experiment)
    

