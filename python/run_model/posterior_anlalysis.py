import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path, Info, Cali, Param
import GEM_tools

output_path = Path.output_path
nodata = -9999

"""
fnames = os.listdir(output_path)
for fname in fnames:
    if "_map" in fname and fname.split('.')[-1]=='bin':
        data = np.fromfile(output_path + fname).reshape(-1, 30, 22)
        data = np.mean(data, axis=0)
        data[data==nodata] = np.nan
        data[data==0] = np.nan
        fig, ax = plt.subplots(1,1)
        im = ax.imshow(data, vmin=np.nanmin(data), vmax=np.nanmax(data))
        fig.colorbar(im, ax=ax)
        fig.savefig(output_path + '0_' + fname.split('.')[0] + '.png', dpi=600)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')
        print(np.nanmin(data), np.nanmean(data), np.nanmax(data), '\n')
        #print(data[:, 9//2])
        #print(data, np.sum(~np.isnan(data)))


    elif fname.split('.')[-1]=='bin' and "_map" not in fname:
        
        data = (np.fromfile(output_path + fname).reshape(-1, 1).T)[:, Info.spin_up:]
        data[data==nodata] = np.nan
        fig, ax = plt.subplots(1,1, figsize=(4,2), dpi=100)
        for kk in range(1):
            ax.plot(data[kk], linewidth=0.3, c='skyblue', zorder=1)
        if "discharge" in fname:
            obs = np.fromfile(Path.data_path + 'discharge_obs.bin')
            X = np.arange(len(obs))
            ax.scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
        #fig.legend()
        fig.savefig(output_path + '1_' + fname.split('.')[0] + '.png', dpi=300)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')
"""

""""""
Vars = ['canopy_storage', 'snow_depth','pond', None, None, None]
Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'groundwater_storage', None, None])
Vars.extend(['snowmelt', 'throufall', None, None, None, None])
Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', None, None])
Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3', None, None])
Vars.extend(['canopy_evap', 'soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', None])
Vars.extend([])
Vars.extend([])
Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
Vars.extend(['overland_flow_toChn','interflow_toChn','GWflow_toChn', 'discharge', None, None])
Vars.extend([])

nrow = 8
ncol = 6


fig, ax = plt.subplots(nrow, ncol, figsize=(30,18), dpi=300)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)

for i in range(len(Vars)):
    if Vars[i] == None:
        ax[i//ncol, i%ncol].axis('off')
    else:
        try:
            data = (np.fromfile(output_path + Vars[i] + '_TS.bin').reshape(-1, 1).T)[:, Info.spin_up:]
            data[data==nodata] = np.nan
            for kk in range(data.shape[0]):
                ax[i//ncol, i%ncol].plot(data[kk], linewidth=0.3, c='skyblue', zorder=1)
        
            title_hgt = 0.9
            hgt_gradient = 0.11
            if "discharge" in Vars[i]:
                obs = np.fromfile(Path.data_path + 'discharge_obs.bin')
                X = np.arange(len(obs))
                ax[i//ncol, i%ncol].scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
                ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(np.mean(data, axis=0)+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(np.mean(data, axis=0)+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=12, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
        except:
            ax[i//ncol, i%ncol].axis('off')

fig.savefig(output_path + '999_All_in_Ts.png')
print('Plot saved at :  ', output_path + '999_All_in_Ts.png')


fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.01, hspace=0.08)
for i in range(len(Vars)):
    if Vars[i] == None:
        pass
        ax[i//ncol, i%ncol].axis('off')
    else:
        try:
            data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, 30, 22))[Info.spin_up:, :, :]
            data[data==nodata] = np.nan
            #ax[i//ncol, i%ncol].axis('off')

            if Vars[i] == 'transp_layer1':
                tmppp = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, 30, 22))
                print(np.mean(tmppp[:, 1, 12]))
                print(np.mean(tmppp[:, 2, 12]))

            im = ax[i//ncol, i%ncol].imshow(np.mean(data, axis=0), cmap='coolwarm', zorder=1, label='1')
            ax[i//ncol, i%ncol].set_frame_on(False)
            ax[i//ncol, i%ncol].set_xticks([])
            ax[i//ncol, i%ncol].set_yticks([])

            tmp = ax[i//ncol, i%ncol].get_position()

            fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%.0e')

            title_hgt = 1.02
            hgt_gradient = 0.11
            
            ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
        except Exception as e:
            print(e)
            pass
            #ax[i//ncol, i%ncol].axis('off')
fig.savefig(output_path + '999_All_in_map.png')
print('Plot saved at :  ', output_path + '999_All_in_map.png')


"""
param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1).T
keys = Param.ref.keys()
param_names = []
for key in keys:
    dict = Param.ref[key]
    if dict['type'] == 'global':
        param_names.append(key)
    elif dict['type'] == 'soil':
        for i in range(Info.N_soil):
            param_names.append(key + '_s' + str(i))
    elif dict['type'] == 'landuse':
        for i in range(Info.N_landuse):
            param_names.append(key + '_v' + str(i))

fig, ax = plt.subplots(1, 1, figsize=(10,20), dpi=300)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
ax.imshow(param, cmap='coolwarm')
ax.set_yticks(np.arange(param.shape[0]))
ax.set_yticklabels(param_names, weight='bold')
fig.savefig('999_param.png')

fig, ax = plt.subplots(1, 1, figsize=(10,20), dpi=300)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
for i in range(param.shape[0]):
    param[i] = np.sort(param[i])
ax.imshow(param, cmap='coolwarm')
ax.set_yticks(np.arange(param.shape[0]))
ax.set_yticklabels(param_names, weight='bold')
fig.savefig('999_param_sorted.png')
"""
"""
fnames = os.listdir(output_path)
for fname in fnames:
    print(fname)
    if "_map" in fname and fname.split('.')[-1]=='bin':
        data = np.fromfile(output_path + fname).reshape(-1, 630, 481)
        data[data==nodata] = np.nan
        data = np.mean(data, axis=0)
        fig, ax = plt.subplots(1,1)
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax)
        fig.savefig(output_path + '0_' + fname.split('.')[0] + '.png', dpi=600)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')
        print(np.nanmin(data), np.nanmean(data), np.nanmax(data))
        print(data, np.sum(~np.isnan(data)))


    elif fname.split('.')[-1]=='bin':
        data = np.fromfile(output_path + fname)
        fig, ax = plt.subplots(1,1)
        ax.plot(data)
        fig.savefig(output_path + '1_' + fname.split('.')[0] + '.png', dpi=300)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')

        #fname_new = fname.split('.')[0] + '.txt'
        #np.savetxt(output_path + fname_new, np.fromfile(output_path + fname))
"""

