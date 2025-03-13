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
    print(Path.config_path+'config.ini')


def set_config(Path):
    with open(Path.run_path+'config.ini', 'r') as f:
        lines = np.array(f.readlines())
        lines = np.append('\nClim_Maps_Folder = ' + Path.data_path + 'climate/\n', lines)
    with open(Path.run_path+'config.ini', 'w') as f:
        f.writelines(lines)