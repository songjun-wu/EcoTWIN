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




def foward_run(catchment_list, chainID_list, temp_res, experiment, second_run):

    nchains = 40
    replace = True

    # set the env
    sort_env_flag = False
    while not sort_env_flag:
        try:
            GEM_tools.sort_directory(mode, Path, Cali, Output, catchment_list=catchment_list)
            GEM_tools.set_env(mode, Path, Cali, Output, catchment_list=catchment_list)
            GEM_tools.set_config(mode, Path, Cali, Output, catchment_list=catchment_list, experiment=experiment)
            sort_env_flag = True
        except:
            time.sleep(5+np.random.rand(1))
    

    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo
    param_N = GEM_tools.get_param_N(Info, Param)
    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)

    for nn, chainID in enumerate(chainID_list):
        tasks = []
        param = _param[chainID, :]

        nn = chainID  # so directory will be cleaned up only when clainID == 0

        layer3_depth_min = Param.ref['depth3']['min'][0]
        layer3_depth_max = Param.ref['depth3']['max'][0]
        layer3_depth = layer3_depth_min + param[0] * (layer3_depth_max - layer3_depth_min)

        

        for catchment_ID in catchment_list:
            run_path = Path.work_path + mode + '/run/' + str(catchment_ID) + '/run/'
            if experiment is None:
                save_path = Path.work_path + mode + '/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/all/'
            else:
                save_path = Path.work_path + mode + '/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/all_'+experiment+'/'
            if second_run:
                finished_batch = np.loadtxt(save_path+'finish_counter/finish_counter_age_chanS_map.bin.txt')
                if finished_batch!= 40 and chainID>=finished_batch:  # First run has not be completed
                    tasks.append((catchment_ID, nn, chainID, run_path, save_path, param.copy(), temp_res, layer3_depth, experiment, second_run))
            else:
                tasks.append((catchment_ID, nn, chainID, run_path, save_path, param.copy(), temp_res, layer3_depth, experiment, second_run))
        
        if len(tasks)>0:
            print(experiment, chainID, len(catchment_list), catchment_list[:5], flush=True)

        # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(foward_run_parallel, tasks)
        

def foward_run_parallel(catchment_ID, nn, chainID, run_path, save_path, param, temp_res, layer3_depth, experiment, second_run):
    if not second_run:
        if os.path.exists(save_path) and nn==0:
            shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    # Use chain-specific initial boundary
    # opt_init_no3 was set to 0
    if experiment is None:
        newlines = [    'opt_init_no3 = 0\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/\n' + \
                        'Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/\n']
    else:
        newlines = [    'opt_init_no3 = 0\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/'+experiment+'/\n' + \
                        'Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/\n']
    with open(run_path + 'config.ini', 'r') as f:
        lines = f.readlines()
    newlines.extend(lines)
    with open(run_path + 'config.ini', 'w') as f:
        f.writelines(newlines)

    runflag = False
    run_times = 0

    while not runflag:
        try:
            GEM_tools.gen_param(run_path, Info, Param, param)
            GEM_tools.gen_no3_addtion(run_path, Info)
            # Model run
            os.chdir(run_path)
            #subprocess.run('./gEcoHydro')          
            subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.chdir(current_path)

            # Save outputs for each catchment

            if experiment is None:
                save_last_timestep_for_spinup(run_path, catchment_ID, chainID)
                
            save_cumulative_outputs_memmap(run_path+'outputs/', save_path)
            #save_cumulative_outputs(run_path+'outputs/', save_path)
            runflag = True
        except Exception as e:
            run_times += 1
            print(catchment_ID, chainID, '   failed!!!! try for the ', run_times, ' times')
            print('Error messasge   :   ', e)


    

def save_last_timestep_for_spinup(run_path, catchment_ID, chainID):
    if experiment is None:
        Vars = ['snow_depth', 'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 
        'age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_SMC_layer3', 'age_chanS',
        'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_SMC_layer3', 'trans_age_chanS',
        'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_chanS']

        output_Vars = ['snow', 'theta1', 'theta2', 'theta3', 'vadose', 'GW',
                    'age_layer1', 'age_layer2', 'age_layer3', 'age_vadose','age_chanS',
                    'trans_age_layer1', 'trans_age_layer2', 'trans_age_layer3', 'trans_age_vadose', 'trans_age_chanS',
                    'no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS']

        for i in range(len(Vars)):
            mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
            
            #offset = (540 - 1) * mask.shape[0] * mask.shape[1] * 8  # only for last timestep
            offset = (12*8) * mask.shape[0] * mask.shape[1] * 8      # only for 1998-2005
            data_last = np.memmap(run_path+'outputs/'+Vars[i]+'_map.bin',  
                                dtype='float64', mode='r',
                                shape=(12*8, mask.shape[0], mask.shape[1]),
                                offset=offset)
            data_last = np.mean(data_last.copy(), axis=0)
            GEM_tools.create_asc(data_last, \
                                 '/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/'+output_Vars[i]+'.asc', \
                                 Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc')
            """
            if Vars[i]=='no3_SMC_layer3':
                data0 = np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/'+output_Vars[i]+'.asc', skiprows=6)
                data1 = np.fromfile(run_path+'outputs/'+Vars[i]+'_map.bin').reshape(-1, mask.shape[0], mask.shape[1])
                data2 = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/'+output_Vars[i]+'.asc', skiprows=6)
                data0[data0==-9999] = np.nan
                data1[data1==-9999] = np.nan
                data2[data2==-9999] = np.nan

                print(data1.shape, data1[12*8:12*16,:,:].shape)

                print(np.nanmean(data0 - np.mean(data1[12*8:12*16,:,:], axis=0)), np.nanmean(data0 - data2), np.nanmean(np.mean(data1[12*8:12*16,:,:], axis=0) - data1[0,:,:]), np.nanmean(data0), np.nanmean(data2))
            """
        




def save_cumulative_outputs_memmap(output_path, save_path):

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_path + '/finish_counter/', exist_ok=True)

    fnames = [f for f in os.listdir(output_path) if f.endswith('bin')]

    for fname in fnames:
        
        if os.path.exists(save_path + fname):
            if os.path.getsize(output_path + fname) == 0:
                continue
            a = np.memmap(save_path + fname, dtype='float64', mode='r+')
            b = np.memmap(output_path + fname, dtype='float64', mode='r')
            a += b
            a.flush()
            del a, b  # 
            finish_counter = np.loadtxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt')
            finish_counter += 1
        else:
            shutil.copyfile(output_path + fname, save_path + fname)
            finish_counter = 1

        os.remove(output_path + fname)
        np.savetxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt', [finish_counter])
        

def save_cumulative_outputs(output_path, save_path):

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_path + '/finish_counter/', exist_ok=True)

    fnames = [f for f in os.listdir(output_path) if f.endswith('bin')]

    for fname in fnames:
        data = np.fromfile(output_path + fname)
        if os.path.exists(save_path + fname):
            data += np.fromfile(save_path + fname)
            finish_counter = np.loadtxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt')
            finish_counter += 1
        else:
            finish_counter = 1

        np.savetxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt', [finish_counter])
        data.tofile(save_path + fname)

        os.remove(output_path + fname)


def construct_initial_states_fluxes():
    Vars = ['snow_depth', 'SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', 
        'age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_SMC_layer3', 'age_chanS',
        'trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_SMC_layer3', 'trans_age_chanS',
        'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_chanS']

    output_Vars = ['snow', 'theta1', 'theta2', 'theta3', 'vadose', 'GW',
                'age_layer1', 'age_layer2', 'age_layer3', 'age_vadose','age_chanS',
                'trans_age_layer1', 'trans_age_layer2', 'trans_age_layer3', 'trans_age_vadose', 'trans_age_chanS',
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


def update_initial_states_fluxes_parallel(catchment_path, spinup_path, catchment_ID, chainID, cali_flag):

    # GW was excluded after 100 years of spinup
    output_Vars = ['snow', 'theta1', 'theta2', 'theta3', 'vadose',
                'age_layer1', 'age_layer2', 'age_layer3', 'age_vadose','age_chanS',
                'trans_age_layer1', 'trans_age_layer2', 'trans_age_layer3', 'trans_age_vadose', 'trans_age_chanS',
                'no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS']
    
    output_Vars = np.array(['no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS'])  # todo; only update nitrate concentration
    Vars_to_correct = np.array(['no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS'])
    thres = [80, 60, 30, 30, 30]
    
    for var in output_Vars:
        if os.path.exists(catchment_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc'):
            os.remove(catchment_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc')
        shutil.copyfile(spinup_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc', \
                        catchment_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc')

        if var in Vars_to_correct:
            idx = np.squeeze(np.where(Vars_to_correct==var))
            file_path = catchment_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc'
            data = np.loadtxt(file_path, skiprows=6)
            data[data>300] = 300
            data[data>thres[idx]] = data[data>thres[idx]]*0.4 + thres[idx]*0.6
            GEM_tools.create_asc(data, \
                                file_path, \
                                Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc')

    if chainID==39:
        print(catchment_ID, '   done!', flush=True)


def corect_initial_states_fluxes_parallel(catchment_path, spinup_path, catchment_ID, chainID, cali_flag):

    # GW was excluded after 100 years of spinup
    output_Vars = ['no3_layer1', 'no3_layer2', 'no3_layer3', 'no3_vadose', 'no3_chanS']
    thres = [50, 35, 20, 20, 20]
    
    
    
    for xx, var in enumerate(output_Vars):
        file_path = catchment_path+catchment_ID+'/spatial_'+str(chainID)+'/'+var+'.asc'
        if os.path.exists(file_path):
            data = np.loadtxt(file_path, skiprows=6)
            data[data>200] = 200
            data[data>thres[xx]] = data[data>thres[xx]]*0.25 + thres[xx]*0.75
        GEM_tools.create_asc(data, \
                            file_path, \
                            Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc')
        
    if chainID==39:
        print(catchment_ID, '   done!', flush=True)

    

def create_initial_states_fluxes_parallel(catchment_path, spinup_path, catchment_ID, chainID, cali_flag):
    #if os.path.exists(catchment_path+catchment_ID+'/spatial_'+str(chainID)):
    #    shutil.rmtree(catchment_path+catchment_ID+'/spatial_'+str(chainID))
    #shutil.copytree(catchment_path+catchment_ID+'/spatial/', catchment_path+catchment_ID+'/spatial_'+str(chainID))

    if cali_flag:
        os.makedirs('/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/cali/'+catchment_ID+'/spatial_'+str(chainID), exist_ok=True)
    else:
        os.makedirs('/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/forward/'+catchment_ID+'/spatial_'+str(chainID), exist_ok=True)

    if chainID==39:
        print(catchment_ID, '   done!', flush=True)

def update_initial_states_fluxes(catchment_IDs, nchains, cali_flag):

    land_mask_EU = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc', skiprows=6)

    if cali_flag:
        catchment_path = '/data/scratch/wusongj/paper4/data/catchment_info/cali/'
        catchment_IDs = ['6_001','291110_001','566445_001','291111_001','1034754_001','1034872_001','129489_001','4_001','83811_001','831616_001','566445_002','84063_001']
        spinup_path = '/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/cali/'
    else:
        catchment_path = '/data/scratch/wusongj/paper4/data/catchment_info/forward/'
        spinup_path = '/data/scratch/wusongj/paper4/forward_all/outputs/spinup_maps/forward/'


    tasks = []
    for yy, catchment_ID in enumerate(catchment_IDs):
        for chainID in range(nchains):
            tasks.append((catchment_path, spinup_path, catchment_ID, chainID, cali_flag))

    with Pool(processes=min(cpu_count(), 40)) as pool:
        pool.starmap(update_initial_states_fluxes_parallel, tasks)
    
   
        

        



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


        
def identify_failed_catchments(catchment_list, experiment):

    failed_catchments = []
    for xx, catchment in enumerate(catchment_list):

        #if not os.path.exists('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp126/soil_evap_map.bin'):
        #    failed_catchments.append(int(catchment))
        
        if os.path.exists('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp126/no3_SMC_layer3_map.bin'):

            data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp126/no3_SMC_layer3_map.bin')
            if np.isnan(data).any():
                failed_catchments.append(int(catchment))

                print('Catchment :  ',catchment ,'  Outputs wrong!')

        else:
            failed_catchments.append(int(catchment))

    if experiment is None:
        np.savetxt('/data/scratch/wusongj/paper4/forward_all/outputs/failed_catchments_forward.txt', failed_catchments)
    else:
        np.savetxt('/data/scratch/wusongj/paper4/forward_all/outputs/failed_catchments_forward_'+experiment+'.txt', failed_catchments)
    
    print(len(failed_catchments))
    

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



if __name__ == "__main__":

    #  OPTIONS
    parser = OptionParser()
    current_path = os.getcwd()
    parser.add_option("--batch_ID",dest="batch_ID",metavar="batch_ID",
                    help="batch_ID")
    parser.add_option("--chain_start",dest="chain_start",metavar="chain_start",
                    help="chain_start")
    parser.add_option("--chain_end",dest="chain_end",metavar="chain_end",
                        help="chain_end")


    (options, args) = parser.parse_args()

    batch_ID = int(options.batch_ID)
    chainID_list = np.arange(int(options.chain_start), int(options.chain_end))

    #mode = 'forward_all'
    mode = 'forward_cmip6'
    second_run = False


    #experiments = ['ssp585']
    experiments = ['ssp126']

    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    
    temp_res = 'monthly'
    nodata = -9999


    #identify_failed_catchments(catchment_list, experiment=experiments[0])


    


    """
    failed_catchments = np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/failed_catchments_forward_ssp126.txt')
    failed_catchments = [str(int(x)) for x in failed_catchments]
    mode = 'forward_all'

    batch_num = 10
    batch_ID = 9
    
    indices = split_indices(n_tasks=len(failed_catchments), n_cores=batch_num)
    start = indices[batch_ID][0]
    end = indices[batch_ID][1]
    failed_catchments_split = failed_catchments[start:end]
    print(batch_ID, start, end, len(failed_catchments_split), '/', len(failed_catchments), failed_catchments_split[:5])
    foward_run(failed_catchments_split, chainID_list, temp_res, experiment=experiments[0], second_run=second_run)
    """



    if mode == 'forward_cmip6':

        mode = 'forward_all'
        
        for experiment in experiments:
            try:
                os.remove('/data/scratch/wusongj/paper4/data/config/config_forward.ini')
            except:
                pass
            shutil.copyfile('/data/scratch/wusongj/paper4/data/config/config_forward_CMIP6_'+temp_res+'.ini', '/data/scratch/wusongj/paper4/data/config/config_forward.ini')



            with open('/data/scratch/wusongj/paper4/data/config/config_forward.ini', 'r') as f:
                lines = f.readlines()
            for xx, line in enumerate(lines):
                if 'Clim_Maps_Folder = ' in line:
                    lines[xx] = 'Clim_Maps_Folder = ./climate/' + experiment + '/\n'
            with open('/data/scratch/wusongj/paper4/data/config/config_forward.ini', 'w') as f:
                f.writelines(lines)

            
            num_explit_batch = 2  # do not change
            batch_num = 10  # do not change
            
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
            print('Batch ID  :   ', batch_ID, flush=True)


            foward_run(catchment_list_split, chainID_list, temp_res, experiment=experiment, second_run=second_run)
            

            #catchment_list_split = ['831616']
            #foward_run(catchment_list_split, chainID_list, temp_res, experiment=experiment, second_run=second_run)


    elif mode == 'forward_all':
        
        experiment = None
        try:
            os.remove('/data/scratch/wusongj/paper4/data/config/config_forward.ini')
        except:
            pass
        shutil.copyfile('/data/scratch/wusongj/paper4/data/config/config_forward_'+temp_res+'.ini', '/data/scratch/wusongj/paper4/data/config/config_forward.ini')


        #clean_directory_parallel(catchment_list, temp_res='yearly')

        # Update ages based on spin-up 50 years run
        #construct_initial_states_fluxes()
        #update_initial_states_fluxes(catchment_list, nchains, cali_flag=False)


        
        num_explit_batch = 2  # do not change
        batch_num = 10  # do not change


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
        print('Batch ID  :   ', batch_ID, flush=True)
        foward_run(catchment_list_split, chainID_list, temp_res, experiment=None, second_run=second_run)



        




    

