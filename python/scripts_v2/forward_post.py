import os
import shutil
import sys
from optparse import OptionParser
import numpy as np
import time

import pickle



import post_plot_v2
from def_GEM_v2 import Path, Info, Cali, Param, Output


# Adapt two-leaf model for photosynthesis
# Calcualte stomal conductance from NPP
# Check Mass balance for carbon addition and carbon transformation
# Add In-stream carbon decomposition
# New evapotranspiration module based on stomatal conductance



# Update 16/02/2026:
# Inundation conceptulization via partial routing of ponding water
# Add capillary flow module (water flow from shallow GW zone to bottom soil layer)

# Update 26/02/2026:
# Percolation and capillary flow thershold can now exceed field capacity
# Update soil moisture factor for carbon decomposition
# Change NPP to plant fraction
# Change reference decomposition rate
# Need to reset reserve pools; green pool is already reset

# Update 04/03/2026 to 15/03/2026:
# Overland flow update: now all overland flow will only routed to river channel (still partially to channel but no routing to terrestrial downstream grids)
# Soluble pool and DOC pool are two independent pools with monotonic relationship (dissolution from soluble pool to DOC pool based on residence time)
# Add two statistical variables: leaching_mass_doc/no3 and drainage_mass_doc/no3
# Disable the near surface mixing (between ponding water and top soil layer) to reduce parameter dimensionality
# Introduce the concept of rock landscapes, which dominates the preferential flow (from ponding water to vadose storage) and the reduction of soil evaporation
# Update the moisture factor for transformation function (set lower boundary to 0.0 instead of wilting point; set optimal moisture to 0.8*field capacity)
# Adjust the soil moisture function for NPP with lower sensitivity to soil moisture (old function overly suppressed the NPP in lowlands)
# Harvest and Herbivory loss added, which are conceptualised by first decay coefficient of plant carbon pools

# Update 20/03/2026:
# Merging vadose mixing to soil transport module for capillary flow mixing
# A bug is corrected for minerlisation from non-wood carbon pools to NO3 pool (in Carbon_transformation function)

# GW storage should be higher in Alpine regions than in lowlands
# We need to lower the DOC GW concentration to increase the leaching concentration
# Preferential flow?




if __name__ == '__main__':


    
    
    plot_path = Path.work_path + 'plots/'
    
    nchains = Cali.nchains
    nchains = 1

    catchment_dicts = {
        '831616_001': 9,
        '291110_001': 1,
        '83749_001': 3,
        '1034724_001': 12,
        '95_001': 16,
    }

    mode = 'forward_cali'


    catchment_list = pickle.load(open(Path.work_path + 'data/catchment_info/cali/sub_catchment_ID_list', 'rb'))


    for catchment_ID in catchment_list[:2]:
        if mode=='forward_sep':
            suffix = '_NPP_ET_drainage_capillary_landuse_ovf100_FCthres_fcttheta_Solubledissolve_DOCdecomp_test6'
            param_path = Path.work_path + 'cali_sep/best_param/best_param_' + catchment_ID + '.bin'
            sim_path = Path.work_path + 'forward_sep/outputs/cali_sep/' + catchment_ID + '/'
            obs_path = Path.work_path + 'data/catchment_info/cali/' + catchment_ID + '/obs/'
        elif mode=='forward_cali':
            suffix = '_test0'
            param_path = Path.work_path + 'forward_cali/best_param/best_param_' + catchment_ID + '.bin'
            sim_path = Path.work_path + 'forward_cali/outputs/' + catchment_ID + '/'
            obs_path = Path.work_path + 'data/catchment_info/cali/' + catchment_ID + '/obs/'

        print('\nPlotting for catchment: ' + catchment_ID)
    
        #post_plot_v2.plot_param_all(param_path, plot_path, catchment_ID, nchains=20, suffix=suffix)
        post_plot_v2.plot_performance_sep(sim_path, obs_path, plot_path, catchment_ID, nchains, suffix=suffix)
        #post_plot_v2.plot_spatial_maps(sim_path, plot_path, catchment_ID, warming_period=2, nchains=nchains, suffix=suffix, 
        #flag_spatial_maps=True, flag_spatial_diff_maps=True, flag_TS_maps=False, flag_correlation_maps=True)

        #post_plot_v2.plot_spatial_stats(sim_path, plot_path, catchment_ID, warming_period=2, nchains=nchains, suffix=suffix)





    #post_plot_v2.plot_performance_scatter_all_catchments(Path.work_path + 'forward_sep/outputs/cali_sep/', Path.work_path + 'data/catchment_info/cali/', plot_path, nchains, suffix='')