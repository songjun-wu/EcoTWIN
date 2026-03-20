import os
from zipfile import ZIP_BZIP2
import numpy as np
import matplotlib.pyplot as plt
from def_GEM_v2 import Path, Info, Cali, Param, Output
import GEM_tools_v2
import pandas as pd
import time
from collections import deque, defaultdict
from matplotlib.colors import LinearSegmentedColormap



import datetime

def read_spatial_data(path, mask, nchains, chanmask=None, weight=1, warming_period=2):
    
    data = np.fromfile(path).reshape(nchains, -1, mask.shape[0], mask.shape[1])
    data = np.mean(data, axis=0)
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan
    
    #data = np.mean(data[warming_period:,:,:], axis=0) * weight
    data = np.mean(data[-10:,:,:], axis=0) * weight
    return data


def read_spatial_data_diff(path, mask, nchains, chanmask=None, weight=1, warming_period=2):
    
    data = np.fromfile(path).reshape(nchains, -1, mask.shape[0], mask.shape[1])
    data = np.mean(data, axis=0)
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan
    
    #data = (np.mean(data[-5:,:,:], axis=0) - np.mean(data[warming_period:warming_period+5,:,:], axis=0)) * weight
    data = (np.mean(data[-5:,:,:], axis=0) - np.mean(data[-10:-5,:,:], axis=0)) * weight
    return data


def read_temporal_data(path, mask, nchains, chanmask=None, weight=1, warming_period=2):
    data = np.fromfile(path).reshape(nchains, -1, mask.shape[0], mask.shape[1])
    data = np.mean(data, axis=0)
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan

    data = np.nanmean(data, axis=(1,2)) * weight    
    return data

def plot_spatial_maps(sim_path, plot_path, catchment_ID, warming_period, nchains, suffix='', flag_landuse_maps=False, flag_spatial_maps=False, flag_spatial_diff_maps=False, flag_TS_maps=False,  flag_correlation_maps=False):

    mask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
    chanmask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/chnwidth.asc', skiprows=6)
    chanmask = chanmask>0

    nrow = 8
    ncol = 6

    vars = ['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'infiltration', 'perc_layer1', 'perc_layer2', 'drainage_from_soil', 'age_chanS', 'trans_age_chanS', 'd18o_chanS', 'doc_chanS', 'no3_chanS', 'deni_soil', 'minerl_soil', 'plant_uptake', 'nitrogen_addition', 'fast_N', 'humus_N', 'net_primary_production', 'soil_respiration', 'plant_C', 'fast_C', 'humus_C']
    weights = [1, 1, 1, 1000*365, 1000*365, 1000*365, 1000*365, 1, 1, 1, 1, 1, 10*365, 10*365, 10*365, 1000*365, 1, 1, 1*365, 1*365, 1, 1, 1]
    is_chans = [False, False, False, True, True, True, True, False, False, True, True, True, False, False, True, False, False, False, True, True, False, False, False]
    vmins = [0.2, 0.2, 0.2, 500, 200, 200, 0, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None]
    vmaxs = [0.4, 0.4, 0.4, 700, 400, 400, 70, None, None, 50, 10, 10, None, None, None, None, None, None, None, None, None, None, None]

    dict_all = {'SMC_layer1':[1,False, 0.3, 0.6],
                'SMC_layer2':[1,False, 0.3, 0.6],
                'SMC_layer3':[1,False, 0.3, 0.6],
                'infiltration':[1000*365,False, 200, 1200],
                'perc_layer1':[1000*365,False, 200, 1200],
                'perc_layer2':[1000*365,False, 200, 1200],

                'soil_evap':[1000*365,False, 0, 1000],
                'transp':[1000*365,False, 0, 1000],
                'age_SMC_layer1':[1,False, 0, 300],
                'age_SMC_layer2':[1,False, 0, 300],
                'age_vadose':[1,False, 0, 3000],
                'age_chanS':[1,True, 0, 3000],


                'overland_flow_output':[1000*365,False, 0, 1000],
                'overland_flow_toChn':[1000*365,False, 0, 500],
                'interflow_output':[1000*365,False, 0, 1000],
                'interflow_toChn':[1000*365,False, 0, 1000],
                'GWflow_output':[1000*365,False, 0, 1000],
                'GWflow_toChn':[1000*365,False, 0, 1000],

                'doc_SMC_layer1':[1,False, 0, 100],
                'doc_SMC_layer2':[1,False, 0, 50],
                'doc_SMC_layer3':[1,False, 0, 50],
                'doc_vadose':[1,False, 0, 50],
                'doc_groundwater_storage':[1,False, 0, 50],
                'doc_chanS':[1,True, 0, 20],         
                #'drainage_from_soil':[1000*365,False, 0, 70],

                'no3_SMC_layer1':[1,False, 0, 50],
                'no3_SMC_layer2':[1,False, 0, 10],
                'no3_SMC_layer3':[1,False, 0, 10],
                'no3_vadose':[1,False, 0, 10],
                'no3_groundwater_storage':[1,False, 0, 10],
                'no3_chanS':[1,True, 0, 10],         

                
                'deni_soil':[1*365,False, 0, 15],
                'minerl_soil':[1*365,False, 0, 15],
                'plant_uptake':[1*365,False, 0, 15],
                'nitrogen_addition':[1*365,False, 0, 15],
                'fast_N':[1,False, 0, 50],
                'humus_N':[1,False, 0, 3000],

                'net_primary_production':[1*365,False, 0, 1000],
                'litter_fall_C':[1*365,False, 0, 1000],
                'soil_respiration_C':[1*365,False, 0, 500],
                'plant_C':[1,False, 0, 3000],
                'fast_C':[1,False, 1000, 3000],
                'humus_C':[1,False, 5000, 10000],

                'respiration_river_C':[1*365,False, 0, 10],
                #'deni_river':[1*365,False, 0, 2],
                'soluble_C':[1,False, 0, 200],

                'leaching_mass_all_doc':[1*365,False, 0, 1, ['leaching_mass_doc', 'drainage_mass_doc'], [1,1], 'viridis'],
                'leaching_mass_all_no3':[1*365,False, 0, 1, ['leaching_mass_no3', 'drainage_mass_no3'], [1,1], 'viridis'],
                'litter_fall-Resp':[1*365,False, 0, 10, ['litter_fall_C', 'soil_respiration_C'], [1,-1], 'coolwarm'],

                'preferential_flow':[1000*365,False, 0, 1000],


                #'pond':[1,False, 0, 3],
                #'capillary_flow':[1000*365,False, 0, 100],
                #'drainage_from_soil':[1000*365,False, 0, 100],
                #'irrigation_from_river':[1000*365,False, 0, 100],
                
                
                
                }
    
    
    

    # Spatial maps
    if flag_spatial_maps:
        fig, ax = plt.subplots(nrow, ncol, figsize=(20,20), dpi=300)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.2)
        i = 0
        for key, value in dict_all.items():
            var = key
            weight = value[0]
            is_chan = value[1]
            vmin = value[2]
            vmax = value[3]

            
            if is_chan:
                chanmask_plot = chanmask>0
            else:
                chanmask_plot = None
            

            vars_to_exluce = ['doc_chanS1111']
            if var not in vars_to_exluce:
                vmin = None  # todo
            if len(value) == 4:
                data = read_spatial_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period)
                cmap = 'viridis'
            else:
                for zz, tmp_var in enumerate(value[4]):
                    if zz==0:
                        data = read_spatial_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
                    else:
                        data += read_spatial_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
                    cmap = value[6]

                
            if vmin is None or vmax is None:
                vmin = np.nanpercentile(data, 2)
                vmax = np.nanpercentile(data, 98)
                if cmap == 'coolwarm':
                    v_tmp = max(np.abs(vmin), np.abs(vmax))
                    vmin = -v_tmp
                    vmax = v_tmp
                locals()['im'+str(i)] = ax[i//ncol, i%ncol].imshow(data, vmin=vmin, vmax=vmax, cmap=cmap)
            else:
                locals()['im'+str(i)] = ax[i//ncol, i%ncol].imshow(data, vmin=vmin, vmax=vmax, cmap=cmap)
            

            ax[i//ncol, i%ncol].set_title(var)
            i += 1

        for r in range(nrow):
            for c in range(ncol):
                ax[r,c].axis('off')

        for r in range(nrow):
            for c in range(ncol):
                try:
                    fig.colorbar(locals()['im'+str(r*ncol+c)], ax=ax[r,c])
                except:
                    pass
        fig.savefig(plot_path+'spatial_maps_'+str(catchment_ID)+suffix+'.png', transparent=False)


    # Plot differences between 1992-1997 to last 5 years
    if flag_spatial_diff_maps:
        fig, ax = plt.subplots(nrow, ncol, figsize=(20,20), dpi=300)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.2)
        i = 0
        for key, value in dict_all.items():
            var = key
            weight = value[0]
            is_chan = value[1]
            vmin = value[2]
            vmax = value[3]

            if is_chan:
                chanmask_plot = chanmask>0
            else:
                chanmask_plot = None
            

            if len(value) == 4:
                data = read_spatial_data_diff(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period)
            else:
                for zz, tmp_var in enumerate(value[4]):
                    if zz==0:
                        data = read_spatial_data_diff(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
                    else:
                        data += read_spatial_data_diff(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
            

            locals()['im'+str(i)] = ax[i//ncol, i%ncol].imshow(data, vmin=-vmax/3, vmax=vmax/3, cmap='coolwarm')


            ax[i//ncol, i%ncol].set_title(var)
            i += 1

        for r in range(nrow):
            for c in range(ncol):
                ax[r,c].axis('off')

        for r in range(nrow):
            for c in range(ncol):
                try:
                    fig.colorbar(locals()['im'+str(r*ncol+c)], ax=ax[r,c])
                except:
                    pass
        fig.savefig(plot_path+'spatial_maps_diff_'+str(catchment_ID)+suffix+'.png', transparent=False)


    # Time series
    if flag_TS_maps:
        fig, ax = plt.subplots(nrow, ncol, figsize=(20,20), dpi=300)
        ref_data = read_temporal_data(sim_path+'SMC_layer1_map.bin', mask, nchains, warming_period=warming_period)
        try:
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='YE')[:len(ref_data)]
        except:
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='Y')[:len(ref_data)]
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.25)

        i = 0
        for key, value in dict_all.items():
            var = key
            weight = value[0]
            is_chan = value[1]
            vmin = value[2]
            vmax = value[3]

            if is_chan:
                chanmask_plot = chanmask>0
            else:
                chanmask_plot = None
            
            if len(value) == 4:
                data = read_temporal_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period)
            else:
                for zz, tmp_var in enumerate(value[4]):
                    if zz==0:
                        data = read_temporal_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
                    else:
                        data += read_temporal_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]

            locals()['im'+str(i)] = ax[i//ncol, i%ncol].plot(tindex, data)

            ax[i//ncol, i%ncol].set_title(var)
            i += 1

        for r in range(nrow):
            for c in range(ncol):
                ax[r,c].set_xticks([pd.Timestamp(1980,1,1), pd.Timestamp(2000,1,1), pd.Timestamp(2020,1,1)])
                ax[r,c].set_xticklabels([])

        fig.savefig(plot_path+'Time_series_'+str(catchment_ID)+suffix+'.png', transparent=False)

    if flag_landuse_maps:
        fig, ax = plt.subplots(4, 4, figsize=(20,20), dpi=300)
        mask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
        mask = mask!=-9999
        for i in range(14):
            p_landuse = np.fromfile(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/category_'+str(i+1)+'.bin').reshape(-1, mask.shape[0], mask.shape[1])
            p_landuse = np.mean(p_landuse, axis=0)
            p_landuse[~mask] = np.nan

            ax[i//4, i%4].imshow(p_landuse, vmin=0, vmax=1, cmap='coolwarm')
            ax[i//4, i%4].set_title('Category '+str(i+1))
        fig.savefig(plot_path+'Landuse_maps_'+str(catchment_ID)+suffix+'.png', transparent=False)




    # Attribution between cropland and wetland
    if flag_correlation_maps:
        fig, ax = plt.subplots(nrow, ncol, figsize=(20,20), dpi=300)
        ref_data = read_temporal_data(sim_path+'SMC_layer1_map.bin', mask, nchains, warming_period=warming_period)
        try:
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='YE')[:len(ref_data)]
        except:
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='Y')[:len(ref_data)]
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.25)

        mask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
        mask = mask!=-9999
        p_cropland = np.fromfile(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/category_8.bin').reshape(-1, mask.shape[0], mask.shape[1])
        p_wetland = np.fromfile(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/category_14.bin').reshape(-1, mask.shape[0], mask.shape[1])
        p_cropland = (np.mean(p_cropland, axis=0)[mask]).flatten()
        p_wetland = (np.mean(p_wetland, axis=0)[mask]).flatten()



        i = 0
        for key, value in dict_all.items():
            var = key
            weight = value[0]
            is_chan = value[1]
            vmin = value[2]
            vmax = value[3]

            if is_chan:
                chanmask_plot = chanmask>0
            else:
                chanmask_plot = None

            x = p_cropland
            y = p_wetland   
            

            if len(value) == 4:
                data = read_spatial_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period)
            else:
                for zz, tmp_var in enumerate(value[4]):
                    if zz==0:
                        data = read_spatial_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
                    else:
                        data += read_spatial_data(sim_path+tmp_var+'_map.bin', mask, nchains, chanmask_plot, weight=weight, warming_period=warming_period) * value[5][zz]
            c = data[mask].flatten()


            locals()['im'+str(i)] = ax[i//ncol, i%ncol].scatter(x, y, c=c, cmap='coolwarm', alpha=0.5)

            ax[i//ncol, i%ncol].set_title(var)
            i += 1

        #for r in range(nrow):
            #for c in range(ncol):
                #ax[r,c].set_xlim([0, 1])
                #ax[r,c].set_ylim([0, 1])
                #ax[r,c].set_xticks([0, 0.5, 1])
                #ax[r,c].set_yticks([0, 0.5, 1])
                #ax[r,c].set_xticklabels([])
                #ax[r,c].set_yticklabels([])

        fig.savefig(plot_path+'Relationship_'+str(catchment_ID)+suffix+'.png', transparent=False)


def plot_spatial_stats(sim_path, plot_path, catchment_ID, warming_period, nchains, suffix=''):
    fig, ax = plt.subplots(1, 1, figsize=(10,10), dpi=300)
    mask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
    mask = mask!=-9999

    # 
    data0 = read_spatial_data(sim_path+'leaching_mass_doc_map.bin', mask, nchains, weight=1, warming_period=warming_period)
    data1 = read_spatial_data(sim_path+'drainage_mass_doc_map.bin', mask, nchains, weight=1, warming_period=warming_period)
    data2 = read_spatial_data(sim_path+'perc_layer3_map.bin', mask, nchains, weight=1, warming_period=warming_period)
    data3 = read_spatial_data(sim_path+'drainage_from_soil_map.bin', mask, nchains, weight=1, warming_period=warming_period)

    data = (data0 + data1) / (data2 + data3)
    data[~mask] = np.nan
    ax.imshow(data, vmin=0, vmax=5, cmap='viridis')
    vmin = np.nanpercentile(data, 2)
    vmax = np.nanpercentile(data, 98)
    fig.colorbar(ax.imshow(data, vmin=vmin, vmax=vmax, cmap='viridis'), ax=ax)
    fig.savefig(plot_path+'spatial_map_stats_'+str(catchment_ID)+suffix+'.png', transparent=False)





def plot_performance_scatter_all_catchments(_sim_path, _obs_path, output_path, nchains, suffix=''):
    
    catchment_IDs = ['95_001','831616_001', '83749_001']

    fig, ax = plt.subplots(2, 2, figsize=(12,8), dpi=300)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.3, hspace=0.2)
    _tindex = pd.date_range('1980-1-1', '2024-12-31')[Info.spin_up:]

    
    counter_key = 0
    for key, value in Output.sim.items():
        sim_all_points = np.array([])
        obs_all_points = np.array([])
        for xx, catchment_ID in enumerate(catchment_IDs):
            catchment_idx = np.squeeze(np.argwhere(np.array(Output.Catchment_ID)==catchment_ID))
            print(catchment_ID, catchment_idx)
            dict = Output.sim[key]
            sim_idx = dict['sim_idx'][catchment_idx]
            N_sites = Output.N_sites[catchment_idx]

            sim_path = _sim_path + catchment_ID + '/'
            obs_path = _obs_path + catchment_ID + '/obs/'

            print(sim_path, obs_path)

            if len(sim_idx) > 0:
                obs_all = np.fromfile(obs_path+dict['obs_file']).reshape(len(sim_idx), -1)
                sim_all = np.fromfile(sim_path+dict['sim_file']).reshape(nchains, -1, N_sites)

                _sim_upper = np.percentile(sim_all, 95, axis=0).T
                _sim_lower = np.percentile(sim_all, 5, axis=0).T
                _sim_mean = np.mean(sim_all, axis=0).T
                _sim_mean = _sim_mean[:, Info.spin_up:]
                _sim_upper = _sim_upper[:, Info.spin_up:]
                _sim_lower = _sim_lower[:, Info.spin_up:]

                tindex = _tindex[:obs_all.shape[-1]]
                
                #tmp_monthly_all = np.array([])
                #sim_obs_all = np.array([])
                for kk in range(len(sim_idx)):

                    sim_mean = _sim_mean[sim_idx[kk],:] + 1e-5
                    sim_upper = _sim_upper[sim_idx[kk],:] + 1e-5
                    sim_lower = _sim_lower[sim_idx[kk],:] + 1e-5
                    obs = obs_all[kk, :] + 1e-5

                    tmp = np.full(len(sim_mean), np.nan)
                    tmp[:len(obs)] = obs                   

                    sim_all_points = np.append(sim_all_points, sim_mean)
                    obs_all_points = np.append(obs_all_points, tmp)
        

        x = sim_all_points
        y = obs_all_points
        ax[counter_key//2, counter_key%2].scatter(sim_all_points, obs_all_points, c='black', s=0.5, alpha=0.1)

        if len(x) > 0:

            x_percentile = np.percentile(x, [2, 98])
            y_percentile = np.percentile(y, [2, 98])
            xlim = [min(x_percentile[0], y_percentile[0]), max(x_percentile[1], y_percentile[1])]
            ax[counter_key//2, counter_key%2].set_xlim(xlim)
            ax[counter_key//2, counter_key%2].set_ylim(xlim)

            # 添加1:1辅助线
            ax[counter_key//2, counter_key%2].plot(xlim, xlim, 'black', linewidth=2, label='1:1 line')

        counter_key += 1

    fig.savefig(output_path+'performance_scatter_all_catchments_'+suffix+'.png', transparent=False)


def plot_performance_sep(sim_path, obs_path, output_path, catchment_ID, nchains, suffix=''):

    catchment_idx = np.squeeze(np.argwhere(np.array(Output.Catchment_ID)==catchment_ID))

    

    dict_vmins = {'q':None, 'iso_stream':None, 'no3':None, 'doc':None}
    dict_vmaxs = {'q':None, 'iso_stream':None, 'no3':None, 'doc':None}

    var_names = ['Q [m3/s]', 'Isotope [‰]', 'NO3 [mg/L]', 'DOC [mg/L]']


    nrow = 10
    ncol = 5
    fig, ax = plt.subplots(nrow, ncol, figsize=(12,8), dpi=300)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.3, hspace=0.2)
    _tindex = pd.date_range('1980-1-1', '2024-12-31')[Info.spin_up:]

    
    
    counter_key = 0
    counter = 0


    n_subplots = np.sum([len(Output.sim[key]['sim_idx'][catchment_idx]) for key in Output.sim.keys()])
    
    for key, value in Output.sim.items():
        dict = Output.sim[key]
        sim_idx = dict['sim_idx'][catchment_idx]
        N_sites = Output.N_sites[catchment_idx]

        
        
        if len(sim_idx) > 0:
            obs_all = np.fromfile(obs_path+dict['obs_file']).reshape(len(sim_idx), -1)
            sim_all = np.fromfile(sim_path+dict['sim_file']).reshape(nchains, -1, N_sites)

            _sim_upper = np.percentile(sim_all, 95, axis=0).T
            _sim_lower = np.percentile(sim_all, 5, axis=0).T
            _sim_mean = np.mean(sim_all, axis=0).T
            _sim_mean = _sim_mean[:, Info.spin_up:]
            _sim_upper = _sim_upper[:, Info.spin_up:]
            _sim_lower = _sim_lower[:, Info.spin_up:]

            tindex = _tindex[:obs_all.shape[-1]]
            
            #tmp_monthly_all = np.array([])
            #sim_obs_all = np.array([])
            for kk in range(len(sim_idx)):

                sim_mean = _sim_mean[sim_idx[kk],:] + 1e-5
                sim_upper = _sim_upper[sim_idx[kk],:] + 1e-5
                sim_lower = _sim_lower[sim_idx[kk],:] + 1e-5
                obs = obs_all[kk, :] + 1e-5

                tmp = np.full(len(sim_mean), np.nan)
                tmp[:len(obs)] = obs
                ax[counter//ncol, counter%ncol].fill_between(tindex, sim_lower, sim_upper, color='gray', alpha=0.3)
                if key == 'q':
                    ax[counter//ncol, counter%ncol].plot(tindex, sim_mean, linewidth=0.5, alpha=0.7)
                    ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=0.5, alpha=0.3)
                else:
                    ax[counter//ncol, counter%ncol].plot(tindex, sim_mean, linewidth=0.5, alpha=0.7)
                    ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=1, alpha=0.8)
                

                    

                # Get average value of tmp for each month
                """
                tmp_monthly = np.zeros(12)
                df_tmp = pd.DataFrame(tmp, index=tindex)
                df_tmp_monthly = df_tmp.resample('M').mean()
                tmp_monthly = df_tmp_monthly.values
                # Average over multiple years
                tmp_monthly = np.nanmean(tmp_monthly.reshape(-1, 12), axis=0)

                tmp_monthly_all = np.concatenate((tmp_monthly_all, tmp_monthly))

                sim_obs_all = np.concatenate((sim_obs_all, sim_mean))
                sim_obs_all = np.concatenate((sim_obs_all, tmp))
                """

                #if key=='no3':
                #    ax[counter//ncol, counter%ncol].set_ylim([-0.1,10.1])
                #    ax[counter//ncol, counter%ncol].set_yticks([0,2,4,6,8,10])

                
                ax[counter//ncol, counter%ncol].set_xticks([datetime.datetime(1980,1,1), datetime.datetime(2000,1,1), datetime.datetime(2020,1,1)])
                ax[counter//ncol, counter%ncol].set_xticklabels(['1980', '2000', '2020'])
                if dict_vmins[key] is not None:
                    ax[counter//ncol, counter%ncol].set_ylim([dict_vmins[key], dict_vmaxs[key]])
                
                # Add text based on the position of axis
                ax[counter//ncol, counter%ncol].text(
                    0.03, 0.95, 
                    var_names[counter_key],
                    transform=ax[counter//ncol, counter%ncol].transAxes,
                    ha="left",
                    va="top",
                    weight='bold',
                    fontsize=8
                )

                ax[counter//ncol, counter%ncol].text(
                    0.95, 0.95, 
                    str('KGE: '+str(np.round(GEM_tools_v2.kge(sim_mean, tmp),2))),
                    transform=ax[counter//ncol, counter%ncol].transAxes,
                    ha="right",
                    va="top",
                    weight='bold',
                    fontsize=8
                )

                if counter >= n_subplots - ncol:
                    ax[counter//ncol, counter%ncol].tick_params(labelbottom=True)
                else:
                    ax[counter//ncol, counter%ncol].tick_params(labelbottom=False)
                
                print(key, kk, np.round(GEM_tools_v2.kge(sim_mean, tmp),2), np.round(GEM_tools_v2.nse(sim_mean, tmp),2), np.round(GEM_tools_v2.rsquare(sim_mean, tmp),2), np.round(GEM_tools_v2.pbias(sim_mean, tmp),2), )

                counter += 1
        counter_key += 1
    
    for i in range(counter, nrow*ncol):
        ax[i//ncol, i%ncol].axis('off')

    fig.savefig(output_path+'performance_'+catchment_ID+suffix+'.png', transparent=False)
    
    #np.savetxt(output_path+'tmp_monthly_all.txt', tmp_monthly_all.reshape(-1, 12))
    #np.savetxt(output_path+'sim_obs_all.txt', (sim_obs_all.reshape(-1, len(tindex))).T)



def plot_param_all(param_path, plot_path, catchment_ID,nchains, suffix=''):

    param = np.fromfile(param_path)
    param = param.reshape(nchains, -1).T

    keys = Param.ref.keys()
    param_names = []
    for key in keys:
        dict = Param.ref[key]
        if dict['fix_value'] is None:
            if dict['type'] == 'global':
                param_names.append(key)
            elif dict['type'] == 'soil':
                for i in range(Info.N_soil):
                    param_names.append(key + '_s' + str(i))
            elif dict['type'] == 'landuse':
                for i in range(Info.N_landuse):
                    param_names.append(key + '_v' + str(i))
        else:
            for i in range(len(dict['fix_value'])):
                if dict['fix_value'][i] is None:
                    param_names.append(key + '_s' + str(i))

    """
    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(param, cmap='viridis', aspect=1.3)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param.png')
    """
    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    for i in range(param.shape[0]):
        param[i] = np.sort(param[i])
    ax.imshow(param, cmap='viridis', aspect=1.3)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig(plot_path + 'param_sorted_'+catchment_ID+suffix+'.png')