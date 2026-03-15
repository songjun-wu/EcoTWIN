from ntpath import exists
import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import subprocess
import post_plot_v2

#import GEM_tools from father directory
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/run_model')
import GEM_tools_v2
from def_GEM_v2 import Path, Info, Cali, Output, Param


def read_spatial_data(path, mask, chanmask=None, weight=1):
    data = np.fromfile(path).reshape(-1, mask.shape[0], mask.shape[1])
    #data = data[2:,:,:]
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan
    
    data = np.mean(data, axis=0) * weight
    return data


def read_temporal_data(path, mask, chanmask=None):
    data = np.fromfile(path).reshape(-1, mask.shape[0], mask.shape[1])
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan
    
    data = np.nanmean(data, axis=(1,2))
    return data


def save_cumulative_outputs_memmap(output_path, save_path, save_all_flag=False, lock=None, replace=False):

    if replace:
        if os.path.exists(save_path):
            shutil.rmtree(save_path)

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_path + '/finish_counter/', exist_ok=True)

    

    if save_all_flag:
        fnames = [f for f in os.listdir(output_path) if '.bin' in f]
    else:
        fnames = [f for f in os.listdir(output_path) if '_TS' in f]

    
    #fnames = np.random.shuffle(fnames)



    for fname in fnames:
        if lock is None:
            if os.path.exists(save_path + fname):
                if os.path.getsize(output_path + fname) == 0:
                    continue
                a = np.memmap(save_path + fname, dtype='float64', mode='r+')
                b = np.memmap(output_path + fname, dtype='float64', mode='r')
                a += b
                a.flush()
                del a, b  # 
                finish_counter = np.loadtxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt')
                finish_counter += 1
            else:
                shutil.copyfile(output_path + fname, save_path + fname)
                finish_counter = 1

            os.remove(output_path + fname)
            np.savetxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt', [finish_counter])
        
        else:
            with lock:
                if os.path.exists(save_path + fname):
                    if os.path.getsize(output_path + fname) == 0:
                        continue
                    a = np.memmap(save_path + fname, dtype='float64', mode='r+')
                    b = np.memmap(output_path + fname, dtype='float64', mode='r')
                    a += b
                    a.flush()
                    del a, b  # 
                    finish_counter = np.loadtxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt')
                    finish_counter += 1
                else:
                    shutil.copyfile(output_path + fname, save_path + fname)
                    finish_counter = 1

                os.remove(output_path + fname)
                np.savetxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt', [finish_counter])


def model_test(mode, catchment_ID):

    os.chdir('/home/wusongj/EcoTWIN/python/development')    
    os.system('python3 develop.py')

    catchment_ID = '83749_001'
    
    GEM_tools_v2.sort_directory(mode, Path, Cali, Output)   # create the working directory
    GEM_tools_v2.set_env(mode, Path, nchains, Output)  # Create run/output path and link model executable
    GEM_tools_v2.set_config(mode, Path, Info, Cali, Output)  # Set configs - input paths, output paths, and running period, etc.

    catchment_dicts = {
        #'831616_001': 9,
        '291110_001': 1,
        #'83749_001': 3,
        #'1034724_001': 12,
        #'95_001': 16,
    }

    
    suffix = '_test1'

    for catchment_ID in catchment_dicts.keys():

        run_path = Path.work_path+mode+'/'+catchment_ID+'/run/'
        save_path = Path.work_path+mode+'/outputs/'+catchment_ID + '/'


        

        #for xxxx in range(nchains):
        for xxxx in [catchment_dicts[catchment_ID]]:
            print(catchment_ID, xxxx)
            param_N = GEM_tools_v2.get_param_N(Info, Param)
            #param = np.fromfile('/data/scratch/wusongj/paper6/cali_sep/best_param/best_param_831616_001_failed.bin').reshape(nchains,-1)[xxxx, :]
            #param = np.fromfile('/data/scratch/wusongj/paper6/cali_sep/best_param/best_param_831616_001.bin').reshape(nchains,-1)[xxxx, :]
            #param = np.fromfile('/data/scratch/wusongj/paper6/cali_sep/best_param/best_param_'+catchment_ID+'.bin').reshape(nchains,-1)[xxxx, :]
            #param = np.fromfile('/data/scratch/wusongj/paper6/cali_sep/best_param/best_param_291110_001.bin').reshape(nchains,-1)[xxxx, :]

            #_param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)
            #param = _param[0, :]
            GEM_tools_v2.gen_param(run_path, Info, Param, param)
            GEM_tools_v2.gen_no3_addtion(run_path, Info)

            # Link latest version of model executable
            if os.path.exists(run_path + 'EcoTWIN'):
                os.remove(run_path + 'EcoTWIN')
            os.symlink('/home/wusongj/EcoTWIN/release_linux/EcoTWIN', run_path + 'EcoTWIN')

            # Set config.ini
            seconds_from_1980 = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/obs/seconds_from_1980.txt')
            newlines = [    'num_category = '+str(int(Info.N_landuse+Info.N_soil+1))+'\n' + \
                            'opt_carbon_sim = 1\n' + \
                            'opt_init_no3 = 0\n' + \
                            #'Simul_end = '+str(int(seconds_from_1980))+' # in second  # Seconds from 1980-1-1 to 2024-12-31\n' + \
                            'Simul_end = '+str(int(86400*365*1))+' # in second  # Seconds from 1980-1-1 to 2024-12-31\n' + \
                            'Clim_Maps_Folder = /data/scratch/wusongj/paper6/data/catchment_info/cali/'+catchment_ID+'/climate/\n' + \
                            'Maps_Folder = /data/scratch/wusongj/paper6/data/catchment_info/cali/'+catchment_ID+'/spatial/\n']
            with open(run_path + 'config.ini', 'r') as f:
                lines = f.readlines()
            newlines.extend(lines)
            with open(run_path + 'config.ini', 'w') as f:
                f.writelines(newlines)


            
            #for i in range(12):
            #    shutil.copyfile('/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/'+'category_'+str(i)+'.bin', spatial_path+'category_'+str(i)+'.bin')
            

            # Run model
            os.chdir(run_path)
            #subprocess.run('./EcoTWIN', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.system('./EcoTWIN')
            # Save outputs
            save_cumulative_outputs_memmap(output_path=run_path+'outputs/', save_path=save_path, save_all_flag=True, replace=True)
            #shutil.rmtree(chain_path)

            #post_plot_v2.plot_spatial_maps(save_path, '/data/scratch/wusongj/paper6/plots/test/', catchment_ID, warming_period=0, nchains=1, suffix=suffix, flag_spatial_maps=True)

        """
        # Plot results 
        #print(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', os.path.exists(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc'))
        mask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
        chanmask = np.loadtxt(Path.data_path+'catchment_info/cali/'+catchment_ID+'/spatial/chnwidth.asc', skiprows=6)
        chanmask = chanmask>0

        nrows = 7
        ncols = 3

        fig, ax = plt.subplots(nrows, ncols, figsize=(10,20), dpi=300)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)
        im0 = ax[0,0].imshow(read_spatial_data(save_path+'SMC_layer1_map.bin', mask), vmin=0.2, vmax=0.8)
        im1 = ax[0,1].imshow(read_spatial_data(save_path+'SMC_layer2_map.bin', mask), vmin=0.2, vmax=0.8)
        im2 = ax[0,2].imshow(read_spatial_data(save_path+'SMC_layer3_map.bin', mask), vmin=0.2, vmax=0.8)


        im3 = ax[1,0].imshow(read_spatial_data(save_path+'infiltration_map.bin', mask, weight=1000*365), vmin=500, vmax=1000)
        im4 = ax[1,1].imshow(read_spatial_data(save_path+'perc_layer1_map.bin', mask, weight=1000*365), vmin=200, vmax=900)
        im5 = ax[1,2].imshow(read_spatial_data(save_path+'perc_layer2_map.bin', mask, weight=1000*365), vmin=200, vmax=700)

        im6 = ax[2,0].imshow(read_spatial_data(save_path+'age_chanS_map.bin', mask, chanmask, weight=1))
        im7 = ax[2,1].imshow(read_spatial_data(save_path+'age_vadose_map.bin', mask, chanmask, weight=1))
        im8 = ax[2,2].imshow(read_spatial_data(save_path+'age_groundwater_storage_map.bin', mask, chanmask, weight=1))

        im9 = ax[3,0].imshow(read_spatial_data(save_path+'snow_depth_map.bin', mask, weight=1))
        im10 = ax[3,1].imshow(read_spatial_data(save_path+'doc_chanS_map.bin', mask, chanmask, weight=1))
        im11 = ax[3,2].imshow(read_spatial_data(save_path+'no3_chanS_map.bin', mask, chanmask, weight=1))

        im12 = ax[4,0].imshow(read_spatial_data(save_path+'overland_flow_toChn_map.bin', mask, weight=1000*365))
        im13 = ax[4,1].imshow(read_spatial_data(save_path+'interflow_toChn_map.bin', mask, weight=1000*365))
        im14 = ax[4,2].imshow(read_spatial_data(save_path+'GWflow_toChn_map.bin', mask, weight=1000*365))

        im15 = ax[5,0].imshow(read_spatial_data(save_path+'soil_evap_map.bin', mask, weight=1000*365))
        im16 = ax[5,1].imshow(read_spatial_data(save_path+'transp_map.bin', mask, weight=1000*365))
        im17 = ax[5,2].imshow(read_spatial_data(save_path+'plant_C_map.bin', mask, weight=1))

        im18 = ax[6,0].imshow(read_spatial_data(save_path+'litter_fall_C_map.bin', mask, weight=1*365))
        im19 = ax[6,1].imshow(read_spatial_data(save_path+'soil_respiration_C_map.bin', mask, weight=1*365))
        im20 = ax[6,2].imshow(read_spatial_data(save_path+'leaching_mass_doc_map.bin', mask, weight=1*365))


        #tmp = read_spatial_data(save_path+'drainage_from_soil_map.bin', mask) * 1000*365
        #print(np.nanmedian(tmp))
        #print(np.nanmax(tmp))
        #print(np.where(tmp == np.nanmax(tmp)))

        for r in range(nrows):
            for c in range(ncols):
                ax[r,c].axis('off')

        #ax[3,0].plot(read_temporal_data(save_path+'plant_C_map.bin', mask))
        #ax[3,1].plot(read_temporal_data(save_path+'fast_C_map.bin', mask))
        #ax[3,2].plot(read_temporal_data(save_path+'humus_C_map.bin', mask))

        # Add colorbar for each subplot
        fig.colorbar(im0, ax=ax[0,0])
        fig.colorbar(im1, ax=ax[0,1])   
        fig.colorbar(im2, ax=ax[0,2])
        fig.colorbar(im3, ax=ax[1,0])
        fig.colorbar(im4, ax=ax[1,1])
        fig.colorbar(im5, ax=ax[1,2])
        fig.colorbar(im6, ax=ax[2,0])
        fig.colorbar(im7, ax=ax[2,1])
        fig.colorbar(im8, ax=ax[2,2])
        fig.colorbar(im9, ax=ax[3,0])
        fig.colorbar(im10, ax=ax[3,1])
        fig.colorbar(im11, ax=ax[3,2])
        fig.colorbar(im12, ax=ax[4,0])
        fig.colorbar(im13, ax=ax[4,1])
        fig.colorbar(im14, ax=ax[4,2])
        fig.colorbar(im15, ax=ax[5,0])
        fig.colorbar(im16, ax=ax[5,1])
        fig.colorbar(im17, ax=ax[5,2])
        fig.colorbar(im18, ax=ax[6,0])
        fig.colorbar(im19, ax=ax[6,1])
        fig.colorbar(im20, ax=ax[6,2])

        fig.savefig('/data/scratch/wusongj/paper6/plots/test/overview_'+str(catchment_ID)+'.png', transparent=True)
        """

    



mode = 'test'
nchains = 20

model_test(mode, catchment_ID='291110_001')
#model_test(mode, catchment_ID='831616_001')
