import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path, Info, Cali, Param, Output
import GEM_tools
import pandas as pd
import GIS_tools


nodata = Info.nodata

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
    Vars = ['d18o_canopy_storage', 'd18o_snow_depth','d18o_pond', None, None, None]
    Vars.extend(['d18o_SMC_layer1', 'd18o_SMC_layer2', 'd18o_SMC_layer3', 'd18o_vadose', 'd18o_groundwater_storage', 'd18o_chanS'])
    Vars.extend(['age_canopy_storage', 'age_snow_depth','age_pond', None, None, None])
    Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_groundwater_storage', None, 'age_chanS'])
    Vars.extend(['no3_canopy_storage', 'no3_snow_depth','no3_pond', None, None, None])
    Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
    Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])
    Vars.extend([None, None, None, None, None, None])

    ylims = [None, None, None, None, None, None]
    ylims.extend([[-15,0],[-15,0],[-15,0],None, None,[-10,0]])
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


def merge_spatial_results_EU(mode, catchment_list, vars, replace=False):

    mask_large = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask_large = mask_large>0

    os.makedirs(Path.work_path + mode +'/outputs/cali_merged/', exist_ok=True)
    
    for var in vars:
        if os.path.exists(Path.work_path + mode +'/outputs/cali_merged/'+var+'.asc') and not replace:
            continue
        data_large = np.full(mask_large.shape, np.nan)
        #counter = 0
        for catchment_ID in catchment_list:
            save_path = Path.work_path + mode +'/outputs/cali/' + str(catchment_ID) + '/'
            upper_left_coord = (np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/upper_left_coord.txt')).astype(np.int64)
            mask_small = np.loadtxt(Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/spatial/dem.asc', skiprows=6)
            mask_small = mask_small!=-9999
            data_small = np.fromfile(save_path+'/'+var+'_map.bin').reshape(-1, mask_small.shape[0], mask_small.shape[1])
            data_small = np.mean(data_small, axis=0)
            data_large = GIS_tools.from_catchment_to_EU(upper_left_coord, mask_small, data_large, data_small)
            #print(var, counter, len(catchment_list))
            #counter += 1
        GEM_tools.create_asc(data_large, Path.work_path + mode +'/outputs/cali_merged/'+var+'.asc', Path.data_path+'catchment_info/land_mask_3035.asc')
        print(var + '  merged and saved at : ' + Path.work_path + mode +'/outputs/cali_merged/'+var+'.asc')
        




def plot_spatial_results_EU(mode, vars, replace=False):

    var_info = {
                'canopy_storage':[[0,2],1000,False],
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
                'soil_evap':[[0,600],1000*365,False],
                'transp_layer1':[[0,200],1000*365,False],
                'transp_layer2':[[0,100],1000*365,False],
                'transp_layer3':[[0,100],1000*365,False],
                'channel_evaporation':[[0,20],1000*365,True],

                'overland_flow_input':[[0,500],1000*365,False],
                'overland_flow_output':[[0,500],1000*365,False],
                'interflow_input':[[0,2000],1000*365,False],
                'interflow_output':[[0,2000],1000*365,False],
                'GWflow_input':[[0,2000],1000*365,False],
                'GWflow_output':[[0,2000],1000*365,False],
                'overland_flow_toChn':[[0,1000],1000*365,True],
                'interflow_toChn':[[0,2000],1000*365,True],
                'GWflow_toChn':[[0,2000],1000*365,True],
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
                'age_groundwater_storage':[[0,4000],1,False],
                'age_chanS':[[0,3500],1,True],

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
                }
    

    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, False)
    chanmask[tmp>0] = True
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1

    for var in vars:
        if os.path.exists(Path.work_path+'plots/'+mode+'/'+var+'.png') and not replace:
            continue
            
        try:
            data = np.loadtxt(Path.work_path + mode +'/outputs/cali_merged/'+var+'.asc', skiprows=6)
        except:
            print(var + '  does not exists!')
            continue
        data *= var_info[var][1]

        if var_info[var][2]:
            data[~chanmask] = np.nan

        vmin = var_info[var][0][0]
        vmax = var_info[var][0][1]

        fig, ax = plt.subplots(1,1, figsize=(15,15), dpi=300)
        ax.imshow(mask, cmap='Purples_r', alpha=0.1, zorder=0, label='1')
        sc0 = ax.imshow(data, vmin=vmin, vmax=vmax, cmap='viridis', zorder=1)
        # Add colorbar
        cbar_ax = fig.add_axes([0.85, 0.4, 0.03, 0.2])
        cbar = fig.colorbar(sc0, cax=cbar_ax, pad=0.02, ticks=[vmin, (vmin+vmax)/2, vmax])
        cbar.ax.tick_params(labelsize=25)
        ax.axis('off')
        fig.savefig(Path.work_path+'plots/'+mode+'/'+var+'.png')
        print(var, np.nanmin(data), np.nanmax(data), np.nanmean(data))
    


def merge_performance(mode, catchment_list):
    import pickle

    vars = ['discharge', 'isotope', 'nitrate']
    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']
    obs_vars = ['discharge', 'd18o_stream', 'no3_stream']

    os.makedirs(Path.work_path + mode +'/outputs/cali/performance/', exist_ok=True)

    for kk in range(len(vars)):
        site_info = pd.read_csv(Path.data_path+'catchment_info/site_info_'+vars[kk]+'.csv', index_col='site')
        KGEs = []
        pbias = []
        site_ids = []
        site_r = []
        site_c = []
        lats = []
        lons = []
        df = pd.DataFrame([])
        for catchment_ID in catchment_list:
            
            save_path = Path.work_path + mode +'/outputs/cali/' + str(catchment_ID) + '/'
            obs_path = Path.data_path+'catchment_info/forward/'+str(catchment_ID)+'/obs/'

            if not os.path.exists(save_path+'age_canopy_storage_map.bin'):
                continue

            keys = pickle.load(open(obs_path+vars[kk]+'_gauge_list', 'rb'))
            sites = pickle.load(open(obs_path+vars[kk]+'_site_list', 'rb'))
            
            if len(keys) > 0:
                _sim = (np.fromfile(save_path+sim_vars[kk]+'.bin').reshape(16437, -1).T)[:, Info.spin_up:]
                _obs = np.fromfile(obs_path+obs_vars[kk]+'_obs.bin').reshape(len(keys), -1)
                _sim += 0.1
                _obs += 0.1
                for i in range(len(keys)):
                    try:
                        site_r.append(site_info.loc[sites[i],:]['idx_row'])
                        site_c.append(site_info.loc[sites[i],:]['idx_col'])
                        lats.append(site_info.loc[sites[i],:]['latitude'])
                        lons.append(site_info.loc[sites[i],:]['longitude'])
                        KGEs.append(GEM_tools.kge(_sim[keys[i],:], _obs[i,:]))
                        pbias.append(GEM_tools.pbias(_sim[keys[i],:], _obs[i,:]))
                        site_ids.append(sites[i])
                        #print(keys, i, _sim.shape, _obs.shape)
                    except:
                        print(sites[i], '  went wrong!')

        
        df['site'] = site_ids
        df['site_r'] = site_r
        df['site_c'] = site_c
        df['latitude'] = lats
        df['longitude'] = lons
        df['kge'] = KGEs
        df['pbias'] = pbias
        df.set_index(df['site'], drop=True)
        df.to_csv(Path.work_path + mode +'/outputs/cali/performance/performance_'+vars[kk]+'.csv')


def plot_performance_EU(mode):
    vars = ['discharge', 'isotope', 'nitrate']
    scatter_size = [120, 400, 280]
    tmp = np.loadtxt(Path.data_path+'catchment_info/channel_length.asc', skiprows=6)
    chanmask = np.full(tmp.shape, np.nan)
    chanmask[tmp>0] = 1
    tmp = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    mask = np.full(chanmask.shape, np.nan)
    mask[tmp>0] = 1
    for kk in range(len(vars)):
        df = pd.read_csv(Path.work_path + mode +'/outputs/cali/performance/performance_'+vars[kk]+'.csv')
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

        fig.savefig(Path.work_path+'plots/'+mode+'/performance_'+vars[kk]+'.png')
