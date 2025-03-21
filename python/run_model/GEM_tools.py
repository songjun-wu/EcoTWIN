import os
import shutil
import numpy as np


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
    shutil.copyfile(Path.config_path+'param.ini',  Path.run_path+'param.ini')


def set_config(Path):
    with open(Path.run_path+'config.ini', 'r') as f:
        lines = np.array(f.readlines())
        lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
    with open(Path.run_path+'config.ini', 'w') as f:
        f.writelines(lines)
    


def save_to_ascii(data, path, ref_path):
    with open(ref_path) as f:
        header = f.readlines()[:6]

    with open(path, 'w') as f:
        f.writelines(header)
    with open(path, 'a') as f:
        np.savetxt(f, data.astype(np.float64))