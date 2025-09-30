import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import shutil
import GEM_tools
from multiprocessing import Pool, cpu_count, Manager
import subprocess

from def_GEM_forward import *
from post_plot import var_info
import GIS_tools


"""
catchment = '291110'

climate_zones = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/spatial/climate_zones.asc', skiprows=6)
climate_zones = len(np.unique(climate_zones))-1

climate_vars = ['PET', 'Ta', 'P', 'RH']
for var in climate_vars:
    data = np.fromfile('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/climate/ssp585/'+var+'.bin').reshape(-1, climate_zones)
    print(var, data.shape, np.min(data), np.max(data), np.mean(data))
    fig, ax = plt.subplots(1,1)
    ts = []
    tindex = pd.date_range('1980-1-1', '2100-12-31')
    for i in range(data.shape[0]):
        ts.append(np.mean(data[i,:]))

    df = pd.DataFrame(ts, index=tindex)
    df = df.resample('Y').mean()
    
    ax.plot(df.index, df)
    fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/tmp/climate_'+var+'_ts.png')




files = os.listdir('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp585')
dem = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/spatial/dem.asc', skiprows=6)

for file in files:
    try:
        data0 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all/'+file).reshape(-1, dem.shape[0], dem.shape[1])
        data1 = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp585/'+file).reshape(-1, dem.shape[0], dem.shape[1])

        data0 /= np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all/finish_counter/finish_counter_'+file+'.txt')
        data1 /= np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment+'/all_ssp585/finish_counter/finish_counter_'+file+'.txt')

        fig, ax = plt.subplots(1,1)

        ts = []
        for i in range(data1.shape[0]):
            ts.append(np.mean(data1[i,:,:][dem!=-9999]))
            if 'channel' in file:
                print(1980+i//12, data1.shape, data0.shape, np.mean(data1[i,:,:][dem!=-9999]))
        ax.plot(np.arange(len(ts)), ts, c='blue')

        ts = []
        for i in range(data0.shape[0]):
            ts.append(np.mean(data0[i,:,:][dem!=-9999]))
        ax.plot(np.arange(len(ts)), ts, c='red')
        
        fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/tmp/'+file+'_ts.png')



        fig, ax = plt.subplots(1,2)
        datas = [np.mean(data0[:12*10,:,:], axis=0), np.mean(data1[-12*10:,:,:], axis=0)]
        tmp = datas[0]
        tmp[dem==-9999] = np.nan
        vmin = np.nanpercentile(tmp, 10)
        vmax = np.nanpercentile(tmp, 90)

        for gg, data in enumerate(datas):
            data[dem==-9999] = np.nan
            ax[gg].imshow(data, vmin=vmin, vmax=vmax)
        
        fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/tmp/'+file+'_map.png')
        print(file, np.where(np.isnan(data1)))


        
            
        

        #data0 = data0[-1,:,:]
        #data1 = data1[1000,:,:]

        #data0[dem==nodata] = np.nan
        #data1[dem==nodata] = np.nan



        #print(file, np.nanmean(data0), np.nanmean(data1))
        
    except Exception as e:
        print(e)
        pass

"""




"""
if os.path.exists('/data/scratch/wusongj/paper4/test/'+catchment_ID):
    shutil.rmtree('/data/scratch/wusongj/paper4/test/'+catchment_ID)
shutil.copytree('/data/scratch/wusongj/paper4/forward_all/run/'+catchment_ID, '/data/scratch/wusongj/paper4/test/'+catchment_ID, ignore=shutil.ignore_patterns('*.bin'))
"""


def check_climate_experiments():
    mask_large = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    vars = ['P', 'PET', 'Ta', 'Rnet']
    save_vars = ['Precipitation_npfloat32', 'Potential_evapotranspiration_npfloat32', 'Mean_air_temperature_npfloat32', 'Surface_net_radiation_npfloat32']
    experiments = ['ssp126', 'ssp585']

    catchment_list = ['291110', '566445','1', '6', '4']


    for xx, var in enumerate(vars):
        for experiment in experiments:
            arr_large = np.full(mask_large.shape, np.nan)

            for yy, catchment in enumerate(catchment_list):
                climate_mask_small = np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/spatial/climate_zones.asc', skiprows=6)
                mask_small = (climate_mask_small!=-9999)
                upper_left_coord = (np.loadtxt('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/spatial/upper_left_coord.txt')).astype(int)

                arr_4326 = np.fromfile('/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment+'/climate/'+experiment+'/'+var+'.bin').reshape(-1, len(np.unique(climate_mask_small))-1)

                """
                #arr_TS = np.mean(arr_4326, axis=1)
                arr_TS = arr_4326[:,-1]
                tindex = pd.date_range('1980-1-1', '2100-12-31')
                fig, ax = plt.subplots(1,1, dpi=300)
                ax.plot(tindex, arr_TS)
                df = pd.DataFrame(arr_TS, index=tindex)
                df = df.resample('Y').mean()
                ax.plot(df.index, df.values)
                fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/diff/difference_TS_'+save_vars[xx]+'_'+experiment+'_'+catchment+'.png')
                """



                arr_4326 = np.mean(arr_4326[110*365:120*365,:], axis=0) - np.mean(arr_4326[35*365:45*365,:], axis=0)
                
                arr_small = np.full(climate_mask_small.shape, np.nan)
                for r in range(arr_small.shape[0]):
                    for c in range(arr_small.shape[1]):
                        if mask_small[r,c]:
                            arr_small[r,c] = arr_4326[int(climate_mask_small[r,c])-1]                      

                arr_large = GIS_tools.from_catchment_to_EU(upper_left_coord, mask_small, arr_large, arr_small)
                
                print(var, experiment,yy)
            
            GEM_tools.create_asc(arr_large, '/data/scratch/wusongj/paper4/data/catchment_info/climate_3035_tmp/difference_'+save_vars[xx]+'_'+experiment+'.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')

            
            fig, ax = plt.subplots(1,1, dpi=300)
            arr_large[arr_large==-9999] = np.nan
            arr_large *= var_info[save_vars[xx]][1]
 
            ax.imshow(arr_large, vmin=-var_info[save_vars[xx]][0][1]/8, vmax=var_info[save_vars[xx]][0][1]/8, cmap='coolwarm')
            fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/diff/difference_'+save_vars[xx]+'_'+experiment+'.png')
            


def save_cumulative_outputs_memmap(output_path, save_path, save_all_flag=False, lock=None):

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_path + '/finish_counter/', exist_ok=True)

    if save_all_flag:
        fnames = [f for f in os.listdir(output_path) if '.bin' in f]
    else:
        fnames = [f for f in os.listdir(output_path) if '_TS' in f]
    
    fnames = np.random.shuffle(fnames)

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





    #fnames = os.listdir('/data/scratch/wusongj/paper4/test/run/'+catchment_list[0]+'/' + str(chainID_list[0]) +'/')

   #shutil.rmtree(chain_path)

def save_cumulative_outputs_memmap_filenames_parallel(fname, catchment_list, chainID_list):

    for catchment_ID in catchment_list:
        
        save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID + '/'
        os.makedirs(save_path, exist_ok=True)
        os.makedirs(save_path + '/finish_counter/', exist_ok=True)

        finish_counter = 0  # todotodo


        if os.path.exists(save_path + fname):

            a = np.memmap(save_path + fname, dtype='float64', mode='r+')
            for nn, chainID in enumerate(chainID_list):
                output_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID) +'/run/outputs/'
                
                if os.path.getsize(output_path + fname) == 0:
                    continue
                
                b = np.memmap(output_path + fname, dtype='float64', mode='r')
                a += b
                finish_counter += 1
                del b

                print(catchment_ID, chainID, fname, flush=True)

            a.flush()
            del a  # 

            finish_counter += np.loadtxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt')

        else:
            for nn, chainID in enumerate(chainID_list):
                output_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID) +'/run/outputs/'
                
                if nn == 0:
                    shutil.copyfile(output_path+fname, save_path+fname)
                    a = np.memmap(save_path + fname, dtype='float64', mode='r+')
                    finish_counter += 1
                
                else:
                    if os.path.getsize(output_path + fname) == 0:
                        continue
                    
                    b = np.memmap(output_path + fname, dtype='float64', mode='r')
                    a += b
                    finish_counter += 1
                    del b

                    print(catchment_ID, chainID, fname, flush=True)
            print(catchment_ID, '      flush!!!!!!!!!!!!', flush=True)
            a.flush()
            del a  #

        np.savetxt(save_path + '/finish_counter/finish_counter_'+fname+'.txt', [finish_counter])












def split_indices(n_tasks, n_cores):
    base = n_tasks // n_cores
    extra = n_tasks % n_cores
    sizes = [base + 1 if i < extra else base for i in range(n_cores)]
    indices = []
    start = 0
    for size in sizes:
        indices.append((start, start + size))
        start += size
    return indices

def foward_run_parallel(catchment_ID, chainID, param, nn, experiment, lock=None):
    chain_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID) +'/'
    save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID + '/'

    print(chain_path)

    if os.path.exists(save_path) and nn==0:
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    os.makedirs(chain_path, exist_ok=True)
    if os.path.exists(chain_path):
        shutil.rmtree(chain_path)
    shutil.copytree('/data/scratch/wusongj/paper4/forward_all/run/'+catchment_ID, chain_path, ignore=shutil.ignore_patterns('*.bin'))

    run_path = chain_path + 'run/'

    #os.remove(run_path + 'config.ini')
    #shutil.copyfile('/data/scratch/wusongj/paper4/data/config/config_forward_monthly.ini', run_path + 'config.ini')

    if experiment is None:
        newlines = [    'opt_init_no3 = 0\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/\n' + \
                        'Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/\n']
    else:
        newlines = [    'opt_init_no3 = 0\n' + \
                        'Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/'+experiment+'/\n' + \
                        'Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/\n']
    with open(run_path + 'config.ini', 'r') as f:
        lines = f.readlines()
    newlines.extend(lines)
    with open(run_path + 'config.ini', 'w') as f:
        f.writelines(newlines)

    
    with open(run_path + 'config.ini', 'r') as f:
        lines = f.readlines()
    newlines.extend(lines)

    with open(run_path + 'config.ini', 'w') as f:
        f.writelines(newlines)

    #os.remove(run_path + 'gEcoHydro')
    #os.symlink('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux/gEcoHydro', run_path + 'gEcoHydro')

       
    GEM_tools.gen_param(run_path, Info, Param, param)
    os.chdir(run_path)
    #os.system('./gEcoHydro')
    subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    


def foward_run_debug(catchment_ID, chainID, nn, save_output_flag=False, experiment=None):

    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)

    param = _param[chainID, :]

    chain_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID) +'/'
    save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID + '/'


    if os.path.exists(save_path) and nn==0:
            shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    os.makedirs(chain_path, exist_ok=True)
    if os.path.exists(chain_path):
        shutil.rmtree(chain_path)
    shutil.copytree('/data/scratch/wusongj/paper4/forward_all/run/'+catchment_ID, chain_path, ignore=shutil.ignore_patterns('*.bin'))

    run_path = chain_path + 'run/'

    """
    os.remove(run_path + 'config.ini')
    shutil.copyfile('/data/scratch/wusongj/paper4/data/config/config_forward_monthly.ini', run_path + 'config.ini')   
    """
    """
    newlines = ['Clim_Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/climate/\n' + \
                    'Maps_Folder = /data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(chainID)+'/\n']

    with open(run_path + 'config.ini', 'r') as f:
        lines = f.readlines()
    newlines.extend(lines)

    with open(run_path + 'config.ini', 'w') as f:
        f.writelines(newlines)


    GEM_tools.gen_param(run_path, Info, Param, param)
    """
    
        

    os.remove(run_path + 'gEcoHydro')
    os.symlink('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux/gEcoHydro', run_path + 'gEcoHydro')

       
    
    os.chdir(run_path)
    os.system('./gEcoHydro')
    #subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if save_output_flag:
        save_cumulative_outputs_memmap(output_path=run_path+'outputs/', save_path=save_path, save_all_flag=True)
        #shutil.rmtree(chain_path)
    
    #print(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', os.path.exists(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc'))
    mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
    data = np.fromfile('/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID+'/no3_SMC_layer1_map.bin').reshape(-1, mask.shape[0], mask.shape[1])
    data[:,mask==-9999] = np.nan
    fig, ax = plt.subplots(1,3)
    ax[0].imshow(np.mean(data, axis=0))
    ax[1].imshow(np.mean(data[0:540], axis=0))
    ax[2].imshow(np.mean(data[-120:-1], axis=0))
    fig.savefig(Path.work_path+'plots/test.png')
    #print(data.shape, data[538:543, 1,13])
    
    

def test0():
    mask = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    da = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/damkholer_num.bin').reshape(-1, mask.shape[0], mask.shape[1])
    pt = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/processing_time.bin').reshape(-1, mask.shape[0], mask.shape[1])
    ns = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/nitrogen_storage.bin').reshape(-1, mask.shape[0], mask.shape[1])
    denis = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/deni_soil.bin').reshape(-1, mask.shape[0], mask.shape[1])
    pu = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/plant_uptake.bin').reshape(-1, mask.shape[0], mask.shape[1])
    age = np.fromfile(Path.work_path + 'forward_all/outputs/cali_merged/monthly/all/trans_age_SMC_soil_all_depths.bin').reshape(-1, mask.shape[0], mask.shape[1])
    
    da = da[:, 57, 582]
    pt = pt[:, 57, 582]
    ns = ns[:, 57, 582]
    denis = denis[:, 57, 582]
    pu = pu[:, 57, 582]
    age = age[:, 57, 582]

    soil_deni_thres = 1 / 10 / 365
    #denis[denis<soil_deni_thres] = soil_deni_thres

    pt_tmp = ns / (denis + pu)
    da_tmp = age / pt_tmp

    fig, ax = plt.subplots(6,2)
    ax[0,0].plot(da)
    ax[1,0].plot(pt)
    ax[2,0].plot(ns)
    ax[3,0].plot(denis)
    ax[4,0].plot(pu)
    ax[5,0].plot(age)
    ax[0,1].plot(da_tmp)
    ax[1,1].plot(pt_tmp)

    fig.savefig('/data/scratch/wusongj/paper4/plots/forward_all/test_da.png')


def test1_examine_experiment_inputs(experiment):

    vars = ['LAI', 'P', 'Ta', 'PET']
    for var in vars:
        for experiment in [None, 'ssp126', 'ssp585']:
            if var == 'LAI':
                freq='7D'
            else:
                freq='D'
            if experiment is None:
                end_date = '2024-12-31'
            else:
                end_date = '2100-12-31'

            tindex = pd.date_range('1980-1-1', end_date, freq=freq)

            if experiment is None:
                _data = np.fromfile(Path.data_path+'catchment_info/forward/291110/climate/'+var+'.bin').reshape(len(tindex), -1)
            else:
                _data = np.fromfile(Path.data_path+'catchment_info/forward/291110/climate/'+experiment+'/'+var+'.bin').reshape(len(tindex), -1)

            print(var, experiment, np.mean(_data[:540]), np.mean(_data[540:]))
            data = np.mean(_data, axis=1)

        """
        df = pd.DataFrame(data, index=tindex)
        df = df.resample('Y').mean()
        fig, ax = plt.subplots(1,1)
        ax.plot(tindex, data)
        ax.plot(df.index, df)
        fig.savefig(Path.work_path+'plots/' + 'climate_'+var+'_'+experiment+'.png')
        """


def boardcast_from_root_spatial_path():
    catchment_list = np.loadtxt(Path.work_path + 'forward_all/outputs/cali_merged/performance/failed_catchments.txt')
    catchment_list = (catchment_list.astype(np.int64)).astype(np.str_)
    for catchment_ID in catchment_list:
        for i in range(40):

            src = '/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial/Gauge_to_Report.asc'
            dst = '/data/scratch/wusongj/paper4/data/catchment_info/forward/'+catchment_ID+'/spatial_'+str(i)+'/Gauge_to_Report.asc'

            shutil.copyfile(src, dst)
        print(catchment_ID, '  done!')

def forward_run_again():
    
    

    
    
    batch_num = 1
    batch_ID = 0
    
    #catchment_list = np.loadtxt(Path.work_path + 'forward_all/outputs/cali_merged/performance/failed_catchments.txt')
    #catchment_list = np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/failed_catchments_forward_ssp126.txt')

    catchment_list = np.array(['566445'])


    catchment_list = (catchment_list.astype(np.int64)).astype(np.str_)
    indices = split_indices(n_tasks=len(catchment_list), n_cores=batch_num)
    start = indices[batch_ID][0]
    end = indices[batch_ID][1]
    catchment_list_split = catchment_list[start:end]
    print(batch_ID, start, end, catchment_list_split[:5])


    for nn, chainID in enumerate(np.arange(0,nchains,1)):
        print(chainID, catchment_list[:5])
        tasks = []
        for catchment_ID in catchment_list_split:  # todo
            tasks.append((catchment_ID, chainID, _param[chainID, :], nn))
        # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(foward_run_parallel, tasks)


def forward_run_again_all_chain_parallel(experiment):

    manager = Manager()
    lock = manager.Lock()

    
    batch_num = 1
    batch_ID = 0
    
    #catchment_list = np.loadtxt(Path.work_path + 'forward_all/outputs/cali_merged/performance/failed_catchments.txt')
    #catchment_list = np.loadtxt('/data/scratch/wusongj/paper4/forward_all/outputs/failed_catchments_forward_ssp126.txt')

    catchment_list = np.array(['566445', '748037', '748077'])
    #catchment_list = np.array(['83811'])


    catchment_list = (catchment_list.astype(np.int64)).astype(np.str_)
    indices = split_indices(n_tasks=len(catchment_list), n_cores=batch_num)
    start = indices[batch_ID][0]
    end = indices[batch_ID][1]
    catchment_list_split = catchment_list[start:end]
    


    chain_start_list = [0,10,20,30]
    chain_end_list = [10,20,30,40]

    for gg in range(len(chain_start_list)):

        chainID_list = np.arange(chain_start_list[gg], chain_end_list[gg])
    
        tasks = []
        for nn, chainID in enumerate(chainID_list):
            for catchment_ID in catchment_list_split:  # todo
                tasks.append((catchment_ID, chainID, _param[chainID, :], chainID, experiment, lock))
            # Use multiprocessing pool to run in parallel
        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(foward_run_parallel, tasks)

        
        print(batch_ID, start, end, catchment_list_split[:5], chainID_list)
        
        fnames = os.listdir('/data/scratch/wusongj/paper4/test/run/'+catchment_list[0]+'/' + str(chainID_list[0]) +'/run/outputs/')
        tasks = []
        for fname in fnames:
            for catchment_ID in catchment_list:
                tasks.append((fname, [catchment_ID], chainID_list))

        with Pool(processes=min(cpu_count(), 40)) as pool:
            pool.starmap(save_cumulative_outputs_memmap_filenames_parallel, tasks)
        

        for catchment_ID in catchment_list:
            for chainID in chainID_list:
                chain_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/' + str(chainID)
                shutil.rmtree(chain_path)
    

def result_transfer_second_post_run():
    catchment_list = np.loadtxt(Path.work_path + 'forward_all/outputs/cali_merged/performance/failed_catchments.txt')
    catchment_list = (catchment_list.astype(np.int64)).astype(np.str_)


    sim_vars = ['discharge_TS', 'd18o_chanS_TS', 'no3_chanS_TS']

    for catchment_ID in catchment_list:

        src_dir = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID + '/'
        dst_dir = Path.work_path + 'forward_all/outputs/cali/monthly/' + str(catchment_ID) + '/all/'
        for var in sim_vars:
            shutil.copyfile(src_dir+var+'.bin', dst_dir+var+'.bin')
            shutil.copyfile(src_dir+'finish_counter/finish_counter_'+var+'.bin.txt', dst_dir+'finish_counter/finish_counter_'+var+'.bin.txt')
        print(catchment_ID, '   done!')
        
def plot_forward_results(experiment):

    catchment_list = ['291110', '566445', '83811', '291111', '129487', '748037']
    vars = ['trans_age_SMC_soil_all_depths', 'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'nitrogen_storage', 'deni_soil', 'plant_uptake', 'processing_time']


    catchment_list = ['291110', '83811', '291111', '129487', '748037']
    vars = ['damkholer_num', 'infiltration', 'trans_age_SMC_soil_all_depths', 'SMC_layer3', 'processing_time', 'no3_SMC_layer3']


    #vars = ['damkholer_num']
    #weights = [1]
    #vmaxs = [None]

    for catchment_ID in catchment_list:
        mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
        save_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment_ID+'/all_'+experiment+'/'
        #save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID+'/'
        catchment_path = ''
        
        for xx, var in enumerate(vars):

            fig, ax = plt.subplots(2,2, figsize=(6,6))

            print(catchment_ID, var)

            if var == 'processing_time':
                data =  np.fromfile(save_path + 'no3_SMC_layer1' + '_map.bin') * np.fromfile(save_path + 'SMC_layer1' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer2' + '_map.bin') * np.fromfile(save_path + 'SMC_layer2' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer3' + '_map.bin') * np.fromfile(save_path + 'SMC_layer3' + '_map.bin') * 1.9
                data /= np.fromfile(save_path + 'deni_soil' + '_map.bin') + np.fromfile(save_path + 'plant_uptake' + '_map.bin')
                data /= np.loadtxt(save_path+'finish_counter/finish_counter_no3_SMC_layer1_map.bin.txt')
                data[data>1e4] = 1e4
                data[np.isnan(data)] = 1e4
                print(np.where(np.isnan(data)))
                data = data.reshape(-1, mask.shape[0], mask.shape[1])
            elif var == 'trans_age_SMC_soil_all_depths':
                data =  (np.fromfile(save_path + 'trans_age_SMC_layer1' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'trans_age_SMC_layer2' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'trans_age_SMC_layer3' + '_map.bin') * 1.9) / \
                        (0.2 + 0.2 + 1.9)
                data /= np.loadtxt(save_path+'finish_counter/finish_counter_trans_age_SMC_layer1_map.bin.txt')
                data = data.reshape(-1, mask.shape[0], mask.shape[1])
            elif var == 'nitrogen_storage':
                data =  np.fromfile(save_path + 'no3_SMC_layer1' + '_map.bin') * np.fromfile(save_path + 'SMC_layer1' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer2' + '_map.bin') * np.fromfile(save_path + 'SMC_layer2' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer3' + '_map.bin') * np.fromfile(save_path + 'SMC_layer3' + '_map.bin') * 1.9
                data /= np.loadtxt(save_path+'finish_counter/finish_counter_no3_SMC_layer1_map.bin.txt')
                data = data.reshape(-1, mask.shape[0], mask.shape[1])
            elif var == 'damkholer_num':

                pt =  np.fromfile(save_path + 'no3_SMC_layer1' + '_map.bin') * np.fromfile(save_path + 'SMC_layer1' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer2' + '_map.bin') * np.fromfile(save_path + 'SMC_layer2' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'no3_SMC_layer3' + '_map.bin') * np.fromfile(save_path + 'SMC_layer3' + '_map.bin') * 1.9
                pt /= np.fromfile(save_path + 'deni_soil' + '_map.bin') + np.fromfile(save_path + 'plant_uptake' + '_map.bin')

                pt[pt>1e4] = 1e4
                pt[np.isnan(pt)] = 1e4
                

                age =  (np.fromfile(save_path + 'trans_age_SMC_layer1' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'trans_age_SMC_layer2' + '_map.bin') * 0.2 + \
                        np.fromfile(save_path + 'trans_age_SMC_layer3' + '_map.bin') * 1.9) / \
                        (0.2 + 0.2 + 1.9)
                
                
                data = age / pt

                data /= np.loadtxt(save_path+'finish_counter/finish_counter_no3_SMC_layer1_map.bin.txt')

                data = data.reshape(-1, mask.shape[0], mask.shape[1])
                data = np.log10(data)
                

            else:
                data = np.fromfile(save_path + var + '_map.bin').reshape(-1, mask.shape[0], mask.shape[1])
                data /= np.loadtxt(save_path+'finish_counter/finish_counter_'+var+'_map.bin.txt')

            data[:,mask==-9999] = np.nan
            data[data==-9999] = np.nan

            data *= var_info[var][1]  # weight

            #data[data>2e5] = 2e5

            # Examine results?
            
            #data[data>300] = 300
            data0 = np.mean(data[35*12:45*12,:,:], axis=0)
            data1 = np.mean(data[110*12:120*12,:,:], axis=0)

            

            """
            r = 50 
            c = 50
            print(data0[r,c])
            print(data1[r,c])
            print(data[35*12:45*12,r,c])
            """

            vmin = var_info[var][0][0]
            vmax = var_info[var][0][1]

            if len(var_info[var]) > 3:
                vmin_diff = var_info[var][3][0]
                vmax_diff = var_info[var][3][1]
            else:
                vmin_diff = -vmax/8
                vmax_diff = vmax/8
            
                

            df = pd.DataFrame(np.nanmean(data, axis=(1,2)), index=pd.date_range('1980-1-1', '2100-12-31', freq='M'))
            df = df.resample('Y').mean()

            ax[0,0].plot(df.index, df)
            ax[0,1].imshow(data1 - data0, vmin=vmin_diff, vmax=vmax_diff, cmap='coolwarm')
            ax[1,0].imshow(data0, vmin=vmin, vmax=vmax, cmap='coolwarm')
            ax[1,1].imshow(data1, vmin=vmin, vmax=vmax, cmap='coolwarm')
            fig.savefig(Path.work_path + 'plots/'+var+'_'+catchment_ID+'_tmp.png')


def plot_forward_results_tmp(experiment):

    catchment_list = ['291110', '566445', '83811', '291111', '129487', '748037']
    vars = ['trans_age_SMC_soil_all_depths', 'no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'nitrogen_storage', 'deni_soil', 'plant_uptake', 'processing_time']
    
    vmaxs = [3000, 80, 50, 30, 100, 0.005, 0.05, 1e4]

    catchment_list = ['566445']
    vars = ['no3_SMC_layer1']
    vmaxs = [80]

    for catchment_ID in catchment_list:
        mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)
        for chainID in range(20):
            save_path = '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/'+catchment_ID+'/all_'+experiment+'/'
            save_path = '/data/scratch/wusongj/paper4/test/outputs/'+catchment_ID+'/'
            save_path = '/data/scratch/wusongj/paper4/test/run/'+catchment_ID+'/'+str(chainID)+'/run/outputs/'
            catchment_path = ''
            
            for xx, var in enumerate(vars):

                fig, ax = plt.subplots(2,2, figsize=(6,6))

                print(catchment_ID, var)

                if var == 'processing_time':
                    data =  np.fromfile(save_path + 'no3_SMC_layer1' + '_map.bin') * np.fromfile(save_path + 'SMC_layer1' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'no3_SMC_layer2' + '_map.bin') * np.fromfile(save_path + 'SMC_layer2' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'no3_SMC_layer3' + '_map.bin') * np.fromfile(save_path + 'SMC_layer3' + '_map.bin') * 1.9
                    data /= np.fromfile(save_path + 'deni_soil' + '_map.bin') + np.fromfile(save_path + 'plant_uptake' + '_map.bin')
                    data /= np.loadtxt(save_path+'finish_counter/finish_counter_no3_SMC_layer1_map.bin.txt')
                    data[data>1e4] = 1e4
                    data[np.isnan(data)] = 1e4
                    print(np.where(np.isnan(data)))
                    data = data.reshape(-1, mask.shape[0], mask.shape[1])
                elif var == 'trans_age_SMC_soil_all_depths':
                    data =  (np.fromfile(save_path + 'trans_age_SMC_layer1' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'trans_age_SMC_layer2' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'trans_age_SMC_layer3' + '_map.bin') * 1.9) / \
                            (0.2 + 0.2 + 1.9)
                    data /= np.loadtxt(save_path+'finish_counter/finish_counter_trans_age_SMC_layer1_map.bin.txt')
                    data = data.reshape(-1, mask.shape[0], mask.shape[1])
                elif var == 'nitrogen_storage':
                    data =  np.fromfile(save_path + 'no3_SMC_layer1' + '_map.bin') * np.fromfile(save_path + 'SMC_layer1' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'no3_SMC_layer2' + '_map.bin') * np.fromfile(save_path + 'SMC_layer2' + '_map.bin') * 0.2 + \
                            np.fromfile(save_path + 'no3_SMC_layer3' + '_map.bin') * np.fromfile(save_path + 'SMC_layer3' + '_map.bin') * 1.9
                    data /= np.loadtxt(save_path+'finish_counter/finish_counter_no3_SMC_layer1_map.bin.txt')
                    data = data.reshape(-1, mask.shape[0], mask.shape[1])
                else:
                    data = np.fromfile(save_path + var + '_map.bin').reshape(-1, mask.shape[0], mask.shape[1])

                    try:
                        data /= np.loadtxt(save_path+'finish_counter/finish_counter_'+var+'_map.bin.txt')
                    except:
                        data /= 1

                data[:,mask==-9999] = np.nan
                data[data==-9999] = np.nan

                #data[data>2e5] = 2e5

                # Examine results?
                
                #data[data>300] = 300
                data0 = np.mean(data[5*12:15*12,:,:], axis=0)
                data1 = np.mean(data[110*12:120*12,:,:], axis=0)


                """
                r = 50 
                c = 50
                print(data0[r,c])
                print(data1[r,c])
                print(data[35*12:45*12,r,c])
                """
                
                

                df = pd.DataFrame(np.nanmean(data, axis=(1,2)), index=pd.date_range('1980-1-1', '2100-12-31', freq='M'))
                df = df.resample('Y').mean()


                vmaxs[xx] = 600

                ax[0,0].plot(df.index, df)
                ax[0,1].imshow(data1 - data0, vmin=-vmaxs[xx]/5, vmax=vmaxs[xx]/5, cmap='coolwarm')
                ax[1,0].imshow(data0, vmin=0, vmax=vmaxs[xx])
                ax[1,1].imshow(data1, vmin=0, vmax=vmaxs[xx])
                fig.savefig(Path.work_path + 'plots/tmp_'+var+'_'+catchment_ID+'_'+str(chainID)+'.png')

if __name__ == "__main__":
    # 1214576, 748037, 1034738
    catchment_ID = '6'
    nchains = 40


    _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)


    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux')
    os.system('make all')

    
    """
    tasks = []
    for nn, chainID in enumerate(np.arange(0,nchains,1)):
        tasks.append((chainID, _param[chainID, :]))

    # Use multiprocessing pool to run in parallel
    with Pool(processes=min(cpu_count(), 40)) as pool:
        pool.starmap(foward_run_parallel, tasks)




    mask = np.loadtxt(Path.data_path+'catchment_info/forward/'+catchment_ID+'/spatial/dem.asc', skiprows=6)

    #vars = ['minerl_soil', 'deni_soil']
    vars = ['no3_SMC_layer3', 'minerl_soil', 'deni_soil']

    tindex = pd.date_range('1980-1-1', '2024-12-31', freq='M')

    for var in vars:

        fig, ax = plt.subplots(11,4, dpi=300)

        for chainID in range(nchains):
            

            output_path = '/data/scratch/wusongj/paper4/test/'+catchment_ID+'/run/' + str(chainID) +'/run/outputs/'
            data = np.fromfile(output_path+var+'_map.bin').reshape(-1, mask.shape[0], mask.shape[1])[:,83,185]

            if chainID == 0:
                cumulative_data = data
            else:
                cumulative_data += data

            ax[chainID//4, chainID%4].plot(tindex, data)

            df = pd.DataFrame(data, columns=['value'], index=tindex)
            df = df.resample('Y').mean()
            ax1 = ax[chainID//4, chainID%4].twinx()
            ax1.plot(df.index,df.value, c='red')

            print(var, chainID)
        
        data = cumulative_data/nchains
        ax[10,0].plot(tindex, data)
        df = pd.DataFrame(data, columns=['value'], index=tindex)
        df = df.resample('Y').mean()
        ax1 = ax[10,0].twinx()
        ax1.plot(df.index,df.value, c='red')

        periods = [[12*5,12*15], [12*35, 12*45]]
        print(np.mean(data[(0+24):(12*8+24)]), np.mean(data[(12*28+24):(12*38+24)]))

        fig.savefig('/data/scratch/wusongj/paper4/plots/'+var+'.png')
    """


    

  
    # Post run for all failed catchments
    #boardcast_from_root_spatial_path()
    #forward_run_again()
    forward_run_again_all_chain_parallel(experiment='ssp126')

    #result_transfer_second_post_run()

    experiment='ssp126'
    #experiment=''
    #test1_examine_experiment_inputs(experiment)
    #check_climate_experiments()
    #plot_forward_results(experiment)

    #plot_forward_results_tmp(experiment)

    #foward_run_debug(catchment_ID='566445', chainID=1, nn=0, save_output_flag=True, experiment=experiment)

    #shutil.copytree('/data/scratch/wusongj/paper4/test/outputs/566445', '/data/scratch/wusongj/paper4/forward_all/outputs/cali/monthly/566445/all_ssp126')

    """
    mask = np.loadtxt(Path.data_path+'catchment_info/land_mask_3035.asc', skiprows=6)
    data = np.fromfile('/data/scratch/wusongj/paper4/forward_all/outputs/cali_merged/monthly/all/young_water_fraction_soil_all_depths.bin')
    data = np.mean(data.reshape(-1, mask.shape[0], mask.shape[1]), axis=0)

    
    GEM_tools.create_asc(data, 'young_water_fraction_soil_all_depths.asc', '/data/scratch/wusongj/paper4/data/catchment_info/land_mask_3035.asc')
    """




    
