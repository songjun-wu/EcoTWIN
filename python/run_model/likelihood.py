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
        catchment_list = [0,6,7]
    elif modelID == 1:
        catchment_list = [1]
    elif modelID == 2:
        catchment_list = [2]
    elif modelID == 3:
        catchment_list = [3,5]

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
                    obs = _obs[i,:]
                    err += (1 - GEM_tools.kge_modified(sim, obs)) * dict['weights'][kk][i]
                    # todo
                    #if chainID==0 and modelID==0:
                    #    print('   ', Output.Catchment_ID[kk], key, i, GEM_tools.kge_modified(sim, obs), dict['weights'][kk][i], np.nanmean(sim), np.nanmean(obs) )
                    #    np.savetxt('/data/scratch/wusongj/paper4/cali/chain_0/param.txt', param)
                
        stop1 = time.time()
        if chainID==0:
            print(chainID, modelID, Output.Catchment_ID[kk], (stop1-stop0)/60, err, flush=True)

    
    os.chdir(local_path)

    if np.isnan(err):
        err = np.inf

    return err



if __name__ == '__main__':
    pass