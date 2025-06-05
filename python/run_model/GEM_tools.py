import os
import shutil
import numpy as np
import subprocess

def checkTaskStatus(mode):
    task = subprocess.Popen("squeue -u wusongj", shell=True, stdout=subprocess.PIPE)
    task_return = [a.decode() for a in task.stdout.readlines()]
    counter = 0
    for i in range(len(task_return)):
        if mode in task_return[i]:
            counter += 1
    return counter

def save_to_ascii(data, path, ref_path):
    with open(ref_path) as f:
        header = f.readlines()[:6]

    with open(path, 'w') as f:
        f.writelines(header)
    with open(path, 'a') as f:
        np.savetxt(f, data.astype(np.float64))


def save_outputs(output_path, save_path):

    os.makedirs(save_path, exist_ok=True)

    fnames = [f for f in os.listdir(output_path) if f.endswith('bin')]

    for fname in fnames:
        data = np.fromfile(output_path + fname)
        if os.path.exists(save_path + fname):
            with open(save_path + fname, 'ab+') as f:
                data.tofile(f)
        else:
            with open(save_path + fname, 'w') as f:
                data.tofile(f)



def kge11(sim, obs):
    """
    Calculate the Kling-Gupta Efficiency (KGE) between simulated and observed data.

    Parameters
    ----------
    sim : array_like
        Simulated values.
    obs : array_like
        Observed values.

    Returns
    -------
    kge : float
        Kling-Gupta Efficiency.
    """
    sim = np.asarray(sim, dtype=np.float64)
    obs = np.asarray(obs, dtype=np.float64)

    # Remove NaNs and placeholder values
    mask = (~np.isnan(sim)) & (~np.isnan(obs)) & (obs != -9999)
    sim = sim[mask]
    obs = obs[mask]

    if len(sim) == 0 or len(obs) == 0:
        return np.nan  # Return nan if no valid data
    
    # Calculate statistics
    r = np.corrcoef(sim, obs)[0, 1]
    alpha = np.std(sim)/np.mean(sim) / (np.std(obs)/np.mean(obs))
    beta = np.mean(sim) / np.mean(obs)
    # Compute KGE
    print('KGE  :   ', r, alpha, beta)
    kge = 1 - np.sqrt((r - 1)**2 + (alpha - 1)**2 + (beta - 1)**2)

    return kge


def kge_modified(sim, obs):
    validIDX = np.logical_not( np.logical_or( np.isnan(sim), np.isnan(obs) ) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]
    
    sim_mean = np.mean(sim,dtype=np.float64)
    obs_mean = np.mean(obs, dtype=np.float64)

    r_num = np.sum((sim - sim_mean) * (obs - obs_mean),
                   axis=0, dtype=np.float64)
    r_den = np.sqrt(np.sum((sim - sim_mean) ** 2,
                           axis=0, dtype=np.float64)
                    * np.sum((obs - obs_mean) ** 2,
                             dtype=np.float64))
    eps = 1e-10
    pearson_r = r_num / (r_den + eps)


    #pearson_r = np.corrcoef(sim, obs)[0,1]
    alpha = (np.std(sim) / sim_mean) / (np.std(obs) / obs_mean)
    beta = sim_mean / obs_mean
    
    kge = 1 - np.sqrt((pearson_r-1)**2 + (alpha-1)**2 + 5 * (beta-1)**2)
    return kge
    

def kge(sim, obs):
    validIDX = np.logical_not( np.logical_or( np.isnan(sim), np.isnan(obs) ) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]


    sim_mean = np.mean(sim,dtype=np.float64)
    obs_mean = np.mean(obs, dtype=np.float64)

    r_num = np.sum((sim - sim_mean) * (obs - obs_mean),
                   axis=0, dtype=np.float64)
    r_den = np.sqrt(np.sum((sim - sim_mean) ** 2,
                           axis=0, dtype=np.float64)
                    * np.sum((obs - obs_mean) ** 2,
                             dtype=np.float64))
    eps = 1e-10
    pearson_r = r_num / (r_den + eps)


    #pearson_r = np.corrcoef(sim, obs)[0,1]
    alpha = (np.std(sim) / sim_mean) / (np.std(obs) / obs_mean)
    beta = sim_mean / obs_mean
    
    kge = 1 - np.sqrt((pearson_r-1)**2 + (alpha-1)**2 + (beta-1)**2)

    return kge

def rsquare(sim, obs):
    from sklearn.metrics import r2_score
    validIDX = np.logical_not( np.logical_or.reduce([np.isnan(sim), np.isnan(obs)]) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]
    return r2_score(obs, sim)

def pbias(sim, obs):
    validIDX = np.logical_not( np.logical_or.reduce([np.isnan(sim), np.isnan(obs), obs==0]) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]
    return np.mean(np.abs((sim - obs)/obs))

def nse(sim, obs):
    validIDX = np.logical_not( np.logical_or( np.isnan(sim), np.isnan(obs) ) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]
    return 1 - (np.sum((sim - obs)**2) / np.sum(((obs - np.mean(obs)))**2))

def rmse(sim, obs):
    validIDX = np.logical_not( np.logical_or( np.isnan(sim), np.isnan(obs) ) )
    validIDX[obs==-9999] = False
    sim = sim[validIDX]
    obs = obs[validIDX]
    return np.sqrt(np.mean((sim-obs)**2))


def lnnse(sim, obs):
    validIDX = np.logical_and (np.logical_not( np.logical_or( np.isnan(sim), np.isnan(obs) ) ), np.logical_not( np.logical_or( sim==0 , obs==0 )))
    sim = sim[validIDX]
    obs = obs[validIDX]
    sim[sim<0] = sim[sim<0] * -1
    obs[obs<0] = obs[obs<0] * -1
    sim = np.log(sim)
    obs = np.log(obs)
    return 1 - (np.sum((sim - obs)**2) / np.sum(((obs - np.mean(obs)))**2))

def nselnnse(sim, obs, weight_nse, weight_lnnse):
    _nse = nse(sim, obs)
    _lnnse = lnnse(sim, obs)
    return np.power(weight_nse*(1 - _nse)**6 + weight_lnnse*(1 - _lnnse)**6, 1/6)

def add_edge(arr, ext=1, no_data = -9999.0):
    rows, cols = arr.shape
    rows += ext * 2
    cols += ext * 2
    arr_new = np.full((rows, cols), no_data)
    arr_new[ext:rows-ext, ext:cols-ext] = arr
    return arr_new




def sort_directory(mode, Path, Cali, Output):
    if mode == 'DREAM_cali' or mode == 'cali_sep':
        os.makedirs(Path.work_path, exist_ok=True)
        for i in range(Cali.nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i) + '/' # Working directory for each chain
            os.makedirs(dir_for_each_chain, exist_ok=True)
            # Create sub-directories for each catchment
            for kk in range(Output.N_catchments):
                catchment_path = dir_for_each_chain + str(Output.Catchment_ID[kk]) + '/'
                run_path =  catchment_path + '/run/'    # The path for model runs
                output_path = run_path + 'outputs/'         # The path for output saving
                os.makedirs(catchment_path, exist_ok=True)
                os.makedirs(run_path, exist_ok=True)
                os.makedirs(output_path, exist_ok=True)
    
    else:
        os.makedirs(Path.work_path, exist_ok=True)
        os.makedirs(Path.work_path+'/'+mode, exist_ok=True)
        os.makedirs(Path.work_path+'/'+mode+'/outputs', exist_ok=True)  # Output folder

        # Create sub-directories for each catchment
        for kk in range(Output.N_catchments):
            catchment_path = Path.work_path + '/' + mode + '/' + str(Output.Catchment_ID[kk]) + '/'
            run_path =  catchment_path + '/run/'    # The path for model runs
            output_path = run_path + 'outputs/'         # The path for output saving
            if os.path.exists(run_path):  # Clean the run path
                shutil.rmtree(run_path)
            os.makedirs(catchment_path, exist_ok=True)
            os.makedirs(run_path, exist_ok=True)
            os.makedirs(output_path, exist_ok=True)

        
 

def set_env(mode, Path, nchains, Output):
    if mode == 'DREAM_cali' or mode=='cali_sep':
        for i in range(nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i) + '/'    # Working directory for each chain

            for kk in range(Output.N_catchments):
                catchment_path = dir_for_each_chain + str(Output.Catchment_ID[kk]) + '/'   # Working directory for each catchment
                run_path =  catchment_path + '/run/'        # The path for model runs

                if os.path.exists(run_path):  # Clean the run path
                    shutil.rmtree(run_path)
                os.mkdir(run_path)

                # link the model
                if not os.path.exists(run_path + Path.path_EXEC):
                    os.symlink(Path.model_path + Path.path_EXEC, run_path + Path.path_EXEC)
                # copy inputs
                #shutil.copytree(Path.data_path+'catchment_info/'+str(Output.Catchment_ID[kk])+'/spatial/', run_path+'spatial/')
                # copy configs
                shutil.copyfile(Path.config_path+'config_cali.ini',  run_path+'config.ini')
    
    else:
        for kk in range(Output.N_catchments):
            catchment_path = Path.work_path + '/' + mode + '/' + str(Output.Catchment_ID[kk]) + '/'
            run_path =  catchment_path + '/run/'    # The path for model runs
            # link the model
            if not os.path.exists(run_path + Path.path_EXEC):
                os.symlink(Path.model_path + Path.path_EXEC, run_path + Path.path_EXEC)
            # copy inputs
            #shutil.copytree(Path.data_path+'spatial/', run_path+'spatial/')
            # copy configs
            if mode == 'SA':
                shutil.copyfile(Path.config_path+'config_cali.ini',  run_path+'config.ini')
            else:
                shutil.copyfile(Path.config_path+'config_forward.ini',  run_path+'config.ini')


def set_config(mode, Path, Cali, Output):
    if mode == 'DREAM_cali' or mode == 'cali_sep':
        for i in range(Cali.nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i) + '/'    # Working directory for each chain
            for kk in range(Output.N_catchments):
                catchment_path = dir_for_each_chain + str(Output.Catchment_ID[kk]) + '/'   # Working directory for each catchment
                run_path =  catchment_path + '/run/'        # The path for model runs
                with open(run_path+'config.ini', 'r') as f:
                    lines = np.array(f.readlines())
                    lines = np.append('Clim_Maps_Folder = ' + Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/climate/\n', lines)
                    lines = np.append('Maps_Folder = ' + Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/spatial/\n', lines)
                    seconds_since_1980 = np.loadtxt( Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/obs/seconds_from_1980.txt')
                    lines = np.append('Simul_end = '+str(int(seconds_since_1980))+' # in second  # Seconds from 1980-1-1 to 2024-12-31\n', lines)

                with open(run_path+'config.ini', 'w') as f:
                    f.writelines(lines)
    
    else:
        for kk in range(Output.N_catchments):
            catchment_path = Path.work_path + '/' + mode + '/' + str(Output.Catchment_ID[kk]) + '/'
            run_path =  catchment_path + '/run/'    # The path for model runs
            with open(run_path+'config.ini', 'r') as f:
                lines = np.array(f.readlines())

                #lines = np.append('Maps_Folder = ' + Path.data_path + 'catchment_info/forward/'+str(Output.Catchment_ID[kk])+'/spatial/\n', lines)
                #lines = np.append('Clim_Maps_Folder = ' + Path.data_path + 'catchment_info/forward/'+str(Output.Catchment_ID[kk])+'/climate/\n', lines)
                lines = np.append('Maps_Folder = ' + Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/spatial/\n', lines) # todo
                lines = np.append('Clim_Maps_Folder = ' + Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/climate/\n', lines)
                if mode == 'SA':
                    seconds_since_1980 = np.loadtxt( Path.data_path + 'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/obs/seconds_from_1980.txt')
                    lines = np.append('Simul_end = '+str(int(seconds_since_1980))+' # in second  # Seconds from 1980-1-1 to 2024-12-31\n', lines)
            with open(run_path+'config.ini', 'w') as f:
                f.writelines(lines)  

def get_restart_param(Path, Cali, param_N, total_iterations):
    starts = []
    for i in range(Cali.nchains):
        likeli = np.fromfile(Path.result_path + Cali.TASK_name + '_logps_chain_'+str(i)+'_'+str(total_iterations)+'.bin')
        tmp = np.fromfile(Path.result_path + Cali.TASK_name + '_sampled_params_chain_'+str(i)+'_'+str(total_iterations)+'.bin').reshape(-1, param_N)
        starts.append(tmp[np.argwhere(likeli == np.max(likeli))[-1][-1], :])
    return starts




def get_param_N(Info, Param):
    param_N = 0
    for key in Param.ref.keys():
        dict = Param.ref.get(key)
        if dict['fix_value'] is None:
            if dict['type'] == 'global':
                param_N += 1
            elif dict['type'] == 'landuse':
                param_N += Info.N_landuse
            elif dict['type'] == 'soil':
                param_N += Info.N_soil
    return param_N


def gen_param(run_path, Info, Param, param_arr):
    landuse_index = Info.landuse_index
    soil_index = Info.soil_index

    N_land_use = len(landuse_index)
    N_soil = len(soil_index)
    N_total = N_land_use + N_soil + 1

    counter = 0
    lines = []
    for key in Param.ref.keys():
        dict = Param.ref.get(key)
        param_values = np.full(N_total, Info.nodata)
        mins = np.array(dict['min'])
        maxs = np.array(dict['max'])
        if dict['fix_value'] is not None:
            fix_value = dict['fix_value']
            if dict['type'] == 'global':
                param_values[0] = fix_value[0]
            elif dict['type'] == 'landuse':
                param_values[landuse_index] = fix_value
            elif dict['type'] == 'soil':
                param_values[soil_index] = fix_value

        else:
            if dict['type'] == 'global':  # The first column is for global parameters
                if dict['log'] == 0:
                    param_values[0] = mins[0] + (maxs[0] - mins[0]) * param_arr[counter]
                else:
                    log_mins = np.log(mins[0])
                    log_maxs = np.log(maxs[0])
                    param_values[0] = np.exp(log_mins + param_arr[counter] * (log_maxs - log_mins))
                counter += 1
            elif dict['type'] == 'landuse':
                if dict['log'] == 0:
                    param_values[landuse_index] = mins + (maxs - mins) * param_arr[counter:counter+N_land_use]
                else:
                    log_mins = np.log(mins)
                    log_maxs = np.log(maxs)
                    param_values[landuse_index] = np.exp( log_mins + param_arr[counter:counter+N_land_use] * (log_maxs - log_mins))
                counter += N_land_use
            elif dict['type'] == 'soil':
                if dict['log'] == 0:
                    param_values[soil_index] = mins + (maxs - mins) * param_arr[counter:counter+N_soil]
                else:
                    log_mins = np.log(mins)
                    log_maxs = np.log(maxs)
                    param_values[soil_index] = np.exp( log_mins + param_arr[counter:counter+N_soil] * (log_maxs - log_mins))
                counter += N_soil
        text = key + ',' + (',').join(param_values.astype(np.str)) + '\n'
        lines.append(text)
    with open(run_path+'param.ini', 'w') as f:
        f.writelines(lines)

  
def gen_no3_addtion(run_path, Info):
    landuse_index = Info.landuse_index
    soil_index = Info.soil_index

    N_land_use = len(landuse_index)
    N_soil = len(soil_index)
    N_total = N_land_use + N_soil + 1

    text_arr = np.full(N_total, Info.nodata)

    lines = []
    text_arr[landuse_index] = 1
    lines.append('is_landuse,' + (',').join(text_arr.astype(np.str)) + '\n')

    for key in Info.nadd.keys():
        text_arr[landuse_index] = Info.nadd[key]['value']
        lines.append(key + ',' + (',').join(text_arr.astype(np.str)) + '\n')
    
    with open(run_path+'Crop_info.ini', 'w') as f:
        f.writelines(lines)


