import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
from multiprocessing import Pool, cpu_count
import numpy as np
import time
import post_plot
import GIS_tools
import pandas as pd
import pickle
import subprocess
from def_GEM_forward import *


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
                

def merge_monthy_outputs(mode, chainID_list):

    Vars = ['ET', 'snow_depth', 'overall_storage', 'unsat_storage']
    Vars = ['ET', 'snow_depth']  # todo
    save_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    os.makedirs(save_path, exist_ok=True)
    for var in Vars:
        for xx, chainID in enumerate(chainID_list):
            save_path_chain = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+str(chainID) + '/'
            print(xx, chainID)
            if xx==0:
                data = np.fromfile(save_path_chain+var+'.bin')
            else:
                data += np.fromfile(save_path_chain+var+'.bin')
            print(xx, chainID, data.shape)
        data /= len(chainID_list)
        data.tofile(save_path+var+'.bin')



def forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, replace, batch_num=None, batch_ID=None):
        if temp_res == 'monthly':
            Vars = ['ET', 'unsat_storage', 'snow_depth']
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
            Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_groundwater_storage', 'age_chanS'])
            Vars.extend(['no3_canopy_storage', 'no3_snow_depth'])
            Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
            Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])

        if batch_num is not None:
            batch_size = len(Vars) // batch_num + 1
            start = batch_size * batch_ID
            end = batch_size*(batch_ID+1) if batch_size*(batch_ID+1) <= len(Vars) else len(Vars)
            Vars = np.array(Vars)[start:end]

        # merge spatial results for each chain
        tasks = []
        for chainID in chainID_list:
            tasks.append((mode, catchment_list, chainID, Vars, temp_res, replace))
        # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(forward_post_spatial_merge_parallel, tasks)

        #forward_post_spatial_parallel(mode, catchment_list, 0, Vars, temp_res, replace)
        

def forward_post_spatial_plot(mode, catchment_list, chainID_list, temp_res, replace, batch_num=None, batch_ID=None):

    if temp_res == 'monthly':
            Vars = ['ET', 'overall_storage', 'unsat_storage', 'snow_depth']
    elif temp_res == 'yearly':
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

    # Spatial plots for each chain
    #for chainID in chainID_list:
    #    post_plot.plot_spatial_results_EU(mode, chainID, chainID_list, Vars, temp_res, replace)
    
    # Averaged spatial plots of all chains
    post_plot.plot_spatial_results_EU(mode, chainID=None, chainID_list=chainID_list, vars=Vars, temp_res=temp_res, replace=replace)
        

def forward_post_spatial_merge_parallel(mode, catchment_list, chainID, Vars, temp_res, replace):
    post_plot.merge_spatial_results_EU(mode, catchment_list, chainID, Vars, temp_res, replace)


    
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

        



if __name__ == "__main__":
    mode = 'forward_all'
    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainID_list = np.arange(40)
    temp_res = 'monthly'



    # model performance
    #sort_obs_gauge_index(mode, catchment_list)
    
    #post_plot.merge_performance_EU(mode, catchment_list, chainID=None, chainID_list=chainID_list, temp_res=temp_res)
    #post_plot.plot_performance_EU(mode, chainID=None)
    #for chainID in chainID_list:
        #post_plot.merge_performance_EU(mode, catchment_list, chainID)
        #post_plot.plot_performance_EU(mode, chainID)
    
    # Merge spatial results
    if temp_res=='monthly':
        forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, replace=True, batch_num=None, batch_ID=None)
        merge_monthy_outputs(mode, chainID_list)
    elif temp_res=='yearly':
        batch_ID = 9
        batch_num = 10
        forward_post_spatial_merge(mode, catchment_list, chainID_list, temp_res, replace=True, batch_num=batch_num, batch_ID=batch_ID)
    

    # Plot yearly spatial maps
    #forward_post_spatial_plot(mode, catchment_list, chainID_list, temp_res, replace=True, batch_num=None, batch_ID=None)

    #post_plot.plot_param_all('/data/scratch/wusongj/paper4/cali/best_param_all.bin', Path.work_path+'plots/'+mode+'/', nchains, suffix=mode)

    

