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

def forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, Vars=None, replace=False, batch_num=None, batch_ID=None):
    if Vars is None:
        if temp_res == 'monthly':
            Vars = [#'ET', 'unsat_storage', 'snow_depth',
                    'snow_depth', 'soil_evap', 'transp',  
                    'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 'channel_storage',
                    'infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose', 'irrigation_from_GW',
                    'interflow_output', 'interflow_toChn', 'GWflow_toChn', 'discharge',
                    'age_SMC_layer3', 'age_chanS', 
                    'no3_SMC_layer3', 'no3_chanS', 'deni_soil',
                    ]

            Vars = [var+'_map' for var in Vars]
            """
            [infiltration, irrigation_from_GW] ->  SMC_layer1 -> [soil_evap, transp, perc_layer1]
            [perc_layer1] ->  SMC_layer2 -> [perc_layer2]
            [perc_layer2] ->  SMC_layer3 -> [perc_layer3]
            [perc_layer3, interflow_input] ->  vadose -> [perc_vadose, interflow_output, interflow_toChn]
            [upstream_inflow, interflow_toChn, GWflow_toChn] ->  ChanS -> [discharge]
            """

        elif temp_res == 'yearly':
            Vars = ['canopy_storage', 'snow_depth']
            Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage'])
            Vars.extend(['snowmelt', 'throufall', 'irrigation_from_GW', 'irrigation_from_river'])
            Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose'])
            Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3'])
            Vars.extend(['soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', 'channel_evaporation'])
            Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
            Vars.extend(['overland_flow_toChn', 'interflow_toChn', 'GWflow_toChn', 'discharge'])
            Vars.extend(['age_canopy_storage', 'age_snow_depth'])
            Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_vadose', 'age_groundwater_storage', 'age_chanS'])
            Vars.extend(['trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_vadose', 'trans_age_groundwater_storage', 'trans_age_chanS'])
            Vars.extend(['no3_canopy_storage', 'no3_snow_depth'])
            Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
            Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])

    """
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
        tasks.append((mode, temp_res, [catchment_ID], chainID_list, Vars, replace))

    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 20)) as pool:          
        pool.starmap(forward_post_chain_merge_parallel, tasks)
        
    """
    
    # Merge results in each catchment to one
    if batch_num is not None:
        indices = split_indices(n_tasks=len(Vars), n_cores=batch_num)
        start = indices[batch_ID][0]
        end = indices[batch_ID][1]
        Vars = Vars[start:end]
        print(batch_ID, start, end, Vars)
    
    tasks = []
    for var in Vars:
        tasks.append((mode, temp_res, catchment_list, chainID_list, [var], replace))
    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 5)) as pool:          
        pool.starmap(forward_post_catchment_merge_parallel, tasks)
    

def forward_post_chain_merge_parallel(mode, temp_res, catchment_list, chainID_list, Vars, replace):
    post_plot.merge_chain(mode, temp_res, catchment_list, chainID_list, Vars, replace)

def forward_post_catchment_merge_parallel(mode, temp_res, catchment_list, chainID_list, Vars, replace):
    post_plot.merge_spatial_results_EU(mode, temp_res, catchment_list, Vars, chainID=None, replace=replace)



# Young water fraction
def forward_post_young_water_fraction(mode, catchment_list, batch_num=None, batch_ID=None):
    
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
        tasks.append((catchment_ID, 3))

    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 20)) as pool:          
        pool.starmap(forward_post_young_water_fraction_parallel, tasks)

def forward_post_young_water_fraction_parallel(catchment_ID, young_water_thres):
    # Young water fraction
    post_plot.yound_water_fraction(catchment_ID, young_water_thres=young_water_thres)


# Plot spatial maps
def forward_post_spatial_plot(mode, catchment_list, chainID_list, temp_res, Vars=None, replace=False, batch_num=None, batch_ID=None, yearly_flag=False):
    if Vars is None:
        if temp_res == 'monthly':
                Vars = ['ET', 'overall_storage', 'unsat_storage', 'snow_depth']
        elif temp_res == 'yearly':
            """
            Vars = ['canopy_storage', 'snow_depth']
            Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage'])
            Vars.extend(['snowmelt', 'throufall', 'irrigation_from_GW', 'irrigation_from_river'])
            Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose'])
            Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3'])
            Vars.extend(['soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', 'channel_evaporation'])
            Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
            Vars.extend(['overland_flow_toChn', 'interflow_toChn', 'GWflow_toChn', 'discharge'])
            Vars.extend(['trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_vadose', 'trans_age_groundwater_storage', 'trans_age_chanS'])
            Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_vadose', 'age_groundwater_storage', 'age_chanS'])
            Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
            Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])
            Vars = ['SMC_layer3', 'groundwater_storage', 'interflow_toChn', 'GWflow_toChn', 'deni_soil']
        """
                   
    # Averaged spatial plots of all chains
    Vars = [var+'.bin' for var in Vars]
    post_plot.plot_spatial_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=replace, yearly_flag=yearly_flag)






        



if __name__ == "__main__":
    mode = 'forward_all'
    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainID_list = np.arange(40)
    temp_res = 'monthly'

    multiprocessing.set_start_method("spawn", force=True)


    # model performance
    #sort_obs_gauge_index(mode, catchment_list)
    
    #post_plot.merge_performance_EU(mode, catchment_list, chainID=None, chainID_list=chainID_list, temp_res=temp_res)
    #post_plot.plot_performance_EU(mode, chainID=None)

    

    # Merge spatial results
    batch_ID = 0
    batch_num = 10

    # === Merge and average chain-specific results ===
    #forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, Vars=None, replace=True, batch_num=batch_num, batch_ID=batch_ID)

    # === Young water fraction ===
    #forward_post_young_water_fraction(mode, catchment_list, batch_num=batch_num, batch_ID=batch_ID)
    #forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, \
    #                Vars=['young_water_fraction_vadose', 'young_water_fraction_sm1', 'young_water_fraction_chanS', 'age_pdf_vadose_wet', 'age_pdf_vadose_dry', 'age_pdf_chanS_wet', 'age_pdf_chanS_dry'], \
    #                replace=True, batch_num=batch_num, batch_ID=batch_ID)

    # === Damkholer Number ===
    #post_plot.calculate_monthly_Damkohler(mode, temp_res)
    


    # Plot yearly spatial maps


    
    Vars = ['young_water_fraction_vadose', 'young_water_fraction_sm1', 'young_water_fraction_chanS',
    'infiltration_map', 'SMC_layer1_map', 'SMC_layer2_map', 'SMC_layer3_map', 'groundwater_storage', 'soil_evap_map','transp_map', 
    'perc_layer1_map', 'perc_layer3_map', 'perc_vadose_map', 'interflow_toChn_map', 'GWflow_toChn_map', 
    'discharge_map', 'GWflow_toChn_map', 'age_chanS_map','age_SMC_layer3_map',
    'no3_SMC_layer3', 'no3_chanS', 'deni_soil',
    'Precipitation_npfloat32_3035', 'Potential_evapotranspiration_npfloat32_3035', 'Mean_air_temperature_npfloat32_3035', 'Surface_net_radiation_npfloat32_3035']

    Vars = ['damkholer_num']

    Vars = [var+'.bin' for var in Vars]

    # === Plot aggregated spatial maps spatial maps ===
    #post_plot.plot_spatial_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)

    # === Plot monthly and annual average of EU  ===
    post_plot.plot_TS_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=True, yearly_flag=False)

    # === Plot increasing/decreasing trend  ===
    #post_plot.plot_spatial_TS_trend_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=False, yearly_flag=False)
    #post_plot.plot_spatial_TS_trend_results_EU_spearman(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=False, yearly_flag=False)
    
    #post_plot.plot_param_all('/data/scratch/wusongj/paper4/cali/best_param_all.bin', Path.work_path+'plots/'+mode+'/', nchains, suffix=mode)

    #post_plot.get_avg_depth()

    
    
    # Test
    #post_plot.yound_water_fraction('831326', young_water_thres=3)

    """
    import matplotlib.pyplot as plt
    output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/831209/all/'
    mask = np.loadtxt(Path.data_path+'catchment_info/forward/831209/spatial/dem.asc', skiprows=6)
    YF_sm1 = np.fromfile(output_path+'young_water_fraction_sm1_map.bin').reshape(-1, mask.shape[0], mask.shape[1])
    YF_vadose = np.fromfile(output_path+'young_water_fraction_vadose_map.bin').reshape(-1, mask.shape[0], mask.shape[1])
    YF_chanS = np.fromfile(output_path+'young_water_fraction_chanS_map.bin').reshape(-1, mask.shape[0], mask.shape[1])

    fig, ax = plt.subplots(2,3, dpi=300)
    ax[0,0].imshow(np.mean(YF_sm1, axis=0), vmin=0, vmax=1)
    #ax[0,1].imshow(np.mean(YF_sm2[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,2].imshow(np.mean(YF_sm3[24:60,:,:], axis=0), vmin=0, vmax=1)
    ax[1,0].imshow(np.mean(YF_vadose, axis=0), vmin=0, vmax=1)
    ax[1,1].imshow(np.mean(YF_chanS, axis=0), vmin=0, vmax=0.3)
    #ax[1,2].imshow(np.mean(discharge, axis=2))
    #ax[1,2].plot(np.nanmean(S_vadose_dry.transpose(1,2,0)[mask], axis=0))
    #ax[1,2].plot(np.nanmean(S_vadose_wet.transpose(1,2,0)[mask], axis=0))
    fig.savefig('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/run_model/zzz.png')
    """
