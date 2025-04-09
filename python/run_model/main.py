import os
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

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')




if mode == 'DREAM_cali':
    from pydream.core import run_dream
    from pydream.parameters import SampledParam
    from pydream.convergence import Gelman_Rubin
    from scipy.stats import uniform
    from likelihood import likelihood

    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')

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




    

elif mode == 'test':
    
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')

    # set the env
    GEM_tools.set_env(mode, Path, Cali)
    GEM_tools.set_config(mode, Path, Cali)
    GEM_tools.gen_param(Path.run_path, Info, Param, np.full(19+5*20, 0.5))

    # Model run
    os.chdir(Path.run_path)
    os.system('./gEcoHydro')

    os.chdir(current_path)
    os.system('python3 posterior_anlalysis.py')


elif mode == 'check_cali':
    for i in range(10):
        loglikes = np.fromfile('/data/scratch/wusongj/paper4/results/DREAM_cali_DMC_logps_chain_'+str(i)+'_500.bin')
        print(len(loglikes), loglikes[-1])
