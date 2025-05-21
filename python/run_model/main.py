import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
import numpy as np
import time



#  OPTIONS
parser = OptionParser()
current_path = os.getcwd()
parser.add_option("--mode",dest="mode",metavar="mode",
                  help="Switch ('DREAM_cali','test')")
parser.add_option("--def_py",dest="def_py",metavar="def_py",
                  help="Configuration file for GEM Protocol")
(options, args) = parser.parse_args()
mode = options.mode

if options.def_py == None:
    options.def_py = 'def_GEM'
if mode == 'DREAM_cali':
    options.def_py = 'def_GEM_cali'

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')



if mode == 'DREAM_cali':
    #GEM_tools.sort_directory(mode, Path, Cali, Output)
    #GEM_tools.set_env(mode, Path, Cali.nchains, Output)
    #GEM_tools.set_config(mode, Path, Cali, Output)

    nbatch = Cali.nbatchs

    cmds = []
    if not Cali.restart:
        nbatch -= 1
        cmds.append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode DREAM_cali --def_py def_GEM_cali --niteration '+str(Cali.niterations)+ \
                    ' --restart False  --restart_niteration ' + str(Cali.restart_niteration))
        for i in range(nbatch):
            cmds.append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode DREAM_cali --def_py def_GEM_cali --niteration '+str(Cali.niterations)+ \
                    ' --restart True  --restart_niteration ' + str(Cali.niterations * (i+1)))
    else:
        for i in range(nbatch):
            cmds.append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode DREAM_cali --def_py def_GEM_cali --niteration '+str(Cali.niterations)+ \
                     ' --restart True  --restart_niteration ' + str(Cali.restart_niteration + Cali.niterations * i ))
    
    for cmd in cmds:
        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali.slurm', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'mpirun' in lines[i]:
                lines[i] = cmd
        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali.slurm', 'w') as f:
            f.writelines(lines)

        os.system('sh protocal_cali.sh')
        print(cmd)
        while (GEM_tools.checkTaskStatus('dmc_cali') > 0):
            time.sleep(10)
    

        
        
elif mode == 'forward':

    runpath = Path.work_path + '/forward/run/'

    os.chdir(Path.work_path)
    # Create and clean the directory
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)

    flag = True
    for niteration in np.arange(0, 1e5, Cali.niterations)[::-1]:
        if flag:
            try:
                # Get param
                param = np.array([])
                for i in range(Cali.nchains):
                    likeli = np.fromfile(Path.result_path + 'DREAM_cali_DMC_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                    tmp = np.fromfile(Path.result_path + 'DREAM_cali_DMC_sampled_params_chain_'+str(i)+'_'+str(int(niteration))+'.bin').reshape(len(likeli), -1)
                    param = np.append(param, tmp[np.argwhere(likeli == np.max(likeli))[-1][-1], :])
                    print(niteration, likeli[np.argwhere(likeli == np.max(likeli))[-1][-1]])

                param.tofile(Path.work_path + 'param.bin')
                param = param.reshape(Cali.nchains, -1)

                _sim_q = np.array([])
                _sim_iso = np.array([])
                _sim_no3 = np.array([])
                
                os.chdir(runpath)
                for i in range(param.shape[0]):
                    shutil.rmtree(runpath + '/outputs')
                    os.mkdir(runpath + '/outputs')
                    GEM_tools.gen_param(runpath, Info, Param, param[i,:])
                    GEM_tools.gen_no3_addtion(runpath, Info)
                    os.system('./gEcoHydro')
                    _sim_q = np.append(_sim_q, np.fromfile(runpath + '/outputs/discharge_TS.bin'))
                    _sim_iso = np.append(_sim_iso, np.fromfile(runpath + '/outputs/d18o_chanS_TS.bin'))
                    _sim_no3 = np.append(_sim_no3, np.fromfile(runpath + '/outputs/no3_chanS_TS.bin'))
                    
                _sim_q.tofile(Path.work_path + '/forward/outputs/discharge_TS.bin')
                _sim_iso.tofile(Path.work_path + '/forward/outputs/d18o_chanS_TS.bin')
                _sim_no3.tofile(Path.work_path + '/forward/outputs/no3_chanS_TS.bin')
                flag = False
            except:
                pass
        else:
            break
            

    

elif mode == 'test':
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # set the env
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)

    #validIdx = np.loadtxt('/data/scratch/wusongj/paper4/param_good.txt').astype(np.int)
    
    counter = 0
    #for i in range(len(validIdx)):
    for i in [4]:
        #for gg in range(len(Output.Catchment_ID)):
        for gg in [0]:
            catchment_ID = Output.Catchment_ID[gg]
            print(Output.Catchment_ID)
            run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'
            #idx = validIdx[i]
            idx = i
            print(idx)
            # Which parameter set to use?
            #param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1)[idx,:]
            param = np.full(300, 0.5)
            GEM_tools.gen_param(run_path, Info, Param, param)
            GEM_tools.gen_no3_addtion(run_path, Info)

            # Model run
            os.chdir(run_path)
            os.system('./gEcoHydro')

            





            """
            # Save outputs
            fnames = os.listdir(run_path + 'outputs/')
            save_path = '/data/scratch/wusongj/paper4/forward/outputs_posterior/'
            for fname in fnames:
                if fname.split('.')[-1] == 'bin':
                    if (counter==0):
                        if os.path.exists(save_path + fname):
                            os.remove(save_path + fname)
                        f = open(save_path + fname, 'w')
                        f.close()
                    with open(save_path + fname, 'ab+') as f:
                        np.fromfile(run_path + 'outputs/' + fname).tofile(f)
            
            counter += 1
                    
            # Plot individual results
            os.chdir(current_path)
            os.system('python3 posterior_anlalysis.py')

            try:
                shutil.copyfile(Path.output_path + '999_All_in_Ts.png', 'plots/999_All_in_Ts.png')
                if os.path.exists('plots/999_All_in_Ts_'+str(idx)+'.png'):
                    os.remove('plots/999_All_in_Ts_'+str(idx)+'.png')
                os.rename('plots/999_All_in_Ts.png', 'plots/999_All_in_Ts_'+str(idx)+'.png')
            except Exception as e:
                pass
            
            try:
                shutil.copyfile(Path.output_path + '999_All_in_map.png', 'plots/999_All_in_map.png')
                if os.path.exists('plots/999_All_in_map_'+str(idx)+'.png'):
                    os.remove('plots/999_All_in_map_'+str(idx)+'.png')
                os.rename('plots/999_All_in_map.png', 'plots/999_All_in_map_'+str(idx)+'.png')
            except Exception as e:
                pass

            try:
                shutil.copyfile(Path.output_path + '999_All_in_Ts_tracking.png', 'plots/999_All_in_Ts_tracking.png')
                if os.path.exists('plots/999_All_in_Ts_'+str(idx)+'_tracking.png'):
                    os.remove('plots/999_All_in_Ts_'+str(idx)+'_tracking.png')
                os.rename('plots/999_All_in_Ts_tracking.png', 'plots/999_All_in_Ts_'+str(idx)+'_tracking.png')
            except Exception as e:
                pass
            
            try:
                shutil.copyfile(Path.output_path + '999_All_in_map_tracking.png', 'plots/999_All_in_map_tracking.png')
                if os.path.exists('plots/999_All_in_map_'+str(idx)+'_tracking.png'):
                    os.remove('plots/999_All_in_map_'+str(idx)+'_tracking.png')
                os.rename('plots/999_All_in_map_tracking.png', 'plots/999_All_in_map_'+str(idx)+'_tracking.png')
            except Exception as e:
                pass
            """


elif mode == 'check':
    arr = []
    lengths = []
    niterations = []
    n_batch = 0
    for i in range(Cali.nchains):
        flag = True
        for niteration in np.arange(0, 2e5, Cali.niterations)[::-1]:
            if flag:
                try:
                    loglikes = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                    #print(len(loglikes), loglikes[-1], np.max(loglikes))
                    arr.append(np.nanmax(loglikes))
                    lengths.append(len(loglikes))
                    niterations.append(niteration)
                    flag = False
                    n_batch += 1
                except:
                    pass
            else:
                break

    print(niterations, lengths)
    print('Chains  :  ', n_batch)
    print('Batch   :  ', int(np.mean(niterations)), np.mean(lengths))
    print('Average :  ', np.mean(arr))
    print('Maximum :  ', np.max(arr))
    print(arr)

elif mode == 'test11':
    loglikes = np.fromfile('/data/scratch/wusongj/paper4/results/DREAM_cali_DMC_logps_chain_'+str(93)+'_500.bin')
    param = np.fromfile('/data/scratch/wusongj/paper4/results/DREAM_cali_DMC_sampled_params_chain_'+str(93)+'_500.bin')
    print(param)

elif mode == 'aaa':
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    sim_q = np.transpose(np.fromfile(Path.work_path + '/forward/outputs/discharge_TS.bin').reshape(Cali.nchains, -1, Output.N_sites), axes=[0,2,1])[:, :, Info.spin_up:]  
    obs_q = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)

    sim_iso = np.transpose(np.fromfile(Path.work_path + '/forward/outputs/d18o_chanS_TS.bin').reshape(Cali.nchains, -1, Output.N_sites), axes=[0,2,1])[:, :, Info.spin_up:]  
    obs_iso = np.fromfile(Path.data_path + 'd18o_stream_obs.bin').reshape(len(Output.sim['iso_stream']['sim_idx']), -1)

    sim_no3 = np.transpose(np.fromfile(Path.work_path + '/forward/outputs/no3_chanS_TS.bin').reshape(Cali.nchains, -1, Output.N_sites), axes=[0,2,1])[:, :, Info.spin_up:]  
    obs_no3 = np.fromfile(Path.data_path + 'no3_stream_obs.bin').reshape(len(Output.sim['no3']['sim_idx']), -1)

    validIdx = []
    
    for i in range(Cali.nchains):
        likelihoods = []
        print(i, end='  ')
        for j in range(len(Output.sim['q']['sim_idx'])):
            X = sim_q[i, Output.sim['q']['sim_idx'][j],:] + 1e-3
            Y = obs_q[j] + 1e-3
            likelihoods.append(GEM_tools.kge(X, Y))
            print(np.round(GEM_tools.kge(X, Y),2), end=" ")
        print(end="     ")
        for j in range(len(Output.sim['iso_stream']['sim_idx'])):
            X = sim_iso[i, Output.sim['iso_stream']['sim_idx'][j],:]
            Y = obs_iso[j]
            likelihoods.append(GEM_tools.kge(X, Y))
            print(np.round(GEM_tools.kge(X, Y),2), end=" ")
        for j in range(len(Output.sim['no3']['sim_idx'])):
            X = sim_no3[i, Output.sim['no3']['sim_idx'][j],:]
            Y = obs_no3[j]
            likelihoods.append(GEM_tools.kge(X, Y))
            print(np.round(GEM_tools.kge(X, Y),2), end=" ")
            
        print('')
        if np.mean(np.array(likelihoods)[[4,5,6]]) > 0.6:
            validIdx.append(i)

    np.savetxt('/data/scratch/wusongj/paper4/param_good.txt', validIdx)
    print(len(validIdx))
    
    sim_q = sim_q[validIdx, :, :][:,Output.sim['q']['sim_idx'],:]
    sim_iso = sim_iso[validIdx, :, :][:,Output.sim['iso_stream']['sim_idx'],:]



    fig, ax = plt.subplots(4,3, figsize=(12,6), dpi=300)
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.99, top=0.99, wspace=0.1, hspace=0.1)
    X = np.arange(datetime(1994,1,1), datetime(2022,1,2), timedelta(days=1)).astype(datetime)
    for i in range(obs_q.shape[0]):
        ax[i,0].fill_between(X, np.percentile(sim_q[:,i,:], 5, axis=0), np.percentile(sim_q[:,i,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
        ax[i,0].plot(X, np.mean(sim_q[:,i,:], axis=0), linewidth=1, c='skyblue', zorder=3)
        ax[i,0].scatter(X, obs_q[i,:], c='salmon', s=0.3, alpha=0.2, zorder=1)
        ax[i,0].set_ylim([-0.1, 1.5])
        ax[i,0].set_yticks([0, 0.5, 1, 1.5])

        ax[i,1].fill_between(X, np.percentile(sim_iso[:,i,:], 5, axis=0), np.percentile(sim_iso[:,i,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
        ax[i,1].plot(X, np.mean(sim_iso[:,i,:], axis=0), linewidth=1, c='skyblue', zorder=3)
        ax[i,1].scatter(X, obs_iso[i,:], c='salmon', s=0.8, alpha=0.2, zorder=4)
        ax[i,1].set_ylim([-10.5, -3])
        ax[i,1].set_yticks([-10, -8, -6, -4])

        ax[i,2].fill_between(X, np.percentile(sim_no3[:,i,:], 5, axis=0), np.percentile(sim_no3[:,i,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
        ax[i,2].plot(X, np.mean(sim_no3[:,i,:], axis=0), linewidth=1, c='skyblue', zorder=3)
        ax[i,2].scatter(X, obs_no3[i,:], c='salmon', s=0.8, alpha=0.2, zorder=4)
        ax[i,2].set_ylim([0, 40])
        ax[i,2].set_yticks([0, 6, 12, 18])

        if i!=(obs_q.shape[0]-1):
            ax[i,0].set_xticklabels([])
            ax[i,1].set_xticklabels([])
            ax[i,2].set_xticklabels([])

    sites = [['Bruch Mill', 'Demnitz Mill', 'Demnitz', "Berkenbrueck"],
             ['Peat South', 'Bruch Mill', 'Demnitz Mill', "Berkenbrueck"]]
    for i in range(obs_q.shape[0]):
        X = np.mean(sim_q[:, i, :],axis=0) + 1e-3
        Y = obs_q[i] + 1e-3
        title_hgt = 0.9
        hgt_gradient = 0.11
        ax[i,0].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge11(X, Y), 2)), fontsize=8, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,0].transAxes)
        #ax[i,0].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(X, Y), 2)), fontsize=7, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,0].transAxes)
        ax[i,0].text(0.05, title_hgt - hgt_gradient * 1, 'Q at '+sites[0][i]+' (m3/s)', fontsize=8, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i,0].transAxes)        
        print(np.round(GEM_tools.nse(X, Y), 2), np.round(GEM_tools.kge(X, Y), 2), end='     ')

        X = np.mean(sim_iso[:, i, :],axis=0)
        Y = obs_iso[i]
        title_hgt = 0.9
        hgt_gradient = 0.11
        ax[i,1].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge11(X, Y), 2)), fontsize=8, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,1].transAxes)
        #ax[i,1].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(X, Y), 2)), fontsize=8, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,1].transAxes)
        ax[i,1].text(0.05, title_hgt - hgt_gradient * 1, 'd18O at '+sites[1][i]+' (per mille)', fontsize=8, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i,1].transAxes)        
        print(np.round(GEM_tools.nse(X, Y), 2), np.round(GEM_tools.kge(X, Y), 2), end='     ')

        X = np.mean(sim_no3[:, i, :],axis=0)
        Y = obs_no3[i]
        title_hgt = 0.9
        hgt_gradient = 0.11
        ax[i,2].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge11(X, Y), 2)), fontsize=8, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,2].transAxes)
        #ax[i,2].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(X, Y), 2)), fontsize=8, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,2].transAxes)
        ax[i,2].text(0.05, title_hgt - hgt_gradient * 1, 'NO3 at '+sites[1][i]+' (mgN/L)', fontsize=8, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i,2].transAxes)        
        print(np.round(GEM_tools.nse(X, Y), 2), np.round(GEM_tools.kge(X, Y), 2))
    
    fig.savefig('tmp.png')



elif mode == 'bbb':
    
    for gg in [0]:
        """"""
        catchment_ID = Output.Catchment_ID[gg]
        nsites = len(np.unique(Output.sim_q_idx[gg]+Output.sim_iso_idx[gg]+Output.sim_no3_idx[gg]))
        discharge = np.fromfile('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/discharge_TS.bin').reshape(-1,nsites)
        iso = np.fromfile('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/d18o_chanS_TS.bin').reshape(-1,nsites)
        no3 = np.fromfile('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/no3_chanS_TS.bin').reshape(-1,nsites)
        print(discharge.shape)
        print(iso.shape)
        print(no3.shape)

        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/discharge_TS.txt', discharge)
        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/d18o_chanS_TS.txt', iso)
        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/no3_chanS_TS.txt', no3)

        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/discharge_TS_mean.txt', np.mean(discharge, axis=1))
        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/d18o_chanS_TS_mean.txt', np.mean(iso, axis=1))
        np.savetxt('/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/outputs/no3_chanS_TS_mean.txt', np.mean(no3, axis=1))
        

        for fname in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/cali/6/climate/'):
            if not fname.endswith('bin'):
                continue
            if fname != 'LAI.bin':
                data = np.fromfile('/data/scratch/wusongj/paper4/data/catchment_info/cali/6/climate/' + fname).reshape(16437, -1)
                np.savetxt('/data/scratch/wusongj/paper4/test/' + fname.split('.')[0] + '.txt', data[:,43])
                print(fname, data.shape)
            else:
                data = np.fromfile('/data/scratch/wusongj/paper4/data/catchment_info/cali/6/climate/LAI.bin').reshape(-1,  185, 160)
                np.savetxt('/data/scratch/wusongj/paper4/data/catchment_info/cali/6/climate/LAI.txt', data[:, 37, 60])
                print(fname, data.shape)




elif mode == 'examine_inputs':
    """
    path1 = '/data/scratch/wusongj/paper4/data/catchment_info/cali/291110/'
    path2 = '/home/wusongj/GEM/test_dmc1//'
    vars = os.listdir(path1+'climate')
    for var in vars:
        try:
            data1 = np.fromfile(path1+'climate/'+var, dtype=np.float64)
            data2 = np.fromfile(path2+'climate/'+var, dtype=np.float64)
            data1[data1==-9999] = np.nan
            data2[data2==-9999] = np.nan
            print(var, np.nanmean(data1), np.nanmean(data2))
        except:
            pass
    

    path1 = '/data/scratch/wusongj/paper4/data/catchment_info/cali/291110/'
    path2 = '/home/wusongj/GEM/test_dmc1/'
    vars = sorted(os.listdir(path1+'spatial/'))
    for var in vars:
        try:
            if var.endswith('asc'):
                data1 = np.loadtxt(path1+'spatial/'+var, skiprows=6)
                data2 = np.loadtxt(path2+'spatial/'+var, skiprows=6)
                data1[data1==-9999] = np.nan
                data2[data2==-9999] = np.nan
                print(var, np.nanmean(data1), np.nanmean(data2))
            elif var.endswith('bin'):
                data1 = np.fromfile(path1+'spatial/'+var, dtype=np.float64)
                data2 = np.fromfile(path2+'spatial/'+var, dtype=np.float64)
                data1[data1==-9999] = np.nan
                data2[data2==-9999] = np.nan
                print(var, np.nanmean(data1), np.nanmean(data2))
        except:
            pass

    cat_0 = np.fromfile('/data/scratch/wusongj/paper4/data/catchment_info/cali/291110/spatial/category_0.bin')
    print(cat_0)
    """
    pass
