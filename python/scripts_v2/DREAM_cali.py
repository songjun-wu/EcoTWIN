import os
import sys
from optparse import OptionParser
import numpy as np
from mpi4py import MPI
from scipy.stats import uniform
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/run_model')
import GEM_tools_v2
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parse command line arguments
parser = OptionParser()
parser.add_option("--mode", dest="mode", help="Switch ('DREAM_cali','test')")
parser.add_option("--def_py", dest="def_py", help="Configuration file for GEM Protocol")
parser.add_option("--niterations", dest="niterations", help="  ")
parser.add_option("--restart", dest="restart", help="  ")
parser.add_option("--restart_niteration", dest="restart_niteration", help="  ")
parser.add_option("--likelihood", dest="likelihood", help="  ")

(options, args) = parser.parse_args()

if options.def_py is None:
    options.def_py = 'def_GEM_cali'

if options.restart == 'True':
    options.restart = True
else:
    options.restart = False

options.niterations = int(options.niterations)
options.restart_niteration = int(options.restart_niteration)


def build_history(TASK_name, nchains, total_iterations, param_N, history_thin):
    _arr = []
    for i in range(nchains):
        
        arr = np.fromfile('results/'+TASK_name + '_sampled_params_chain_'+str(i)+'_'+str(total_iterations)+'.bin').reshape(-1, param_N)
        arr_dim = arr.shape[0]
        arr_idx = np.arange(arr_dim, 0, -history_thin)[::-1] - 1        
        arr = arr[arr_idx, :]
        _arr.append(arr)


    lengths = [x.shape[0] for x in _arr]
    if np.any(lengths != min(lengths)):
        _arr = [x[(x.shape[0] - min(lengths)):, :] for x in _arr]
    
    _arr = np.transpose(np.array(_arr), (1,0,2)).flatten()
    
    np.save(TASK_name+'_DREAM_chain_history.npy', _arr)
    np.save(TASK_name+'_DREAM_chain_adapted_crossoverprob.npy', [0.33])
    np.save(TASK_name+'_DREAM_chain_adapted_gammalevelprob.npy', [0.4])




try:
    # Import configuration
    sys.path.insert(0, os.getcwd())
    config = __import__(options.def_py)
    Path = config.Path
    Cali = config.Cali
    Info = config.Info
    Param = config.Param
    Output = config.Output
    
    history_thin = Cali.history_thin
    if options.likelihood is not None:
        exec('from ' + options.likelihood + ' import *')
    else:
        if options.mode == 'DREAM_cali':
            from likelihood import likelihood
        elif options.mode == 'cali_sep':
            from likelihood_sep import likelihood
    

    if options.mode == 'DREAM_cali' or options.mode == 'cali_sep':
        from pydream.core import run_dream
        from pydream.parameters import SampledParam

        # Set number of chains equal to number of processes
        nchains = min(size // Cali.cores_for_each_chain, Cali.nchains)
        Cali.nchains = nchains

        if rank != 0:
            time.sleep(5)

        # Only rank 0 does initialization
        if rank == 0:
            try:
                os.chdir(Path.work_path)
                GEM_tools_v2.sort_directory(options.mode, Path, Cali, Output)
                GEM_tools_v2.set_env(options.mode, Path, Cali, Output)
                GEM_tools_v2.set_config(options.mode, Path, Info, Cali, Output)
                param_N = GEM_tools_v2.get_param_N(Info, Param)
                print(f"Rank 0: Initialization complete. Starting {nchains} chains, param_N={param_N}", flush=True)
            except Exception as e:
                print(f"Rank 0: Initialization failed: {e}", flush=True)
                raise
        else:
            os.chdir(Path.work_path)
            param_N = None

        

        # Broadcast necessary data to all ranks
        param_N = comm.bcast(param_N, root=0)

        # Create parameter objects (all ranks need this)
        parameters_to_sample = SampledParam(uniform, loc=np.full(param_N, 0.0), scale=1)

        if rank == 0:
            print("============================================================", flush=True)
            print("DREAM calibration inputs : ", flush=True)
            print("savePath: ", Path.work_path+'/results/', flush=True)
            print("parameters: ", parameters_to_sample, flush=True)
            print("likelihood: ", likelihood, flush=True)
            print("niterations: ", int(options.niterations), flush=True)
            print("nchains: ", nchains, flush=True)
            print("cores_for_each_chain: ", Cali.cores_for_each_chain, flush=True)
            print("multitry: ", False, flush=True)
            print("gamma_levels: ", 4, flush=True)
            print("adapt_gamma: ", True, flush=True)
            print("history_thin: ", history_thin, flush=True)
            print("model_name: ", Cali.TASK_name, flush=True)
            print("verbose: ", False, flush=True)
            print("restart: ", options.restart, flush=True)
            print("============================================================", flush=True)
        
        # Main DREAM execution (all ranks participate)
        if not options.restart:
            total_iterations = int(options.niterations)
            try:
                #print(f"Rank {rank}: Starting initial DREAM run", flush=True)
                run_dream(
                    savePath=Path.work_path+'/results/',
                    parameters=[parameters_to_sample],
                    likelihood=likelihood,
                    niterations=int(options.niterations),
                    total_iterations=total_iterations,
                    nchains=nchains,
                    cores_for_each_chain = Cali.cores_for_each_chain,
                    multitry=False,
                    gamma_levels=4,
                    adapt_gamma=True,
                    history_thin=history_thin,
                    model_name=Cali.TASK_name,
                    verbose=False,
                    restart=False
                )
                print(f"Rank {rank}: Initial DREAM run completed", flush=True)
            except Exception as e:
                #print(f"Rank {rank}: Initial DREAM run failed: {e}", flush=True)
                raise

            
        else:
            
            total_iterations = int(options.restart_niteration)
            if rank==0:
                build_history(Cali.TASK_name, nchains, total_iterations, param_N, history_thin)
            starts = GEM_tools_v2.get_restart_param(Path, Cali, param_N, total_iterations)
            total_iterations += int(options.niterations)
            comm.Barrier()
            """"""
            try:
                #print(f"Rank {rank}: Starting restart batch {i+1}", flush=True)
                run_dream(
                    savePath=Path.result_path,
                    parameters=[parameters_to_sample],
                    likelihood=likelihood,
                    niterations=int(options.niterations),
                    total_iterations=total_iterations,
                    nchains=nchains,
                    cores_for_each_chain = Cali.cores_for_each_chain,
                    start=starts,
                    multitry=False,
                    gamma_levels=4,
                    adapt_gamma=True,
                    history_thin=history_thin,
                    model_name=Cali.TASK_name,
                    verbose=False,
                    restart=True
                )
                #print(f"Rank {rank}: Restart batch {i+1} completed", flush=True)
            except Exception as e:
                #print(f"Rank {rank}: Restart batch {i+1} failed: {e}", flush=True)
                raise

        comm.Barrier()
        if rank == 0:
            print("DREAM calibration completed successfully", flush=True)
        
except Exception as e:
    print(f"Rank {rank}: Error: {e}", flush=True)
    comm.Abort(1)


if options.mode == 'test':
    param_N = GEM_tools_v2.get_param_N(Info, Param)
    total_iterations = int(options.restart_niteration)
    #if rank==0:
    #    build_history(Cali.TASK_name, 50, total_iterations, param_N, history_thin)
    starts = GEM_tools_v2.get_restart_param(Path, Cali, param_N, total_iterations)
    print(len(starts), starts[49])


