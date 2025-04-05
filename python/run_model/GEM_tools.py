import os
import shutil
import numpy as np


def add_edge(arr, ext=1, no_data = -9999.0):
    rows, cols = arr.shape
    rows += ext * 2
    cols += ext * 2
    arr_new = np.full((rows, cols), no_data)
    arr_new[ext:rows-ext, ext:cols-ext] = arr
    return arr_new

def set_env(Path):
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


def set_config(Path):
    with open(Path.run_path+'config.ini', 'r') as f:
        lines = np.array(f.readlines())
        lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
    with open(Path.run_path+'config.ini', 'w') as f:
        f.writelines(lines)
    

def gen_param(Path, Info, Param, param_arr):
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
        if dict['type'] == 'global':  # The first column is for global parameters
            if dict['log'] == 0:
                param_values[0] = mins + (maxs - mins) * param_arr[counter]
            else:
                log_mins = np.log(mins)
                log_maxs = np.log(maxs)
                param_values[0] = np.exp( log_mins + param_arr[counter] * (log_maxs - log_mins))
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
    with open(Path.run_path+'param.ini', 'w') as f:
        f.writelines(lines)

def save_to_ascii(data, path, ref_path):
    with open(ref_path) as f:
        header = f.readlines()[:6]

    with open(path, 'w') as f:
        f.writelines(header)
    with open(path, 'a') as f:
        np.savetxt(f, data.astype(np.float64))
