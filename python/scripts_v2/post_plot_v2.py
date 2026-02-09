import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM_v2 import Path, Info, Cali, Param, Output
import GEM_tools
import pandas as pd
import GIS_tools
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
    
    data = np.mean(data[warming_period:,:,:], axis=0) * weight
    return data


def read_spatial_data_diff(path, mask, nchains, chanmask=None, weight=1, warming_period=2):
    
    data = np.fromfile(path).reshape(nchains, -1, mask.shape[0], mask.shape[1])
    data = np.mean(data, axis=0)
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan
    
    data = (np.mean(data[-5:,:,:], axis=0) - np.mean(data[warming_period:warming_period+5,:,:], axis=0)) * weight
    return data


def read_temporal_data(path, mask, nchains, chanmask=None, weight=1):
    data = np.fromfile(path).reshape(nchains, -1, mask.shape[0], mask.shape[1])
    data = np.mean(data, axis=0)
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan

    data = np.nanmean(data, axis=(1,2)) * weight    
    return data

def plot_spatial_maps(sim_path, plot_path, catchment_ID, nchains, suffix=''):

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

    dict_all = {'SMC_layer1':[1,False, 0.2, 0.8],
                'SMC_layer2':[1,False, 0.2, 0.8],
                'SMC_layer3':[1,False, 0.2, 0.8],
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
                'doc_chanS':[1,True, 0, 50],         
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

                'net_primary_production':[1*365,False, 0, 1500],
                'litter_fall_C':[1*365,False, 0, 1000],
                'soil_respiration_C':[1*365,False, 0, 1000],
                'plant_C':[1,False, 0, 3000],
                'fast_C':[1,False, 1000, 3000],
                'humus_C':[1,False, 5000, 30000],

                'respiration_river_C':[1*365,False, 0, 10],
                'deni_river':[1*365,False, 0, 2],
                
                
                }
    
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
        
        locals()['im'+str(i)] = ax[i//ncol, i%ncol].imshow(read_spatial_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight), vmin=vmin, vmax=vmax)

        tmppp = read_spatial_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight)
        print(var, tmppp.shape, np.nanmin(tmppp), np.nanmax(tmppp), np.nanmean(tmppp), flush=True)

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
        

        locals()['im'+str(i)] = ax[i//ncol, i%ncol].imshow(read_spatial_data_diff(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight), vmin=-vmax/3, vmax=vmax/3, cmap='coolwarm')

        tmppp = read_spatial_data_diff(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight)
        #print(var, tmppp.shape, np.nanmin(tmppp), np.nanmax(tmppp), np.nanmean(tmppp), flush=True)

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
    fig, ax = plt.subplots(nrow, ncol, figsize=(20,20), dpi=300)
    ref_data = read_temporal_data(sim_path+'SMC_layer1_map.bin', mask, nchains)
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

        locals()['im'+str(i)] = ax[i//ncol, i%ncol].plot(tindex, read_temporal_data(sim_path+var+'_map.bin', mask, nchains, chanmask_plot, weight=weight))

        ax[i//ncol, i%ncol].set_title(var)
        i += 1

    for r in range(nrow):
        for c in range(ncol):
            ax[r,c].set_xticks([pd.Timestamp(1980,1,1), pd.Timestamp(2000,1,1), pd.Timestamp(2020,1,1)])
            ax[r,c].set_xticklabels([])

    fig.savefig(plot_path+'Time_series_'+str(catchment_ID)+suffix+'.png', transparent=False)




def plot_performance_sep(sim_path, obs_path, output_path, catchment_ID, nchains, suffix=''):

    catchment_idx = np.squeeze(np.argwhere(np.array(Output.Catchment_ID)==catchment_ID))

    dict_vmins = {'q':None, 'iso_stream':None, 'no3':None, 'doc':0}
    dict_vmaxs = {'q':None, 'iso_stream':None, 'no3':None, 'doc':10}


    nrow = 10
    ncol = 5

    fig, ax = plt.subplots(nrow, ncol, figsize=(12,8), dpi=300)
    _tindex = pd.date_range('1980-1-1', '2024-12-31')[Info.spin_up:]

    counter = 0
    
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
                ax[counter//ncol, counter%ncol].plot(tindex, sim_mean, linewidth=0.5, alpha=0.7)
                ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=0.5, alpha=0.3)

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

                if dict_vmins[key] is not None:
                    ax[counter//ncol, counter%ncol].set_ylim([dict_vmins[key], dict_vmaxs[key]])
                
                print(key, kk, np.round(GEM_tools.kge(sim_mean, tmp),2), np.round(GEM_tools.nse(sim_mean, tmp),2), np.round(GEM_tools.rsquare(sim_mean, tmp),2), np.round(GEM_tools.pbias(sim_mean, tmp),2), )

                counter += 1

    fig.savefig(output_path+'performance_'+catchment_ID+suffix+'.png', transparent=False)

    #np.savetxt(output_path+'tmp_monthly_all.txt', tmp_monthly_all.reshape(-1, 12))
    #np.savetxt(output_path+'sim_obs_all.txt', (sim_obs_all.reshape(-1, len(tindex))).T)



def plot_param_all(param_path, plot_path, nchains, suffix=''):

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
    fig.savefig(plot_path + 'param_sorted_'+suffix+'.png')