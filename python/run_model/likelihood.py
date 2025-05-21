import os
import GEM_tools
import shutil
import subprocess
import numpy as np
from def_GEM_cali import *
import time


def likelihood(param, chainID, modelID):

    err = 0

    if modelID == 0:
        catchment_list = [0,1,4]
    elif modelID == 1:
        catchment_list = [2,3]
    
    # Loop over each catchment
    for kk in catchment_list:

        stop0 = time.time()

        local_path = os.getcwd()
        runpath = Path.work_path + '/chain_' +str(chainID)  + '/' + str(Output.Catchment_ID[kk]) + '/run/'


        # Sort env
        GEM_tools.gen_param(runpath, Info, Param, param)
        GEM_tools.gen_no3_addtion(runpath, Info)

        # Model run        
        os.chdir(runpath)
        if os.path.exists('outputs'):
            shutil.rmtree('outputs')
        os.mkdir('outputs')
        #os.system('./gEcoHydro')
        subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Calculate simulation error for each variables
        for key in Output.sim.keys():
            dict = Output.sim.get(key)
            if len(dict['weights'][kk]) > 0:  # Skip if there is no observation


                _sim = np.fromfile(runpath + 'outputs/' + dict['sim_file']).reshape(-1, Output.N_sites[kk]).T[:, Info.spin_up:]
                _obs = np.fromfile(Path.data_path+'catchment_info/cali/'+str(Output.Catchment_ID[kk])+'/obs/'+dict['obs_file']).reshape(len(dict['sim_idx'][kk]), -1)
                if key == 'q':
                    _sim += 1e-3
                    _obs += 1e-3
                if key == 'iso_stream':
                    obs_min = np.nanmin(_obs)
                    _sim -= obs_min
                    _obs -= obs_min
                
                for i in range(_obs.shape[0]):
                    sim = _sim[dict['sim_idx'][kk][i], :]
                    obs = _obs[i,:]
                    err += (1 - GEM_tools.kge_modified(sim, obs)) * dict['weights'][kk][i]
                    #print(key, i, err, dict['weights'][kk][i])
                
        stop1 = time.time()
        print(chainID, modelID, Output.Catchment_ID[kk], (stop1-stop0)/60, flush=True)

    
    os.chdir(local_path)

    return err



if __name__ == '__main__':
    likelihood(np.full(300, 0.5), 0, 0)
    pass