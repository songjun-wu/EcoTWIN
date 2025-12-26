import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import shutil
import GEM_tools
from multiprocessing import Pool, cpu_count, Manager
import subprocess

from def_GEM_v2 import *
from post_plot import var_info
import GIS_tools
import post_plot

from datetime import datetime

def save_cumulative_outputs_memmap(output_path, save_path, save_all_flag=False, lock=None):

    

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

def read_spatial_data(path, mask, chanmask=None):
    data = np.fromfile(path).reshape(-1, mask.shape[0], mask.shape[1])
    
    if chanmask is not None:
        data[:,~chanmask] = np.nan
    else:
        data[:,mask==-9999] = np.nan

    data = np.mean(data, axis=0)
    return data

def write_ascii(data, dst_asc, ref_asc):

    data[np.isnan(data)] = -9999.0
    with open(ref_asc, 'r') as f:
        lines = f.readlines()
        headers = lines[:6]
    with open(dst_asc, 'w') as f:
        f.writelines(headers)
    with open(dst_asc, 'ab+') as f:
        np.savetxt(f, data)


def generate_carbon_inputs(path):
    
    unit_data = np.loadtxt(path+'dem.asc', skiprows=6)
    unit_data[unit_data==-9999] = np.nan
    unit_data[unit_data!=-9999] = 1.0
    unit_data_chn = np.loadtxt(path+'chnlength.asc', skiprows=6)
    unit_data_chn[unit_data_chn!=0.0] = 1.0

    ref_asc = path + 'dem.asc'

    write_ascii(unit_data*10.0, path+'plant_green_CP.asc', ref_asc)
    write_ascii(unit_data*100.0, path+'plant_wood_CP.asc', ref_asc)
    write_ascii(unit_data*20.0, path+'plant_reserve_CP.asc', ref_asc)

    write_ascii(unit_data*100, path+'acid_CP1_nonwood.asc', ref_asc)
    write_ascii(unit_data*100, path+'ethanol_CP1_nonwood.asc', ref_asc)
    write_ascii(unit_data*100, path+'nonsoluble_CP1_nonwood.asc', ref_asc)

    write_ascii(unit_data*100, path+'acid_CP1_wood.asc', ref_asc)
    write_ascii(unit_data*100, path+'ethanol_CP1_wood.asc', ref_asc)
    write_ascii(unit_data*100, path+'nonsoluble_CP1_wood.asc', ref_asc)
    write_ascii(unit_data*100, path+'humus_CP1.asc', ref_asc)

    write_ascii(unit_data*200, path+'acid_CP2_wood.asc', ref_asc)
    write_ascii(unit_data*200, path+'ethanol_CP2_wood.asc', ref_asc)
    write_ascii(unit_data*200, path+'nonsoluble_CP2_wood.asc', ref_asc)
    write_ascii(unit_data*200, path+'humus_CP2.asc', ref_asc)

    write_ascii(unit_data*500, path+'acid_CP3_wood.asc', ref_asc)
    write_ascii(unit_data*500, path+'ethanol_CP3_wood.asc', ref_asc)
    write_ascii(unit_data*500, path+'nonsoluble_CP3_wood.asc', ref_asc)
    write_ascii(unit_data*500, path+'humus_CP3.asc', ref_asc)

    write_ascii(unit_data*5, path+'doc_I.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_snow.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_pond.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_layer1.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_layer2.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_layer3.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_vadose.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_GW.asc', ref_asc)
    write_ascii(unit_data_chn*5, path+'doc_chanS.asc', ref_asc)
    write_ascii(unit_data*5, path+'doc_rain.asc', ref_asc)


    write_ascii(unit_data*0, path+'C4_flag.asc', ref_asc)



def read_temporal_data(path, mask, chanmask=None):
    if chanmask is not None:
        mask = chanmask
    
    mask_bool = np.full(mask.shape, False)
    mask_bool[mask>0] = True
    
    data = np.fromfile(path).reshape(-1, mask.shape[0], mask.shape[1])
    data = np.mean(data[:,mask_bool], axis=1)

    return data
    
    
    

def foward_run_debug(catchment_ID, chainID, nn, save_output_flag=False, experiment=None):

    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)

    param = _param[chainID, :]

    chain_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID) +'/'
    save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID + '/'
    run_path = chain_path + 'run/'

    if os.path.exists(save_path) and nn==0:
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    """
    os.makedirs(chain_path, exist_ok=True)
    if os.path.exists(chain_path):
        shutil.rmtree(chain_path)
    shutil.copytree('/data/scratch/wusongj/paper4/forward_all/run/'+catchment_ID, chain_path, ignore=shutil.ignore_patterns('*.bin'))
    shutil.copytree('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID), run_path+'spatial')
    generate_carbon_inputs(run_path+'spatial/')
    """
    

    if not os.path.exists(run_path+'Crop_info.ini'):
        shutil.copyfile('/data/scratch/wusongj/paper4/forward_all/run/1/run/Crop_info.ini', run_path+'Crop_info.ini')

    shutil.copyfile('/home/wusongj/EcoTWIN/config.ini', run_path+'config.ini')
    if experiment is None:
        newlines = [    'opt_carbon_sim = 1\n' + \
                        'opt_init_no3 = 0\n' + \
                        'Simul_end = 1420070400 # in second  # Seconds from 1980-1-1 to 2024-12-31\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/\n' + \
                        'Maps_Folder = '+run_path+'spatial/\n']
    else:
        newlines = [    'opt_carbon_sim = 1\n' + \
                        'opt_init_no3 = 0\n' + \
                        'Simul_end = 3818448000 # in second  # Seconds from 1980-1-1 to 2024-12-31\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/'+experiment+'/\n' + \
                        'Maps_Folder = '+run_path+'spatial/\n']
    with open(run_path + 'config.ini', 'r') as f:
        lines = f.readlines()
        for yy, line in enumerate(lines):
            if 'report_trans_age' in line or 'report_doc' in line or 'report_no3' in line or 'report_soil_respiration' in line \
                or 'report_net_primary_production' in line or 'plant_CP' in line:
                key, _ = line.split('=')
                lines[yy] = f"{key.strip()} = 2\n"
    newlines.extend(lines)
    with open(run_path + 'config.ini', 'w') as f:
        f.writelines(newlines)
    

    


    GEM_tools.gen_param(run_path, Info, Param, param)

    
        

    os.remove(run_path + 'gEcoHydro')
    #os.symlink('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux/gEcoHydro', run_path + 'gEcoHydro')
    os.symlink('/home/wusongj/EcoTWIN/release_linux/gEcoHydro', run_path + 'gEcoHydro')

       
    
    os.chdir(run_path)
    os.system('./gEcoHydro')
    #subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if save_output_flag:
        save_cumulative_outputs_memmap(output_path=run_path+'outputs/', save_path=save_path, save_all_flag=True)
        #shutil.rmtree(chain_path)
    
    #print(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', os.path.exists(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc'))
    data_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID+'/'
    mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
    chanmask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/chnwidth.asc', skiprows=6)
    chanmask = chanmask>0
    

    fig, ax = plt.subplots(3,3)

    ims = []

    ims.append(ax[0,0].imshow(read_spatial_data(data_path+'net_primary_production_map.bin', mask)))
    ims.append(ax[1,0].imshow(read_spatial_data(data_path+'trans_age_chanS_map.bin', mask, chanmask)))
    
    ims.append(ax[0,1].imshow(read_spatial_data(data_path+'doc_SMC_layer1_map.bin', mask)))
    ims.append(ax[1,1].imshow(read_spatial_data(data_path+'doc_chanS_map.bin', mask, chanmask)))
    
    ims.append(ax[0,2].imshow(read_spatial_data(data_path+'no3_SMC_layer1_map.bin', mask)))
    ims.append(ax[1,2].imshow(read_spatial_data(data_path+'no3_chanS_map.bin', mask, chanmask)))


    k = 0
    for c in range(3):
        for r in range(2):
            fig.colorbar(ims[k], ax=ax[r,c])
            k += 1

    ax[2,0].plot(read_temporal_data(data_path+'net_primary_production_map.bin', mask))
    ax[2,1].plot(read_temporal_data(data_path+'plant_CP_map.bin', mask))
    ax[2,2].plot(read_temporal_data(data_path+'doc_SMC_layer1_map.bin', mask, chanmask))
    #ax[0,0].imshow(read_spatial_data(data_path+'SMC_layer1.bin', mask))
    #ax[1,0].imshow(read_spatial_data(data_path+'perc_layer1_map.bin', mask))



    fig.savefig('/data/scratch/wusongj/paper6/plots/test/overview_'+str(catchment_ID)+'.png', transparent=True)
    #print(data.shape, data[538:543, 1,13])




if __name__ == "__main__":
    catchment_ID = '6'
    nchains = 40


    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)


    #os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux')
    #os.system('make all')

    os.chdir('/home/wusongj/EcoTWIN/python/development')
    os.system('python3 develop.py')


    foward_run_debug(catchment_ID='831616', chainID=0, nn=0, save_output_flag=True, experiment=None)