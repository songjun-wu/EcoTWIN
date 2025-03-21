###########################################
# Configuration file for model runs
###########################################

from datetime import datetime
import numpy as np

class Path:

    model_path = '/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux/' # The path for model executable file
    path_EXEC = 'gEcoHydro'  

    work_path = '/home/wusongj/GEM/291110/'            # Working directory
    data_path = work_path                   # The path with spatial and climate data
    config_path = work_path                 # The path with configuration files (.ini)
    run_path = work_path + 'run/'           # The path for model runs
    output_path = work_path + 'output/'     # The path for output saving

    
class Data:
    # Simulation begining
    simbeg = datetime(1992,1,1)
    # Total simulation timesteps
    lsim = 10959

    # GEM sort grids sequentially (column first)
    sim_order = [16,14,1,12,11,13,2,6,3,10,7,8,9,15,4,17,5]
    nts = len(sim_order)

    sim_idx       = np.array([3,4,17,5]) # 32, 26, 26a, 29a
    # variables needs for outputs
    obs = {}
    obs['transp']       = {'sim_file':'transp.tab' ,'sim_pts':sim_idx,'conv':1,'type':'Ts'}


class Param:
    ref = {}
    # parameters to calibrate
    ref['albedoS']   = {'soil':1, 'veg':0, 'log':0, 'file':'albedo',       'min':[0.1,0.1,0.1,0.1],    'max':[0.4,0.4,0.4,0.4]}