import os
import shutil
import sys
from optparse import OptionParser
import numpy as np
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/run_model')
import GEM_tools
import post_plot
import post_plot_v2
from def_GEM_v2 import Path, Info, Cali, Param, Output


# Adapt two-leaf model for photosynthesis
# Calcualte stomal conductance from NPP
# Check Mass balance for carbon addition and carbon transformation
# Add In-stream carbon decomposition


if __name__ == '__main__':

    catchment_ID = '291110_001'
    #catchment_ID = '831616_001'
    suffix = '_7_with_NPP_instream_ET'
    
    param_path = Path.work_path + 'cali_sep/best_param/best_param_' + catchment_ID + '.bin'
    sim_path = Path.work_path + 'forward_sep/outputs/cali_sep/' + catchment_ID + '/'
    obs_path = Path.work_path + 'data/catchment_info/cali/' + catchment_ID + '/obs/'
    plot_path = Path.work_path + 'plots/'
    
    nchains = Cali.nchains
    nchains = 1
    
    #post_plot_v2.plot_param_all(param_path, plot_path, nchains=20, suffix=suffix)
    #post_plot_v2.plot_performance_sep(sim_path, obs_path, plot_path, catchment_ID, nchains, suffix=suffix)
    post_plot_v2.plot_spatial_maps(sim_path, plot_path, catchment_ID, nchains, suffix=suffix)