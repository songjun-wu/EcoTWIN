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
    for niteration in np.arange(0, 1e4, Cali.niterations)[::-1]:
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

                _sim = np.array([])
                
                os.chdir(runpath)
                for i in range(param.shape[0]):
                    shutil.rmtree(runpath + '/outputs')
                    os.mkdir(runpath + '/outputs')
                    GEM_tools.gen_param(runpath, Info, Param, param[i,:])
                    os.system('./gEcoHydro')
                    _sim = np.append(_sim, np.fromfile(runpath + '/outputs/discharge_TS.bin'))
                _sim.tofile(Path.work_path + '/forward/outputs/discharge_TS.bin')
                flag = False
            except:
                pass
        else:
            break
            

    

elif mode == 'test':
    
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')

    # set the env
    GEM_tools.set_env(mode, Path, Cali)
    GEM_tools.set_config(mode, Path, Cali)

    #for i in range(Cali.nchains):
    for i in [10]:
        # Which parameter set to use?
        param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1)[i,:]
        #param = np.full(104, 0.5)
        GEM_tools.gen_param(Path.run_path, Info, Param, param)

        # Model run
        os.chdir(Path.run_path)
        os.system('./gEcoHydro')

        os.chdir(current_path)
        os.system('python3 posterior_anlalysis.py')
        try:
            os.remove('999_All_in_Ts_'+str(i)+'.png')
            os.remove('999_All_in_map_'+str(i)+'.png')
        except:
            pass
        try:
            shutil.copyfile(Path.output_path + '999_All_in_Ts.png', '999_All_in_Ts.png')
            os.rename('999_All_in_Ts.png', '999_All_in_Ts_'+str(i)+'.png')
            shutil.copyfile(Path.output_path + '999_All_in_map.png', '999_All_in_map.png')
            os.rename('999_All_in_map.png', '999_All_in_map_'+str(i)+'.png')
        except Exception as e:
            print(e)
            pass
        


elif mode == 'check':
    arr = []
    lengths = []
    niterations = []

    for i in range(Cali.nchains):
        flag = True
        for niteration in np.arange(0, 1e4, Cali.niterations)[::-1]:
            if flag:
                try:
                    loglikes = np.fromfile('/data/scratch/wusongj/paper4/results/DREAM_cali_DMC_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                    #print(len(loglikes), loglikes[-1], np.max(loglikes))
                    arr.append(np.max(loglikes))
                    lengths.append(len(loglikes))
                    niterations.append(niteration)
                    flag = False
                except:
                    pass
            else:
                break
    print('Batch   :  ', int(np.mean(niterations)), np.mean(lengths))
    print('Average :  ' ,np.mean(arr))
    print('Maximum :  ' ,np.max(arr))


elif mode == 'aaa':
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    sim = np.fromfile(Path.work_path + '/forward/outputs/discharge_TS.bin').reshape(Cali.nchains, -1)[:, 731:]
    obs = np.fromfile(Path.data_path + 'discharge_obs.bin')

    fig, ax = plt.subplots(1,1, figsize=(4,2), dpi=300)
    X = np.arange(datetime(1994,1,1), datetime(2022,1,2), timedelta(days=1)).astype(datetime)
    ax.fill_between(X, np.percentile(sim[:,:], 5, axis=0), np.percentile(sim[:,:], 95, axis=0), linewidth=1, alpha=0.4, color='skyblue', zorder=2)
    ax.plot(X, np.mean(sim[:,:], axis=0), linewidth=1, c='skyblue', zorder=3)
    ax.scatter(X, obs, c='salmon', s=0.3, alpha=0.2, zorder=1)
    fig.savefig('tmp.png')

    for i in range(Cali.nchains):
        X = sim[i,:] + 1e-3
        Y = obs + 1e-3
        print(GEM_tools.nse(X, Y), GEM_tools.lnnse(X, Y))
    X = np.mean(sim,axis=0) + 1e-3
    print(GEM_tools.nse(X, Y), GEM_tools.lnnse(X, Y))

    _nse = 0.2055
    _lnnse =  0.0331
    err = np.power(1*(1 - _nse)**6 + 0*(1 - _lnnse)**6, 1/6)
    print(np.log(err))
