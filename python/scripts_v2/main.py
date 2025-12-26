import os
import shutil
import sys
from optparse import OptionParser
import numpy as np
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/run_model')
import GEM_tools
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
    options.def_py = 'def_GEM_v2'
if (mode == 'DREAM_cali') or (mode == 'check'):
    options.def_py = 'def_GEM_v2_cali'
elif (mode == 'cali_sep') or (mode == 'check_sep'):
    options.def_py = 'def_GEM_v2_cali_sep'

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')


# Calibrate seperate catchments
if mode == 'cali_sep':
    #catchment_to_cali = pickle.load(open(Path.data_path+'catchment_info/cali/sub_catchment_ID_list','rb'))
    catchment_to_cali = ['831616_001']


    for catchment in catchment_to_cali:
        os.makedirs('/data/scratch/wusongj/paper6/cali_sep/' + catchment, exist_ok=True)

    max_nodes = 12 
    max_nodes = max_nodes if len(catchment_to_cali) > max_nodes else len(catchment_to_cali)

    print(max_nodes, Cali.niterations)
    os.makedirs(Path.work_path+'/scripts', exist_ok=True)
    shutil.copyfile('def_GEM_v2_cali_sep.py', Path.work_path+'/scripts/def_GEM_v2_cali_sep.py')

    
    # Construct cmd for each catchment
    for batchID in range(max_nodes):
        nbatch = Cali.nbatchs
        locals()['cmds'+str(batchID)] = []
        if not Cali.restart:
            nbatch -= 1
            locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_v2_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart False  --restart_niteration ' + str(Cali.restart_niteration))
            for i in range(nbatch):
                locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_v2_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart True  --restart_niteration ' + str(Cali.niterations * (i+1)))
        else:
            for i in range(nbatch):
                locals()['cmds'+str(batchID)].append('mpirun -np $SLURM_NTASKS python3 DREAM_cali.py --mode cali_sep --def_py def_GEM_v2_cali_sep_'+str(batchID)+' --niteration '+str(Cali.niterations)+ \
                        ' --likelihood likelihood_sep_'+str(batchID)+' --restart True  --restart_niteration ' + str(Cali.restart_niteration + Cali.niterations * i ))
    
    
    for batchID in range(max_nodes):

        # Construct DREAM algorithm for each catchment
        shutil.copyfile(Path.work_path+'/scripts/likelihood_sep.py', Path.work_path+'/scripts/likelihood_sep_'+str(batchID)+'.py')
        with open(Path.work_path+'/scripts/likelihood_sep_'+str(batchID)+'.py', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'from def_GEM_v2_cali_sep' in lines[i]:
                lines[i] = 'from def_GEM_v2_cali_sep_'+str(batchID)+' import *\n'
        with open(Path.work_path+'/scripts/likelihood_sep_'+str(batchID)+'.py', 'w') as f:
            f.writelines(lines)

        # Construct slurm submission file for each catchment
        shutil.copyfile(Path.work_path+'/scripts/protocal_cali_sep.sh', Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh')
        with open(Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'sbatch' in lines[i]:
                lines[i] = 'sbatch DREAM_cali_'+str(batchID)+'.slurm'
        with open(Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh', 'w') as f:
            f.writelines(lines)
    
        # Constrcut slurm config
        shutil.copyfile(Path.work_path+'/scripts/DREAM_cali.slurm', Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm')
        with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'mpirun' in lines[i]:
                lines[i] = locals()['cmds'+str(batchID)][0]
            if '#SBATCH --job-name=' in lines[i]:
                lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
        with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'w') as f:
            f.writelines(lines)
        
        # Construct def.py
        shutil.copyfile(Path.work_path+'/scripts/def_GEM_v2_cali_sep.py', Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py')
        with open(Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py', 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if 'work_path = ' in lines[i]:
                lines[i] = "    work_path = '/data/scratch/wusongj/paper6/cali_sep/"+catchment_to_cali[batchID]+"/'\n"
            if 'Catchment_ID    =' in lines[i]:
                lines[i] = '    Catchment_ID    = ["'+catchment_to_cali[batchID]+'"]\n'
        with open(Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py', 'w') as f:
            f.writelines(lines)
        # Initial submission
        os.system('sh '+Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh')

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
                    shutil.copyfile(Path.work_path+'/scripts/DREAM_cali.slurm', Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm')
                    with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'r') as f:
                        lines = f.readlines()
                    for i in range(len(lines)):
                        if 'mpirun' in lines[i]:
                            lines[i] = locals()['cmds'+str(batchID)][completed_tasks_for_each_catchment[batchID]]
                        if '#SBATCH --job-name=' in lines[i]:
                            lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
                    with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'w') as f:
                        f.writelines(lines)
                    os.system('sh '+Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh')

                
                # Move to next catchment once completed
                elif completed_tasks_for_each_catchment[batchID] == Cali.nbatchs and completed_tasks_for_each_catchment[batchID]!=-1:

                    completed_catchments += 1

                    try:
                        catchment_under_cali[batchID] = catchment_to_cali[max_nodes+completed_catchments]
                        # Constrcut slurm config
                        shutil.copyfile(Path.work_path+'/scripts/DREAM_cali.slurm', Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm')
                        with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'r') as f:
                            lines = f.readlines()
                        for i in range(len(lines)):
                            if 'mpirun' in lines[i]:
                                lines[i] = locals()['cmds'+str(batchID)][completed_tasks_for_each_catchment[batchID]]
                            if '#SBATCH --job-name=' in lines[i]:
                                lines[i] = '#SBATCH --job-name=' + '"c' + str(batchID) + '"\n'
                        with open(Path.work_path+'/scripts/DREAM_cali_'+str(batchID)+'.slurm', 'w') as f:
                            f.writelines(lines)
                        
                        # Construct def.py
                        shutil.copyfile(Path.work_path+'/scripts/def_GEM_v2_cali_sep.py', Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py')
                        with open(Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py', 'r') as f:
                            lines = f.readlines()
                        for i in range(len(lines)):
                            if 'work_path = ' in lines[i]:
                                lines[i] = "    work_path = /data/scratch/wusongj/paper6/cali_sep/"+catchment_to_cali[max_nodes+completed_catchments]+"/'\n"
                            if 'Catchment_ID    =' in lines[i]:
                                lines[i] = '    Catchment_ID    = ["'+catchment_to_cali[max_nodes+completed_catchments]+'"]\n'
                        with open(Path.work_path+'/scripts/def_GEM_v2_cali_sep_'+str(batchID)+'.py', 'w') as f:
                            f.writelines(lines)
                        os.system('sh '+Path.work_path+'/scripts/protocal_cali_sep_'+str(batchID)+'.sh')
                        completed_tasks_for_each_catchment[batchID] = 0
                    except:
                        completed_tasks_for_each_catchment[batchID] = -1


        print(completed_catchments, completed_tasks_for_each_catchment, catchment_under_cali)                
        time.sleep(120)





elif mode == 'forward_sep':
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # set the env
    #GEM_tools.sort_directory(mode, Path, Cali, Output)
    #GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)
   
    nchains = 20

    counter = 0
    #for i in range(len(validIdx)):
    #for gg in [0,5,6,7]:  # Catchment ID
    for gg in [0]:  # Catchment ID

        catchment_ID = Output.Catchment_ID[gg]
        run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'
        
        param_all = np.array([])
        if os.path.exists(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID):
            shutil.rmtree(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID)

        for chainID in range(nchains):
            print(catchment_ID, chainID)
            idx = chainID
            # Which parameter set to use?
            param_N = GEM_tools.get_param_N(Info, Param)

            completed_nbatches = [f.split('.')[0].split('_')[-1] for f in os.listdir(Path.work_path+'/cali_sep/'+catchment_ID+'/results/')]
            max_nbatches = np.max(np.array(completed_nbatches).astype(np.int16))

            likeli = np.fromfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(idx)+'_'+str(max_nbatches)+'.bin')
            best_likeli_loc = np.argwhere(likeli==np.max(likeli))[0][0]
            param = np.fromfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/sep_cali_sampled_params_chain_'+str(idx)+'_'+str(max_nbatches)+'.bin').reshape(-1, param_N)[best_likeli_loc,:]
            param_all = np.append(param_all, param)
 
            GEM_tools.gen_param(run_path, Info, Param, param)
            GEM_tools.gen_no3_addtion(run_path, Info)
            
            # Model run
            os.chdir(run_path)           
            #os.system('./gEcoHydro')
            os.chdir(current_path)

            # Save outputs for each catchment
            GEM_tools.save_outputs(run_path+'outputs/', Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/')
            # Plot performance

        param_all.tofile(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/param.bin')

        #post_plot.plot_performance_all(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/',Path.work_path+'/data/catchment_info/cali/'+catchment_ID+'/obs/', Path.work_path+'/plots/', catchment_ID, nchains)
        post_plot.plot_param_all(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/', Path.work_path+'plots/', nchains, catchment_ID)




elif mode == 'check_sep':
    print('')
    for catchment_ID in os.listdir(Path.work_path+'/cali_sep'):
        if catchment_ID == 'best_param':
            continue
        if not os.path.isdir(Path.work_path+'/cali_sep/'+catchment_ID):
            continue
        try:
            best_param = np.array([])
            arr = []
            lengths = []
            niterations = []
            n_batch = 0
            for i in range(Cali.nchains):
                flag = True
                for niteration in np.arange(0, 2e5, Cali.niterations)[::-1]:
                    if flag:
                        try:
                            loglikes = np.fromfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/DREAM_cali_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                            params = np.fromfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/DREAM_cali_sampled_params_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                            #print(len(loglikes), loglikes[-1], np.max(loglikes))
                            arr.append(np.nanmax(loglikes))
                            best_param = np.append(best_param, params[np.argmax(loglikes)])
                            lengths.append(len(loglikes))
                            niterations.append(niteration)
                            flag = False
                            n_batch += 1
                        except Exception as e:
                            pass
                    else:
                        break

            #print(niterations, lengths)
            if len(niterations)>0:
                print('***** Catchment : ' + catchment_ID + '   Chains : ' + str(n_batch) + '   Batch : ', int(np.mean(niterations)), np.mean(lengths))
                print('Average :  ', np.mean(arr))
                print('Maximum :  ', np.max(arr), ' found in  chain ', np.argwhere(arr==np.max(arr))[0][0])

            os.makedirs(Path.work_path+'/cali_sep/best_param', exist_ok=True)
            #shutil.copyfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/DREAM_cali_logps_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
            #                Path.work_path+'/cali_sep/best_param/'+catchment_ID+'_sep_cali_logps_chain.bin')
            #shutil.copyfile(Path.work_path+'/cali_sep/'+catchment_ID+'/results/DREAM_cali_sampled_params_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
            #                Path.work_path+'/cali_sep/best_param/'+catchment_ID+'_sep_cali_sampled_params_chain.bin')
            print(Path.work_path+'/cali_sep/best_param/best_param_'+catchment_ID+'.bin')
            best_param.tofile(Path.work_path+'/cali_sep/best_param/best_param_'+catchment_ID+'.bin')
            
            #print(arr, np.argwhere(arr==np.max(arr)))
        except Exception as e:
            print('No results found in catchment ',  catchment_ID)






