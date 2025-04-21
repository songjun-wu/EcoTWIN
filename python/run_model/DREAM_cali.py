import os
import sys
from optparse import OptionParser
import numpy as np
from mpi4py import MPI
from scipy.stats import uniform
import GEM_tools

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parse command line arguments
parser = OptionParser()
parser.add_option("--mode", dest="mode", help="Switch ('DREAM_cali','test')")
parser.add_option("--def_py", dest="def_py", help="Configuration file for GEM Protocol")
(options, args) = parser.parse_args()

if options.def_py is None:
    options.def_py = 'def_GEM'

try:
    # Import configuration
    sys.path.insert(0, os.getcwd())
    config = __import__(options.def_py)
    Path = config.Path
    Cali = config.Cali
    Info = config.Info
    Param = config.Param

    if options.mode == 'DREAM_cali':
        from pydream.core import run_dream
        from pydream.parameters import SampledParam
        from likelihood import likelihood

        Cali.nchains = size

        # Only rank 0 does initialization
        if rank == 0:
            try:
                os.chdir(Path.work_path)
                GEM_tools.sort_directory(options.mode, Path, Cali)
                GEM_tools.set_env(options.mode, Path, Cali.nchains)
                GEM_tools.set_config(options.mode, Path, Cali)
                param_N = GEM_tools.get_param_N(Info, Param)
                print(f"Rank 0: Initialization complete. Starting {size} chains, param_N={param_N}", flush=True)
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

        # Set number of chains equal to number of processes
        Cali.nchains = size

        # Main DREAM execution (all ranks participate)
        if not Cali.restart:
            total_iterations = Cali.niterations
            try:
                print(f"Rank {rank}: Starting initial DREAM run", flush=True)
                run_dream(
                    savePath=Path.result_path,
                    parameters=[parameters_to_sample],
                    likelihood=likelihood,
                    niterations=Cali.niterations,
                    total_iterations=total_iterations,
                    nchains=Cali.nchains,
                    multitry=False,
                    gamma_levels=4,
                    adapt_gamma=True,
                    history_thin=1,
                    model_name=Cali.TASK_name,
                    verbose=False,
                    restart=False
                )
                print(f"Rank {rank}: Initial DREAM run completed", flush=True)
            except Exception as e:
                print(f"Rank {rank}: Initial DREAM run failed: {e}", flush=True)
                raise

            # Batch continuation
            for i in range(Cali.nbatchs - 1):
                comm.Barrier()
                starts = GEM_tools.get_restart_param(Path, Cali, param_N, total_iterations)
                total_iterations += Cali.niterations
                try:
                    print(f"Rank {rank}: Starting batch {i+1}", flush=True)
                    run_dream(
                        savePath=Path.result_path,
                        parameters=[parameters_to_sample],
                        likelihood=likelihood,
                        niterations=Cali.niterations,
                        total_iterations=total_iterations,
                        nchains=Cali.nchains,
                        start=starts,
                        multitry=False,
                        gamma_levels=4,
                        adapt_gamma=True,
                        history_thin=1,
                        model_name=Cali.TASK_name,
                        verbose=False,
                        restart=True
                    )
                    print(f"Rank {rank}: Batch {i+1} completed", flush=True)
                except Exception as e:
                    print(f"Rank {rank}: Batch {i+1} failed: {e}", flush=True)
                    raise
        else:
            total_iterations = Cali.restart_niteration
            """
            for i in range(Cali.nbatchs):   # todo
                comm.Barrier()
                if rank == 0:
                    starts = GEM_tools.get_restart_param(Path, Cali, param_N, total_iterations)
                else:
                    starts = None
                total_iterations += Cali.niterations    
                starts = comm.bcast(starts, root=0)
 
            """
            
            for i in range(Cali.nbatchs):
                comm.Barrier()
                starts = GEM_tools.get_restart_param(Path, Cali, param_N, total_iterations)
                total_iterations += Cali.niterations
                """"""
                try:
                    print(f"Rank {rank}: Starting restart batch {i+1}", flush=True)
                    run_dream(
                        savePath=Path.result_path,
                        parameters=[parameters_to_sample],
                        likelihood=likelihood,
                        niterations=Cali.niterations,
                        total_iterations=total_iterations,
                        nchains=Cali.nchains,
                        start=starts,
                        multitry=False,
                        gamma_levels=4,
                        adapt_gamma=True,
                        history_thin=1,
                        model_name=Cali.TASK_name,
                        verbose=False,
                        restart=True
                    )
                    print(f"Rank {rank}: Restart batch {i+1} completed", flush=True)
                except Exception as e:
                    print(f"Rank {rank}: Restart batch {i+1} failed: {e}", flush=True)
                    raise

        comm.Barrier()
        if rank == 0:
            print("DREAM calibration completed successfully", flush=True)
        
except Exception as e:
    print(f"Rank {rank}: Error: {e}", flush=True)
    comm.Abort(1)