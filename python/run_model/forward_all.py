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
from def_GEM import *

def foward_run(catchment_list, chainID_list):

    nchains = 40
    replace = True

    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo
    param_N = GEM_tools.get_param_N(Info, Param)
    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)


    

    for chainID in chainID_list:
        tasks = []
        param = _param[chainID, :]
        for catchment_ID in catchment_list:
            run_path = Path.work_path + mode + '/run/' + str(catchment_ID) + '/run/'
            save_path = Path.work_path + mode + '/outputs/cali/' + str(catchment_ID) + '/' + str(chainID) + '/'
            tasks.append((catchment_ID, run_path, save_path, param.copy()))
        # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(foward_run_parallel, tasks)

def foward_run_parallel(catchment_ID, run_path, save_path, param):
    # set the env
    #GEM_tools.sort_directory(mode, Path, Cali, Output, catchment_list=catchment_list)
    #GEM_tools.set_env(mode, Path, Cali, Output, catchment_list=catchment_list)
    #GEM_tools.set_config(mode, Path, Cali, Output, catchment_list=catchment_list)  
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)
    GEM_tools.gen_param(run_path, Info, Param, param)
    GEM_tools.gen_no3_addtion(run_path, Info)
    # Model run
    os.chdir(run_path)           
    os.system('./gEcoHydro')
    os.chdir(current_path)
    # Save outputs for each catchment
    GEM_tools.save_outputs(run_path+'outputs/', save_path)


def forward_post_performance(mode, catchment_list):
    post_plot.merge_performance(mode, catchment_list)
    #post_plot.plot_performance_EU(mode)

def forward_post_spatial(mode, catchment_list):
        Vars = ['canopy_storage', 'snow_depth']
        Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage'])
        Vars.extend(['snowmelt', 'throufall', 'irrigation_from_GW', 'irrigation_from_river'])
        Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose'])
        Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3'])
        Vars.extend(['soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', 'channel_evaporation'])
        Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
        Vars.extend(['overland_flow_toChn', 'interflow_toChn', 'GWflow_toChn', 'discharge'])
        Vars.extend(['d18o_canopy_storage', 'd18o_snow_depth'])
        Vars.extend(['d18o_SMC_layer1', 'd18o_SMC_layer2', 'd18o_SMC_layer3', 'd18o_vadose', 'd18o_groundwater_storage', 'd18o_chanS'])
        Vars.extend(['age_canopy_storage', 'age_snow_depth'])
        Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_groundwater_storage', 'age_chanS'])
        Vars.extend(['no3_canopy_storage', 'no3_snow_depth'])
        Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
        Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])
        #post_plot.merge_spatial_results_EU(mode, catchment_list, Vars, replace)
        #post_plot.plot_spatial_results_EU(mode, Vars, replace)
        


if __name__ == "__main__":
    mode = 'forward_all'
    current_path = os.getcwd()
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainID_list = np.arange(1, 40)

    #foward_run(catchment_list, chainID_list)


    #forward_post_performance(mode, catchment_list)
    #forward_post_spatial(mode, catchment_list)

    #post_plot.plot_param_all(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/', Path.work_path+'plots/', nchains, catchment_ID)
    post_plot.plot_param_all('/data/scratch/wusongj/paper4/cali/best_param_all.bin', Path.work_path+'plots/'+mode+'/', nchains, suffix=mode)