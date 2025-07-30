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

def foward_run(catchment_list, chainID_list, temp_res):

    nchains = 40
    replace = True

    # set the env
    sort_env_flag = False
    while not sort_env_flag:
        try:
            GEM_tools.sort_directory(mode, Path, Cali, Output, catchment_list=catchment_list)
            GEM_tools.set_env(mode, Path, Cali, Output, catchment_list=catchment_list)
            GEM_tools.set_config(mode, Path, Cali, Output, catchment_list=catchment_list)
            sort_env_flag = True
        except:
            time.sleep(5+np.random.rand(1))
    

    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo
    param_N = GEM_tools.get_param_N(Info, Param)
    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)

    for chainID in chainID_list:
        tasks = []
        param = _param[chainID, :]

        layer3_depth_min = Param.ref['depth3']['min'][0]
        layer3_depth_max = Param.ref['depth3']['max'][0]
        layer3_depth = layer3_depth_min + param[0] * (layer3_depth_max - layer3_depth_min)

        for catchment_ID in catchment_list:
            run_path = Path.work_path + mode + '/run/' + str(catchment_ID) + '/run/'
            save_path = Path.work_path + mode + '/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/' + str(chainID) + '/'
            tasks.append((catchment_ID, run_path, save_path, param.copy(), temp_res, layer3_depth))
        # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(foward_run_parallel, tasks)

def foward_run_parallel(catchment_ID, run_path, save_path, param, temp_res, layer3_depth):
     
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)
    GEM_tools.gen_param(run_path, Info, Param, param)
    GEM_tools.gen_no3_addtion(run_path, Info)
    # Model run
    os.chdir(run_path)           
    subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(current_path)

    #if temp_res=='monthly':
    #    post_plot.get_overall_ET(run_path+'outputs/')
    #    post_plot.get_overall_storage(run_path+'outputs/', layer3_depth)

    # Save outputs for each catchment
    GEM_tools.save_outputs(run_path+'outputs/', save_path)


def construct_initial_states_fluxes():
    Vars = ['snow_depth', 'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 
    'age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_vadose', 'age_groundwater_storage', 'age_chanS',
    'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_vadose', 'trans_age_groundwater_storage', 'trans_age_chanS',
    'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_chanS']

    output_Vars = ['snow', 'theta1', 'theta2', 'theta3', 'vadose', 'GW',
                'age_layer1', 'age_layer2', 'age_layer3', 'age_vadose', 'age_GW', 'age_chanS',
                'trans_age_layer1', 'trans_age_layer2', 'trans_age_layer3', 'trans_age_vadose', 'trans_age_GW', 'trans_age_chanS',
                'no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS']
    
    land_mask_EU = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc', skiprows=6)

    for var in Vars:
        try:
            if os.path.exists('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'+var+'_map.bin'):
                data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'+var+'_map.bin').reshape(-1, land_mask_EU.shape[0], land_mask_EU.shape[1])
            else:
                data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/yearly/all/'+var+'_map.bin').reshape(-1, land_mask_EU.shape[0], land_mask_EU.shape[1])
        except:
            print(var, '   not found!')
            continue

        GEM_tools.create_asc(data[-1,:,:], Path.data_path+'catchment_info/spin_up_results/'+var+'.asc', Path.data_path+'catchment_info/land_mask_3035.asc')
        print(var, ' spin up results sorted')


def update_initial_states_fluxes(catchment_IDs, cali_flag):

    Vars = ['snow_depth', 'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 
    'age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_vadose', 'age_groundwater_storage', 'age_chanS',
    'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_vadose', 'trans_age_groundwater_storage', 'trans_age_chanS',
    'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_SMC_layer3', 'no3_chanS']

    output_Vars = ['snow', 'theta1', 'theta2', 'theta3', 'vadose', 'GW',
                'age_layer1', 'age_layer2', 'age_layer3', 'age_vadose', 'age_GW', 'age_chanS',
                'trans_age_layer1', 'trans_age_layer2', 'trans_age_layer3', 'trans_age_vadose', 'trans_age_GW', 'trans_age_chanS',
                'no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS']



    land_mask_EU = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc', skiprows=6)

    if cali_flag:
        catchment_path = '/data/scratch/wusongj/paper4/data/catchment_info/cali/'
        catchment_IDs = ['6_001','291110_001','566445_001','291111_001','1034754_001','1034872_001','129489_001','4_001','83811_001','831616_001','566445_002','84063_001']
    else:
        catchment_path = '/data/scratch/wusongj/paper4/data/catchment_info/forward/'

    for xx, var in enumerate(Vars):

        #data_EU = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'+var+'.bin').reshape(-1, land_mask_EU.shape[0], land_mask_EU.shape[1])
        #data_EU = data_EU[-1,:,:]
        data_EU = np.loadtxt(Path.data_path+'catchment_info/spin_up_results/'+var+'.asc', skiprows=6)

        for yy, catchment_ID in enumerate(catchment_IDs):
            spatial_path = catchment_path+catchment_ID+'/spatial/'
            upper_left_coord = np.loadtxt(spatial_path+'upper_left_coord.txt').astype(np.int64)
            mask_cat = np.loadtxt(spatial_path+'dem.asc', skiprows=6)
            mask_cat[mask_cat==nodata] = np.nan
            data_cat = GIS_tools.from_EU_to_catchment(upper_left_coord, mask_cat, data_EU, nodata)
            GEM_tools.create_asc(data_cat, spatial_path+output_Vars[xx]+'.asc', spatial_path+'dem.asc')
            print(xx, var, yy)

        

        



def clean_directory(path_to_remove):
    if os.path.exists(path_to_remove):
        print(path_to_remove)
        shutil.rmtree(path_to_remove)

def clean_directory_parallel(catchment_list, temp_res):
    tasks = []
    for catchment_ID in catchment_list:
        path_to_remove = Path.work_path + mode + '/outputs/cali/'+temp_res+'/' + str(catchment_ID)
        tasks.append((path_to_remove))
    print(len(tasks), tasks[0])
    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 40)) as pool:
        pool.map(clean_directory, tasks)


        



if __name__ == "__main__":
    mode = 'forward_all'
    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainID_list = np.arange(40)
    temp_res = 'monthly'
    nodata = -9999

    try:
        os.remove('/data/scratch/wusongj/paper4/data/config/config_forward.ini')
    except:
        pass
    shutil.copyfile('/data/scratch/wusongj/paper4/data/config/config_forward_'+temp_res+'.ini', '/data/scratch/wusongj/paper4/data/config/config_forward.ini')


    #clean_directory_parallel(catchment_list, temp_res='yearly')

    # Update ages based on spin-up 50 years run
    #construct_initial_states_fluxes()
    #update_initial_states_fluxes(catchment_list, cali_flag=True)
    #update_initial_states_fluxes(catchment_list, cali_flag=False)

    

    num_explit_batch = 2
    batch_num = 10

    batch_ID = 9
    
    
    explit_catchment_list = np.array(['566445', '748037', '748077'])
    catchment_list = np.array([x for x in catchment_list if x not in explit_catchment_list])
    

    if batch_ID == 0:
        catchment_list_split = [explit_catchment_list[0]]
    elif batch_ID == 1:
        catchment_list_split = explit_catchment_list[[1,2]]
    else:
        batch_ID -= num_explit_batch
        batch_size = len(catchment_list) // (batch_num - 2) + 1
        start = batch_size * (batch_ID)
        end = batch_size*(batch_ID+1) if batch_size*(batch_ID+1) <= len(catchment_list) else len(catchment_list)
        catchment_list_split = np.array(catchment_list)[start:end]
    foward_run(catchment_list_split, chainID_list, temp_res)
    

    #catchment_list_split = ['1206837']
    #foward_run(catchment_list_split, chainID_list, temp_res)



    





    

