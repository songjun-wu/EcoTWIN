import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
import numpy as np
import time
import post_plot



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
elif (mode == 'DREAM_cali') or (mode == 'check'):
    options.def_py = 'def_GEM_cali'
elif (mode == 'cali_sep') or (mode == 'check_sep'):
    options.def_py = 'def_GEM_cali_sep'

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
        while (GEM_tools.checkTaskStatus('EU_cali') > 0):
            time.sleep(10)
    

# Calibrate seperate catchments
if mode == 'cali_sep':
    import pickle
    #catchment_to_cali = pickle.load(open(Path.data_path+'catchment_info/cali/sub_catchment_ID_list','rb'))
    catchment_to_cali = ['831616_001', '83811_001', '291111_001', '6_001']


    for catchment in catchment_to_cali:
        os.makedirs('/data/scratch/wusongj/paper4/cali_sep/' + catchment, exist_ok=True)

    max_nodes = 5 if len(catchment_to_cali) > 5 else len(catchment_to_cali)

    print(max_nodes, Cali.niterations)
    shutil.copyfile('def_GEM_cali_sep.py', '/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep.py')

    
    # Construct cmd for each catchment
    for batchID in range(max_nodes):
        nbatch = Cali.nbatchs
        locals()['cmds'+str(batchID)] = []
        if not Cali.restart:
            nbatch -= 1
            locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart False  --restart_niteration ' + str(Cali.restart_niteration))
            for i in range(nbatch):
                locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart True  --restart_niteration ' + str(Cali.niterations * (i+1)))
        else:
            for i in range(nbatch):
                locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart True  --restart_niteration ' + str(Cali.restart_niteration + Cali.niterations * i ))
    
    
    for batchID in range(max_nodes):

        # Construct DREAM algorithm  for each catchment
        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/likelihood_sep.py', '/data/scratch/wusongj/paper4/scripts/likelihood_sep_'+str(batchID)+'.py')
        with open('/data/scratch/wusongj/paper4/scripts/likelihood_sep_'+str(batchID)+'.py', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'from def_GEM_cali_sep' in lines[i]:
                lines[i] = 'from def_GEM_cali_sep_'+str(batchID)+' import *\n'
        with open('/data/scratch/wusongj/paper4/scripts/likelihood_sep_'+str(batchID)+'.py', 'w') as f:
            f.writelines(lines)

        # Construct slurm submission file for each catchment
        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/protocal_cali_sep.sh', '/data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh')
        with open('/data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'sbatch' in lines[i]:
                lines[i] = 'sbatch DREAM_cali_sep_'+str(batchID)+'.slurm'
        with open('/data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh', 'w') as f:
            f.writelines(lines)
    
        # Constrcut slurm config
        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep.slurm', '/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm')
        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'mpirun' in lines[i]:
                lines[i] = locals()['cmds'+str(batchID)][0]
            if '#SBATCH --job-name=' in lines[i]:
                lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'w') as f:
            f.writelines(lines)
        
        # Construct def.py
        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep.py', '/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py')
        with open('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'work_path = ' in lines[i]:
                lines[i] = "    work_path = '/data/scratch/wusongj/paper4/cali_sep/"+catchment_to_cali[batchID]+"/'\n"
            if 'Catchment_ID    =' in lines[i]:
                lines[i] = '    Catchment_ID    = ["'+catchment_to_cali[batchID]+'"]\n'
        with open('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py', 'w') as f:
            f.writelines(lines)
        # Initial submission
        os.system('sh /data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh')

    # Monitor tasks and renew submission
    catchment_under_cali = [f for f in catchment_to_cali[:max_nodes]]
    completed_tasks_for_each_catchment = np.full(max_nodes, 0)
    completed_catchments = 0
    while completed_catchments!=len(catchment_to_cali):
        for batchID in range(max_nodes):

            if completed_tasks_for_each_catchment[batchID]==-1:
                continue

            if (GEM_tools.checkTaskStatus('c' + str(batchID)) <= 0):
                completed_tasks_for_each_catchment[batchID] += 1
                # To next task
                if completed_tasks_for_each_catchment[batchID] < Cali.nbatchs:
                    # Constrcut slurm config
                    shutil.copyfile('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep.slurm', '/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm')
                    with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'r') as f:
                        lines = f.readlines()
                    for i in range(len(lines)):
                        if 'mpirun' in lines[i]:
                            lines[i] = locals()['cmds'+str(batchID)][completed_tasks_for_each_catchment[batchID]]
                        if '#SBATCH --job-name=' in lines[i]:
                            lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
                    with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'w') as f:
                        f.writelines(lines)
                    os.system('sh /data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh')

                
                # Move to next catchment once completed
                elif completed_tasks_for_each_catchment[batchID] == Cali.nbatchs and completed_tasks_for_each_catchment[batchID]!=-1:

                    completed_catchments += 1

                    try:
                        catchment_under_cali[batchID] = catchment_to_cali[max_nodes+completed_catchments]
                        # Constrcut slurm config
                        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep.slurm', '/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm')
                        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'r') as f:
                            lines = f.readlines()
                        for i in range(len(lines)):
                            if 'mpirun' in lines[i]:
                                lines[i] = locals()['cmds'+str(batchID)][completed_tasks_for_each_catchment[batchID]]
                            if '#SBATCH --job-name=' in lines[i]:
                                lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
                        with open('/data/scratch/wusongj/paper4/scripts/DREAM_cali_sep_'+str(batchID)+'.slurm', 'w') as f:
                            f.writelines(lines)
                        
                        # Construct def.py
                        shutil.copyfile('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep.py', '/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py')
                        with open('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py', 'r') as f:
                            lines = f.readlines()
                        for i in range(len(lines)):
                            if 'work_path = ' in lines[i]:
                                lines[i] = "    work_path = '/data/scratch/wusongj/paper4/cali_sep/"+catchment_to_cali[max_nodes+completed_catchments]+"/'\n"
                            if 'Catchment_ID    =' in lines[i]:
                                lines[i] = '    Catchment_ID    = ["'+catchment_to_cali[max_nodes+completed_catchments]+'"]\n'
                        with open('/data/scratch/wusongj/paper4/scripts/def_GEM_cali_sep_'+str(batchID)+'.py', 'w') as f:
                            f.writelines(lines)
                        os.system('sh /data/scratch/wusongj/paper4/scripts/protocal_cali_sep_'+str(batchID)+'.sh')
                        completed_tasks_for_each_catchment[batchID] = 0
                    except:
                        completed_tasks_for_each_catchment[batchID] = -1


        print(completed_catchments, completed_tasks_for_each_catchment, catchment_under_cali)                
        time.sleep(120)


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
    for i in [10]:  # chainID
        #for gg in range(len(Output.Catchment_ID)):
        #for gg in [0,1,2,3,5,6,7]:
        for gg in [0]:  # Catchment ID

            catchment_ID = Output.Catchment_ID[gg]
            print(catchment_ID)
            run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'
            #idx = validIdx[i]
            idx = i
            print(idx, catchment_ID)
            # Which parameter set to use?
            param_N = GEM_tools.get_param_N(Info, Param)
            #param = np.loadtxt('/data/scratch/wusongj/paper4/cali/chain_0/param.txt')
            #param = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_sampled_params_chain_'+str(idx)+'_200.bin').reshape(-1, 189)[-1,:]
            likeli = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+str(catchment_ID)+'_sep_cali_logps_chain_'+str(idx)+'_1000.bin')
            best_likeli_loc = np.argwhere(likeli==np.max(likeli))[0][0]
            param = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+str(catchment_ID)+'_sep_cali_sampled_params_chain_'+str(idx)+'_1000.bin').reshape(-1, param_N)[best_likeli_loc,:]
            
            #param = np.full(300, 0.5)
            GEM_tools.gen_param(run_path, Info, Param, param)
            GEM_tools.gen_no3_addtion(run_path, Info)
            
            # Model run
            os.chdir(run_path)           
            os.system('./gEcoHydro')
            os.chdir(current_path)

            
            # Plot spatial maps and Ts results
            post_plot.plot_hydrology(run_path+'outputs/', 'hydro_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/')
            post_plot.plot_tracking(run_path+'outputs/', 'WQ_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/')

            fnames = ['hydro_'+str(catchment_ID)+'_Ts.png', 'hydro_'+str(catchment_ID)+'_map.png',
                      'WQ_'+str(catchment_ID)+'_Ts.png', 'WQ_'+str(catchment_ID)+'_map.png']
            for fname in fnames:
                if os.path.exists(run_path+'outputs/'+fname):
                    shutil.copyfile(run_path+'outputs/'+fname, 'plots/'+fname.split('.')[0]+'_'+str(idx)+'.png')


            # Plot performance
            post_plot.plot_performance(run_path+'outputs/', '/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/obs/', current_path+'/plots/', catchment_ID, idx)
    

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

    #print(niterations, lengths)
    print('Chains  :  ', n_batch)
    print('Batch   :  ', int(np.mean(niterations)), np.mean(lengths))
    print('Average :  ', np.mean(arr))
    print('Maximum :  ', np.max(arr))
    #print(arr, np.argwhere(arr==np.max(arr)))

elif mode == 'check_sep':
    for catchment_ID in os.listdir('/data/scratch/wusongj/paper4/cali_sep'):
        if not os.path.isdir('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID):
            continue
        try:
            print('')
            arr = []
            lengths = []
            niterations = []
            n_batch = 0
            for i in range(Cali.nchains):
                flag = True
                for niteration in np.arange(0, 2e5, Cali.niterations)[::-1]:
                    if flag:
                        try:
                            loglikes = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
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

            #print(niterations, lengths)
            print('Catchment : ' + catchment_ID + '   Chains : ' + str(n_batch) + '   Batch : ', int(np.mean(niterations)), np.mean(lengths))
            print('Average :  ', np.mean(arr))
            print('Maximum :  ', np.max(arr), ' found in  chain ', np.argwhere(arr==np.max(arr))[0][0])

            #shutil.copyfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
            #                '/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'_sep_cali_logps_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin')
            #shutil.copyfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_sampled_params_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
            #                '/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'_sep_cali_sampled_params_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin')
            
            #print(arr, np.argwhere(arr==np.max(arr)))
        except:
            print('No results found in catchment ',  catchment_ID)





elif mode == 'bbb':


    
    for gg in [4]:
        print(Output.Catchment_ID)
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
        
    """
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
    """
    pass



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
