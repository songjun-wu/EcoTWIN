import os
import shutil
import sys
import subprocess
import numpy as np
from optparse import OptionParser
from mpi4py import MPI
import os
import numpy as np
from SA import Morris
import GEM_tools


#  OPTIONS
parser = OptionParser()
current_path = os.getcwd()
parser.add_option("--catchment_ID",dest="catchment_ID",metavar="catchment_ID",
                  help="Switch ('DREAM_cali','test')")
parser.add_option("--def_py",dest="def_py",metavar="def_py",
                  help="Configuration file for GEM Protocol")
(options, args) = parser.parse_args()

mode = 'SA'
if options.def_py == None:
    options.def_py = 'def_GEM'
if (mode == 'DREAM_cali') or (mode == 'check'):
    options.def_py = 'def_GEM_cali'
elif (mode == 'cali_sep') or (mode == 'check_sep'):
    options.def_py = 'def_GEM_cali_sep'

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')




# === MPI Setup ===
comm = MPI.COMM_WORLD
rank = comm.Get_rank()       # current processor ID
size = comm.Get_size()       # total processors

# === Static Setup ===
mode = 'SA'
param_N = GEM_tools.get_param_N(Info, Param)
catchment_ID = str(options.catchment_ID)

# === Preprocessing (only rank 0) ===
if rank == 0:
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)
    params = Morris.OAT_sampling(
        xmins=np.full(param_N, 0.0),
        xmaxs=np.full(param_N, 1.0),
        xdistribution=np.full(param_N, 'uniform'),
        nsample=50,
        des_type='trajectory'
    )
    os.makedirs(Path.work_path + mode + '/outputs/SA/' + catchment_ID + '/', exist_ok=True)
else:
    params = None

params = comm.bcast(params, root=0)
run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run_MPI/' + str(rank) + '/'
if os.path.exists(run_path):
    shutil.rmtree(run_path)
shutil.copytree(Path.work_path + mode + '/' + str(catchment_ID) + '/run/', run_path)


# Divide param jobs by rank
param_indices = list(range(len(params)))
local_indices = [i for i in param_indices if i % size == rank]
local_likelihood = []

Output.Catchment_ID = np.char.strip(np.char.replace(np.array(Output.Catchment_ID).astype(str), "'", ''))
kk = np.where(Output.Catchment_ID == catchment_ID)[0][0]
print(kk, flush=True)

# === Loop through the assigned parameter for each rank ===
for gg in local_indices:
    param = params[gg]
    GEM_tools.gen_param(run_path, Info, Param, param)
    GEM_tools.gen_no3_addtion(run_path, Info)

    os.chdir(run_path)
    subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(current_path)  # restore

    err = 0
    for key, dict in Output.sim.items():
        if len(dict['weights'][kk]) == 0:
            continue
        _sim = np.fromfile(run_path + 'outputs/' + dict['sim_file']).reshape(-1, Output.N_sites[kk]).T[:, Info.spin_up:]
        _obs = np.fromfile(Path.data_path + 'catchment_info/cali/' + catchment_ID + '/obs/' + dict['obs_file']).reshape(len(dict['sim_idx'][kk]), -1)

        if key == 'q':
            _sim += 1e-5
            _obs += 1e-5
        elif key == 'iso_stream':
            obs_min = np.nanmin(_obs)
            _sim -= obs_min
            _obs -= obs_min
        else:
            _sim += 1e-5
            _obs += 1e-5

        for i in range(_obs.shape[0]):
            sim = _sim[dict['sim_idx'][kk][i], :]
            obs = _obs[i, :]
            err += (1 - GEM_tools.kge_modified(sim, obs)) * dict['weights'][kk][i] * len(Output.Catchment_ID)

    log_err = -np.inf if np.isnan(err) else np.log(err) * (-100)
    local_likelihood.append((gg, log_err))
    #print(f"[Rank {rank}] Param {gg} Likelihood: {log_err:.2f}", gg, len(local_indices), flush=True)

# === Gather results across ranks ===
gathered = comm.gather(local_likelihood, root=0)

if rank == 0:
    full_likelihood = np.full(len(params), -np.inf)
    for group in gathered:
        for idx, val in group:
            full_likelihood[idx] = val
    full_likelihood.tofile(Path.work_path + mode + '/outputs/SA/' + catchment_ID + '/likeli.bin')
    params.tofile(Path.work_path + mode + '/outputs/SA/' + catchment_ID + '/param.bin')
