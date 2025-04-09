import os
import GEM_tools
import shutil
import subprocess
import numpy as np
from def_GEM import *


def likelihood(param, chainID):

    local_path = os.getcwd()
    runpath = Path.work_path + '/chain_' +str(chainID)  + '/run/'
    GEM_tools.gen_param(runpath, Info, Param, param)

    os.chdir(runpath)
    if os.path.exists('outputs'):
        shutil.rmtree('outputs')
    os.mkdir('outputs')

    subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    """"""
    err = 0
    for key in Output.sim.keys():
        dict = Output.sim.get(key)
        _sim = np.fromfile(runpath + 'outputs/' + dict['sim_file']).reshape(-1, Output.N_sites).T[:, Info.spin_up:]
        _obs = np.fromfile(Path.data_path + dict['obs_file']).reshape(len(dict['sim_idx']), -1)
        for i in range(_obs.shape[0]):
            sim = _sim[dict['sim_idx'][i], :]
            obs = _obs[i,:]
            err += GEM_tools.nselnnse(sim, obs, weight_nse=0.9, weight_lnnse=0.1)

    loglikeli = np.log(err) * (-1*500)
    if np.isnan(loglikeli):
        loglikeli = -np.inf
    
    os.chdir(local_path)

    return loglikeli
