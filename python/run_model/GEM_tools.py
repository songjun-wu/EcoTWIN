import os
import shutil
import numpy as np

def save_to_ascii(data, path, ref_path):
    with open(ref_path) as f:
        header = f.readlines()[:6]

    with open(path, 'w') as f:
        f.writelines(header)
    with open(path, 'a') as f:
        np.savetxt(f, data.astype(np.float64))

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
    pearson_r = r_num / r_den


    #pearson_r = np.corrcoef(sim, obs)[0,1]
    alpha = np.var(sim) / np.var(obs)
    beta = np.sum(sim) / np.sum(obs)
    
    kge = 1 - np.sqrt((pearson_r-1)**2 + (alpha-1)**2 + (beta-1)**2)

    return kge

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




def sort_directory(mode, Path, Cali):
    if mode == 'DREAM_cali':
        if not os.path.exists(Path.work_path):
            os.mkdir(Path.work_path)
        for i in range(Cali.nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i) # Working directory for each chain
            if not os.path.exists(dir_for_each_chain):
                os.mkdir(dir_for_each_chain)
            
            run_path =  dir_for_each_chain + '/run/'    # The path for model runs
            output_path = run_path + 'outputs/'         # The path for output saving
            if not os.path.exists(run_path):
                os.mkdir(run_path)
            if not os.path.exists(output_path):
                os.mkdir(output_path)
    
    elif mode == 'forward':
        if not os.path.exists(Path.work_path):
            os.mkdir(Path.work_path)

        if not os.path.exists(Path.work_path+'/forward'):
            os.mkdir(Path.work_path+'/forward')
        if not os.path.exists(Path.work_path+'/forward/outputs'):
            os.mkdir(Path.work_path+'/forward/outputs')
        run_path =  Path.work_path + '/forward/run/'    # The path for model runs
        if os.path.exists(run_path):  # Clean the run path
            shutil.rmtree(run_path)
        os.mkdir(run_path)
        output_path = run_path + 'outputs/'         # The path for output saving
        if not os.path.exists(run_path):
            os.mkdir(run_path)
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        
 

def set_env(mode, Path, nchains):
    if mode == 'DREAM_cali':
        for i in range(nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i)    # Working directory for each chain
            run_path =  dir_for_each_chain + '/run/'        # The path for model runs

            if os.path.exists(run_path):  # Clean the run path
                shutil.rmtree(run_path)
            os.mkdir(run_path)

            # link the model
            os.symlink(Path.model_path + Path.path_EXEC, run_path + Path.path_EXEC)
            # copy inputs
            shutil.copytree(Path.data_path+'spatial/', run_path+'spatial/')
            # copy configs
            shutil.copyfile(Path.config_path+'config.ini',  run_path+'config.ini')
    
    elif mode == 'forward':
        run_path =  Path.work_path + '/forward/run/'    # The path for model runs
        # link the model
        os.symlink(Path.model_path + Path.path_EXEC, run_path + Path.path_EXEC)
        # copy inputs
        shutil.copytree(Path.data_path+'spatial/', run_path+'spatial/')
        # copy configs
        shutil.copyfile(Path.config_path+'config.ini',  run_path+'config.ini')
        
    elif mode == 'test':
        # Clear run path
        if os.path.exists(Path.run_path):
            shutil.rmtree(Path.run_path)
        os.mkdir(Path.run_path)
        os.mkdir(Path.run_path + 'outputs/')
        # link the model
        os.symlink(Path.model_path + Path.path_EXEC, Path.run_path + Path.path_EXEC)
        # copy inputs
        shutil.copytree(Path.data_path+'spatial/', Path.run_path+'spatial/')
        # copy configs
        shutil.copyfile(Path.config_path+'config.ini',  Path.run_path+'config.ini')
        #shutil.copyfile(Path.config_path+'param.ini',  Path.run_path+'param.ini')

def get_restart_param(Path, Cali, param_N, total_iterations):
    starts = []
    for i in range(Cali.nchains):
        likeli = np.fromfile(Path.result_path + Cali.TASK_name + '_logps_chain_'+str(i)+'_'+str(total_iterations)+'.bin')
        tmp = np.fromfile(Path.result_path + Cali.TASK_name + '_sampled_params_chain_'+str(i)+'_'+str(total_iterations)+'.bin').reshape(-1, param_N)
        starts.append(tmp[np.argwhere(likeli == np.max(likeli))[-1][-1], :])
    return starts

def set_config(mode, Path, Cali):
    if mode == 'DREAM_cali':
        for i in range(Cali.nchains):
            dir_for_each_chain = Path.work_path + '/chain_' +str(i)    # Working directory for each chain
            run_path =  dir_for_each_chain + '/run/'        # The path for model runs

            with open(run_path+'config.ini', 'r') as f:
                lines = np.array(f.readlines())
                lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
            with open(run_path+'config.ini', 'w') as f:
                f.writelines(lines)
    
    elif mode == 'forward':
        run_path =  Path.work_path + '/forward/run/'    # The path for model runs
        with open(run_path+'config.ini', 'r') as f:
            lines = np.array(f.readlines())
            lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
        with open(run_path+'config.ini', 'w') as f:
            f.writelines(lines)

    
    elif mode == 'test':
        with open(Path.run_path+'config.ini', 'r') as f:
            lines = np.array(f.readlines())
            lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
        with open(Path.run_path+'config.ini', 'w') as f:
            f.writelines(lines)

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
    
    with open(run_path+'N_addition.ini', 'w') as f:
        f.writelines(lines)
