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
    output_path = run_path + 'outputs/'     # The path for output saving

class Info:
    
    nodata = -9999.0 # nodata value for param.ini and all spatial maps

    N_soil = 4  # Number of soil types
    N_landuse = 5 # Number of land use types
    
    soil_index = [1,2,3,4]  # Column index in param.ini
    landuse_index = [5,6,7,8,9]  # Column index in param.ini
    

    



class Param:
    ref = {}
    # parameters to calibrate
    ref['alpha']   =            {'type':'landuse',  'log':0, 'file':'alpha',   'min':[0.1], 'max':[0.4]}
    ref['rE']   =               {'type':'landuse',  'log':0, 'file':'rE',   'min':[0.1], 'max':[0.4]}
    ref['snow_rain_thre']   =   {'type':'global',   'log':0, 'file':'snow_rain_thre',   'min':[0.1], 'max':[0.4]}
    ref['deg_day_min']   =      {'type':'global',   'log':0, 'file':'deg_day_min',   'min':[0.1], 'max':[0.4]}
    ref['deg_day_max']   =      {'type':'global',   'log':0, 'file':'deg_day_max',   'min':[0.1], 'max':[0.4]}
    ref['deg_day_increase']   = {'type':'global',   'log':0, 'file':'deg_day_increase',   'min':[0.1], 'max':[0.4]}

