import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
import numpy as np



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

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')




if mode == 'DREAM_cali':
    from pydream.core import run_dream
    from pydream.parameters import SampledParam
    from pydream.convergence import Gelman_Rubin
    from scipy.stats import uniform
    from likelihood import likelihood

    # Model structure update
    #os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    #os.system('python3 develop.py')

    os.chdir(Path.work_path)
    
    # Create and clean the directory
    GEM_tools.sort_directory(mode, Path, Cali)
    GEM_tools.set_env(mode, Path, Cali)
    GEM_tools.set_config(mode, Path, Cali)
    param_N = GEM_tools.get_param_N(Info, Param)

    # Define parameters
    parameters_to_sample = SampledParam(uniform, loc=np.full(param_N, 0.0), scale=1) # Parameter ranges from 0 to 1

    # Start calibration
    try:
        Cali.nchains = int(os.environ.get('SLURM_NTASKS', 20))
    except:
        pass
    if not Cali.restart:
        total_iterations = Cali.niterations
        run_dream(savePath=Path.result_path, parameters=[parameters_to_sample], likelihood=likelihood, niterations=Cali.niterations, total_iterations=total_iterations, nchains=Cali.nchains, multitry=False, gamma_levels=4, adapt_gamma=True, history_thin=1, model_name=Cali.TASK_name, verbose=False, restart=False)
    
        for i in range(Cali.nbatchs-1):
            starts = GEM_tools.get_restart_param(Path, Cali, param_N, total_iterations)
            total_iterations += Cali.niterations
            run_dream(savePath=Path.result_path, parameters=[parameters_to_sample], likelihood=likelihood,
                                                niterations=Cali.niterations, total_iterations=total_iterations,  nchains=Cali.nchains, start=starts, multitry=False, gamma_levels=4,
                                                adapt_gamma=True, history_thin=1, model_name=Cali.TASK_name,
                                                verbose=False, restart=True)
    else:
        total_iterations = Cali.restart_niteration

        for i in range(Cali.nbatchs):
            starts = GEM_tools.get_restart_param(Path, Cali, param_N, total_iterations)
            total_iterations += Cali.niterations
            run_dream(savePath=Path.result_path, parameters=[parameters_to_sample], likelihood=likelihood,
                                                niterations=Cali.niterations, total_iterations=total_iterations,  nchains=Cali.nchains, start=starts, multitry=False, gamma_levels=4,
                                                adapt_gamma=True, history_thin=1, model_name=Cali.TASK_name,
                                                verbose=False, restart=True)
        
        
elif mode == 'forward':

    runpath = Path.work_path + '/forward/run/'

    os.chdir(Path.work_path)
    # Create and clean the directory
    GEM_tools.sort_directory(mode, Path, Cali)
    GEM_tools.set_env(mode, Path, Cali)
    GEM_tools.set_config(mode, Path, Cali)

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
                
                os.chdir(runpath)
                for i in range(param.shape[0]):
                    shutil.rmtree(runpath + '/outputs')
                    os.mkdir(runpath + '/outputs')
                    GEM_tools.gen_param(runpath, Info, Param, param[i,:])
                    os.system('./gEcoHydro')
                    _sim_q = np.append(_sim_q, np.fromfile(runpath + '/outputs/discharge_TS.bin'))
                    _sim_iso = np.append(_sim_iso, np.fromfile(runpath + '/outputs/d18o_chanS_TS.bin'))
                    
                _sim_q.tofile(Path.work_path + '/forward/outputs/discharge_TS.bin')
                _sim_iso.tofile(Path.work_path + '/forward/outputs/d18o_chanS_TS.bin')
                flag = False
            except:
                pass
        else:
            break
            

    

elif mode == 'test':
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    #os.system('python3 develop.py')  # todo

    # set the env
    GEM_tools.set_env(mode, Path, Cali)
    GEM_tools.set_config(mode, Path, Cali)

    validIdx = np.loadtxt('/data/scratch/wusongj/paper4/param_good.txt').astype(np.int)
    
    #for i in range(len(validIdx)):
    for i in [0]:
        idx = validIdx[i]
        print(idx)
        # Which parameter set to use?
        param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1)[idx,:]
        #param = np.append(param, np.full(50, 0.5))
        #param = np.full(150, 0.5)
        GEM_tools.gen_param(Path.run_path, Info, Param, param)
        GEM_tools.gen_no3_addtion(Path.run_path, Info)
        """"""
        # Model run
        os.chdir(Path.run_path)
        os.system('./gEcoHydro')

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
        


elif mode == 'check':
    arr = []
    lengths = []
    niterations = []
    n_batch = 0
    for i in range(Cali.nchains):
        flag = True
        for niteration in np.arange(0, 1e5, Cali.niterations)[::-1]:
            if flag:
                try:
                    loglikes = np.fromfile('/data/scratch/wusongj/paper4/results/DREAM_cali_DMC_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                    #print(len(loglikes), loglikes[-1], np.max(loglikes))
                    arr.append(np.max(loglikes))
                    lengths.append(len(loglikes))
                    niterations.append(niteration)
                    flag = False
                    n_batch += 1
                except:
                    pass
            else:
                break
    print('Chains  :  ', n_batch)
    print('Batch   :  ', int(np.mean(niterations)), np.mean(lengths))
    print('Average :  ' ,np.mean(arr))
    print('Maximum :  ' ,np.max(arr))



elif mode == 'aaa':
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    sim_q = np.transpose(np.fromfile(Path.work_path + '/forward/outputs/discharge_TS.bin').reshape(Cali.nchains, -1, Output.N_sites), axes=[0,2,1])[:, :, Info.spin_up:]  
    obs_q = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)

    sim_iso = np.transpose(np.fromfile(Path.work_path + '/forward/outputs/d18o_chanS_TS.bin').reshape(Cali.nchains, -1, Output.N_sites), axes=[0,2,1])[:, :, Info.spin_up:]  
    obs_iso = np.fromfile(Path.data_path + 'd18o_stream_obs.bin').reshape(len(Output.sim['iso_stream']['sim_idx']), -1)


    validIdx = []
    
    for i in range(Cali.nchains):
        likelihoods = []
        print(i, end='  ')
        for j in range(len(Output.sim['q']['sim_idx'])):
            X = sim_q[i, Output.sim['q']['sim_idx'][j],:] + 1e-3
            Y = obs_q[j] + 1e-3
            likelihoods.append(GEM_tools.nse(X, Y))
            print(np.round(GEM_tools.nse(X, Y),2), end=" ")
        print(end="     ")
        for j in range(len(Output.sim['iso_stream']['sim_idx'])):
            X = sim_iso[i, Output.sim['iso_stream']['sim_idx'][j],:]
            Y = obs_iso[j]
            likelihoods.append(GEM_tools.nse(X, Y))
            print(np.round(GEM_tools.nse(X, Y),2), end=" ")
            
        print('')
        if np.mean(likelihoods[:3]) > 0.4:
            validIdx.append(i)
    np.savetxt('/data/scratch/wusongj/paper4/param_good.txt', validIdx)
    print(len(validIdx))
    
    sim_q = sim_q[validIdx, :, :][:,Output.sim['q']['sim_idx'],:]
    sim_iso = sim_iso[validIdx, :, :][:,Output.sim['iso_stream']['sim_idx'],:]

    fig, ax = plt.subplots(4,2, figsize=(8,6), dpi=300)
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.99, top=0.99, wspace=0.1, hspace=0.1)
    X = np.arange(datetime(1994,1,1), datetime(2022,1,2), timedelta(days=1)).astype(datetime)
    for i in range(obs_q.shape[0]):
        ax[i,0].fill_between(X, np.percentile(sim_q[:,i,:], 5, axis=0), np.percentile(sim_q[:,i,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
        ax[i,0].plot(X, np.mean(sim_q[:,i,:], axis=0), linewidth=1, c='skyblue', zorder=3)
        ax[i,0].scatter(X, obs_q[i,:], c='salmon', s=0.3, alpha=0.2, zorder=1)

        ax[i,1].fill_between(X, np.percentile(sim_iso[:,i,:], 5, axis=0), np.percentile(sim_iso[:,i,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
        ax[i,1].plot(X, np.mean(sim_iso[:,i,:], axis=0), linewidth=1, c='skyblue', zorder=3)
        ax[i,1].scatter(X, obs_iso[i,:], c='salmon', s=0.3, alpha=0.2, zorder=1)

        if i!=(obs_q.shape[0]-1):
            ax[i,0].set_xticklabels([])
            ax[i,1].set_xticklabels([])

    sites = [['Bruch Mill', 'Demnitz Mill', 'Demnitz', "Berkenbrueck"],
             ['Peat South', 'Bruch Mill', 'Demnitz Mill', "Berkenbrueck"]]
    for i in range(obs_q.shape[0]):
        X = np.mean(sim_q[:, i, :],axis=0) + 1e-3
        Y = obs_q[i] + 1e-3

        title_hgt = 0.9
        hgt_gradient = 0.11
        ax[i,0].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(X, Y), 2)), fontsize=7, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,0].transAxes)
        ax[i,0].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(X, Y), 2)), fontsize=7, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,0].transAxes)
        ax[i,0].text(0.05, title_hgt - hgt_gradient * 1, 'Q at '+sites[0][i]+' (m3/s)', fontsize=8, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i,0].transAxes)        
        print(np.round(GEM_tools.nse(X, Y), 2))
        X = np.mean(sim_iso[:, i, :],axis=0)
        Y = obs_iso[i]
        title_hgt = 0.9
        hgt_gradient = 0.11
        ax[i,1].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(X, Y), 2)), fontsize=7, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,1].transAxes)
        ax[i,1].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(X, Y), 2)), fontsize=7, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i,1].transAxes)
        ax[i,1].text(0.05, title_hgt - hgt_gradient * 1, 'd18O at '+sites[1][i]+' (per mille)', fontsize=8, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i,1].transAxes)        
        
    
    fig.savefig('tmp.png')