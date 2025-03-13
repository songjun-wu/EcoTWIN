###########################################
# Configuration file for model runs
###########################################

from datetime import datetime
import numpy as np

class Path:
    model_path = '/home/wusongj/GEM/release_linux/'  # The path for model executable file
    path_EXEC = 'gEcoHydro'
    data_path = '/home/wusongj/GEM/c1_dmc/'  # the path with spatial and climate data
    config_path = '/home/wusongj/GEM/c1_dmc/' # the path with configuration files (.ini)
    main_path = '/home/wusongj/GEM/c1_dmc/'  # the path for model runs and output saving
    run_path = main_path + 'run/'


class Site:
    # Soil types
    soils = ['BE','GL','PE','PZ']
    nsoil = len(soils)
    sfiles = ['unit.soil_' + s + '.map' for s in soils]
    # Vegetation types
    vegs = ['Crops','Broad','Conif','Past']
    nveg = len(vegs)
    vfile = ['unit.veg_' + s + '.map' for s in soils]
    
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