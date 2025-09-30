import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path, Info, Cali, Param, Output
import GEM_tools
import pandas as pd
import GIS_tools
import time
from collections import deque, defaultdict
from matplotlib.colors import LinearSegmentedColormap



def get_cmcrameri_cmap(cmap, start=0, end=1, alpha=1):
    cmap_path = '/home/wusongj/dependecies/cmaps_cmcrameri-1.9/'
    rgb = np.loadtxt(cmap_path + cmap + '.txt')  # shape (N, 3)
    start = int(start * rgb.shape[0])
    end = int(end * rgb.shape[0])
    rgb = rgb[start:end,:]
    rgba = np.column_stack([rgb, np.full((rgb.shape[0],), alpha)])
    custom_cmap = LinearSegmentedColormap.from_list("my_cmap", rgba)
    return custom_cmap

nodata = Info.nodata

colors_with_positions = [
        (0.0, "#7EA6D9"),   # Start
        (0.25, "#D4E6BC"),
        (0.5, "#f8f2a4"),
        (1.0, "#edc3a5")     # End
    ]
custom_cmap = LinearSegmentedColormap.from_list("my_cmap", colors_with_positions)

colors_with_positions = [
        (0.0, "#5894E2"),   # Start
        (0.25, "#8CC048"),
        (0.75, "#fdaa0e"),
        (1.0, "#fa7d56")     # End
    ]
custom_cmap_1 = LinearSegmentedColormap.from_list("my_cmap", colors_with_positions)

colors_with_positions = [
        (0.0, "#5592E2"),   # Start
        (0.33, "#7BB72C"),
        (0.66, "#e9ac05"),
        (1.0, "#ef6e47")     # End
    ]
custom_cmap_2 = LinearSegmentedColormap.from_list("my_cmap", colors_with_positions)

colors_with_positions = [
        (0.0, "#7EA6D9"),   # Start
        (0.33, "#D2E1AAE4"),
        (0.66, "#f4eea0"),
        (1.0, "#e87856")     # End
    ]
custom_cmap_3 = LinearSegmentedColormap.from_list("my_cmap", colors_with_positions)

var_info = {
                'Precipitation_npfloat32':[[0,1200],1000*365,False, 400],
                'Potential_evapotranspiration_npfloat32':[[0,1200],1000*365,False, 400],
                'Mean_air_temperature_npfloat32':[[-5,25],1,False, 8],
                'Surface_net_radiation_npfloat32':[[-100,600],1,False, 15],

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
                'rperc_vadose':[[0,500],1000*365,False],
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
                'age_soil_all_depths':[[0,3000],1,False],
                'age_vadose':[[0,3500],1,False],
                'age_groundwater_storage':[[0,4000],1,False],
                'age_chanS':[[0,3500],1,True],

                'trans_age_canopy_storage':[[0,10],1,False],
                'trans_age_snow_depth':[[0,500],1,False],
                'trans_age_SMC_layer1':[[0,500],1,False],
                'trans_age_SMC_layer2':[[0,1000],1,False],
                'trans_age_SMC_layer3':[[0,3500],1,False],
                'trans_age_soil_all_depths':[[0,3000],1,False],
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
                'nitrogen_addition':[[0,180],10*365,False, 15],
                'plant_uptake':[[0,100],10*365,False, 15],
                'deni_soil':[[0,40],10*365,False, 15],
                
                'minerl_soil':[[0,70],10*365,False, 15],
                'degrad_soil':[[0,50],10*365,False, 15],
                'deni_river':[[0,0.5],10*365,True],

                'nitrogen_storage':[[0,80],10,False, 10],
                'nitrogen_input':[[0,200],10*365,False, 15],
                'nitrogen_uptake':[[0,100],10*365,False, 15],
                'nitrogen_leaching':[[0,100],10*365,False, 15],
                'wet_deposition':[[0,40],10*365,False],
                'nitrogen_surplus':[[-20,20],10*365,False],


                
                'young_water_fraction_sm1':[[0,100],100,False],
                'young_water_fraction_sm2':[[0,100],100,False],
                'young_water_fraction_sm3':[[0,100],100,False],
                'young_water_fraction_soil_all_depths':[[5,30],100,False, 5],
                'young_water_fraction_vadose':[[0,40],100,False],
                'young_water_fraction_chanS':[[0,10],100,True],

                'damkholer_num':[[-1, 1],1,False, [-2,2]],

                'processing_time':[[0, 1e4],1,False, [1,3]],

                'interflow_length':[[0, 1],1,False],


                'Evapotranspiration':[[200,700],1000*365,False],
                'Evapotranspiration_fraction':[[30,100],100,False],

                'trans_age_SMC_soil_all_depths':[[0,3500],1,False, [1,3]],
                'age_SMC_soil_all_depths':[[0,3500],1,False],

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
        
                    data = (np.fromfile(output_path + Vars[i] + '.bin').reshape(-1, mask.shape[0], mask.shape[1]))[2:, :, :] # Skip first two years
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
            fig.savefig(output_path + output_name +'.png')
            #print('Plot saved at :  ', output_path + output_name +'_Ts.png')


    else:
        chanmask = np.loadtxt(spatial_path + '/chnwidth.asc', skiprows=6)
        ntimestep = (np.fromfile(output_path + Vars[0] + '.bin').reshape(-1, chanmask.shape[0], chanmask.shape[1])).shape[0]
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
                        
                        data = (np.fromfile(output_path + Vars[i] + '.bin').reshape(-1, mask.shape[0], mask.shape[1]))
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
                fig.savefig(output_path + 'tmp_plots_for_animation/' + output_name + '_' + str(int(1980+tt)) + '.png')
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

                data = (np.fromfile(output_path + Vars[i] + '.bin').reshape(-1, chanmask.shape[0], chanmask.shape[1]))[:, :, :]
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
        fig.savefig(output_path + output_name + '.png')

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
    for yy, catchment_ID in enumerate(catchment_list):
        
        output_path = Path.work_path + mode +'/outputs/cali/'+temp_res+'/'+str(catchment_ID)+'/'

        fail_flag = False
              
        for var in vars:
            try:
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

            
            except Exception as e:
                fail_flag = True
                print(xx, catchment_ID, var, ' FAILED!!!!!!!!!!!!!', flush=True)
                print(e)

        if not fail_flag:
            print(yy, catchment_ID, ' done!', flush=True)  


def merge_spatial_results_EU_debug(mode, temp_res, catchment_list, vars, chainID=None, replace=False, experiment=None):

    mask_large = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask_large = mask_large>0

    if experiment is None:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'

    os.makedirs(save_path, exist_ok=True)
    
    for var in vars:
        try:

            if os.path.exists(save_path+var+'.bin') and np.logical_not(replace):
                print(var, ' of chain ', chainID, 'has been sorted!', flush=True)
                continue

            for xx, catchment_ID in enumerate(catchment_list):
                if experiment is None:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all/'
                else:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all_'+experiment+'/'

                if not os.path.exists(output_path):
                    print(catchment_ID, '  NOT FOUND!!', flush=True)
                    continue

                upper_left_coord = (np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/upper_left_coord.txt')).astype(np.int64)
                mask_small = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/dem.asc', skiprows=6)
                mask_small = mask_small!=-9999
                try:
                    data_small = np.fromfile(output_path+'/'+var+'_map.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
            
                    print(data_small.shape, data_small[538:543,5,5])
                    
                    if os.path.exists(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt'):
                        finish_counter = np.loadtxt(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt')
                    else:
                        finish_counter = 1
                except:  # todo
                    data_small = np.fromfile(output_path+'/'+var+'.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
                    if os.path.exists(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt'):
                        finish_counter = np.loadtxt(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt')
                    else:
                        finish_counter = 1
                
                data_small /= int(finish_counter)                

        except Exception as e:
            print(catchment_ID, var + '   sorting failed!!', e, flush=True)

def merge_spatial_results_EU(mode, temp_res, catchment_list, vars, chainID=None, replace=False, experiment=None):

    mask_large = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask_large = mask_large>0

    if experiment is None:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        save_path  = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'

    os.makedirs(save_path, exist_ok=True)
    
    for var in vars:
        try:

            if os.path.exists(save_path+var+'.bin') and np.logical_not(replace):
                print(var, ' of chain ', chainID, 'has been sorted!', flush=True)
                continue

            for xx, catchment_ID in enumerate(catchment_list):
                if experiment is None:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all/'
                else:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all_'+experiment+'/'

                if not os.path.exists(output_path):
                    print(catchment_ID, '  NOT FOUND!!', flush=True)
                    continue

                upper_left_coord = (np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/upper_left_coord.txt')).astype(np.int64)
                mask_small = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/dem.asc', skiprows=6)
                mask_small = mask_small!=-9999
                try:
                    data_small = np.fromfile(output_path+'/'+var+'_map.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
                    if os.path.exists(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt'):
                        finish_counter = np.loadtxt(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt')
                    else:
                        finish_counter = 1
                except:  # todo
                    data_small = np.fromfile(output_path+'/'+var+'.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
                    if os.path.exists(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt'):
                        finish_counter = np.loadtxt(output_path+'/finish_counter/finish_counter_'+var+'_map.bin.txt')
                    else:
                        finish_counter = 1
                
                data_small /= int(finish_counter)                
                
                if xx == 0:
                    data_large = np.full((data_small.shape[0], mask_large.shape[0], mask_large.shape[1]), np.nan)

                data_large = GIS_tools.from_catchment_to_EU(upper_left_coord, mask_small, data_large, data_small)
                
            data_large.tofile(save_path+var+'.bin')
            print(var + '  merged and saved at : ' + save_path+var+'.bin', flush=True)


            """
            for xx, catchment_ID in enumerate(catchment_list):
                if experiment is None:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all/'
                else:
                    output_path = Path.work_path + mode +'/outputs/cali/' +temp_res+ '/' + str(catchment_ID) + '/all_'+experiment+'/'
                if os.path.exists(output_path+'/'+var+'.bin'):
                    os.remove(output_path+'/'+var+'.bin')
                elif os.path.exists(output_path+'/'+var+'_map.bin'):
                    os.remove(output_path+'/'+var+'_map.bin')
            """

        except Exception as e:
            print(catchment_ID, var + '   sorting failed!!', e, flush=True)
        

def get_overall_ET(path):
    data = np.fromfile(path+'soil_evap.bin') + np.fromfile(path+'transp.bin')
    data.tofile(path+'ET.bin')
    os.remove(path+'soil_evap.bin')
    os.remove(path+'transp.bin')

def get_overall_storage(path, layer3_depth):
    data =  np.fromfile(path+'snow_depth.bin') + \
            np.fromfile(path+'SMC_layer1.bin') * 0.2 +  \
            np.fromfile(path+'SMC_layer2.bin') * 0.2 +  \
            np.fromfile(path+'SMC_layer3.bin') * layer3_depth + \
            np.fromfile(path+'vadose.bin')
    data.tofile(path+'unsat_storage.bin')

    #data += np.fromfile(path+'groundwater_storage.bin')
    #data.tofile(path+'overall_storage.bin')

    for file in ['SMC_layer1.bin','SMC_layer2.bin','SMC_layer3.bin','vadose.bin','groundwater_storage.bin']:
        os.remove(path+file)
    


def sort_dominant_factor(mode):
  
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

  

    precip_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/Precipitation_npfloat32_3035_diff.asc', skiprows=6)
    pet_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/Potential_evapotranspiration_npfloat32_3035_diff.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff.asc', skiprows=6)
    damkohler_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/damkholer_num_diff.asc', skiprows=6)
    addition_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_addition_diff.asc', skiprows=6)
    storage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_storage_diff.asc', skiprows=6)
    

    data = np.full(pet_diff.shape, 3.0)
    #data [((precip_diff>0)&(tranage_diff<0)) | ((precip_diff<0)&(tranage_diff>0))] = 1
    data [((precip_diff>0)&(ywf_diff>0)) | ((precip_diff<0)&(ywf_diff<0))] = 1
    data [(((pet_diff<0)&(tranage_diff<0)) | ((pet_diff>0)&(tranage_diff>0))) & (data!=1)] = 2
    data[mask!=1] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, vmin=1, vmax=3, cmap=custom_cmap, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')

    fig.savefig(Path.work_path+'plots/'+mode+'/dominant_factor_ywf.png', transparent=True)

    n_valid = np.sum(mask==1)
    for i in [1,2,3]:
        n_factor = np.sum(data==i)
        print(n_factor / n_valid)
    print('')




    #data = np.full(precip_diff.shape, 1.0)
    #data [((addition_diff>0)&(storage_diff>0)) | ((addition_diff<0)&(storage_diff<0))] = 2

    data = np.full(precip_diff.shape, 2.0)
    data[((addition_diff>0)&(storage_diff>0)) | ((addition_diff<0)&(storage_diff<0))] = 1

    data[mask!=1] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, vmin=1, vmax=2, cmap=custom_cmap, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')

    fig.savefig(Path.work_path+'plots/'+mode+'/dominant_factor_nitrogen_storage.png', transparent=True)

    n_valid = np.sum(mask==1)
    for i in [1,2]:
        n_factor = np.sum(data==i)
        print(n_factor / n_valid)

def plot_risky_region(mode):
  
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

  

    #precip_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/Precipitation_npfloat32_3035_diff.asc', skiprows=6)
    #pet_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/Potential_evapotranspiration_npfloat32_3035_diff.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    #tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff.asc', skiprows=6)
    damkohler_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/damkholer_num_diff.asc', skiprows=6)
    #addition_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_addition_diff.asc', skiprows=6)
    storage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_storage_diff.asc', skiprows=6)
    no3_layer3 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/no3_SMC_layer3.bin').reshape(-1, ywf_diff.shape[0], ywf_diff.shape[1])
    no3_layer3 = np.mean(no3_layer3[24:,:,:], axis=0)
    


    data = np.full(ywf_diff.shape, 0.0)
    data[(ywf_diff<0)] = 1

    data[mask!=1] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, cmap=custom_cmap_1, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    fig.savefig(Path.work_path+'plots/'+mode+'/risky_region_hydrology.png', transparent=True)

    data = np.full(ywf_diff.shape, 0.0)
    data[((damkohler_diff<0) & (storage_diff>0) & (no3_layer3>5))] = 1

    data[mask!=1] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, cmap=custom_cmap_1, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    fig.savefig(Path.work_path+'plots/'+mode+'/risky_region_nitrogen.png', transparent=True)

    

    data = np.full(ywf_diff.shape, 0.0)
    data[((damkohler_diff<0) & (storage_diff>0) & (no3_layer3>5)) & (ywf_diff<0)] = 1

    data[mask!=1] = np.nan

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, cmap=custom_cmap_1, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    fig.savefig(Path.work_path+'plots/'+mode+'/risky_region_both.png', transparent=True)

def plot_risky_regions(mode):

    #experiments = [None, 'ssp126', 'ssp585']
    experiments = [None]

    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(tmp.shape, np.nan)
    mask[tmp>0] = 1

    for experiment in experiments:
        
        if experiment is None:
            exp_suffix = ''
        else:
            exp_suffix = '_' + experiment

        ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff'+exp_suffix+'.asc', skiprows=6)
        tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff'+exp_suffix+'.asc', skiprows=6)
        damkohler_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/damkholer_num_diff'+exp_suffix+'.asc', skiprows=6)
        print(tranage_diff.shape, damkohler_diff.shape)
        data = np.full(tranage_diff.shape, np.nan)
        #data[(ywf_diff<0) & (damkohler_diff<0)] = 4    
        #data[(ywf_diff>0) & (damkohler_diff<0)] = 3
        #data[(ywf_diff<0) & (damkohler_diff>0)] = 2
        #data[(ywf_diff>0) & (damkohler_diff>0)] = 1
        data[(tranage_diff>0) & (damkohler_diff<0)] = 4    
        data[(tranage_diff<0) & (damkohler_diff<0)] = 3
        data[(tranage_diff>0) & (damkohler_diff>0)] = 2
        data[(tranage_diff<0) & (damkohler_diff>0)] = 1
        
        data[mask!=1] = np.nan

        custom_cmap = custom_cmap_3

        N = np.argwhere(mask==1).shape[0]
        N1 = np.argwhere(data==1).shape[0] 
        N2 = np.argwhere(data==2).shape[0] 
        N3 = np.argwhere(data==3).shape[0] 
        N4 = np.argwhere(data==4).shape[0] 

        print(N, N1/N, N2/N, N3/N, N4/N, (N1+N2)/N)


        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
        sc0 = ax.imshow(data, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
        # Add colorbar
        #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
        #cbar.ax.tick_params(labelsize=25)
        ax.axis('off')
        fig.savefig(Path.work_path+'plots/'+mode+'/analysis/analysis_corr_damkohler_age'+exp_suffix+'.png', transparent=True)


        if experiment is None:
            addition_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_addition_diff.asc', skiprows=6)

            data_new = data.copy()
            data_new[~(addition_diff<0)] = np.nan
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data_new, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
            ax.axis('off')
            fig.savefig(Path.work_path+'plots/'+mode+'/analysis/analysis_corr_damkohler_age'+exp_suffix+'_addition_decrease.png', transparent=True)

            data_new = data.copy()
            data_new[~(addition_diff>0)] = np.nan
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data_new, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
            ax.axis('off')
            fig.savefig(Path.work_path+'plots/'+mode+'/analysis/analysis_corr_damkohler_age'+exp_suffix+'_addition_increase.png', transparent=True)

            data_new = data.copy()
            data_new[~(addition_diff==0)] = np.nan
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data_new, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
            ax.axis('off')
            fig.savefig(Path.work_path+'plots/'+mode+'/analysis/analysis_corr_damkohler_age'+exp_suffix+'_addition_nochange.png', transparent=True)


def plot_risky_regions_scatter(mode):

    import matplotlib.cm as cm

    experiments = [None]
    #experiments = [None]

    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(tmp.shape, np.nan)
    mask[tmp>0] = 1

    for experiment in experiments:
        
        if experiment is None:
            exp_suffix = ''
        else:
            exp_suffix = '_' + experiment

        precip_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/Precipitation_npfloat32_diff'+exp_suffix+'.asc', skiprows=6)
        addition_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_addition_diff.asc', skiprows=6)
        ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff'+exp_suffix+'.asc', skiprows=6)
        tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff'+exp_suffix+'.asc', skiprows=6)
        damkohler_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/damkholer_num_diff'+exp_suffix+'.asc', skiprows=6)

        addition = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/nitrogen_addition.bin').reshape(-1, mask.shape[0], mask.shape[1])
        addition = np.mean(addition, axis=0)

        precip_diff = precip_diff[mask==1]
        addition_diff = addition_diff[mask==1]


        damkohler_diff = damkohler_diff[mask==1]
        addition = addition[mask==1]

        

        custom_cmap = custom_cmap_3

        fig, ax = plt.subplots(1,1, figsize=(3,3), dpi=300)

        vmin = -0.5
        vmax = 0.5

        
        colors = np.full(len(damkohler_diff), np.nan)
        
        tmp = damkohler_diff.copy()
        tmp = np.log10(tmp)
        tmp[tmp>vmax] = vmax
        tmp[tmp<vmin] = vmin
        tmp = (tmp - vmin) / (vmax - vmin)
        valid_idx = np.where(~np.isnan(tmp))
        colors[valid_idx] = 0.5 + tmp[valid_idx] * 0.5
        


        tmp = damkohler_diff.copy()
        tmp = np.log10(-tmp)
        tmp[tmp>vmax] = vmax
        tmp[tmp<vmin] = vmin
        tmp = (tmp - vmin) / (vmax - vmin)
        valid_idx = np.where(~np.isnan(tmp))
        colors[valid_idx] = 0.5 - tmp[valid_idx] * 0.5
        
        
        #sorted_idx = np.argsort(colors)[::-1]
        sorted_idx = colors<100
        ax.scatter(addition_diff[sorted_idx], precip_diff[sorted_idx], facecolors='none', edgecolors=cm.coolwarm(colors[sorted_idx]), s=15, linewidths=0.5, alpha=0.01)

        sorted_idx = np.logical_and(colors<0.5, precip_diff<-200)
        ax.scatter(addition_diff[sorted_idx], precip_diff[sorted_idx], facecolors='none', edgecolors=cm.coolwarm(colors[sorted_idx]), s=15, linewidths=0.5, alpha=0.1)
        
        ax.set_xlim(-210, 210)
        ax.set_xticks([-200, 0, 200])
        ax.set_ylim(-700, 700)
        ax.set_yticks([-600, 0, 600])
        ax.tick_params(axis='both', labelsize=10)

        ax.plot(np.full(2000, 0), np.arange(-1000,1000), c='black', alpha=0.3, linewidth=1, linestyle='--')
        ax.plot(np.arange(-1000,1000), np.full(2000, 0), c='black', alpha=0.3, linewidth=1, linestyle='--')

        fig.savefig(Path.work_path+'plots/'+mode+'/analysis/risky_region_scatter.png', transparent=True)

        

def analysis(mode):
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(tmp.shape, False)
    mask[tmp>0] = True

    spatial_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'
    typical_region_path = '/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/'
    asc_path = '/data/scratch/wusongj/paper4/plots/forward_all/asc/'

    dominant_landuse = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/dominant_landuse.asc', skiprows=6)


    data = np.mean(np.fromfile(spatial_path + 'young_water_fraction_soil_all_depths.bin').reshape(-1, mask.shape[0], mask.shape[1])[:24,:,:], axis=0)   
    #data = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/'+'young_water_fraction_soil_all_depths'+'_diff.asc', skiprows=6)
    data[data==-9999] = np.nan

    # trans_age_SMC_soil_all_depths
    #data[data>5000] = 5000
    #data[data<-5000] = -5000 

    #data[data<0] = np.nan
    #data[data>200] = 200 # no3_SMC_all_layers
    #~(np.loadtxt(typical_region_path + 'typical_regions_mountains.asc', skiprows=6)==1)
    # damkholer_num
    #data[data>100] = 100
    #data = np.log10(data)
    region_mask = np.logical_and.reduce([
                                         #np.loadtxt(typical_region_path+'typical_regions_Ts_southern_europe.asc', skiprows=6)==1,
                                         np.loadtxt(typical_region_path+'typical_regions_mountains.asc', skiprows=6)==1,
                                        ])
    

    data = trimmed_mean_2d(data, low=10, high=90, axis=0, mask=(region_mask), warming_period=0)
    data_mean = np.nanmean(data)
    data_min = np.nanmin(data)
    data_max = np.nanmax(data)
    data_median = np.nanmedian(data)

    #N = len(np.where(~np.isnan(data))[0])
    #N1 = len(np.where(np.logical_and(~np.isnan(data), data>0))[0])
    #print(N, N1, N1/N)


    print(data_mean, data_min, data_max, data_median)
    #print(np.power(10, data_mean), np.power(10, data_min), np.power(10, data_max), np.power(10, data_median))


    




def plot_risky_regions_TS(mode):
    from datetime import datetime
    from scipy.stats import linregress
    import matplotlib.dates as mdates

    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(tmp.shape, np.nan)
    mask[tmp>0] = 1

    """
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff.asc', skiprows=6)

    #mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'central_west_europe_with_lower_age'+'.asc', skiprows=6)

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'central_west_europe_with_lower_age'+'.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    print(np.mean(ywf_diff[mask_tmp]), np.mean(tranage_diff[mask_tmp]))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'northern_europe'+'.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    print(np.mean(ywf_diff[mask_tmp]), np.mean(tranage_diff[mask_tmp]))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'eastern_europe'+'.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    print(np.mean(ywf_diff[mask_tmp]), np.mean(tranage_diff[mask_tmp]))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'southern_europe'+'.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    print(np.mean(ywf_diff[mask_tmp]), np.mean(tranage_diff[mask_tmp]))
    """
    pass
    
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    tranage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/trans_age_SMC_soil_all_depths_diff.asc', skiprows=6)
    damkohler_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/damkholer_num_diff.asc', skiprows=6)
    data = np.full(tranage_diff.shape, np.nan)
    #data[(ywf_diff<0) & (damkohler_diff<0)] = 4    
    #data[(ywf_diff>0) & (damkohler_diff<0)] = 3
    #data[(ywf_diff<0) & (damkohler_diff>0)] = 2
    #data[(ywf_diff>0) & (damkohler_diff>0)] = 1
    
    data[(tranage_diff>0) & (damkohler_diff<0)] = 4    
    data[(tranage_diff<0) & (damkohler_diff<0)] = 3
    data[(tranage_diff>0) & (damkohler_diff>0)] = 2
    data[(tranage_diff<0) & (damkohler_diff>0)] = 1
    
    data[mask!=1] = np.nan

    custom_cmap = custom_cmap_2

    """
    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    fig.savefig(Path.work_path+'plots/'+mode+'/analysis/analysis_corr_damkohler_age.png', transparent=True)
    """

    dominant_landuse = np.loadtxt(Path.data_path+'catchment_info/dominant_landuse.asc', skiprows=6)
    invalid_region = np.loadtxt(Path.data_path+'catchment_info/typical_regions/invalid_region_eastern_europe.asc', skiprows=6)
    

    mask_1 = data.copy()
    #vars = ['nitrogen_inputs', 'plant_uptake', 'deni_soil', 'deni_fraction', 'plant_uptake_fraction', 'leaching_fraction', 'trans_age_SMC_soil_all_depths', 'damkholer_num']
    #vars = ['infiltration', 'Evapotranspiration_fraction', 'SMC_soil_all_depths', 'deni_fraction', 'plant_uptake_fraction', 'nitrogen_storage', 'trans_age_SMC_soil_all_depths', 'damkholer_num']
    #vars = ['SMC_soil_all_depths']
    vars = ['damkholer_num']
    ylim_dict = {'infiltration':[[450,750],[500,600,700]],
                 'Evapotranspiration_fraction':[[58, 82], [60,70,80]],
                 'SMC_soil_all_depths':[[0.23,0.31],[0.24, 0.27, 0.30]],
                 'deni_fraction':[[3,11],[4,7,10]],
                 'plant_uptake_fraction':[[23,39], [24,30,36]],
                 'nitrogen_storage':[[180,520], [200,350,500]],
                 'trans_age_SMC_soil_all_depths':[[1400, 4600], [1500, 3000, 4500]],
                 'damkholer_num':[[-0.92, -0.27], [-0.9, -0.6, -0.3]]}
    #vars = []
    custom_cmap = custom_cmap_2
    #custom_cmap = plt.cm.Spectral_r
    #custom_cmap = get_cmcrameri_cmap('batlowW', start=0.1, end=0.95, alpha=1)

    tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')
    
    for var in vars:
        fig, ax = plt.subplots(1,1, figsize=(4,2), dpi=300)
        plt.subplots_adjust(left=0.16, bottom=0.13, right=0.99, top=0.99, wspace=0.01, hspace=0.01)
        
                
        for kk in [1,2,3,4]:
            mask_tmp = np.logical_and.reduce([(mask_1==kk), (dominant_landuse==1), (invalid_region!=1)])
            #mask_tmp = (mask_1==kk)
            color = custom_cmap((kk-1)/(len([1,2,3,4])-1))
            if var =='Evapotranspiration_fraction':
                data0 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/Evapotranspiration.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data0 = np.nanmean(data0[:,mask_tmp], axis=(1))
                df0 = pd.DataFrame(data0, index=tindex).resample('Y').mean()
                data1 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/infiltration.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df1 = pd.DataFrame(data1, index=tindex).resample('Y').mean()
                df = df0/df1
            elif var =='SMC_soil_all_depths':
                #data1 = ((np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/SMC_layer1.bin') * 0.2 + 
                #          np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/SMC_layer2.bin') * 0.2 + 
                #          np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/SMC_layer3.bin') * 1.9) /
                #          (0.2 + 0.2 + 1.9)).reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data1 =  ((np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/SMC_layer1.bin') + 
                          np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/SMC_layer1.bin')) / 2).reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df = pd.DataFrame(data1, index=tindex).resample('Y').mean()
            elif var =='nitrogen_inputs':
                data1 = (np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/nitrogen_addition.bin') + 
                         np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/minerl_soil.bin') +
                         np.fromfile(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin')).reshape(-1, mask_1.shape[0], mask_1.shape[1])  
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df = pd.DataFrame(data1, index=tindex).resample('Y').mean()
            elif var == 'deni_fraction':
                data0 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/deni_soil.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data0 = np.nanmean(data0[:,mask_tmp], axis=(1))
                df0 = pd.DataFrame(data0, index=tindex).resample('Y').mean()
                data1 = (np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/nitrogen_addition.bin') + 
                         np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/minerl_soil.bin') +
                         np.fromfile(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin')).reshape(-1, mask_1.shape[0], mask_1.shape[1])  
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df1 = pd.DataFrame(data1, index=tindex).resample('Y').mean()
                df = df0/df1
            
            elif var == 'plant_uptake_fraction':
                data0 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/plant_uptake.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data0 = np.nanmean(data0[:,mask_tmp], axis=(1))
                df0 = pd.DataFrame(data0, index=tindex).resample('Y').mean()
                data1 = (np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/nitrogen_addition.bin') + 
                         np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/minerl_soil.bin') +
                         np.fromfile(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin')).reshape(-1, mask_1.shape[0], mask_1.shape[1])              
                        
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df1 = pd.DataFrame(data1, index=tindex).resample('Y').mean()
                df = df0/df1
            
            elif var == 'leaching_fraction':
                data0 = (np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/no3_SMC_layer3.bin') * 
                         np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/perc_layer3.bin')).reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data0 = np.nanmean(data0[:,mask_tmp], axis=(1))
                df0 = pd.DataFrame(data0, index=tindex).resample('Y').mean()
                data1 = (np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/nitrogen_addition.bin') + 
                         np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/minerl_soil.bin') +
                         np.fromfile(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin')).reshape(-1, mask_1.shape[0], mask_1.shape[1])              
                        
                data1 = np.nanmean(data1[:,mask_tmp], axis=(1))
                df1 = pd.DataFrame(data1, index=tindex).resample('Y').mean()
                df = df0/df1

            elif var == 'damkholer_num':
                data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'+var+'.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data = np.log10(data)
                data = np.nanmean(data[:,mask_tmp], axis=(1))
                df = pd.DataFrame(data, index=tindex)
                df = df.resample('Y').mean()

            else:
                data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/'+var+'.bin').reshape(-1, mask_1.shape[0], mask_1.shape[1])
                data = np.nanmean(data[:,mask_tmp], axis=(1))
                df = pd.DataFrame(data, index=tindex)
                df = df.resample('Y').mean()


            df = df['1985-1-1':]
        
            if 'fraction' in var:
                df *= 100
            elif var!='SMC_soil_all_depths':
                df *= var_info[var][1]


            slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(df.index)), np.squeeze(df.values))

            df = df[:'2023-12-31']

            if kk == 1:
                white_background = np.ones((100, 100, 3)) * 255
                ax.imshow(white_background, extent=[mdates.date2num(datetime(1980,1,1)), mdates.date2num(datetime(2030,1,1)), ylim_dict[var][0][0], ylim_dict[var][0][1]], 
                        aspect='auto', zorder=0)

            ax.plot(df.index, df.values, color=color, alpha=0.4, zorder=3)
            X = np.arange(len(df.index))
            Y = slope * X + intercept
            ax.plot(df.index[8:-8], Y[8:-8], linewidth=3.5,  color=color, linestyle='--', alpha=1, zorder=5)     
            
            ax.set_xlim([datetime(1984,1,1), datetime(2026,1,1)])
            ax.set_xticks([datetime(1990,1,1), datetime(2000,1,1), datetime(2010,1,1), datetime(2020,1,1)])
            ax.set_xticklabels(['1990', '2000', '2010', '2020'])
            ax.tick_params(axis='both', labelsize=14)

            
            
            try:
                ax.set_ylim(ylim_dict[var][0])
                ax.set_yticks(ylim_dict[var][1])
            except Exception as e:
                print(e)
                pass
        
            if var == 'damkholer_num':
                ax.set_yticklabels([r"$10^{-0.9}$", r"$10^{-0.6}$", r"$10^{-0.3}$"])

            

            print(var, kk, slope, p_value, np.mean(df.values))
            
        fig.savefig(Path.work_path+'plots/'+mode+'/analysis/age_damkohler_region_'+var+'.png', transparent=True,
                    )



    """
    no3_layer3 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/no3_SMC_layer3.bin').reshape(-1, tranage_diff.shape[0], tranage_diff.shape[1])
    no3_layer3 = np.mean(no3_layer3[24:,:,:], axis=0)
    data[no3_layer3<5] = 1
    data[data==4] = 1

    fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
    sc0 = ax.imshow(data, vmin=1, vmax=4, cmap=custom_cmap, alpha=1, zorder=1)
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[1, 2, 3])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    fig.savefig(Path.work_path+'plots/'+mode+'/analysis_corr_damkohler_age_filtered_by_no3conc.png', transparent=True)

    #addition_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_addition_diff.asc', skiprows=6)
    #storage_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/nitrogen_storage_diff.asc', skiprows=6)
    """
    



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
        
        if var == 'Evapotranspiration_fraction':
            _data = np.mean(read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/Evapotranspiration.'+extension, mask)[24:,:,:], axis=0) /  \
                    np.mean(read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/infiltration.'+extension, mask)[24:,:,:], axis=0)
        elif var == 'nitrogen_uptake':
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/deni_soil.'+extension, mask) +  \
                    read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/plant_uptake.'+extension, mask)
        elif var == 'nitrogen_input':
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/nitrogen_addition.'+extension, mask) +  \
                    read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/minerl_soil.'+extension, mask) +  \
                    read_outputs(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin', mask)
        elif var == 'wet_deposition':
            _data = read_outputs('/data/scratch/wusongj/paper4/data/catchment_info/others/wet_deposition_monthly.bin', mask)
        elif var == 'damkholer_num':
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'_annually.'+extension, mask)
        else:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
            except Exception as e:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)


        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        if extension=='bin':

            alpha = 1


            if var == 'Evapotranspiration_fraction':
                data = _data
            else:
                if temp_res=='monthly':
                    data = np.mean(_data[24:,:,:], axis=0)
                else:
                    data = np.mean(_data[2:,:,:], axis=0)
            

            
            if var=='damkholer_num':
                data = np.log10(data)
                cmap = 'coolwarm'
                alpha = 1
            elif var=='infiltration':
                cmap = 'Blues'
            elif 'Evapotranspiration' in var:
                cmap = 'Oranges'
            elif 'nitrogen' in var or var=='deni_soil':
                cmap = get_cmcrameri_cmap('lipari', start=0.2, end=0.99, alpha=1)
            else:
                cmap = get_cmcrameri_cmap('batlowW', start=0.1, end=0.95, alpha=1)
            

            if var_info[var][2]:
                data[~chanmask] = np.nan
            else:
                data[mask!=1] = np.nan

            
 

            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, alpha=alpha, zorder=1)
            # Add colorbar
            #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
            #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
            #cbar.ax.tick_params(labelsize=25)
            ax.axis('off')

            fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_all.png', transparent=True)



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

            fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'_all.png', transparent=True)


def plot_spatial_results_EU_diff(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False, experiment=None):

    import matplotlib.cm as cm
    from matplotlib.colors import ListedColormap  

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    if experiment is None:
        path_flag = 'all'
    else:
        path_flag = 'all_' + experiment

    for var in vars:

        extension = var.split('.')[-1]
        var = var.split('.')[0]

        if '_map' in var:
            var = var[:-4]

        if experiment is not None and var in ['Precipitation_npfloat32', 'Potential_evapotranspiration_npfloat32', 'Mean_air_temperature_npfloat32', 'Surface_net_radiation_npfloat32']:
            data = read_outputs('/data/scratch/wusongj/paper4/data/catchment_info/climate_3035_tmp/difference_'+var+'_'+experiment+'.asc', mask)
            data *= var_info[var][1]  # weight
            

        else:
            if var=='damkholer_num' or var=='processing_time':

                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/'+var+'_annually.'+extension, mask)

                if experiment is None:
                    periods = [[5,15], [35,45]]    
                else:
                    periods = [[45,55], [110, 120]]

            else:        
            
                if var == 'Evapotranspiration_fraction':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/Evapotranspiration.'+extension, mask) /  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/infiltration.'+extension, mask)
                elif var == 'nitrogen_uptake':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/deni_soil.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/plant_uptake.'+extension, mask)
                elif var == 'nitrogen_input':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/nitrogen_addition.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/minerl_soil.'+extension, mask) +  \
                            read_outputs(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin', mask)
                elif var == 'wet_deposition':
                    _data = read_outputs('/data/scratch/wusongj/paper4/data/catchment_info/others/wet_deposition_monthly.bin', mask)
                else:
                    try:
                        _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/'+path_flag+'/'+var+'.'+extension, mask)
                    except Exception as e:
                        _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'_3035.'+extension, mask, dtype=np.float32)

                #if var=='damkholer_num' or var=='trans_age_SMC_soil_all_depths' or var=='processing_time':
                #    _data = np.log10(_data)

                if experiment is None:
                    periods = [[5*12,15*12], [15*12,25*12], [25*12,35*12], [35*12,45*12]]    
                else:
                    periods = [[45*12,55*12], [110*12, 120*12]]
            
            
            _data *= var_info[var][1]  # weight
            

            baseline = np.mean(_data[periods[0][0] : periods[0][1], :, :], axis=0)

            """
            if experiment is not None:
                r = 392
                c = 708
                if var=='damkholer_num' or var=='processing_time':
                    df0 = pd.DataFrame(_data[:,r,c], index=pd.date_range('1980-1-1', '2100-12-31', freq='Y'))
                else:
                    df0 = pd.DataFrame(_data[:,r,c], index=pd.date_range('1980-1-1', '2100-12-31', freq='M'))
                    df0 = df0.resample('Y').mean()
                fig, ax = plt.subplots(1,1, figsize=(5,5), dpi=300)
                ax.plot(df0.index, df0.values)
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_debug_'+experiment+'.png')
                np.savetxt(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_debug_'+experiment+'.txt', _data[:,r,c])
            """

        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]


        if np.logical_not(np.logical_and(experiment is not None, var in ['Precipitation_npfloat32', 'Potential_evapotranspiration_npfloat32', 'Mean_air_temperature_npfloat32', 'Surface_net_radiation_npfloat32'])):
            data = np.mean(_data[periods[-1][0] : periods[-1][1], :, :], axis=0) - baseline

        data[mask!=1] = np.nan

        if var=='damkholer_num' or var=='trans_age_SMC_soil_all_depths' or var=='processing_time':
            # Average first and log
            diff_upper_cap_min = var_info[var][3][0]
            diff_upper_cap_max = var_info[var][3][1]
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(np.log10(data), vmin=diff_upper_cap_min, vmax=diff_upper_cap_max, cmap=ListedColormap(cm.coolwarm(np.linspace(0.5, 1, 256))), zorder=1)
            sc1 = ax.imshow(np.log10(-data), vmin=diff_upper_cap_min, vmax=diff_upper_cap_max, cmap=ListedColormap(cm.coolwarm(np.linspace(0.5, 0, 256))), zorder=1)
            ax.axis('off')

            if experiment is None:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff.png', transparent=True)
            else:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff_'+experiment+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_'+experiment+'.png', transparent=True)
            
            """ 
            # log first and average
            diff_upper_cap_min = var_info[var][3][0]
            diff_upper_cap_max = var_info[var][3][1]
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data, vmin=-diff_upper_cap_max, vmax=diff_upper_cap_max, cmap='coolwarm', zorder=1)

            ax.axis('off')

            if experiment is None:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff.png', transparent=True)
            else:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff_'+experiment+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_'+experiment+'.png', transparent=True)
            """
            print(var, diff_upper_cap_min, diff_upper_cap_max)
            

        else:
                            
            if len(var_info[var]) > 3:
                diff_upper_cap = var_info[var][3]
            else:
                diff_upper_cap = vmax / 8

        
            if var_info[var][2]:
                data[~chanmask] = np.nan
            
            

            
            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data, vmin=-diff_upper_cap, vmax=diff_upper_cap, cmap='coolwarm', zorder=1)
            # Add colorbar
            #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
            #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[-diff_upper_cap, 0, diff_upper_cap])
            #cbar.ax.tick_params(labelsize=25)
            ax.axis('off')

            if experiment is None:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff.png', transparent=True)
            else:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff_'+experiment+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_'+experiment+'.png', transparent=True)
            print(var, -diff_upper_cap, diff_upper_cap)
    
        """
        #for yy, data in enumerate([baseline, np.mean(_data[periods[-1][0] : periods[-1][1], :, :], axis=0)]):
        for yy, data in enumerate([_data[0, :, :], _data[-1, :, :]]):

            if var=='damkholer_num':
                data = np.log10(data)
                cmap = 'coolwarm'
            else:
                cmap = 'viridis'

            fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
            ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
            sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, zorder=1)
            # Add colorbar
            #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
            #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
            #cbar.ax.tick_params(labelsize=25)
            ax.axis('off')
            if experiment is None:
                #GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/asc/'+var+'_diff_diagnose_'+str(yy)+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_diagnose_'+str(yy)+'.png')
            else:
                GEM_tools.create_asc(data, Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_diagnose_'+str(yy)+'_'+experiment+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
                fig.savefig(Path.work_path+'plots/'+mode+'/diff/'+var+'_diff_diagnose_'+str(yy)+'_'+experiment+'.png')
        """
        
def trimmed_mean(data, low=5, high=95, axis=0, mask=None, warming_period=0):           

    low_value, high_value = np.percentile(data, [low,high], axis=axis, keepdims=False)
    data[data<low_value] = np.nan
    data[data>high_value] = np.nan

    if mask is not None:
        data[:,~mask] = np.nan
            
    
    data_mean = np.nanmean(data, axis=(1,2))[warming_period:]
    #data_5_perc = np.nanpercentile(data, 15, axis=(1,2))[warming_period:]
    #data_95_perc = np.nanpercentile(data, 85, axis=(1,2))[warming_period:]

    return data_mean


def trimmed_mean_2d(data, low=5, high=95, axis=0, mask=None, warming_period=0):           

    low_value, high_value = np.percentile(data, [low,high], keepdims=False)
    data[data<low_value] = np.nan
    data[data>high_value] = np.nan

    if mask is not None:
        data[~mask] = np.nan
            
    return data

def plot_TS_results_EU(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False, experiment=None):
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    if experiment is None:
        output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'

    for var in vars:

        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])
        if '_map' in var:
            var = var[:-4]    
        try:

            try:
                if var == 'nitrogen_uptake':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/deni_soil.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/plant_uptake.'+extension, mask)
                elif var == 'nitrogen_input':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/nitrogen_addition.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/minerl_soil.'+extension, mask) +  \
                            read_outputs(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin', mask)
                else:
                    _data = read_outputs(output_path+var+'.'+extension, mask)
                
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)               
        except:
            continue


        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        
 

        if var_info[var][2]:
            data = np.nanmedian(_data[:,chanmask], axis=(1))[24:]
        else:
            data = trimmed_mean(_data, low=5, high=95, mask=mask, warming_period=24)
        if var == 'damkholer_num':
            data = np.log10(data)
            vmin, vmax = [1, 4]
        if experiment is None:
            tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')[24:]
            tindex_label = pd.date_range('1980-1-1', '2024-12-31', freq='M').strftime('%Y-%m')[24:]
        else:
            tindex = pd.date_range('1980-1-1', '2100-12-31', freq='M')[24:]
            tindex_label = pd.date_range('1980-1-1', '2100-12-31', freq='M').strftime('%Y-%m')[24:]


        


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

        if experiment is None:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS.png'
        else:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS_'+experiment+'.png'
        fig.savefig(save_file_path)
        print('Figure saved at :   ' + save_file_path)

def plot_TS_results_EU_by_regions(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False, experiment=None):
    
    from datetime import datetime
    from scipy.stats import linregress
    #from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    if experiment is None:
        output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'
    
    if os.path.exists('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc'):
        ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    else:
        ywf_diff = read_outputs(output_path+'young_water_fraction_soil_all_depths.bin', mask).reshape(-1, mask.shape[0], mask.shape[1])
        ywf_diff = np.mean(ywf_diff[35*12:45*12,:,:], axis=0) - np.mean(ywf_diff[5*12:15*12,:,:], axis=0)
        GEM_tools.create_asc(ywf_diff, '/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')


    ['central_west_europe_with_lower_age', 'south_europe', 'eastern_europe', 'northern_europe', 'western_europe']

    region_masks = []

    dominant_landuse = np.loadtxt(Path.data_path+'catchment_info/dominant_landuse.asc', skiprows=6)

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'central_west_europe_with_lower_age'+'.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'northern_europe'+'.asc', skiprows=6)
    mask_tmp = mask_tmp > 0
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'eastern_europe'+'.asc', skiprows=6)
    mask_tmp = mask_tmp > 0
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'southern_europe'+'.asc', skiprows=6)
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    mask_tmp = mask_tmp > 0
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))



    for var in vars:
        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])
        if '_map' in var:
            var = var[:-4]    
        try:

            try:
                
                if var == 'nitrogen_uptake':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/deni_soil.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/plant_uptake.'+extension, mask)
                elif var == 'nitrogen_input':
                    _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/nitrogen_addition.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/minerl_soil.'+extension, mask) +  \
                            read_outputs(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin', mask)
                elif var =='nitrogen_surplus':
                    _data = (read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/nitrogen_addition.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/minerl_soil.'+extension, mask) +  \
                            read_outputs(Path.data_path + 'catchment_info/others/wet_deposition_monthly.bin', mask)) -\
                            (read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/deni_soil.'+extension, mask) +  \
                            read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/plant_uptake.'+extension, mask)) \

                            

                     
                else:
                    _data = read_outputs(output_path+var+'.'+extension, mask)
                
            except Exception as e:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)               
        except:
            continue


        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        if var == 'Evapotranspiration_fraction':
            _data[_data>120] = 120  # To avoid Inf


        #fig, ax = plt.subplots(len(region_masks),1, figsize=(5,5), dpi=300)
        #for xx, region_mask in enumerate(region_masks):
        #    ax[xx].imshow(np.logical_and(region_mask, mask))
        #fig.savefig(Path.work_path+'plots/'+mode+'/TS_regions.png')


        fig, ax = plt.subplots(1,2, figsize=(8,3), gridspec_kw={'width_ratios': [4, 1]}, dpi=300)
        plt.subplots_adjust(left=0.08, bottom=0.1, right=0.92, top=0.98, wspace=0.07, hspace=0.1)
        #ax_inset = inset_axes(ax, width="10%", height="40%", loc="upper right")
        
        for xx, region_mask in enumerate(region_masks):

            

            if var_info[var][2]:
                region_mask = np.logical_and(region_mask, chanmask)
                #data = np.nanmean(_data[:,region_mask], axis=(1))[24:]
            else:
                region_mask = np.logical_and(region_mask, mask)
                #data = np.nanmean(_data[:,region_mask], axis=(1))[24:]

            if var == 'damkholer_num':
                data = np.log10(_data.copy())
            else:
                data = _data.copy()

            data = trimmed_mean(data, low=5, high=95, mask=region_mask, warming_period=12*5)



            if experiment is None:
                tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')[12*5:]
                tindex_label = pd.date_range('1980-1-1', '2024-12-31', freq='M').strftime('%Y-%m')[12*5:]
            else:
                tindex = pd.date_range('1980-1-1', '2100-12-31', freq='M')[12*5:]
                tindex_label = pd.date_range('1980-1-1', '2100-12-31', freq='M').strftime('%Y-%m')[12*5:]


            #df = pd.DataFrame(np.stack([data, data_upper, data_lower], axis=0).T, columns=['mean', '5perc', '95perc'], index=tindex)
            df = pd.DataFrame(data, columns=['mean'], index=tindex)
            #df.index = pd.to_datetime(df.index)
            df = df.resample('Y').mean()
            df = df['1985-1-1':]

            slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(df.index)), df['mean'])

            styles = ['-', '--']
            custom_cmap = custom_cmap_1
            #custom_cmap = plt.cm.Spectral_r
            #custom_cmap = get_cmcrameri_cmap('batlowW', start=0.1, end=0.95, alpha=1)
            color = custom_cmap((xx//2)/(len(region_masks)/2-1))
            style = styles[xx%2]

            ylims_0_dict = {'Precipitation_npfloat32_3035':[-30,2000], 
                            'infiltration':[-100, 2000],
                            'Evapotranspiration_fraction':[-5, 180],
                            'young_water_fraction_soil_all_depths':[2, 36],
                            'nitrogen_addition':[-10,220],
                            'damkholer_num':[-2,4],
                            'nitrogen_storage':[-50,800],
                            'nitrogen_surplus':[-15,200]}
            ylims_1_dict = {'Precipitation_npfloat32_3035':[250,1100], 
                            'infiltration':[460,940],
                            'Evapotranspiration_fraction':[60, 90],
                            'young_water_fraction_soil_all_depths':[4,20],
                            'nitrogen_addition':[-5,150],
                            'damkholer_num':[-0.8, 0.8],
                            'nitrogen_storage':[-20,450],
                            'nitrogen_surplus':[-3,125]}
            yticks_0_dict = {'Precipitation_npfloat32_3035':[0,600,1200], 
                            'infiltration':[0, 600, 1200],
                            'Evapotranspiration_fraction':[0, 70, 140],
                            'young_water_fraction_soil_all_depths':[5,15,25],
                            'nitrogen_addition':[0,60,120],
                            'damkholer_num':[-1,0,1],
                            'nitrogen_storage':[0,200,400],
                            'nitrogen_surplus':[0,60,120]}
            yticks_1_dict = {'Precipitation_npfloat32_3035':[300,650,1000], 
                            'infiltration':[500, 700, 900],
                            'Evapotranspiration_fraction':[0,60,120],
                            'young_water_fraction_soil_all_depths':[6,12,18],
                            'nitrogen_addition':[0,60,120],
                            'damkholer_num':[-0.5, 0, 0.5],
                            'nitrogen_storage':[0,200,400],
                            'nitrogen_surplus':[0,50,100]}
            

            print(var, xx, slope, r_value, p_value)

            
            

            #ax.scatter(tindex, data, s=5, color=color, alpha=0.2)
            ax[0].plot(tindex, data, linewidth=3, linestyle=style, color=color, alpha=0.1, zorder=0)
            ax[0].plot(df.index, df['mean'], linewidth=3, linestyle=style, color=color, alpha=1, zorder=2)
            
            #X = tindex[10*12:-10*12]
            #Y = slope * np.arange(10*12, 10*12+len(X), 1) + intercept
            #ax.plot(df.index[8:-8], Y[8:-8], linewidth=3,  color=color, linestyle=style, alpha=1, zorder=5)
            #ax.plot(df.index, df['mean'], linewidth=4, linestyle=style, color=color, alpha=0.2)
            X = np.arange(len(df.index))
            Y = slope * X + intercept
            ax[1].plot(df.index, Y, linewidth=3,  color=color, linestyle=style, alpha=1, zorder=5)       
            #ax_inset.plot(df.index, Y, linewidth=3,  color=color, linestyle=style, alpha=1, zorder=5)
            #ax_inset.set_facecolor("white")

            ax[1].yaxis.tick_right()
            # 
            ax[0].set_xticks([datetime(1985,1,1), datetime(1995,1,1), datetime(2005,1,1), datetime(2015,1,1), datetime(2024,12,31)])
            ax[1].set_xticks([datetime(1985,1,1), datetime(2024,12,31)])
            ax[0].set_xticklabels([])
            ax[1].set_xticklabels([])

            ax[0].set_ylim(ylims_0_dict[var])
            ax[1].set_ylim(ylims_1_dict[var])
            ax[0].set_yticks(yticks_0_dict[var])
            ax[1].set_yticks(yticks_1_dict[var])

            if var == 'damkholer_num':
                ax[0].set_yticklabels(['0.1', '1', '10'])
                ax[1].set_yticklabels([r"$\frac{1}{\sqrt{10}}$", "1", r"$\sqrt{10}$"])

            ax[0].tick_params(axis='both', labelsize=15)
            ax[1].tick_params(axis='both', labelsize=15)

            #ax1 = ax.twinx()
            #ax1.plot(df.index,df.value, linewidth=3, color=custom_cmap(xx/len(region_masks)))
            
            #ax1.set_ylim(vmin, vmax)


        if experiment is None:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS_by_regions.png'
        else:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS_by_regions_'+experiment+'.png'
        fig.savefig(save_file_path, transparent=True)
        print('Figure saved at :   ' + save_file_path)


def plot_TS_results_EU_experiments(mode, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):

    from scipy.stats import gaussian_kde
    import matplotlib.dates as mdates
    from datetime import datetime
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    vars = ['trans_age_SMC_soil_all_depths', 'damkholer_num', 'young_water_fraction_soil_all_depths']
    ymins = [0, -1, 0, 1]
    ymaxs = [3000, 3, 30, 5]
    ylims = [[-100, 3100], [-1.1, 2.1], [-1,32]]
    yticks = [[0,1500,3000], [-1,0,1,2], [0,15,30]]
    xticks =[datetime(1985,1,1), datetime(2020,1,1), datetime(2060,1,1), datetime(2100,1,1)]
    xticklabels =[str(x) for x in [1985,2020,2060,2100]]

    for yy, var in enumerate(vars):

        if yy!=2:
            continue

        fig, ax = plt.subplots(1,1, figsize=(4,2), dpi=300)
        plt.subplots_adjust(left=0.15, bottom=0.12, right=0.95, top=0.98, wspace=0.07, hspace=0.1)

        for xx, experiment in enumerate(['ssp126', 'ssp585']):

            if experiment is None:
                output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
            else:
                output_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'

            if experiment is None:
                tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')[24:]
                tindex_yearly = pd.date_range('1980-1-1', '2024-12-31', freq='Y')[2:]
                tindex_label = pd.date_range('1980-1-1', '2024-12-31', freq='M').strftime('%Y-%m')[24:]
            else:
                tindex = pd.date_range('1980-1-1', '2100-12-31', freq='M')[24:]
                tindex_yearly = pd.date_range('1980-1-1', '2100-12-31', freq='Y')[2:]
                tindex_label = pd.date_range('1980-1-1', '2100-12-31', freq='M').strftime('%Y-%m')[24:]


            _data = read_outputs(output_path+var+'.bin', mask)

            _data *= var_info[var][1]  # weight
            vmin = var_info[var][0][0]
            vmax = var_info[var][0][1]


            _data_yearly = np.mean(_data.reshape(-1,12,mask.shape[0],mask.shape[1]), axis=1) # monthly to yearly
    
            if var == 'damkholer_num' or var == 'processing_time':
                vmin, vmax = [1, 4]
                _data_yearly = read_outputs(output_path+var+'_annually.bin', mask)
                _data_yearly = np.log10(_data_yearly)
            
            
            data_yearly = np.nanmedian(_data_yearly[:,mask>0], axis=1)[2:]

            
            np.random.seed(0)
            data_tmp = _data_yearly[:,mask>0][2:]
            
            
            valid_cols = ~(np.any(np.isnan(data_tmp), axis=0) | np.any(np.isinf(data_tmp), axis=0))
            data_tmp = data_tmp[:, valid_cols]

            
            t = np.arange(data_tmp.shape[0])  # 时间轴长度
            
            

            # 定义纵轴范围
            ymin = ymins[yy]
            ymax = ymaxs[yy]
            ygrid = np.linspace(ymin, ymax, 80)       # 在纵轴上取网格

            # 保存每个时间点的密度
            density_matrix = np.zeros((len(ygrid), len(t)))

            for i, ti in enumerate(t):
                print(i)
                kde = gaussian_kde(data_tmp[i, :])  # 第 i 个时间点，所有空间点的分布
                density_matrix[:, i] = kde(ygrid)

            # 画图
            X = mdates.date2num(tindex_yearly)                     # 转成 float
            #X = np.concatenate([X, [X[-1] + (X[-1]-X[-2])]])      # +1 个点
            Y = np.linspace(ymin, ymax, density_matrix.shape[0])
            print(X.shape, Y.shape, density_matrix.T.shape, data_tmp.shape, _data_yearly.shape)
            r, g, b, _ = custom_cmap_1(float(xx))  # 忽略原本 alpha
            # 创建 colormap：alpha 从 0 → 1
            colors = [(r, g, b, alpha) for alpha in [0, 0.6]]
            my_cmap = LinearSegmentedColormap.from_list("my_alpha_cmap", colors)

            c = ax.pcolormesh(X, Y, density_matrix, linewidth=0,
                            shading='auto', cmap=my_cmap)
            #fig.colorbar(c, ax=ax, label="Density")

            
           
            #ax.plot(tindex, data, alpha=0.1, zorder=0)
            ax.plot(tindex_yearly, data_yearly, c=custom_cmap_1(float(xx)), zorder=10)

            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels)
            ax.set_ylim(ylims[yy])
            ax.set_yticks(yticks[yy])

            ax.tick_params(axis='both', labelsize=12)

            # Add colorbar
            #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
            #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
            #cbar.ax.tick_params(labelsize=25)
            #ax.axis('off')

        if experiment is None:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS.png'
        else:
            save_file_path = Path.work_path+'plots/'+mode+'/'+var+'_TS_'+experiment+'.png'
        fig.savefig(save_file_path)
        print('Figure saved at :   ' + save_file_path)

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
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
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
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
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


def plot_water_balance(mode, temp_res, experiment=None):

    #depth3 = get_avg_depth()
    mask = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)

    # Inflow
    if experiment is None:
        save_path = Path.work_path+mode+'/outputs/cali_merged/'+temp_res+'/all/'
        n_steps = len(pd.date_range('1980-1-1', '2024-12-31', freq='M'))
    else:
        save_path = Path.work_path+mode+'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'
        n_steps = len(pd.date_range('1980-1-1', '2100-12-31', freq='M'))



    
    Infilt = np.memmap(save_path+'infiltration.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    rInfilt = np.memmap(save_path+'rinfiltration.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    ovf_in = np.memmap(save_path+'overland_flow_input.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    interf_in = np.memmap(save_path+'interflow_input.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    #GWf_in = np.memmap(save_path+'GWflow_input.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')

    # Outflow
    evap = np.memmap(save_path+'soil_evap.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    transp = np.memmap(save_path+'transp.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    perc_layer3 = np.memmap(save_path+'perc_layer3.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    rperc_layer3 = np.memmap(save_path+'rperc_layer3.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    #perc_vadose = np.memmap(save_path+'perc_vadose.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    #rperc_vadose = np.memmap(save_path+'rperc_vadose.bin', shape=(n_steps, mask.shape[0], mask.shape[1]), dtype=np.float64, mode='r')
    #ovf_out = np.memmap(save_path+'overland_flow_output.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    #ovf_toChn = np.memmap(save_path+'overland_flow_toChn.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    #interf_out = np.memmap(save_path+'interflow_output.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    #interf_toChn = np.memmap(save_path+'interflow_toChn.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')

    #GWf_out = np.memmap(save_path+'GWflow_output.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')
    #GWf_toChn = np.memmap(save_path+'GWflow_toChn.bin', dtype=np.float64, shape=(n_steps, mask.shape[0], mask.shape[1]), mode='r')

    water_balance = np.full(Infilt.shape, np.nan)

    for r in range(mask.shape[0]):
        print(r)
        for c in range(mask.shape[1]):
            if mask[r,c]>0:
                # Soil and vadose
                #inflow = Infilt[:,r,c] + rInfilt[:,r,c] + ovf_in[:,r,c] + interf_in[:,r,c]
                #outflow = evap[:,r,c] + transp[:,r,c] + perc_vadose[:,r,c] + rperc_vadose[:,r,c] + ovf_out[:,r,c] + ovf_toChn[:,r,c] + interf_out[:,r,c] + interf_toChn[:,r,c]

                # Soil
                inflow = Infilt[:,r,c] + rInfilt[:,r,c]
                outflow = evap[:,r,c] + transp[:,r,c] + perc_layer3[:,r,c] + rperc_layer3[:,r,c]
                water_balance[:,r,c] = inflow - outflow

                


    water_balance = water_balance[24:,:,:]
    water_balance *= 1000*24
    periods = [[0,12*8], [12*8, 12*18], [12*18, 12*28], [12*28, 12*38]]

    fig, ax  = plt.subplots(2,1, dpi=300)
    ax[0].imshow(np.mean(water_balance, axis=0), vmin=-5, vmax=5, cmap='coolwarm', label='water balance')
    ax[1].plot(np.nanmean(water_balance, axis=(1,2)))
    
    print(np.nanmean(water_balance))

    plt.savefig(Path.work_path+'plots/'+mode+'/water_balance.png')

    for i in range(len(periods)):
        fig, ax  = plt.subplots(2,1, dpi=300)
        ax[0].imshow(np.mean(water_balance[periods[i][0]:periods[i][1]], axis=0), vmin=-5, vmax=5, cmap='coolwarm', label='water balance')
        ax[1].plot(np.nanmean(water_balance[periods[i][0]:periods[i][1]], axis=(1,2)))
        
        print(np.nanmean(water_balance[periods[i][0]:periods[i][1]]))

        plt.savefig(Path.work_path+'plots/'+mode+'/water_balance_'+str(i)+'.png')
    

            
    

    
def calculate_yearly_Damkohler(mode, temp_res, experiment=None):

    depth3 = get_avg_depth()
    work_path = Path.work_path
    mask = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    
    if experiment is None:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all/'
        shape_3d = (540, mask.shape[0], mask.shape[1])
        shape_annual_3d = (45, mask.shape[0], mask.shape[1])

    else:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all_'+experiment+'/'
        shape_3d = (1452, mask.shape[0], mask.shape[1])
        shape_annual_3d = (121, mask.shape[0], mask.shape[1])

    # 打开 memmap 而不是一次性读入

    no3_storage = np.memmap(output_path+'nitrogen_storage.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)

    plant_uptake = np.memmap(output_path+'plant_uptake.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)

    deni_soil = np.memmap(output_path+'deni_soil.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)
    
    travel_time    = np.memmap(output_path+'trans_age_SMC_soil_all_depths.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)

    n = len(no3_storage)
    soil_deni_thres = 1 / 10 / 365
    processing_time_thres = 1e5

    # 输出文件 memmap
    processing_time = np.memmap(output_path+'processing_time_annually.bin',
                                dtype=np.float64, mode='w+', shape=shape_annual_3d)
    damkholer_num   = np.memmap(output_path+'damkholer_num_annually.bin',
                                dtype=np.float64, mode='w+', shape=shape_annual_3d)
    

    no3_storage_annual = np.mean((no3_storage.copy()).reshape(shape_annual_3d[0],12,mask.shape[0],mask.shape[1]), axis=1)
    uptake_annual = np.mean(((plant_uptake+deni_soil).copy()).reshape(shape_annual_3d[0],12,mask.shape[0],mask.shape[1]), axis=1)
    travel_time_annual = np.mean((travel_time.copy()).reshape(shape_annual_3d[0],12,mask.shape[0],mask.shape[1]), axis=1)


    
    for r in range(mask.shape[0]):
        for c in range(mask.shape[1]):
            if mask[r,c]>0:

                uptake = uptake_annual[:,r,c]
                pt = no3_storage_annual[:,r,c] / uptake
                damkholer_num[:,r,c] = travel_time_annual[:,r,c] /pt
                processing_time[:,r,c] = pt

            else:
                processing_time[:,r,c] = np.nan
                damkholer_num[:,r,c] = np.nan

    processing_time.flush()
    damkholer_num.flush()


def calculate_monthly_Damkohler(mode, temp_res, experiment=None):

    depth3 = get_avg_depth()
    work_path = Path.work_path
    
    if experiment is None:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all/'
    else:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all_'+experiment+'/'

    # 打开 memmap 而不是一次性读入
    no3_SMC1 = np.memmap(output_path+'no3_SMC_layer1.bin',
                         dtype=np.float64, mode='r')
    SMC1     = np.memmap(output_path+'SMC_layer1.bin',
                         dtype=np.float64, mode='r')

    no3_SMC2 = np.memmap(output_path+'no3_SMC_layer2.bin',
                         dtype=np.float64, mode='r')
    SMC2     = np.memmap(output_path+'SMC_layer2.bin',
                         dtype=np.float64, mode='r')

    no3_SMC3 = np.memmap(output_path+'no3_SMC_layer3.bin',
                         dtype=np.float64, mode='r')
    SMC3     = np.memmap(output_path+'SMC_layer3.bin',
                         dtype=np.float64, mode='r')

    plant_uptake = np.memmap(output_path+'plant_uptake.bin',
                          dtype=np.float64, mode='r')

    deni_soil = np.memmap(output_path+'deni_soil.bin',
                          dtype=np.float64, mode='r')
    travel    = np.memmap(output_path+'trans_age_SMC_soil_all_depths.bin',
                          dtype=np.float64, mode='r')

    n = len(SMC1)
    soil_deni_thres = 1 / 10 / 365
    processing_time_thres = 1e5

    # 输出文件 memmap
    processing_time = np.memmap(output_path+'processing_time.bin',
                                dtype=np.float64, mode='w+', shape=(n,))
    damkholer_num   = np.memmap(output_path+'damkholer_num.bin',
                                dtype=np.float64, mode='w+', shape=(n,))

    # 分块计算
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        print(i, flush=True)
        j = min(i+chunk_size, n)

        # NO3 storage
        no3_storage = (no3_SMC1[i:j] * SMC1[i:j] * 0.2 +
                       no3_SMC2[i:j] * SMC2[i:j] * 0.2 +
                       no3_SMC3[i:j] * SMC3[i:j] * depth3)

        # soil denitrification
        deni = deni_soil[i:j].copy()
        #deni[deni < soil_deni_thres] = soil_deni_thres

        pu = plant_uptake[i:j].copy()

        # processing time
        pt = no3_storage / (deni + pu)

        pt[np.isnan(pt)] = processing_time_thres
        pt[pt>processing_time_thres] = processing_time_thres

        # damkholer number
        dn = travel[i:j] / pt

        processing_time[i:j] = pt
        damkholer_num[i:j]   = dn

    processing_time.flush()
    damkholer_num.flush()


    """
    df = pd.DataFrame([])
    r = 390
    c = 144
    df['no3_storage'] = no3_storage[:,r,c]
    df['soil_deni'] = soil_deni[:,r,c]
    df['processing_time'] = df['no3_storage'] / df['soil_deni']
    df['travel_time'] = travel_time[:,r,c]
    df['damkholer_num'] = df['travel_time'] / df['processing_time']

    df.to_csv(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/damkholer_num.csv')
    """



def calculate_monthly_Damkohler_debug(mode, temp_res, experiment=None):

    depth3 = get_avg_depth()
    work_path = Path.work_path
    
    if experiment is None:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all/'
    else:
        output_path = work_path + mode + f'/outputs/cali_merged/{temp_res}/all_'+experiment+'/'

    mask = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    shape_3d = (1452, mask.shape[0], mask.shape[1])


    # 打开 memmap 而不是一次性读入
    no3_SMC1 = np.memmap(output_path+'no3_SMC_layer1.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)
    SMC1     = np.memmap(output_path+'SMC_layer1.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)

    no3_SMC2 = np.memmap(output_path+'no3_SMC_layer2.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)
    SMC2     = np.memmap(output_path+'SMC_layer2.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)

    no3_SMC3 = np.memmap(output_path+'no3_SMC_layer3.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)
    SMC3     = np.memmap(output_path+'SMC_layer3.bin',
                         dtype=np.float64, mode='r', shape=shape_3d)

    plant_uptake = np.memmap(output_path+'plant_uptake.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)

    deni_soil = np.memmap(output_path+'deni_soil.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)
    travel    = np.memmap(output_path+'trans_age_SMC_soil_all_depths.bin',
                          dtype=np.float64, mode='r', shape=shape_3d)

    n = len(SMC1)
    soil_deni_thres = 1 / 10 / 365
    processing_time_thres = 1e5

    r = 392
    c = 708
    # NO3 storage
    no3_storage = (no3_SMC1[:,r,c] * SMC1[:,r,c] * 0.2 +
                    no3_SMC2[:,r,c] * SMC2[:,r,c] * 0.2 +
                    no3_SMC3[:,r,c] * SMC3[:,r,c] * depth3)
    # soil denitrification
    deni = deni_soil[:,r,c].copy()
    #deni[deni < soil_deni_thres] = soil_deni_thres

    pu = plant_uptake[:,r,c].copy()

    # processing time
    pt = no3_storage / (deni + pu)

    pt[np.isnan(pt)] = processing_time_thres
    pt[pt>processing_time_thres] = processing_time_thres

    # damkholer number
    dn = travel[:,r,c] / pt

    np.savetxt('/data/scratch/wusongj/paper4/plots/forward_all/pt_debug.txt', pt)
    np.savetxt('/data/scratch/wusongj/paper4/plots/forward_all/age_debug.txt', travel[:,r,c])
    np.savetxt('/data/scratch/wusongj/paper4/plots/forward_all/DA_debug.txt', dn)


def read_outputs(file_path, mask=None, counter_path=None, dtype=np.float64):
    if file_path.split('.')[-1]=='bin':
        data = np.fromfile(file_path, dtype=dtype).reshape(-1, mask.shape[0], mask.shape[1])
    elif file_path.split('.')[-1]=='asc':
        data = np.loadtxt(file_path, skiprows=6)
    
    if counter_path is not None:
        counter = np.loadtxt(counter_path)
        data /= counter
    
    return data


def merge_performance_EU(mode, catchment_list, chainID=None, chainID_list=None, temp_res='yearly'):
    import pickle

    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    os.makedirs(Path.work_path + mode +'/outputs/cali_merged/performance/', exist_ok=True)
    failed_catchments = []

    

    for kk in range(len(vars)):
                
        site_info = pd.read_csv(Path.data_path+'catchment_info/site_info_'+vars[kk]+'.csv', index_col='site')
        KGEs = []
        pbias = []
        site_ids = []
        site_r = []
        site_c = []
        lats = []
        lons = []
        catchments = []
        avg_sim_Q = []
        avg_obs_Q = []
        avg_sim_iso = []
        avg_obs_iso = []
        obs_iso_N = []
        avg_sim_no3 = []
        avg_obs_no3 = []
        obs_no3_N = []

        obs_Q_N = []
        obs_iso_N = []
        obs_no3_N = []

        avg_list = [avg_sim_Q, avg_obs_Q, avg_sim_iso, avg_obs_iso, avg_sim_no3, avg_obs_no3, obs_Q_N, obs_iso_N, obs_no3_N]
        
        df = pd.DataFrame([])

        for xx, catchment_ID in enumerate(catchment_list):

            obs_path = Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/obs/'

            keys = pickle.load(open(obs_path+vars[kk]+'_gauge_list', 'rb'))
            sites = pickle.load(open(obs_path+vars[kk]+'_site_list', 'rb'))
                        
            if len(keys) > 0:
                """
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
                """
                save_path = Path.work_path + mode +'/outputs/cali/' + temp_res + '/' + str(catchment_ID) + '/all/'
                _sim = (np.fromfile(save_path+sim_vars[kk]+'.bin').reshape(16437, -1).T)[:, Info.spin_up:]
                finish_counter = np.loadtxt(save_path+'finish_counter/finish_counter_'+sim_vars[kk]+'.bin.txt')
                _sim /= finish_counter


                _obs = np.fromfile(obs_path+obs_vars[kk]+'_obs.bin').reshape(len(keys), -1)
                _sim += 0.5
                _obs += 0.5
                for i in range(len(keys)):
                    try:
                        idx_row_tmp = site_info.loc[sites[i],:]['idx_row']
                        idx_col_tmp = site_info.loc[sites[i],:]['idx_col']
                        latitude_tmp = site_info.loc[sites[i],:]['latitude']
                        longitude_tmp = site_info.loc[sites[i],:]['longitude']
                        kge_tmp = GEM_tools.kge(_sim[keys[i],:], _obs[i,:])
                        pbias_tmp = GEM_tools.pbias(_sim[keys[i],:], _obs[i,:])
                        catchments.append(catchment_ID)
                        site_r.append(idx_row_tmp)
                        site_c.append(idx_col_tmp)
                        lats.append(latitude_tmp)
                        lons.append(longitude_tmp)
                        KGEs.append(kge_tmp)
                        pbias.append(pbias_tmp)
                        site_ids.append(sites[i])

                        
                        for gg in range(3):
                            sites_tmp = pickle.load(open(obs_path+vars[gg]+'_site_list', 'rb'))
                            _sim_tmp = (np.fromfile(save_path+sim_vars[gg]+'.bin').reshape(16437, -1).T)[:, Info.spin_up:]
                            finish_counter_tmp = np.loadtxt(save_path+'finish_counter/finish_counter_'+sim_vars[0]+'.bin.txt')
                            _sim_tmp /= finish_counter_tmp
                            avg_list[gg*2].append(np.mean(_sim_tmp[keys[i],:]))

                            
                            if os.path.exists(obs_path+obs_vars[gg]+'_obs.bin') and (sites[i] in sites_tmp):
                                idxxx = np.where(np.array((sites_tmp)).astype(np.str_)==sites[i])
                                _obs_tmp = np.fromfile(obs_path+obs_vars[gg]+'_obs.bin').reshape(len(keys), -1)
                                avg_list[gg*2+1].append(np.nanmean(_obs_tmp[idxxx,:]))
                                avg_list[6+gg].append(np.count_nonzero(~np.isnan(_obs_tmp[idxxx,:])))
                            else:
                                avg_list[gg*2+1].append(np.nan)
                                avg_list[6+gg].append(0)
                            
                        #print(keys, i, _sim.shape, _obs.shape)
                        #print(keys, i, KGEs[-1])
                        
                    except Exception as e:
                        print(e)
                        failed_catchments.append(catchment_ID)
                        print(catchment_ID, sites[i], '  went wrong!', _sim.shape, _obs.shape)
                print(xx, catchment_ID, '   done!')

        print(len(site_r), len(site_c), len(lats), len(lons), len(KGEs), len(pbias), len(site_ids))

        df['catchment'] = catchments
        df['site'] = site_ids
        df['site_r'] = site_r
        df['site_c'] = site_c
        df['latitude'] = lats
        df['longitude'] = lons
        df['kge'] = KGEs
        df['pbias'] = pbias
        df['avg_sim_Q'] = avg_list[0]
        df['avg_obs_Q'] = avg_list[1]
        df['obs_Q_N'] = avg_list[6]
        df['avg_sim_iso'] = avg_list[2]
        df['avg_obs_iso'] = avg_list[3]
        df['obs_iso_N'] = avg_list[7]
        df['avg_sim_no3'] = avg_list[4]
        df['avg_obs_no3'] = avg_list[5]
        df['obs_no3_N'] = avg_list[8]
        

        df.set_index(df['site'], drop=True)
        if chainID is None:
            df.to_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_all.csv')
        else:
            df.to_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_'+str(chainID)+'.csv')
        

    failed_catchments = np.unique(failed_catchments)
    failed_catchments = np.array(failed_catchments, dtype=object)
    print(failed_catchments, len(failed_catchments))
    np.savetxt(Path.work_path + mode +'/outputs/cali_merged/performance/failed_catchments.txt', failed_catchments, fmt='%s')


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
        df.sort_values(by='kge', ascending=True, inplace=True)
        print(df)

        valid_idx = np.where(df['kge']>0)[0]
        x = df['site_c'].to_numpy()[valid_idx]
        y = df['site_r'].to_numpy()[valid_idx]
        c = df['kge'].to_numpy()[valid_idx]
        
        sc0 = ax.scatter(x=x, y=y, c=c, s=scatter_size[kk], vmin=0, vmax=0.5, alpha=0.7, cmap='coolwarm_r', zorder=2)
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

def plot_performance_specific_site(mode, site):
    import pickle

    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    scatter_size = [120, 400, 280]
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, np.nan)
    chanmask[tmp>0] = 1
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    exist_flag = False
    kk = 0
    while (not exist_flag) and kk<len(vars):
        try:
            df = pd.read_csv(Path.work_path + mode +'/outputs/cali_merged/performance/performance_'+vars[kk]+'_all.csv')
            df = df[df['site']==site]
            if len(df) > 0:
                catchment = df['catchment'].to_numpy()[0]
                exist_flag = True
            else:
                kk += 1
        except Exception as e:
            kk += 1

    fig, ax = plt.subplots(3,1, figsize=(8,5), dpi=300)
    tindex = pd.date_range('1982-1-1', '2024-12-31')

    for kk in range(len(vars)):
        

        obs_path = Path.data_path+'catchment_info/forward/'+str(catchment)+'/obs/'
        keys = pickle.load(open(obs_path+vars[kk]+'_gauge_list', 'rb'))
        sites = pickle.load(open(obs_path+vars[kk]+'_site_list', 'rb'))
        
        if len(keys) > 0:
            save_path = Path.work_path + mode +'/outputs/cali/monthly/' + str(catchment) + '/all/'
            _sim = (np.fromfile(save_path+sim_vars[kk]+'.bin').reshape(16437, -1).T)[:, Info.spin_up:]
            finish_counter = np.loadtxt(save_path+'finish_counter/finish_counter_'+sim_vars[kk]+'.bin.txt')
            _sim /= finish_counter


            _obs = np.fromfile(obs_path+obs_vars[kk]+'_obs.bin').reshape(len(keys), -1)
            _sim += 0.5
            _obs += 0.5
            for i in range(len(keys)):
                if sites[i] == site:


                    sim = _sim[keys[i],:]
                    obs = _obs[i,:]
                
                    ax[kk].plot(tindex, sim)
                    ax[kk].scatter(tindex, obs, s=2)

                    print(GEM_tools.kge(_sim[keys[i],:], _obs[i,:]))

        
        

    fig.savefig(Path.work_path+'plots/'+mode+'/performance/performance_'+site+'.png')






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

def young_water_fraction(catchment_ID, young_water_thres, experiment=None):
    if experiment is None:
        output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+str(catchment_ID)+'/all/'
    else:
        output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+str(catchment_ID)+'/all_'+experiment+'/'

    fdir = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/fdir.asc', skiprows=6).astype(np.int64)
    mask = np.full(fdir.shape, False)
    mask[fdir!=-9999] = True

    depth3 = get_avg_depth()
    sm1 = read_outputs(output_path+'SMC_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    sm2 = read_outputs(output_path+'SMC_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    sm3 = read_outputs(output_path+'SMC_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    vadose = read_outputs(output_path+'vadose'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'vadose'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    chanS = read_outputs(output_path+'channel_storage'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'channel_storage'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)


    inftr = read_outputs(output_path+'infiltration'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'infiltration'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc1 = read_outputs(output_path+'perc_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc2 = read_outputs(output_path+'perc_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc3 = read_outputs(output_path+'perc_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31

    rinftr = read_outputs(output_path+'rinfiltration'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rinfiltration'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc1 = read_outputs(output_path+'rperc_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc2 = read_outputs(output_path+'rperc_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc3 = read_outputs(output_path+'rperc_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31



    interf_out = read_outputs(output_path+'interflow_output'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'interflow_output'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    interf_toChn = read_outputs(output_path+'interflow_toChn'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'interflow_toChn'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    GWf_toChn = read_outputs(output_path+'GWflow_toChn'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'GWflow_toChn'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    discharge = read_outputs(output_path+'discharge'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'discharge'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31 * 86400 / (5000*5000)

    irrigation_GW = read_outputs(output_path+'irrigation_from_GW'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'irrigation_from_GW'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    #irrigation_river = read_outputs(output_path+'irrigation_from_river'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'irrigation_from_GW'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31


    """
    sm1 = np.fromfile(output_path+'SMC_layer1.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) / \
    sm2 = np.fromfile(output_path+'SMC_layer2.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    sm3 = np.fromfile(output_path+'SMC_layer3.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    vadose = np.fromfile(output_path+'vadose.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    chanS = np.fromfile(output_path+'channel_storage.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    

    inftr = np.fromfile(output_path+'infiltration.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc1 = np.fromfile(output_path+'perc_layer1.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc2 = np.fromfile(output_path+'perc_layer2.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc3 = np.fromfile(output_path+'perc_layer3.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31

    interf_out = np.fromfile(output_path+'interflow_output.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    interf_toChn = np.fromfile(output_path+'interflow_toChn.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    GWf_toChn = np.fromfile(output_path+'GWflow_toChn.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    discharge = np.fromfile(output_path+'discharge.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31 * 86400 / (5000*5000)

    irrigation_GW = np.fromfile(output_path+'irrigation_from_GW.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    """

    
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
            S_sm1[r,c] = Mix_age_distribution(S_sm1[r,c], sm1[r,c,t]*0.2, np.append(np.array([1]), np.zeros(59)), inftr[r,c,t]+rinftr[r,c,t])
            S_sm1[r,c] = Mix_age_distribution(S_sm1[r,c], sm1[r,c,t]*0.2, S_GW[r,c], irrigation_GW[r,c,t])
            YF_sm1[r,c,t] = np.sum(S_sm1[r,c,:young_water_thres]) / np.sum(S_sm1[r,c])

            # === Soil layer 2 ===
            S_sm2[r,c] = Mix_age_distribution(S_sm2[r,c], sm2[r,c,t]*0.2, S_sm1[r,c], perc1[r,c,t]+rperc1[r,c,t])
            YF_sm2[r,c,t] = np.sum(S_sm2[r,c,:young_water_thres]) / np.sum(S_sm2[r,c])

            # === Soil layer 3 ===
            S_sm3[r,c] = Mix_age_distribution(S_sm3[r,c], sm3[r,c,t]*depth3, S_sm2[r,c], perc2[r,c,t]+rperc2[r,c,t])
            YF_sm3[r,c,t] = np.sum(S_sm3[r,c,:young_water_thres]) / np.sum(S_sm3[r,c])


            # === Vadose zone ===
            S_vadose[r,c] = Mix_age_distribution(S_vadose[r,c], vadose[r,c,t], S_sm3[r,c], perc3[r,c,t]+rperc3[r,c,t])
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

    #S_chanS_dry.tofile(output_path+'age_pdf_chanS_dry.bin')
    #S_chanS_wet.tofile(output_path+'age_pdf_chanS_wet.bin')
    #S_vadose_dry.tofile(output_path+'age_pdf_vadose_dry.bin')
    #S_vadose_wet.tofile(output_path+'age_pdf_vadose_wet.bin')
    YF_sm1.tofile(output_path+'young_water_fraction_sm1.bin')
    YF_sm2.tofile(output_path+'young_water_fraction_sm2.bin')
    YF_sm3.tofile(output_path+'young_water_fraction_sm3.bin')
    #YF_vadose.tofile(output_path+'young_water_fraction_vadose.bin')
    YF_chanS.tofile(output_path+'young_water_fraction_chanS.bin')

    print(catchment_ID, '  done!', flush=True)

       
    #fig, ax = plt.subplots(2,3, dpi=300)
    #ax[0,0].imshow(np.mean(YF_sm1[:,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,1].imshow(np.mean(YF_sm2[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,2].imshow(np.mean(YF_sm3[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[1,0].imshow(np.mean(YF_vadose, axis=0), vmin=0, vmax=1)
    #ax[1,1].imshow(np.mean(YF_chanS, axis=0), vmin=0, vmax=0.3)
    #ax[1,2].imshow(np.mean(discharge, axis=2))
    #ax[1,2].plot(np.nanmean(S_vadose_dry.transpose(1,2,0)[mask], axis=0))
    #ax[1,2].plot(np.nanmean(S_vadose_wet.transpose(1,2,0)[mask], axis=0))


    #fig.savefig('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/run_model/zzz.png')

def calculate_additional_parameters(mode, temp_res, experiment=None):

    if experiment is None:
        save_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'
    else:
        save_path = Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all_'+experiment+'/'
    
    depth3 = get_avg_depth()


    # ET
    A = np.memmap(save_path+'soil_evap.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'transp.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'Evapotranspiration.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        C[i:j] = A[i:j] + B[i:j]
    C.flush()
    del A, B, C

    


    # Total water storage
    A = np.memmap(save_path+'SMC_layer1.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'SMC_layer2.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'SMC_layer3.bin', dtype=np.float64, mode="r")
    D = np.memmap(save_path+'vadose.bin', dtype=np.float64, mode="r")
    E = np.memmap(save_path+'snow_depth.bin', dtype=np.float64, mode="r")
    F = np.memmap(save_path+'total_water_storage.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        F[i:j] = A[i:j]*0.2 + B[i:j]*0.2 + C[i:j]*depth3 + D[i:j] + E[i:j]
    F.flush()
    del A, B, C, D, E, F


    # Nitrogen storage
    A = np.memmap(save_path+'SMC_layer1.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'SMC_layer2.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'SMC_layer3.bin', dtype=np.float64, mode="r")
    D = np.memmap(save_path+'no3_SMC_layer1.bin', dtype=np.float64, mode="r")
    E = np.memmap(save_path+'no3_SMC_layer2.bin', dtype=np.float64, mode="r")
    F = np.memmap(save_path+'no3_SMC_layer3.bin', dtype=np.float64, mode="r")
    G = np.memmap(save_path+'nitrogen_storage.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        G[i:j] = A[i:j]*D[i:j]*0.2 + B[i:j]*E[i:j]*0.2 + C[i:j]*F[i:j]*depth3
        print(i, j)
    G.flush()
    del A, B, C, D, E, F, G

    # Nitrogen leaching from soils
    A = np.memmap(save_path+'perc_layer3.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'no3_SMC_layer3.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'nitrogen_leaching.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        C[i:j] = A[i:j]*B[i:j]
        print(i)
    C.flush()
    del A, B, C



    # Soil travel time
    A = np.memmap(save_path+'trans_age_SMC_layer1.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'trans_age_SMC_layer2.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'trans_age_SMC_layer3.bin', dtype=np.float64, mode="r")
    D = np.memmap(save_path+'trans_age_SMC_soil_all_depths.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        D[i:j] = (A[i:j] * 0.2 + B[i:j] * 0.2 + C[i:j] * depth3) / (0.2+0.2+depth3)
    D.flush()
    del A, B, C, D


    # Soil water age
    A = np.memmap(save_path+'age_SMC_layer1.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'age_SMC_layer2.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'age_SMC_layer3.bin', dtype=np.float64, mode="r")
    D = np.memmap(save_path+'age_SMC_soil_all_depths.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        D[i:j] = (A[i:j] * 0.2 + B[i:j] * 0.2 + C[i:j] * depth3) / (0.2+0.2+depth3)
    D.flush()
    del A, B, C, D



    # Soil young water fraction
    A = np.memmap(save_path+'young_water_fraction_sm1.bin', dtype=np.float64, mode="r")
    B = np.memmap(save_path+'young_water_fraction_sm2.bin', dtype=np.float64, mode="r")
    C = np.memmap(save_path+'young_water_fraction_sm3.bin', dtype=np.float64, mode="r")
    D = np.memmap(save_path+'young_water_fraction_soil_all_depths.bin', dtype=np.float64, mode="w+", shape=A.shape)
    n = len(A)
    chunk_size = n//10
    for i in range(0, n, chunk_size):
        j = min(i+chunk_size, n)
        D[i:j] = (A[i:j] * 0.2 + B[i:j] * 0.2 + C[i:j] * depth3) / (0.2+0.2+depth3)
    D.flush()
    del A, B, C, D



def sort_statistics_by_countries(mode, temp_res):
    import pickle
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    vars = ['Precipitation_npfloat32_3035', 'young_water_fraction_soil_all_depths', 'infiltration', 'soil_evap', 'transp', 'discharge', 'deni_soil', 'damkholer_num']
    vars = [var+'.bin' for var in vars]
    with open(Path.data_path+'catchment_info/country_codes.pkl', 'rb') as f:
        country_dict = pickle.load(f)

    country_distribution = np.loadtxt(Path.data_path+'catchment_info/world_map_3035.asc', skiprows=6)

    df = pd.DataFrame([], index=country_dict.keys())

    for var in vars:
        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])    

        if '_map' in var:
            var = var[:-4]


        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)

        if var == 'damkholer_num':
            _data[_data>2] = 2


        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        data = []
        for key in country_dict.keys():
            country_mask = np.isin(country_distribution, country_dict.get(key))
            data.append(np.nanmean(_data[:,country_mask]))
        
        df[var] = data
        print(df)

    df = df.round(1)
    df.to_csv(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/country_statistics.csv')


def plot_typical_regions(mode, temp_res):
    import pickle

    os.makedirs(Path.work_path+'plots/'+mode+'/typical_regions', exist_ok=True)

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    dominant_landuse = np.loadtxt(Path.data_path+'catchment_info/dominant_landuse.asc', skiprows=6)

    vars = ['young_water_fraction_soil_all_depths']
    vars = [var+'.bin' for var in vars]

    typical_regions = ['west_coast', 'mountains', 'west_lowlands', 'east_lowlands', 'south_region' ]

    for typical_region in typical_regions:
        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)

        data = np.loadtxt(Path.data_path+'catchment_info/typical_regions/typical_regions_'+typical_region+'.asc', skiprows=6)
        data[data!=1] = np.nan
        
        ax.imshow(mask, cmap='Purples_r', alpha=0.3, zorder=0, label='1')
        ax.imshow(data, cmap='Greys_r', alpha=0.8, zorder=1)

        ax.axis('off')
        print(typical_region)
        fig.savefig(Path.work_path+'plots/'+mode+'/typical_regions/distribution_'+typical_region+'_'+'.png', transparent=True)



def plot_typical_regions_Ts(mode, temp_res):
    import pickle

    os.makedirs(Path.work_path+'plots/'+mode+'/typical_regions', exist_ok=True)

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    region_masks = []

    dominant_landuse = np.loadtxt(Path.data_path+'catchment_info/dominant_landuse.asc', skiprows=6)

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'central_west_europe_with_lower_age'+'.asc', skiprows=6)
    ywf_diff = np.loadtxt('/data/scratch/wusongj/paper4/plots/forward_all/asc/young_water_fraction_soil_all_depths_diff.asc', skiprows=6)
    mask_tmp = np.logical_and(mask_tmp>0, ywf_diff<0)
    region_masks.append(mask_tmp)
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'northern_europe'+'.asc', skiprows=6)
    mask_tmp = mask_tmp > 0
    region_masks.append(mask_tmp)
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'eastern_europe'+'.asc', skiprows=6)
    mask_tmp = mask_tmp > 0
    region_masks.append(mask_tmp)
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    mask_tmp = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/typical_regions/typical_regions_Ts_'+'southern_europe'+'.asc', skiprows=6)
    #mask_tmp = np.logical_and(mask_tmp>0, ywf_diff>0)
    mask_tmp = mask_tmp > 0
    region_masks.append(mask_tmp)
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse==1))
    #region_masks.append(np.logical_and(mask_tmp, dominant_landuse!=1))

    region_names = ['west', 'north', 'east', 'south']

    for xx, region_mask in enumerate(region_masks):
        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)

        data = np.full(region_mask.shape, np.nan)
        data[region_mask] = 1
        
        ax.imshow(mask, cmap='Purples_r', alpha=0.3, zorder=0, label='1')
        ax.imshow(data, cmap='Greys_r', alpha=0.8, zorder=1)

        ax.axis('off')
        fig.savefig(Path.work_path+'plots/'+mode+'/typical_regions/distribution_'+region_names[xx]+'_'+'.png', transparent=True)


        

def plot_pdf_by_typical_regions(mode, temp_res):
    import pickle

    os.makedirs(Path.work_path+'plots/'+mode+'/typical_regions', exist_ok=True)

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    dominant_landuse = np.loadtxt(Path.data_path+'catchment_info/dominant_landuse.asc', skiprows=6)

    vars = ['young_water_fraction_soil_all_depths', 'damkholer_num', 'nitrogen_leaching']
    vars = [var+'.bin' for var in vars]

    nbins_list = [40, 40, 40]
    bin_min_list = [0, -1, 0]
    bin_max_list = [60, 1, 120]
    bin_upper_cap_list = [110, 2.5, 500]

    typical_regions = ['west_coast', 'mountains', 'west_lowlands', 'east_lowlands', 'south_region' ]

    for typical_region in typical_regions:
        locals()[typical_region] = np.loadtxt(Path.data_path+'catchment_info/typical_regions/typical_regions_'+typical_region+'.asc', skiprows=6)



    for xx, var in enumerate(vars):
        
        extension = var.split('.')[-1]
        var = ('.').join(var.split('.')[:-1])    

        if '_map' in var:
            var = var[:-4]


        try:
            _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        except Exception as e:
            try:
                _data = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
            except:
                _data = read_outputs(Path.data_path+'catchment_info/climate_3035_tmp/'+var+'.'+extension, mask, dtype=np.float32)


        _data = np.mean(_data, axis=0)

        if var == 'damkholer_num':
            _data = np.log10(_data)
            _data[_data>2] = 2

        _data *= var_info[var][1]  # weight
        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        

        ylim_max = 0.2
        ylim_min = -0.05

        fig, ax = plt.subplots(len(typical_regions), 1, figsize=(2.7, 10), dpi=300)
        plt.subplots_adjust(left=0.04, bottom=0.04, right=0.98, top=0.98, wspace=0.15, hspace=0.15)

        for yy, typical_region in enumerate(typical_regions):
            data = _data[locals()[typical_region]==1]
            dominant_landuse_typical_region = dominant_landuse[locals()[typical_region]==1]
            idx = np.where(~(np.isnan(data)))
            data = data[idx]
            dominant_landuse_typical_region = dominant_landuse_typical_region[idx]
            print(var, np.mean(data), data.shape)

            # Define bins for histogram
            nbins = nbins_list[xx]
            bin_min = bin_min_list[xx]
            bin_max = bin_max_list[xx]
            bin_upper_cap = bin_upper_cap_list[xx]
            bins = np.append(np.arange(bin_min, bin_max, ((bin_max-bin_min)/nbins)), bin_upper_cap)
            categories = ['urban', 'crop', 'pasture', 'grass', 'forest', 'sparse']
            colors = {"urban": "gray", "crop":"red", "pasture":"salmon", "grass": "gold", "forest": "green", "sparse": "blueviolet"}

            # Calculate fractions for each bin
            bin_centers = (bins[:-1] + bins[1:]) / 2
            bin_centers[-1] = bin_centers[-2] + (bin_centers[-2] - bin_centers[-3]) * 5


            
            # Overlay the total histogram line (normalized to fraction=1)
            total_counts, _ = np.histogram(data, bins=bins)
            pdf = total_counts / total_counts.sum()
            ax[yy].plot(bin_centers, pdf,
                    color='black', lw=2, label='Total histogram', zorder=5)
       
            # Count per category
            counts_per_cat = []
            for cat in np.arange(0, len(categories), 1):
                counts, _ = np.histogram(data[dominant_landuse_typical_region == cat], bins=bins)
                counts_per_cat.append(counts)

            counts_per_cat = np.array(counts_per_cat)  # shape: (n_cat, n_bins-1)

            # Convert to fractions
            totals = counts_per_cat.sum(axis=0)
            fractions_per_cat = counts_per_cat / totals[np.newaxis, :]
            fractions_per_cat[:, totals == 0] = 0  # avoid NaNs


            #if typical_region=='west_lowlands':
            #    for i in range(fractions_per_cat.shape[1]):
            #        if np.sum(fractions_per_cat[:,i])!=0:
            #            print(i, fractions_per_cat[:,i])



            # Stack-fill under the curve
            bottom = np.full(len(bin_centers), ylim_min)

            for i, cat in enumerate(categories):
                top = bottom + fractions_per_cat[i] * (pdf - ylim_min) * 0.98  #ylim_max * 0.99
                ax[yy].fill_between(bin_centers, bottom, top,
                                color=colors[cat], linewidth=0, alpha=0.3, step='mid', label=cat, zorder=0)
                bottom = top

                

            

            ax[yy].set_ylim(ylim_min, ylim_max)
            ax[yy].set_xlim([bin_centers[0]-(bin_centers[-1]-bin_centers[0])*0.05, bin_centers[-1]+(bin_centers[-1]-bin_centers[0])*0.05])
            ax[yy].set_xticks([bin_centers[0], np.mean(bin_centers[[0,-2]]), bin_centers[-2], bin_centers[-1]])
            ax[yy].set_yticks([0, ylim_max/2, ylim_max])
            ax[yy].set_xticklabels([])
            ax[yy].set_yticklabels([])
            ax[yy].tick_params(direction='out', length=7, width=2)
            [x.set_linewidth(2) for x in ax[yy].spines.values()]
        fig.savefig(Path.work_path+'plots/'+mode+'/typical_regions/pdf_'+var+'.png', transparent=True)
            
        






        




# The distance of at least 1% of precipitation can travel
def flow_path_length(catchment_ID, experiment=None):

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

    if experiment is None:
        output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+str(catchment_ID)+'/all/'
    else:
        output_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+str(catchment_ID)+'/all_'+experiment+'/'

    fdir = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/fdir.asc', skiprows=6).astype(np.int64)
    mask = np.full(fdir.shape, False)
    mask[fdir!=-9999] = True

    depth3 = get_avg_depth()

    sm1 = read_outputs(output_path+'SMC_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    sm2 = read_outputs(output_path+'SMC_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    sm3 = read_outputs(output_path+'SMC_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'SMC_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    vadose = read_outputs(output_path+'vadose'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'vadose'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)
    #chanS = read_outputs(output_path+'channel_storage'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'channel_storage'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0)


    inftr = read_outputs(output_path+'infiltration'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'infiltration'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc1 = read_outputs(output_path+'perc_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc2 = read_outputs(output_path+'perc_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    perc3 = read_outputs(output_path+'perc_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'perc_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rinftr = read_outputs(output_path+'rinfiltration'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rinfiltration'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc1 = read_outputs(output_path+'rperc_layer1'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer1'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc2 = read_outputs(output_path+'rperc_layer2'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer2'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    rperc3 = read_outputs(output_path+'rperc_layer3'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'rperc_layer3'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31


    interf_out = read_outputs(output_path+'interflow_output'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'interflow_output'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    #interf_toChn = read_outputs(output_path+'interflow_toChn'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'interflow_toChn'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    #GWf_toChn = read_outputs(output_path+'GWflow_toChn'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'GWflow_toChn'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31
    #discharge = read_outputs(output_path+'discharge'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'discharge'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31 * 86400 / (5000*5000)

    #irrigation_GW = read_outputs(output_path+'irrigation_from_GW'+'_map.bin', counter_path=output_path+'finish_counter/finish_counter_'+'irrigation_from_GW'+'_map.bin.txt', mask=mask, dtype=np.float64).transpose(1,2,0) * 31

    

    """
    sm1 = np.fromfile(output_path+'SMC_layer1.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    sm2 = np.fromfile(output_path+'SMC_layer2.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    sm3 = np.fromfile(output_path+'SMC_layer3.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    vadose = np.fromfile(output_path+'vadose.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    chanS = np.fromfile(output_path+'channel_storage.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0)
    

    inftr = np.fromfile(output_path+'infiltration.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc1 = np.fromfile(output_path+'perc_layer1.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc2 = np.fromfile(output_path+'perc_layer2.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    perc3 = np.fromfile(output_path+'perc_layer3.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    interf_out = np.fromfile(output_path+'interflow_output.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    interf_toChn = np.fromfile(output_path+'interflow_toChn.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    GWf_toChn = np.fromfile(output_path+'GWflow_toChn.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    discharge = np.fromfile(output_path+'discharge.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31 * 86400 / (5000*5000)

    irrigation_GW = np.fromfile(output_path+'irrigation_from_GW.bin').reshape(-1, mask.shape[0], mask.shape[1]).transpose(1,2,0) * 31
    """
    
    T_total = inftr.shape[-1]
    sorted_cells, inflow_map = sort_grid_cells_d8(fdir, mask)

    flow_length = np.full((mask.shape[0], mask.shape[1], T_total), 0.0)
    


    #for t in range(24,60):
    for t in range(T_total):
        p_origin = np.full((mask.shape[0], mask.shape[1]), 1.0)
        for i in range(len(sorted_cells)):
            r, c = sorted_cells[i]

            # === Soil layer 1 ===
            p_origin[r,c] *= (inftr[r,c,t]+rinftr[r,c,t]) / sm1[r,c,t]*0.2

            # === Soil layer 2 ===
            p_origin[r,c] *= (perc1[r,c,t]+rperc1[r,c,t]) / sm2[r,c,t]*0.2

            # === Soil layer 3 ===
            p_origin[r,c] *= (perc2[r,c,t]+rperc2[r,c,t]) / sm3[r,c,t]*depth3


            # === Vadose zone ===
            p_origin[r,c] *= (perc3[r,c,t]+rperc3[r,c,t]) / vadose[r,c,t]

            # === Interflow routing ===
            if fdir[r,c] not in directions.keys():
                continue
            while p_origin[r,c] > 0.01:
                dr, dc = directions[fdir[r,c]]
                p_origin[r,c] *= interf_out[r,c,t] / (interf_out[r,c,t]+vadose[r+dr,c+dc,t])
                if p_origin[r,c] > 0.01:
                    flow_length[r,c,t] += 1


    flow_length = flow_length.transpose(2,0,1)
    flow_length.tofile(output_path+'interflow_length.bin')

    print(catchment_ID, '  done!', flush=True)

       
    #fig, ax = plt.subplots(2,3, dpi=300)
    #ax[0,0].imshow(np.nanmean(flow_length[:,:,:], axis=2), vmin=0, vmax=10)
    #ax[0,1].imshow(np.mean(YF_sm2[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[0,2].imshow(np.mean(YF_sm3[24:60,:,:], axis=0), vmin=0, vmax=1)
    #ax[1,0].imshow(np.mean(YF_vadose, axis=0), vmin=0, vmax=1)
    #ax[1,1].imshow(np.mean(YF_chanS, axis=0), vmin=0, vmax=0.3)
    #ax[1,2].imshow(np.mean(discharge, axis=2))
    #ax[1,2].plot(np.nanmean(S_vadose_dry.transpose(1,2,0)[mask], axis=0))
    #ax[1,2].plot(np.nanmean(S_vadose_wet.transpose(1,2,0)[mask], axis=0))


    #fig.savefig('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/run_model/zzz.png')



def plot_interflow_path(mode, catchment_list, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):

    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401, needed for 3D plotting
    from matplotlib import cm
    import pickle
    import sys

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
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    dem = np.loadtxt(Path.data_path+'catchment_info/dem_5km_interpolated.asc', skiprows=6)
    dem[dem<0] = 0
    
    #dem = np.power(dem, 0.8)
    dem = np.power(dem, 1/2)
    dem[~mask] = 0


    # Merge flow direction
    if not os.path.exists(Path.data_path+'catchment_info/flow_direction.asc'):
        for xx, catchment_ID in enumerate(catchment_list):
            output_path = Path.data_path + 'catchment_info/forward/' + str(catchment_ID) + '/spatial/'
            upper_left_coord = (np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/upper_left_coord.txt')).astype(np.int64)
            mask_small = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/dem.asc', skiprows=6)
            mask_small = mask_small!=-9999
            
            data_small = np.loadtxt(Path.data_path + 'catchment_info/forward/' + str(catchment_ID) + '/spatial/fdir.asc', skiprows=6)
            
            if xx == 0:
                data_large = np.full((dem.shape[0], dem.shape[1]), np.nan)

            data_large = GIS_tools.from_catchment_to_EU(upper_left_coord, mask_small, data_large, data_small)
        GEM_tools.create_asc(data_large, Path.data_path+'catchment_info/flow_direction.asc', Path.data_path+'catchment_info/land_mask_3035.asc')

    # Sort the flow path
    if (not os.path.exists(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/flow_path_list_mean')) or replace:
        var = 'interflow_length'
        extension = 'bin'
        fdir = np.loadtxt(Path.data_path+'catchment_info/flow_direction.asc', skiprows=6).astype(np.int64)
        flow_path = []
        flow_length = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        flow_length = np.mean(flow_length, axis=0)
        
        for r in range(dem.shape[0]):
            for c in range(dem.shape[1]):
                if flow_length[r, c] >= 1:
                    tmp = [[r, c, dem[r, c]]]
                    r_, c_ = r, c
                    for tt in range(int(flow_length[r, c]+1)):
                        if fdir[r_, c_] in directions.keys():
                            dr, dc = directions[fdir[r_, c_]]
                            r_ += dr
                            c_ += dc
                            tmp.append([r_, c_, dem[r_, c_]])
                    flow_path.append(tmp)
                else:
                    flow_path.append([])

        with open(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/flow_path_list_mean', 'wb') as handle:
            pickle.dump(flow_path, handle)
    
    # Sort the flow path
    if (not os.path.exists(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/flow_path_list_max'))  or replace:
        var = 'interflow_length'
        extension = 'bin'
        fdir = np.loadtxt(Path.data_path+'catchment_info/flow_direction.asc', skiprows=6).astype(np.int64)
        flow_path = []
        flow_length = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/'+var+'.'+extension, mask)
        flow_length = np.max(flow_length, axis=0)
        
        for r in range(dem.shape[0]):
            for c in range(dem.shape[1]):
                if flow_length[r, c] >= 1:
                    tmp = [[r, c, dem[r, c]]]
                    r_, c_ = r, c
                    for tt in range(int(flow_length[r, c]+1)):
                        if fdir[r_, c_] in directions.keys():
                            dr, dc = directions[fdir[r_, c_]]
                            r_ += dr
                            c_ += dc
                            tmp.append([r_, c_, dem[r_, c_]])
                    flow_path.append(tmp)
                else:
                    flow_path.append([])

        with open(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/flow_path_list_max', 'wb') as handle:
            pickle.dump(flow_path, handle)

                

    # Build RGBA facecolors
    colors = np.ones((*dem.shape, 4))  # base white and fully opaque
    # Set ocean cells to blue (RGBA)
    #colors[~mask] = [0.2, 0.4, 1.0, 0.3]  # light blue
    colors[~mask] = [0,0,0,0]  # Transparency

    # Optional: make land transparent (or apply terrain colormap)
    # colors[~ocean_mask] = [1, 1, 1, 0]  # fully transparent
    # or:
    norm = (dem -np.percentile(dem[mask], 0.1)) / (dem[mask].max() - np.percentile(dem[mask], 0.1))
    norm = 0.6 + norm/1.6
    colors[mask] = cm.Greys_r(norm[mask])  # apply colormap only to land
    colors[..., 3][mask] = 0.7

    
    # Verify no NaNs
    #if np.isnan(dem).any():
    #    dem = np.nan_to_num(dem, nan=0.0)
    #dem = np.ma.masked_invalid(dem)
    
    

    rows, cols = dem.shape
    x = np.linspace(0, cols, cols)  # Adjust range as needed (e.g., real-world coords)
    y = np.linspace(0, rows, rows)
    X, Y = np.meshgrid(x, y[::-1])

    #X = np.flip(X, axis=1)
    #dem = np.flip(dem, axis=0)
    #dem = np.flip(dem, axis=1)
    #colors = np.flip(colors, axis=0)
    #colors = np.flip(colors, axis=1)


    fig, _ = plt.subplots(1,1, figsize=(15,15), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.2, hspace=0.2)


  
    surf = ax.plot_surface(X, Y, dem, 
                            facecolors=colors,
                            edgecolor='none',         # Black grid
                            linewidth=0,
                            #alpha=0.8,
                            antialiased=False,
                            shade=False,
                            rstride=1, cstride=1,
                            zorder=0)



    #ax.set_xlim(dem.shape[1], 0)
    ax.set_zlim(0, np.max(dem)*10)

    

    
    with open(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/flow_path_list_max', 'rb') as handle:
        flow_path = pickle.load(handle)
    
    counter = 0
    
    flow_length = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/interflow_length.bin', mask)
    flow_length = np.max(flow_length, axis=0)

    flow_length_int = flow_length.astype('int')
        
    cmap = get_cmcrameri_cmap('acton', start=0, end=0.9, alpha=0.7)
    cmap = cm.GnBu
    
    for bb, f_length in enumerate(np.unique(flow_length_int)):
        if f_length > 0:
            #print(bb, len(np.unique(flow_length)))
            for tt in range(len(flow_path)):
                if len(flow_path[tt]) == f_length:
                    coord = np.asarray(flow_path[tt])
                    nn = flow_length[int(coord[0,0]), int(coord[0,1])]
                    weight = np.min([(nn-1)/(20-1), 1])
                    weight = np.max(weight, 0)

                
                    line_color = cmap(weight)
                    

                    linewidth = 0.1 + (nn/10) * 1.4
                    if linewidth > 1.5:
                        linewidth = 1.5
                    



                    alpha = 0.3 + (nn/10) * 0.5
                    if alpha > 0.8:
                        alpha = 0.8
                    

                    # For max flow path only
                    linewidth *= 0.3
                    alpha *= 0.2

                    ax.plot(coord[:,1], dem.shape[0]-coord[:,0], coord[:,2]+dem[coord[:,0].astype(int), coord[:,1].astype(int)]*0.05, color=line_color, linewidth=linewidth, alpha=alpha, zorder=3+bb)
                    counter += 1
        
        
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    ax.set_axis_off()

    #ax.view_init(elev=60, azim=100)  # Clear view angle
    ax.view_init(elev=60, azim=-90)  # Clear view angle
    #ax.view_init(elev=90, azim=90)  # Clear view angle

    ax.axis('off')

    fig.savefig(Path.work_path+'plots/'+mode+'/interflow_length_3d.png', transparent=True)
    print('Figure saved at :   ' + Path.work_path+'plots/'+mode+'/interflow_length_3d.png')



def plot_interflow_connection(mode, catchment_list, chainID, chainID_list, vars, temp_res, replace=False, yearly_flag=False):

    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401, needed for 3D plotting
    from matplotlib import cm
    import pickle
    import sys

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
    
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, False)
    mask[tmp>0] = True

    dem = np.loadtxt(Path.data_path+'catchment_info/dem_5km_interpolated.asc', skiprows=6)
    dem[dem<0] = 0
    
    #dem = np.power(dem, 0.8)
    dem = np.power(dem, 1/2)
    dem[~mask] = 0


    flow_length = read_outputs(Path.work_path + mode +'/outputs/cali_merged/'+temp_res+'/all/interflow_length.bin', mask)
    data = np.full((flow_length.shape[1], flow_length.shape[2]), 0.0)
    for r in range(flow_length.shape[1]):
        for c in range(flow_length.shape[2]):
            if mask[r,c]:
                tmp = flow_length[:,r,c]
                data[r,c] = np.sum(tmp>0) / len(tmp)
 
    # Build RGBA facecolors
    colors = np.ones((*dem.shape, 4))  # base white and fully opaque
    # Set ocean cells to blue (RGBA)
    #colors[~mask] = [0.2, 0.4, 1.0, 0.3]  # light blue
    colors[~mask] = [0,0,0,0]  # Transparency

    # Optional: make land transparent (or apply terrain colormap)
    # colors[~ocean_mask] = [1, 1, 1, 0]  # fully transparent
    # or:
    norm = (data - 0) / (0.5 - 0)
    colors[mask] = cm.viridis(norm[mask])  # apply colormap only to land
    colors[..., 3][mask] = 0.8

    
    # Verify no NaNs
    #if np.isnan(dem).any():
    #    dem = np.nan_to_num(dem, nan=0.0)
    #dem = np.ma.masked_invalid(dem)
    
    

    rows, cols = dem.shape
    x = np.linspace(0, cols, cols)  # Adjust range as needed (e.g., real-world coords)
    y = np.linspace(0, rows, rows)
    X, Y = np.meshgrid(x, y[::-1])

    #X = np.flip(X, axis=1)
    #dem = np.flip(dem, axis=0)
    #dem = np.flip(dem, axis=1)
    #colors = np.flip(colors, axis=0)
    #colors = np.flip(colors, axis=1)


    fig, _ = plt.subplots(1,1, figsize=(15,15), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection='3d')


  
    surf = ax.plot_surface(X, Y, dem, 
                            facecolors=colors,
                            edgecolor='none',         # Black grid
                            linewidth=0,
                            #alpha=0.8,
                            antialiased=False,
                            shade=False,
                            rstride=1, cstride=1,
                            zorder=0)



    #ax.set_xlim(dem.shape[1], 0)
    ax.set_zlim(0, np.max(dem)*10)

    
    
    # Add colorbar
    #cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
    #cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
    #cbar.ax.tick_params(labelsize=25)
    ax.axis('off')
    ax.set_axis_off()

    #ax.view_init(elev=60, azim=100)  # Clear view angle
    ax.view_init(elev=100, azim=-90)  # Clear view angle
    #ax.view_init(elev=90, azim=90)  # Clear view angle

    fig.savefig(Path.work_path+'plots/'+mode+'/interflow_connection_3d.png')
    print('Figure saved at :   ' + Path.work_path+'plots/'+mode+'/interflow_connection_3d.png')