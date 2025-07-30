import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path, Info, Cali, Param, Output
import GEM_tools
import pandas as pd
import GIS_tools
import time
from collections import deque, defaultdict


nodata = Info.nodata
var_info = {
                'Precipitation_npfloat32_3035':[[0,1200],1000*365,False],
                'Potential_evapotranspiration_npfloat32_3035':[[0,1200],1000*365,False],
                'Mean_air_temperature_npfloat32_3035':[[-5,25],1,False],
                'Surface_net_radiation_npfloat32_3035':[[-100,600],1,False],

                'canopy_storage':[[0,5],1000,False],
                'snow_depth':[[0,100],1000,False],
                'SMC_layer1':[[0.2,0.6],1,False],
                'SMC_layer2':[[0.2,0.6],1,False],
                'SMC_layer3':[[0.2,0.6],1,False],
                'vadose':[[0,100],1000,False],
                'groundwater_storage':[[0,50000],1000,False],
                'snowmelt':[[0,300],1000*365,False],
                'throufall':[[0,1200],1000*365,False],
                'irrigation_from_GW':[[0,200],1000*365,False],
                'irrigation_from_river':[[0,100],1000*365,True],
                'infiltration':[[0,1500],1000*365,False],
                'perc_layer1':[[0,900],1000*365,False],
                'perc_layer2':[[0,900],1000*365,False],
                'perc_layer3':[[0,900],1000*365,False],
                'perc_vadose':[[0,900],1000*365,False],
                'rinfiltration':[[0,500],1000*365,False],
                'rperc_layer1':[[0,500],1000*365,False],
                'rperc_layer2':[[0,500],1000*365,False],
                'rperc_layer3':[[0,500],1000*365,False],
                'soil_evap':[[0,300],1000*365,False],
                'transp':[[0,500],1000*365,False],
                'transp_layer1':[[0,300],1000*365,False],
                'transp_layer2':[[0,100],1000*365,False],
                'transp_layer3':[[0,100],1000*365,False],
                'channel_evaporation':[[0,20],1000*365,True],

                'overland_flow_input':[[0,2000],1000*365,False],
                'overland_flow_output':[[0,2000],1000*365,False],
                'interflow_input':[[0,2000],1000*365,False],
                'interflow_output':[[0,2000],1000*365,False],
                'GWflow_input':[[0,2000],1000*365,False],
                'GWflow_output':[[0,2000],1000*365,False],
                'overland_flow_toChn':[[0,500],1000*365,True],
                'interflow_toChn':[[0,2000],1000*365,True],
                'GWflow_toChn':[[0,1000],1000*365,True],
                'discharge':[[0,200],1,True],
                
                'd18o_canopy_storage':[[-15,0],1,False],
                'd18o_snow_depth':[[-15,0],1,False],
                'd18o_SMC_layer1':[[-15,0],1,False],
                'd18o_SMC_layer2':[[-15,0],1,False],
                'd18o_SMC_layer3':[[-15,0],1,False],
                'd18o_vadose':[[-15,0],1,False],
                'd18o_groundwater_storage':[[-15,0],1,False],
                'd18o_chanS':[[-15,0],1,True],

                'age_canopy_storage':[[0,10],1,False],
                'age_snow_depth':[[0,500],1,False],
                'age_SMC_layer1':[[0,500],1,False],
                'age_SMC_layer2':[[0,1000],1,False],
                'age_SMC_layer3':[[0,3500],1,False],
                'age_vadose':[[0,3500],1,False],
                'age_groundwater_storage':[[0,4000],1,False],
                'age_chanS':[[0,3500],1,True],

                'trans_age_canopy_storage':[[0,10],1,False],
                'trans_age_snow_depth':[[0,500],1,False],
                'trans_age_SMC_layer1':[[0,500],1,False],
                'trans_age_SMC_layer2':[[0,1000],1,False],
                'trans_age_SMC_layer3':[[0,3500],1,False],
                'trans_age_vadose':[[0,3500],1,True],
                'trans_age_groundwater_storage':[[0,4000],1,False],
                'trans_age_chanS':[[0,3500],1,True],

                'no3_canopy_storage':[[0,4],1,False],
                'no3_snow_depth':[[0,15],1,False],
                'no3_SMC_layer1':[[0,100],1,False],
                'no3_SMC_layer2':[[0,30],1,False],
                'no3_SMC_layer3':[[0,30],1,False],
                'no3_vadose':[[0,15],1,False],
                'no3_groundwater_storage':[[0,15],1,False],
                'no3_chanS':[[0,10],1,True],
                'nitrogen_addition':[[0,100],10*365,False],
                'plant_uptake':[[0,100],10*365,False],
                'deni_soil':[[0,70],10*365,False],
                'minerl_soil':[[0,70],10*365,False],
                'degrad_soil':[[0,50],10*365,False],
                'deni_river':[[0,0.5],10*365,True],


                
                'young_water_fraction_sm1':[[0,1],1,False],
                'young_water_fraction_vadose':[[0,0.3],1,False],
                'young_water_fraction_chanS':[[0,0.1],1,True],

                'damkholer_num':[[-2,2],1,False],

                'processing_time':[[0, 1e4],1,False],

                }

def IMGtoVideo(save_path, plot_path, output_name):
    import cv2

    video_name = save_path + output_name + '.mp4'

    if os.path.exists(video_name):
        os.remove(video_name)

    images = [img for img in os.listdir(plot_path) if '.png' in img]
    images = sorted(images, key=lambda fname : int(fname.split('.')[0].split('_')[-2]))
    

    frame = cv2.resize(cv2.imread(os.path.join(plot_path, images[0])), (0,0), fx = 0.5, fy = 0.5)
    height, width, layers = frame.shape


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = len(images) / 40
    video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))

    for image in images:
        video.write(cv2.resize(cv2.imread(os.path.join(plot_path, image)), (0,0), fx = 0.5, fy = 0.5))
        #os.remove(os.path.join(plot_path, image))

    print('Video saved at:     ', video_name)
    video.release()
    cv2.destroyAllWindows()


def plot_hydrology(output_path, output_name, spatial_path, catchment_ID=None, if_average=False):
    Vars = ['canopy_storage', 'snow_depth','pond', None, None, None]
    Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage', None])
    Vars.extend(['snowmelt', 'throufall', 'irrigation_from_GW', 'irrigation_from_river', None, None])
    Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose', None])
    Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3', None, None])
    Vars.extend(['canopy_evap', 'soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', 'channel_evaporation'])
    Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
    Vars.extend(['overland_flow_toChn', None, 'interflow_toChn', None, 'GWflow_toChn', 'discharge'])

    ylims = [[0, 5],[0, 20],[0, 5], None, None, None]
    ylims.extend([[0, 0.75],[0, 0.75],[0, 0.75],[0,2e2],[0, 1e4], None])
    ylims.extend([[0, 1e2], [0, 1.3e3], [0, 1e2], [0, 1e2], None, None])
    ylims.extend([[0, 1.3e3],[0, 7e2],[0, 7e2],[0, 3e2], [0,3e2], None])
    ylims.extend([[0, 5e2],[0, 5e2],[0, 5e2],[0, 5e2], [0, 5e2], [0, 5e2]])
    ylims.extend([[0, 3e2],[0, 5e2],[0, 5e2],[0, 2e2],[0, 1e2], [0, 2e1]])
    ylims.extend([[0, 1e3],[0, 1e3],[0, 2e3],[0, 2e3],[0, 4e3],[0, 4e3]])
    ylims.extend([[0, 1e3],[0, 1e3],[0, 2e3],[0, 2e3],[0, 2e3], None])

    #ylims = np.full(len(ylims), None)

    weights = [1e3, 1e3, 1e3, 1e3, 1e3, 1e3]
    weights.extend([1, 1, 1, 1e3, 1e3, 1e3])
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3])  # mm/yr
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3])
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3])
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3])
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3])
    weights.extend([365*1e3, 365*1e3, 365*1e3, 365*1e3, 365*1e3, 1])

    

    nrow = 8
    ncol = 6


    fig, ax = plt.subplots(nrow, ncol, figsize=(30,18), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.99, wspace=0.2, hspace=0.2)

    valid_subplots = 0
    if not if_average:
        for i in range(len(Vars)):
            if Vars[i] == None:
                ax[i//ncol, i%ncol].axis('off')
            else:
                try:
                    catchment_idx = np.where(Output.catchment_to_cali==catchment_ID)[0][0]
                    data = (np.fromfile(output_path + Vars[i] + '_TS.bin').reshape(-1, Output.N_sites[catchment_idx]).T)[:, Info.spin_up:]
                    site_idx = Output.sim['no3']['sim_idx'][catchment_idx][-1]
                    data = data[site_idx,:]
                    data[data==nodata] = np.nan
                    data *= weights[i]
                    ax[i//ncol, i%ncol].plot(data, linewidth=0.3, c='skyblue', zorder=1)

                    
                        
                    title_hgt = 0.9
                    hgt_gradient = 0.11
                    if "discharge" in Vars[i]:
                        obs = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)[site_idx, :]
                        X = np.arange(len(obs))
                        ax[i//ncol, i%ncol].scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
                        ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                        ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=12, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.nanmean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.nanmax(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    valid_subplots += 1
                except Exception as e:
                    ax[i//ncol, i%ncol].axis('off')
        if valid_subplots>2:
            fig.savefig(output_path + output_name + '_Ts.png')
        #print('Plot saved at :  ', output_path + '999_All_in_Ts.png')


        fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.97, top=0.99, wspace=0.01, hspace=0.08)
        valid_subplots = 0
        for i in range(len(Vars)):
            if Vars[i] == None:
                pass
                ax[i//ncol, i%ncol].axis('off')
            else:
                try:
                    chanmask = np.loadtxt(spatial_path + '/chnwidth.asc', skiprows=6)
                    chanmask = chanmask>0
                    mask = np.full(chanmask.shape, np.nan)
                    tmp = np.loadtxt(spatial_path + '/dem.asc', skiprows=6)
                    tmp = tmp>0
                    mask[tmp] = 1 
        
                    data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, mask.shape[0], mask.shape[1]))[2:, :, :] # Skip first two years
                    data[data==nodata] = np.nan
                    data *= weights[i]
                    
                    print(Vars[i], data.shape, np.nanmean(data[:]))  # todo

                    if ('discharge' in Vars[i]) or ('_toChn' in Vars[i]) or ('chanS' in Vars[i]):
                        for kk in range(data.shape[0]):
                            data[kk,:,:][ ~chanmask] = np.nan

                    data = np.nanmean(data, axis=0)
                    data[data==0.0] = np.nan

                    ax[i//ncol, i%ncol].imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
                    if ylims[i] is None:
                        im = ax[i//ncol, i%ncol].imshow(data, cmap='viridis', zorder=1, label='1')
                    else:
                        im = ax[i//ncol, i%ncol].imshow(data, cmap='viridis', vmin=ylims[i][0], vmax=ylims[i][1], zorder=1, label='1')
                    ax[i//ncol, i%ncol].set_frame_on(False)
                    ax[i//ncol, i%ncol].set_xticks([])
                    ax[i//ncol, i%ncol].set_yticks([])

                    tmp = ax[i//ncol, i%ncol].get_position()
        
                    fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%0.2f')
                    #fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%.0e')

                    title_hgt = 1.02
                    hgt_gradient = 0.11
                    
                    ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    valid_subplots += 1
                except Exception as e:
                    pass
                    #ax[i//ncol, i%ncol].axis('off')
        if valid_subplots > 0:
            fig.savefig(output_path + output_name +'_map.png')
            #print('Plot saved at :  ', output_path + output_name +'_Ts.png')


    else:
        chanmask = np.loadtxt(spatial_path + '/chnwidth.asc', skiprows=6)
        ntimestep = (np.fromfile(output_path + Vars[0] + '_map.bin').reshape(-1, chanmask.shape[0], chanmask.shape[1])).shape[0]
        os.makedirs(output_path + 'tmp_plots_for_animation', exist_ok=True)
        for tt in range(ntimestep):
            fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
            plt.subplots_adjust(left=0.05, bottom=0.05, right=0.97, top=0.99, wspace=0.01, hspace=0.08)
            valid_subplots = 0
            for i in range(len(Vars)):
                if Vars[i] == None:
                    pass
                    ax[i//ncol, i%ncol].axis('off')
                else:
                    try:
                        chanmask = np.loadtxt(spatial_path + '/chnwidth.asc', skiprows=6)
                        chanmask = chanmask>0
                        mask = np.full(chanmask.shape, np.nan)
                        tmp = np.loadtxt(spatial_path + '/dem.asc', skiprows=6)
                        tmp = tmp>0
                        mask[tmp] = 1 
                        
                        data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, mask.shape[0], mask.shape[1]))
                        data = data[tt, :, :]
                        data[data==nodata] = np.nan
                        data *= weights[i]
                        data[data==0.0] = np.nan

                        ax[i//ncol, i%ncol].imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
                        if ylims[i] is None:
                            im = ax[i//ncol, i%ncol].imshow(data, cmap='viridis', zorder=1, label='1')
                        else:
                            im = ax[i//ncol, i%ncol].imshow(data, cmap='viridis', vmin=ylims[i][0], vmax=ylims[i][1], zorder=1, label='1')

                        ax[i//ncol, i%ncol].set_frame_on(False)
                        ax[i//ncol, i%ncol].set_xticks([])
                        ax[i//ncol, i%ncol].set_yticks([])

                        tmp = ax[i//ncol, i%ncol].get_position()
            
                        fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%0.2f')
                        #fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%.0e')

                        title_hgt = 1.02
                        hgt_gradient = 0.11
                        
                        ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                        valid_subplots += 1
                    except Exception as e:
                        print(Vars[i], e)
                        ax[i//ncol, i%ncol].axis('off')
                        pass
            if valid_subplots > 0:
                fig.savefig(output_path + 'tmp_plots_for_animation/' + output_name + '_' + str(int(1980+tt)) + '_map.png')
                #print('Plot saved at :  ', output_path + output_name +'_Ts.png')


def plot_tracking(output_path, output_name, spatial_path, catchment_ID=None, if_average=False):
    #Vars = ['d18o_canopy_storage', 'd18o_snow_depth','d18o_pond', None, None, None]
    #Vars.extend(['d18o_SMC_layer1', 'd18o_SMC_layer2', 'd18o_SMC_layer3', 'd18o_vadose', 'd18o_groundwater_storage', 'd18o_chanS'])
    Vars = ['trans_age_canopy_storage', 'trans_age_snow_depth','trans_age_pond', None, None, None]
    Vars.extend(['trans_age_SMC_layer1', 'trans_age_SMC_layer2', 'trans_age_SMC_layer3', 'trans_age_vadose', 'trans_age_groundwater_storage', 'trans_age_chanS'])
    Vars.extend(['age_canopy_storage', 'age_snow_depth','age_pond', None, None, None])
    Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_vadose', 'age_groundwater_storage', 'age_chanS'])
    Vars.extend(['no3_canopy_storage', 'no3_snow_depth','no3_pond', None, None, None])
    Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
    Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])
    Vars.extend([None, None, None, None, None, None])

    print(Vars)

    #ylims = [None, None, None, None, None, None]
    #ylims.extend([[-15,0],[-15,0],[-15,0],None, None,[-10,0]])
    ylims = [None, None, None, None, None, None]
    ylims.extend([None, None, None, None, None, None])
    ylims.extend([None, None, None, None, None, None])
    ylims.extend([None, None, None, None, None, None])
    ylims.extend([None, None, None, None, None, None])
    ylims.extend([[0,15], [0,15], [0,15], [0,15], [0,15], [0,10]])
    ylims.extend([[0,100], [0,100], [0,100], [0,100], [0,100], [0,1]])
    ylims.extend([None, None, None, None, None, None])

    #ylims = np.full(len(ylims), None)

    weights = [1, 1, 1, 1, 1, 1]
    weights.extend([1, 1, 1, 1, 1, 1])
    weights.extend([1, 1, 1, 1, 1, 1])
    weights.extend([1, 1, 1, 1, 1, 1])
    weights.extend([1, 1, 1, 1, 1, 1])
    weights.extend([1, 1, 1, 1, 1, 1])
    weights.extend([10*365, 10*365, 10*365, 10*365, 10*365, 10*365])

    nrow = 8
    ncol = 6


    fig, ax = plt.subplots(nrow, ncol, figsize=(30,18), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.99, wspace=0.2, hspace=0.2)

    site_idx = 3  # Demnitz Millcreek 26

    valid_subplots = 0
    for i in range(len(Vars)):
        if Vars[i] == None:
            ax[i//ncol, i%ncol].axis('off')
        else:
            try:

                catchment_idx = np.where(Output.catchment_to_cali==catchment_ID)[0][0]
                data = (np.fromfile(output_path + Vars[i] + '_TS.bin').reshape(-1, Output.N_sites[catchment_idx]).T)[:, Info.spin_up:]
                site_idx = Output.sim['no3']['sim_idx'][catchment_idx][-1]
                data = data[site_idx,:]
                
                data[data==nodata] = np.nan
                data *= weights[i]

                ax[i//ncol, i%ncol].plot(data, linewidth=0.3, c='skyblue', zorder=1)
                    
                title_hgt = 0.9
                hgt_gradient = 0.11
                if "discharge" in Vars[i]:
                    obs = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)[site_idx, :]
                    X = np.arange(len(obs))
                    ax[i//ncol, i%ncol].scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=12, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.nanmean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.nanmax(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                valid_subplots += 1
            except Exception as e:
                ax[i//ncol, i%ncol].axis('off')
    if valid_subplots > 2:
        fig.savefig(output_path + output_name + '_Ts.png')
    #print('Plot saved at :  ', output_path + '999_All_in_Ts_tracking.png')


    fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.01, hspace=0.08)
    valid_subplots = 0
    for i in range(len(Vars)):
        if Vars[i] == None:
            ax[i//ncol, i%ncol].axis('off')
            pass
        else:
            try:
                chanmask = np.loadtxt(spatial_path + '/chnwidth.asc', skiprows=6)
                chanmask = chanmask>0

                data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, chanmask.shape[0], chanmask.shape[1]))[:, :, :]
                data[data==nodata] = np.nan
                data *= weights[i]
               
                if ('discharge' in Vars[i]) or ('_toChn' in Vars[i]) or ('_chanS' in Vars[i]) or ('river' in Vars[i]):
                    for kk in range(data.shape[0]):
                        data[kk,:,:][ ~chanmask] = np.nan
                if ylims[i] is not None:
                    im = ax[i//ncol, i%ncol].imshow(np.nanmean(data, axis=0), vmin=ylims[i][0], vmax=ylims[i][1], cmap='viridis', zorder=1, label='1')
                else:
                    im = ax[i//ncol, i%ncol].imshow(np.nanmean(data, axis=0), cmap='viridis', zorder=1, label='1')
                ax[i//ncol, i%ncol].set_frame_on(False)
                ax[i//ncol, i%ncol].set_xticks([])
                ax[i//ncol, i%ncol].set_yticks([])

                tmp = ax[i//ncol, i%ncol].get_position()

                fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%0.2f')

                title_hgt = 1.02
                hgt_gradient = 0.11
                
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                valid_subplots += 1
            except Exception as e:
                print(e)
                ax[i//ncol, i%ncol].axis('off')
            
    if valid_subplots > 0:
        fig.savefig(output_path + output_name + '_map.png')

def plot_performance(sim_path, obs_path, output_path, catchment_ID, chainID):

    catchment_idx = np.squeeze(np.argwhere(np.array(Output.Catchment_ID)==catchment_ID))


    nrow = 10
    ncol = 4

    fig, ax = plt.subplots(nrow, ncol, figsize=(12,8), dpi=300)
    tindex = pd.date_range('1980-1-1', '2024-12-31')[Info.spin_up:]

    counter = 0
    
    for key, value in Output.sim.items():
        dict = Output.sim[key]
        sim_idx = dict['sim_idx'][catchment_idx]
        N_sites = Output.N_sites[catchment_idx]
        if len(sim_idx) > 0:
            obs_all = np.fromfile(obs_path+dict['obs_file']).reshape(len(sim_idx), -1)
            sim_all = np.fromfile(sim_path+dict['sim_file']).reshape(-1, N_sites).T

            sim_all = sim_all[:, Info.spin_up:]
            

            for kk in range(len(sim_idx)):

                sim = sim_all[sim_idx[kk],:] + 1e-5
                obs = obs_all[kk, :] + 1e-5

                tmp = np.full(len(sim), np.nan)
                tmp[:len(obs)] = obs

                ax[counter//ncol, counter%ncol].plot(tindex, sim, linewidth=0.5, alpha=0.7)
                ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=0.5, alpha=0.3)

                if key=='no3':
                    ax[counter//ncol, counter%ncol].set_ylim([-0.1,10.1])
                    ax[counter//ncol, counter%ncol].set_yticks([0,2,4,6,8,10])
                
                print(key, kk, np.round(GEM_tools.kge(sim, tmp),2), np.round(GEM_tools.nse(sim, tmp),2), np.round(GEM_tools.rsquare(sim, tmp),2), np.round(GEM_tools.pbias(sim, tmp),2), )

                counter += 1

    fig.savefig(output_path+'performance_'+catchment_ID+'_'+str(chainID)+'.png', transparent=False)

def plot_performance_all(sim_path, obs_path, output_path, catchment_ID, nchains, plot_each_chain=False):

    catchment_idx = np.squeeze(np.argwhere(np.array(Output.Catchment_ID)==catchment_ID))

    nrow = 9
    ncol = 4

    
    tindex = pd.date_range('1980-1-1', '2024-12-31')[Info.spin_up:]

    if plot_each_chain:
        for chainID in range(nchains):
            fig, ax = plt.subplots(nrow, ncol, figsize=(12,8), dpi=300)
            counter = 0
            for key, value in Output.sim.items():
                dict = Output.sim[key]
                N_sites = dict['N_sites'][catchment_idx]
                sim_idx = dict['sim_idx'][catchment_idx]
                if len(sim_idx) > 0:
                    obs_all = np.fromfile(obs_path+dict['obs_file']).reshape(len(sim_idx), -1)
                    sim_all = np.fromfile(sim_path+dict['sim_file']).reshape(nchains, -1, N_sites)
                    sim_all = sim_all[chainID, Info.spin_up:,:]
                    sim_all = sim_all.T           
                    for kk in range(len(sim_idx)):
                        sim = sim_all[sim_idx[kk],:] + 1e-5
                        obs = obs_all[kk, :] + 1e-5

                        tmp = np.full(len(sim), np.nan)
                        tmp[:len(obs)] = obs

                        ax[counter//ncol, counter%ncol].plot(tindex, sim, linewidth=0.5, alpha=0.7)
                        ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=0.5, alpha=0.3)
                        
                        print(key, kk, np.round(GEM_tools.kge(sim, tmp),2), np.round(GEM_tools.kge_modified(sim, tmp),2), np.round(np.log(1-GEM_tools.kge_modified(sim, tmp))*-100))
                        counter += 1
            fig.savefig(output_path+'performance_'+catchment_ID+'_'+str(chainID)+'.png', transparent=False)

    else:
        fig, ax = plt.subplots(nrow, ncol, figsize=(12,8), dpi=300)
        counter = 0
        for key, value in Output.sim.items():
            dict = Output.sim[key]
            N_sites = dict['N_sites'][catchment_idx]
            sim_idx = dict['sim_idx'][catchment_idx]
            if len(sim_idx) > 0:
                obs_all = np.fromfile(obs_path+dict['obs_file']).reshape(len(sim_idx), -1)
                sim_all = np.fromfile(sim_path+dict['sim_file']).reshape(nchains, -1, N_sites)
                sim_all = sim_all[:, Info.spin_up:,:]
                sim_all = np.mean(sim_all, axis=0).T           
                for kk in range(len(sim_idx)):
                    sim = sim_all[sim_idx[kk],:] + 1e-5
                    obs = obs_all[kk, :] + 1e-5

                    tmp = np.full(len(sim), np.nan)
                    tmp[:len(obs)] = obs

                    ax[counter//ncol, counter%ncol].plot(tindex, sim, linewidth=0.5, alpha=0.7)
                    ax[counter//ncol, counter%ncol].scatter(tindex, tmp, c='red', s=0.5, alpha=0.3)

                    if key=='no3':
                        ax[counter//ncol, counter%ncol].set_ylim([-0.1,10.1])
                        ax[counter//ncol, counter%ncol].set_yticks([0,2,4,6,8,10])
                    
                    print(key, kk, np.round(GEM_tools.kge(sim, tmp),2), np.round(GEM_tools.kge_modified(sim, tmp),2), np.round(np.log(1-GEM_tools.kge_modified(sim, tmp))*-100))
                    counter += 1
        fig.savefig(output_path+'performance_'+catchment_ID+'_all_chains.png', transparent=False)


def plot_param_all(param_path, plot_path, nchains, suffix):

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

def plot_SA(catchment_list, plot_path):
    from SA import Morris

    mode = 'SA'
    param_N = GEM_tools.get_param_N(Info, Param)

    mi_all = np.array([])
    sigma_all = np.array([])
    for catchment_ID in catchment_list:
        
        param  = np.fromfile(Path.work_path + mode + '/outputs/SA/' + catchment_ID + '/param.bin').reshape(-1, param_N)
        likeli = np.fromfile(Path.work_path + mode + '/outputs/SA/' + catchment_ID + '/likeli.bin')

        mi, sigma, EE_filtered = Morris.EE_indices(nsample=50, xmins=np.full(param_N, 0.0), xmaxs=np.full(param_N, 1.0), X=param, Y=likeli, design_type='trajectory', filterPercentage=0.1)
        
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
        mi_all = np.append(mi_all, mi)
        sigma_all = np.append(sigma_all, mi)

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
    mi_all[mi_all > 0] = np.log10(mi_all[mi_all > 0])
    mi_all[mi_all==0] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mi_all.reshape(-1, param_N).T, cmap='Oranges', aspect=0.2, vmin=-2, vmax=1.5)
    ax.set_yticks(np.arange(param.shape[1]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig(plot_path + 'Morris_mi.png')

def plot_param():
    param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1).T
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

    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(param, cmap='viridis', aspect=1.3)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param.png')

    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    for i in range(param.shape[0]):
        param[i] = np.sort(param[i])
    ax.imshow(param, cmap='viridis', aspect=1.3)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param_sorted.png')


def plot_param_valid():
    param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1).T
    validIdx = np.loadtxt('/data/scratch/wusongj/paper4/param_good.txt').astype(np.int)
    aspect = 1.3 * len(validIdx) / param.shape[1]

    param = param[:, validIdx]
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

    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(param, cmap='viridis', aspect=aspect)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param_valid.png')

    fig, ax = plt.subplots(1, 1, figsize=(15,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    for i in range(param.shape[0]):
        param[i] = np.sort(param[i])
    ax.imshow(param, cmap='viridis', aspect=aspect)
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param_valid_sorted.png')

def merge_chain_outputs(mode, chainID_list, temp_res, Vars=None):
    if Vars is None:
        Vars = os.listdir(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+str(0) + '/')
    save_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    os.makedirs(save_path, exist_ok=True)
    for var in Vars:
        for xx, chainID in enumerate(chainID_list):
            save_path_chain = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+str(chainID) + '/'
            print(xx, chainID, flush=True)
            if xx==0:
                if var.split('.')[-1] == 'bin':
                    data = np.fromfile(save_path_chain+var)
                elif var.split('.')[-1] == 'asc':
                    data = np.loadtxt(save_path_chain+var, skiprows=6)
            else:
                if var.split('.')[-1] == 'bin':
                    data += np.fromfile(save_path_chain+var)
                elif var.split('.')[-1] == 'asc':
                    data += np.loadtxt(save_path_chain+var, skiprows=6)
            #os.remove(save_path_chain+var)
            print(xx, chainID, data.shape)
        data /= len(chainID_list)

        if var.split('.')[-1] == 'bin':
            data.tofile(save_path+var)
        elif var.split('.')[-1] == 'asc':
            GEM_tools.create_asc(data, save_path+var, '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')

        # Clean directory
        for xx, chainID in enumerate(chainID_list):
            save_path_chain = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+str(chainID) + '/'
            os.remove(save_path_chain+var)

def merge_chain(mode, temp_res, catchment_list, chainID_list, vars, replace=False):
    for xx, catchment_ID in enumerate(catchment_list):
        output_path = Path.work_path + mode +'/outputs/cali/'+temp_res+'/'+str(catchment_ID)+'/'
        for var in vars:
            if os.path.exists((output_path+'all/'+var+'.bin')) and np.logical_not(replace):
                continue
            start_time = time.time()
            for xx, chainID in enumerate(chainID_list):
                if xx==0:
                    data = np.memmap(output_path+str(chainID)+'/'+var+'.bin', dtype=np.float64, mode='r').copy()
                else:
                    data += np.memmap(output_path+str(chainID)+'/'+var+'.bin', dtype=np.float64, mode='r')
            data /= len(chainID_list)
            os.makedirs(output_path+'all/', exist_ok=True)
            data.tofile(output_path+'all/'+var+'.bin')

            for xx, chainID in enumerate(chainID_list):
                os.remove(output_path+str(chainID)+'/'+var+'.bin')

        print(xx, catchment_ID, ' done!', flush=True)



def merge_spatial_results_EU(mode, temp_res, catchment_list, vars, chainID=None, replace=False):

    mask_large = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask_large = mask_large>0

    if chainID is None:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+str(chainID) + '/'

    os.makedirs(save_path, exist_ok=True)
    
    for var in vars:
        try:

            if os.path.exists(save_path+var+'.bin') and np.logical_not(replace):
                print(var, ' of chain ', chainID, 'has been sorted!', flush=True)
                continue

            for xx, catchment_ID in enumerate(catchment_list):
                if chainID is None:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all/'
                else:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/' + str(chainID) + '/'

                if not os.path.exists(output_path):
                    print(catchment_ID, '  NOT FOUND!!', flush=True)
                    continue

                upper_left_coord = (np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/upper_left_coord.txt')).astype(np.int64)
                mask_small = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/dem.asc', skiprows=6)
                mask_small = mask_small!=-9999
                try:
                    data_small = np.fromfile(output_path+'/'+var+'_map.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
                except:  # todo
                    data_small = np.fromfile(output_path+'/'+var+'.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
                
                if xx == 0:
                    data_large = np.full((data_small.shape[0], mask_large.shape[0], mask_large.shape[1]), np.nan)

                data_large = GIS_tools.from_catchment_to_EU(upper_left_coord, mask_small, data_large, data_small)
                
            data_large.tofile(save_path+var+'.bin')
            print(var + '  merged and saved at : ' + save_path+var+'.bin', flush=True)

            """
            for xx, catchment_ID in enumerate(catchment_list):
                if chainID is None:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all/'
                else:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/' + str(chainID) + '/'
                if os.path.exists(output_path+'/'+var+'.bin'):
                    os.remove(output_path+'/'+var+'.bin')
                elif os.path.exists(output_path+'/'+var+'_map.bin'):
                    os.remove(output_path+'/'+var+'_map.bin')
            """
        except Exception as e:
            print(var + '   sorting failed!!', e, flush=True)
        

def get_overall_ET(path):
    data = np.fromfile(path+'soil_evap_map.bin') + np.fromfile(path+'transp_map.bin')
    data.tofile(path+'ET.bin')
    os.remove(path+'soil_evap_map.bin')
    os.remove(path+'transp_map.bin')

def get_overall_storage(path, layer3_depth):
    data =  np.fromfile(path+'snow_depth_map.bin') + \
            np.fromfile(path+'SMC_layer1_map.bin') * 0.2 +  \
            np.fromfile(path+'SMC_layer2_map.bin') * 0.2 +  \
            np.fromfile(path+'SMC_layer3_map.bin') * layer3_depth + \
            np.fromfile(path+'vadose_map.bin')
    data.tofile(path+'unsat_storage.bin')

    #data += np.fromfile(path+'groundwater_storage_map.bin')
    #data.tofile(path+'overall_storage.bin')

    for file in ['SMC_layer1_map.bin','SMC_layer2_map.bin','SMC_layer3_map.bin','vadose_map.bin','groundwater_storage_map.bin']:
        os.remove(path+file)
    


def plot_spatial_results_EU(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):
  

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    for var in vars:

        extension = var.split('.')[-1]
        var = var.split('.')[0]

        if '_map' in var:
            var = var[:-4]        
        
        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'_map.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)

        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        

        if extension=='bin':
            if yearly_flag:
                os.makedirs(Path.work_path+'plots/'+mode+'/yearly/'+var+'/', exist_ok=True)
                if temp_res=='monthly':
                    for mm in range(_data.shape[0]//12):
                        data = np.mean(_data[mm*12 : mm*12+12, :, :], axis=0)
      
                        if var_info[var][2]:
                            data[~chanmask] = np.nan
                        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
                        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
                        sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, zorder=1)
                        # Add colorbar
                        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
                        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
                        cbar.ax.tick_params(labelsize=25)
                        ax.axis('off')
                        fig.savefig(Path.work_path+'plots/'+mode+'/yearly/'+var+'/'+var+'_'+str(1980+mm)+'.png')
                else:
                    
                    for mm in range(_data.shape[0]):
                        data = _data[mm, :, :]
                        if var_info[var][2]:
                            data[~chanmask] = np.nan

                        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
                        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
                        sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, zorder=1)
                        # Add colorbar
                        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
                        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
                        cbar.ax.tick_params(labelsize=25)
                        ax.axis('off')
                        fig.savefig(Path.work_path+'plots/'+mode+'/yearly/'+var+'/'+var+'_'+str(1980+mm)+'.png')
            else:
                if temp_res=='monthly':
                    data = np.mean(_data[24:,:,:], axis=0)
                else:
                    data = np.mean(_data[2:,:,:], axis=0)
                if var_info[var][2]:
                    data[~chanmask] = np.nan
                
                if var=='damkholer_num':
                    data = np.log10(data)
                    cmap = 'coolwarm'
                else:
                    cmap = 'viridis'

                fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
                ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
                sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, zorder=1)
                # Add colorbar
                cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
                cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
                cbar.ax.tick_params(labelsize=25)
                ax.axis('off')

                fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_all.png')



        elif extension=='asc':

            if var_info[var][2]:
                _data[~chanmask] = np.nan

            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(_data, vmin=vmin, vmax=vmax, cmap='viridis', zorder=1)
            # Add colorbar
            cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
            cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
            cbar.ax.tick_params(labelsize=25)
            ax.axis('off')

            fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_all.png')


def plot_TS_results_EU(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    for var in vars:

        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])
        if '_map' in var:
            var = var[:-4]    

        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
           
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'_map.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)


        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        

        if temp_res=='monthly':
            if var_info[var][2]:
                data = np.nanmean(_data[:,chanmask], axis=(1))[24:]
            else:
                data = np.nanmean(_data[:,mask], axis=(1))[24:]
            if var == 'damkholer_num':
                data = np.log10(data)
                vmin, vmax = [1, 4]
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')[24:]
            tindex_label = pd.date_range('1980-1-1', '2024-12-31', freq='M').strftime('%Y-%m')[24:]
        else:
            if var_info[var][2]:
                data = np.nanmean(_data[:,chanmask], axis=(1))[2:]
            else:
                data = np.nanmean(_data[:,mask], axis=(1))[2:]
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')[2:]
            tindex_label = pd.date_range('1980-1-1', '2024-12-31', freq='Y').strftime('%Y-%m')[2:]

        


        df = pd.DataFrame(data, columns=['value'], index=tindex)
        #df.index = pd.to_datetime(df.index)
        df = df.resample('Y').mean()

        

        fig, ax = plt.subplots(1,1, figsize=(5,2), dpi=300)
        ax.plot(tindex, data)
        ax1 = ax.twinx()
        ax1.plot(df.index,df.value, c='red')
        ax.set_ylim(vmin, vmax)
        ax1.set_ylim(vmin, vmax)

        # Add colorbar
        #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
        #cbar.ax.tick_params(labelsize=25)
        #ax.axis('off')

        fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_TS.png')
        print('Figure saved at :   ' + Path.work_path+'plots/'+mode+'/'+var+'_TS.png')

def plot_spatial_TS_trend_results_EU(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1


    for var in vars:

        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])    

        if '_map' in var:
            var = var[:-4]

        if (not replace) and os.path.exists(Path.work_path+'plots/'+mode+'/asc/'+var+'_trend.asc'):
            continue   

        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'_map.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)
        
        

        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]
        

        if var_info[var][2]:
            valid_mask = chanmask
        else:
            valid_mask = mask

        corr = np.full(mask.shape, np.nan)

        # From monthly to yearly
        data = np.array([np.mean(_data[i*12:i*12+12,:,:], axis=0) for i in range(_data.shape[0]//12)])
        data = data[2:,:,:]


        for r in range(mask.shape[0]):
            for c in range(mask.shape[1]):
                if valid_mask[r,c] and np.logical_not(np.isnan(valid_mask[r,c])):
                    result = GEM_tools.mann_kendall_test(data[:,r,c])
                    if result['p'] < 0.05:
                        corr[r,c] = result['tau']
            print(r)
        
        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
        sc0 = ax.imshow(corr, vmin=-0.5, vmax=0.5, cmap='coolwarm', zorder=1)
        # Add colorbar
        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[-0.5,0,0.5])
        cbar.ax.tick_params(labelsize=25)
        ax.axis('off')

        fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_trend.png')


        GEM_tools.create_asc(corr, Path.work_path+'plots/'+mode+'/asc/'+var+'_trend.asc', Path.data_path+'catchment_info/land_mask_3035.asc')

def plot_spatial_TS_trend_results_EU_spearman(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):

    from scipy.stats import spearmanr

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1


    for var in vars:

        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])    

        if '_map' in var:
            var = var[:-4]

        if (not replace) and os.path.exists(Path.work_path+'plots/'+mode+'/asc/'+var+'_trend_spearman.asc'):
            continue   

        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'_map.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)
        
        

        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]
        

        if var_info[var][2]:
            valid_mask = chanmask
        else:
            valid_mask = mask

        corr = np.full(mask.shape, np.nan)

        # From monthly to yearly
        data = np.array([np.mean(_data[i*12:i*12+12,:,:], axis=0) for i in range(_data.shape[0]//12)])
        data = data[2:,:,:]

        time = np.arange(data.shape[0])


        for r in range(mask.shape[0]):
            for c in range(mask.shape[1]):
                if valid_mask[r,c] and np.logical_not(np.isnan(valid_mask[r,c])):
                    ts = data[:,r,c]
                    if np.all(np.isnan(ts)):
                        continue
                    rho, p = spearmanr(time, ts, nan_policy='omit')
                    if p < 0.05:
                        corr[r,c] = rho
            print(r)
        
        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
        sc0 = ax.imshow(corr, vmin=-0.5, vmax=0.5, cmap='coolwarm', zorder=1)
        # Add colorbar
        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[-0.5,0,0.5])
        cbar.ax.tick_params(labelsize=25)
        ax.axis('off')

        fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_trend_spearman.png')


        GEM_tools.create_asc(corr, Path.work_path+'plots/'+mode+'/asc/'+var+'_trend_spearman.asc', Path.data_path+'catchment_info/land_mask_3035.asc')



def get_avg_depth():
    param_N = GEM_tools.get_param_N(Info, Param)
    depth_param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(-1, param_N)[:,0]
    param_min = Param.ref['depth3']['min'][0]
    param_max = Param.ref['depth3']['max'][0]

    avg_depth = param_min + np.mean(depth_param) * (param_max - param_min)
    
    return avg_depth

    


def calculate_monthly_Damkohler(mode, temp_res):

    # (no3 * sm * depth) / soil deni
    #  Tavel time
    
    depth3 = get_avg_depth()
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(tmp.shape, np.nan)
    mask[tmp>0] = 1
    
    no3_storage =   read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/no3_SMC_layer3_map.bin', mask) * \
                    read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/SMC_layer3_map.bin', mask) * \
                    depth3
    soil_deni =     read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/deni_soil_map.bin', mask)

    travel_time =   read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/age_SMC_layer3_map.bin', mask) # travel time needed
    
    soil_deni_thres = 1 / 10 / 365 # Minimal cap set as 1 kg/hayr
    soil_deni[soil_deni < soil_deni_thres] = soil_deni_thres

    processing_time = no3_storage/soil_deni

    damkholer_num = travel_time / processing_time

    #processing_time.tofile(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/processing_time.bin')
    damkholer_num.tofile(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/damkholer_num.bin')



def read_outputs(file_path, mask=None, dtype=np.float64):

    if file_path.split('.')[-1]=='bin':
        data = np.fromfile(file_path, dtype=dtype).reshape(-1, mask.shape[0], mask.shape[1])
    elif file_path.split('.')[-1]=='asc':
        data = np.loadtxt(file_path, skiprows=6)
    return data


def merge_performance_EU(mode, catchment_list, chainID=None, chainID_list=None, temp_res='yearly'):
    import pickle

    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    os.makedirs(Path.work_path + mode +'/outputs/cali_merged/performance/', exist_ok=True)

    #for kk in range(len(vars)):
    for kk in range(1):
        site_info = pd.read_csv(Path.data_path+'catchment_info/site_info_'+vars[kk]+'.csv', index_col='site')
        KGEs = []
        pbias = []
        site_ids = []
        site_r = []
        site_c = []
        lats = []
        lons = []
        df = pd.DataFrame([])

        for xx, catchment_ID in enumerate(catchment_list):

            print(xx)  # todo
             
            obs_path = Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/obs/'
            keys = pickle.load(open(obs_path+vars[kk]+'_gauge_list', 'rb'))
            sites = pickle.load(open(obs_path+vars[kk]+'_site_list', 'rb'))
            
            if len(keys) > 0:
                if chainID is None:
                    for xx, chainID_tmp in enumerate(chainID_list):
                        save_path = Path.work_path + mode +'/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/' + str(chainID_tmp) + '/'
                        if xx == 0:
                            _sim = np.fromfile(save_path+sim_vars[kk]+'.bin')
                        else:
                            _sim += np.fromfile(save_path+sim_vars[kk]+'.bin')
                    _sim = (_sim.reshape(16437, -1).T)[:, Info.spin_up:] / len(chainID_list)
                    
                        
                else:
                    save_path = Path.work_path + mode +'/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/' + str(chainID_tmp) + '/'
                    _sim = (np.fromfile(save_path+sim_vars[kk]+'.bin').reshape(16437, -1).T)[:, Info.spin_up:]


                _obs = np.fromfile(obs_path+obs_vars[kk]+'_obs.bin').reshape(len(keys), -1)
                _sim += 0.1
                _obs += 0.1
                for i in range(len(keys)):
                    try:
                        idx_row_tmp = site_info.loc[sites[i],:]['idx_row']
                        idx_col_tmp = site_info.loc[sites[i],:]['idx_col']
                        latitude_tmp = site_info.loc[sites[i],:]['latitude']
                        longitude_tmp = site_info.loc[sites[i],:]['longitude']
                        kge_tmp = GEM_tools.kge(_sim[keys[i],:], _obs[i,:])
                        pbias_tmp = GEM_tools.pbias(_sim[keys[i],:], _obs[i,:])
                        site_r.append(idx_row_tmp)
                        site_c.append(idx_col_tmp)
                        lats.append(latitude_tmp)
                        lons.append(longitude_tmp)
                        KGEs.append(kge_tmp)
                        pbias.append(pbias_tmp)
                        site_ids.append(sites[i])
                        #print(keys, i, _sim.shape, _obs.shape)
                    except:
                        print(sites[i], '  went wrong!')
        print(len(site_r), len(site_c), len(lats), len(lons), len(KGEs), len(pbias), len(site_ids))

        df['site'] = site_ids
        df['site_r'] = site_r
        df['site_c'] = site_c
        df['latitude'] = lats
        df['longitude'] = lons
        df['kge'] = KGEs
        df['pbias'] = pbias
        df.set_index(df['site'], drop=True)
        if chainID is None:
            df.to_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_all.csv')
        else:
            df.to_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_'+str(chainID)+'.csv')


def plot_performance_EU(mode, chainID=None):
    vars = ['discharge', 'isotope', 'nitrate']
    scatter_size = [120, 400, 280]
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, np.nan)
    chanmask[tmp>0] = 1
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1
    for kk in range(len(vars)):
        if chainID is None:
            df = pd.read_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_all.csv')
        else:
            df = pd.read_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_'+str(chainID)+'.csv')
        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0)
        #ax.imshow(chanmask, cmap='bone', alpha=0.1, zorder=1)

        # todo
        valid_idx = np.where(df['kge']>0)[0]
        
        sc0 = ax.scatter(x=df['site_c'][valid_idx], y=df['site_r'][valid_idx], c=df['kge'][valid_idx], s=scatter_size[kk], vmin=0, vmax=0.5, alpha=0.7, cmap='coolwarm_r', zorder=2)
        # Add colorbar
        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[0.0, 0.25, 0.5])
        cbar.ax.tick_params(labelsize=25)
        #cbar.set_label('KGE', fontsize=25)
        ax.axis('off')
        if chainID is None:
            fig.savefig(Path.work_path+'plots/'+mode+'/performance_'+vars[kk]+'_all.png')
        else:
            fig.savefig(Path.work_path+'plots/'+mode+'/performance_'+vars[kk]+'_'+str(chainID)+'.png')





def sort_grid_cells_d8(flow_dir, mask=None):
    """
    Sorts grid cells based on a D8 flow direction array from upstream to downstream,
    and identifies upstream cells that directly route to each grid.
    
    Parameters:
    - flow_dir: 2D numpy array of D8 flow directions (1-8, or 0 for no flow/sink)
    - mask: Optional 2D boolean numpy array, True for valid cells to process
    
    Returns:
    - sorted_cells: List of (row, col) tuples in topologically sorted order (upstream to downstream)
    - upstream: Dictionary mapping (row, col) to list of upstream (row, col) tuples
    """
    import numpy as np
    
    # Get grid dimensions
    rows, cols = flow_dir.shape
    
    # Define D8 direction offsets (1:NE, 2:E, 3:SE, 4:S, 5:SW, 6:W, 7:NW, 8:N)
    directions = {
    1:  (0, 1),    # East
    2:  (1, 1),    # Southeast
    4:  (1, 0),    # South
    8:  (1, -1),   # Southwest
    16: (0, -1),   # West
    32: (-1, -1),  # Northwest
    64: (-1, 0),   # North
    128: (-1, 1)   # Northeast
    }
    
    # Create mask if not provided
    if mask is None:
        mask = np.ones_like(flow_dir, dtype=bool)
    
    # Initialize data structures
    upstream = {}
    in_degree = {}  # Number of upstream cells for each cell
    sorted_cells = []
    outlets = []
    
    # Initialize upstream and in-degree counts
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c]:
                continue
            cell = (r, c)
            upstream[cell] = []
            in_degree[cell] = 0
    
    # Build upstream relationships and count in-degrees (upstream cells)
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c] or flow_dir[r, c] == 0:
                continue
            cell = (r, c)
            dir_val = flow_dir[r, c]
            if dir_val in directions:
                dr, dc = directions[dir_val]
                down_r, down_c = r + dr, c + dc
                if 0 <= down_r < rows and 0 <= down_c < cols and mask[down_r, down_c]:
                    downstream = (down_r, down_c)
                    upstream[downstream].append(cell)
                    in_degree[downstream] = in_degree.get(downstream, 0) + 1
    
    # Identify outlets (cells with no downstream flow or flow_dir = 0)
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c]:
                continue
            cell = (r, c)
            if np.logical_not(flow_dir[r, c] in directions):
                outlets.append(cell)
            elif flow_dir[r, c] in directions:
                dr, dc = directions[flow_dir[r, c]]
                down_r, down_c = r + dr, c + dc
                if not (0 <= down_r < rows and 0 <= down_c < cols and mask[down_r, down_c]):
                    outlets.append(cell)

    # Initialize queue with cells that have no upstream cells (sources)
    queue = [(r, c) for r in range(rows) for c in range(cols) 
             if mask[r, c] and in_degree.get((r, c), 0) == 0 and (r, c) not in outlets]


    # Topological sort (upstream to downstream)
    visited = set()
    while queue:
        cell = queue.pop(0)
        if cell in visited:
            continue
        sorted_cells.append(cell)
        visited.add(cell)
        
        # Process downstream cell
        r, c = cell
        if flow_dir[r, c] != 0 and flow_dir[r, c] in directions:
            dr, dc = directions[flow_dir[r, c]]
            down_r, down_c = r + dr, c + dc
            if 0 <= down_r < rows and 0 <= down_c < cols and mask[down_r, down_c]:
                downstream = (down_r, down_c)
                if downstream not in outlets:
                    in_degree[downstream] -= 1
                    if in_degree[downstream] == 0 and downstream not in visited:
                        queue.append(downstream)
    
    # Append outlets last
    sorted_cells.extend(outlets)
    
    # Check for cycles
    #unvisited = [(r, c) for r in range(rows) for c in range(cols) 
    #             if mask[r, c] and (r, c) not in visited and (r, c) not in outlets]
    #if unvisited:
    #    print(f"Warning: Possible cycles detected in cells: {unvisited}")
    return sorted_cells, upstream


def Advance_age_distribution(S):
    S[:,:,-2] += S[:,:,-1]
    S[:,:,1:] = S[:,:,:-1]
    S[:,:,0] = 0.0
    return S

def Mix_age_distribution(S, storage, S_in, influx):
    if (storage + influx) > 0:
        S = S * storage + S_in * influx
        S /= np.sum(S)
    return S

def yound_water_fraction(catchment_ID, young_water_thres):
    output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+str(catchment_ID)+'/all/'
    fdir = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/fdir.asc', skiprows=6).astype(np.int64)
    mask = np.full(fdir.shape, False)
    mask[fdir!=-9999] = True

    depth3 = get_avg_depth()
    

    sm1 = np.fromfile(output_path+'SMC_layer1_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    sm2 = np.fromfile(output_path+'SMC_layer2_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    sm3 = np.fromfile(output_path+'SMC_layer3_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    vadose = np.fromfile(output_path+'vadose_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    chanS = np.fromfile(output_path+'channel_storage_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    

    inftr = np.fromfile(output_path+'infiltration_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc1 = np.fromfile(output_path+'perc_layer1_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc2 = np.fromfile(output_path+'perc_layer2_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc3 = np.fromfile(output_path+'perc_layer3_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    interf_out = np.fromfile(output_path+'interflow_output_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    interf_toChn = np.fromfile(output_path+'interflow_toChn_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    GWf_toChn = np.fromfile(output_path+'GWflow_toChn_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    discharge = np.fromfile(output_path+'discharge_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31 * 86400 / (5000*5000)

    irrigation_GW = np.fromfile(output_path+'irrigation_from_GW_map.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31

    
    T_total = inftr.shape[-1]
    sorted_cells, inflow_map = sort_grid_cells_d8(fdir, mask)



    S_sm1 = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_sm2 = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_sm3 = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_vadose = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_GW = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_chanS = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)

    S_chanS_dry = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_chanS_wet = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_vadose_dry = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)
    S_vadose_wet = np.zeros((mask.shape[0], mask.shape[1],60))   # age distribution (monthly up to 5 years)

    

    S_sm1[:,:,0] = 1.0
    S_sm2[:,:,0] = 1.0
    S_sm3[:,:,0] = 1.0
    S_vadose[:,:,0] = 1.0
    S_GW[:,:,-1] = 1.0 # GW constantly older than 5 years
    S_chanS[:,:,0] = 1.0

    
    
    YF_sm1 = np.zeros((mask.shape[0], mask.shape[1],T_total))
    YF_sm2 = np.zeros((mask.shape[0], mask.shape[1],T_total))
    YF_sm3 = np.zeros((mask.shape[0], mask.shape[1],T_total))
    YF_vadose = np.zeros((mask.shape[0], mask.shape[1],T_total))
    YF_chanS =  np.zeros((mask.shape[0], mask.shape[1],T_total))


    #for t in range(24,60):
    for t in range(T_total):
        for i in range(len(sorted_cells)):
            r, c = sorted_cells[i]

            # === Soil layer 1 ===
            S_sm1[r,c] = Mix_age_distribution(S_sm1[r,c], sm1[r,c,t]*0.2, np.append(np.array([1]), np.zeros(59)), inftr[r,c,t])
            S_sm1[r,c] = Mix_age_distribution(S_sm1[r,c], sm1[r,c,t]*0.2, S_GW[r,c], irrigation_GW[r,c,t])
            YF_sm1[r,c,t] = np.sum(S_sm1[r,c,:young_water_thres]) / np.sum(S_sm1[r,c])

            # === Soil layer 2 ===
            S_sm2[r,c] = Mix_age_distribution(S_sm2[r,c], sm2[r,c,t]*0.2, S_sm1[r,c], perc1[r,c,t])
            YF_sm2[r,c,t] = np.sum(S_sm2[r,c,:young_water_thres]) / np.sum(S_sm2[r,c])

            # === Soil layer 3 ===
            S_sm3[r,c] = Mix_age_distribution(S_sm3[r,c], sm3[r,c,t]*depth3, S_sm2[r,c], perc2[r,c,t])
            YF_sm3[r,c,t] = np.sum(S_sm3[r,c,:young_water_thres]) / np.sum(S_sm3[r,c])


            # === Vadose zone ===
            S_vadose[r,c] = Mix_age_distribution(S_vadose[r,c], vadose[r,c,t], S_sm3[r,c], perc3[r,c,t])
            #vadose[r,c,t] += perc3[r,c,t]
            for kk in range(len(inflow_map[r,c])):
                dr, dc = inflow_map[r,c][kk]
                S_vadose[r,c] = Mix_age_distribution(S_vadose[r,c], vadose[r,c,t], S_vadose[dr,dc], interf_out[dr,dc,t])
                vadose[r,c,t] += interf_out[dr,dc,t]
            if vadose[r,c,t]==0:
                YF_vadose[r,c,t] = 0
            else:
                YF_vadose[r,c,t] = np.sum(S_vadose[r,c,:young_water_thres]) / np.sum(S_vadose[r,c])

            
            # === Channel storage ===
            S_chanS[r,c] = Mix_age_distribution(S_chanS[r,c], chanS[r,c,t], S_vadose[r,c], interf_toChn[r,c,t])
            S_chanS[r,c] = Mix_age_distribution(S_chanS[r,c], chanS[r,c,t], S_GW[r,c], GWf_toChn[r,c,t])
            for kk in range(len(inflow_map[r,c])):
                dr, dc = inflow_map[r,c][kk]
                if discharge[dr,dc,t] > 0:
                    S_chanS[r,c] = Mix_age_distribution(S_chanS[r,c], chanS[r,c,t], S_chanS[dr,dc], discharge[dr,dc,t])
                    chanS[r,c,t] += discharge[dr,dc,t]
                
            if chanS[r,c,t]==0:
                YF_chanS[r,c,t] = 0
            else:
                YF_chanS[r,c,t] = np.sum(S_chanS[r,c,:young_water_thres]) / np.sum(S_chanS[r,c])
            

        if np.logical_or(t%12>4, t%12<8):  # June (5), July (6), Aug (7)
            S_chanS_dry += S_chanS
            S_vadose_dry += S_vadose
        if np.logical_or(t%12<2, t%12>1000): # Dec (11), Jan (0), Feb (1)
            S_chanS_wet += S_chanS
            S_vadose_wet += S_vadose

        # Aging
        Advance_age_distribution(S_sm1)
        Advance_age_distribution(S_sm2)
        Advance_age_distribution(S_sm3)
        Advance_age_distribution(S_vadose)
        #Advance_age_distribution(S_GW)
        Advance_age_distribution(S_chanS)


    for i in range(len(sorted_cells)):
        r, c = sorted_cells[i]
        S_chanS_dry[r,c] /= np.sum(S_chanS_dry[r,c])
        S_chanS_wet[r,c] /= np.sum(S_chanS_wet[r,c])
        S_vadose_dry[r,c] /= np.sum(S_chanS_dry[r,c])
        S_vadose_wet[r,c] /= np.sum(S_chanS_wet[r,c])

    S_chanS_dry = S_chanS_dry.transpose(2,0,1)
    S_chanS_wet = S_chanS_wet.transpose(2,0,1)
    S_vadose_dry = S_vadose_dry.transpose(2,0,1)
    S_vadose_wet = S_vadose_wet.transpose(2,0,1)
    YF_sm1 = YF_sm1.transpose(2,0,1)
    YF_sm2 = YF_sm2.transpose(2,0,1)
    YF_sm3 = YF_sm3.transpose(2,0,1)
    YF_vadose = YF_vadose.transpose(2,0,1)
    YF_chanS = YF_chanS.transpose(2,0,1)

    S_chanS_dry.tofile(output_path+'age_pdf_chanS_dry_map.bin')
    S_chanS_wet.tofile(output_path+'age_pdf_chanS_wet_map.bin')
    S_vadose_dry.tofile(output_path+'age_pdf_vadose_dry_map.bin')
    S_vadose_wet.tofile(output_path+'age_pdf_vadose_wet_map.bin')
    YF_sm1.tofile(output_path+'young_water_fraction_sm1_map.bin')
    YF_vadose.tofile(output_path+'young_water_fraction_vadose_map.bin')
    YF_chanS.tofile(output_path+'young_water_fraction_chanS_map.bin')

    print(catchment_ID, '  done!', flush=True)

       
    fig, ax = plt.subplots(2,3, dpi=300)
    ax[0,0].imshow(np.mean(YF_sm1[:,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,1].imshow(np.mean(YF_sm2[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,2].imshow(np.mean(YF_sm3[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[1,0].imshow(np.mean(YF_vadose, axis=0), vmin=0, vmax=1)
    #ax[1,1].imshow(np.mean(YF_chanS, axis=0), vmin=0, vmax=0.3)
    #ax[1,2].imshow(np.mean(discharge, axis=2))
    #ax[1,2].plot(np.nanmean(S_vadose_dry.transpose(1,2,0)[mask], axis=0))
    #ax[1,2].plot(np.nanmean(S_vadose_wet.transpose(1,2,0)[mask], axis=0))


    fig.savefig('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/run_model/zzz.png')
    