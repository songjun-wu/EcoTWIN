import os
import shutil
import GEM_tools
import sys
from optparse import OptionParser
import numpy as np
import time
import post_plot
import GIS_tools



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
if (mode == 'DREAM_cali') or (mode == 'check'):
    options.def_py = 'def_GEM_cali'
elif (mode == 'cali_sep') or (mode == 'check_sep'):
    options.def_py = 'def_GEM_cali_sep'

sys.path.insert(0, current_path+'/')
exec('from ' + options.def_py + ' import *')


if mode == 'SA':

    from SA import Morris

    os.chdir('/data/scratch/wusongj/paper4/scripts/SA/')
    

    catchment_list = ['831616_001', '83811_001', '1034751_001', '442364_001']

    
    for catchment_ID in catchment_list:
        """"""
        with open('/data/scratch/wusongj/paper4/scripts/SA/SA.slurm', 'r') as f:
            lines = f.readlines()
    
        for i in range(len(lines)):
            if '#SBATCH --job-name' in lines[i]:
                lines[i] = '#SBATCH --job-name="S'+catchment_ID+'"\n'
            elif 'mpirun -np $SLURM_NTASKS python3 Sens_analysis.py' in lines[i]:
                lines[i] = 'mpirun -np $SLURM_NTASKS python3 Sens_analysis.py --catchment_ID '+catchment_ID + '\n'
        
        with open('/data/scratch/wusongj/paper4/scripts/SA/SA.slurm', 'w') as f:
                f.writelines(lines)
        
        os.system('sbatch SA.slurm')
        time.sleep(5)
        
    #post_plot.plot_SA(catchment_list[:], plot_path=Path.work_path+'plots/')


elif mode == 'DREAM_cali':
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
elif mode == 'cali_sep':
    import pickle
    #catchment_to_cali = pickle.load(open(Path.data_path+'catchment_info/cali/sub_catchment_ID_list','rb'))
    catchment_to_cali = ['6_001', '291110_001', '566445_001', '4_001', '1034872_001', '1034754_001', '291111_001', '83811_001', '831616_001', '129489_001', '566445_002', '442364_001', '566445_003']


    for catchment in catchment_to_cali:
        os.makedirs('/data/scratch/wusongj/paper4/cali_sep/' + catchment, exist_ok=True)

    max_nodes = 12 
    max_nodes = max_nodes if len(catchment_to_cali) > max_nodes else len(catchment_to_cali)

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

        # Construct DREAM algorithm for each catchment
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


elif mode == 'test_cali':
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # set the env
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)

    counter = 0

    for gg in range(13):  # Catchment ID
        catchment_ID = Output.Catchment_ID[gg]
        print(catchment_ID)
        run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'
        # Which parameter set to use?
        param_N = GEM_tools.get_param_N(Info, Param)
        """
        try:
            likeli = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+str(catchment_ID)+'_sep_cali_logps_chain.bin')
            best_likeli_loc = np.argwhere(likeli==np.max(likeli))[0][0]
            param = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+str(catchment_ID)+'_sep_cali_sampled_params_chain.bin').reshape(-1, param_N)[best_likeli_loc,:]
        except Exception as e:
            print(e)
            continue
        """
        # todo
        #param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param.bin')

        param = np.full(300, 0.5)  # todo
        
        GEM_tools.gen_param(run_path, Info, Param, param)
        GEM_tools.gen_no3_addtion(run_path, Info)
        
        # Model run
        os.chdir(run_path)           
        os.system('./gEcoHydro')
        os.chdir(current_path)
        
        # Plot spatial maps and Ts results
        post_plot.plot_hydrology(run_path+'outputs/', 'hydro_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/', catchment_ID=catchment_ID, if_average=False)
        post_plot.plot_tracking(run_path+'outputs/', 'WQ_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/', catchment_ID=catchment_ID, if_average=False)

        fnames = ['hydro_'+str(catchment_ID)+'_Ts.png', 'hydro_'+str(catchment_ID)+'_map.png',
                    'WQ_'+str(catchment_ID)+'_Ts.png', 'WQ_'+str(catchment_ID)+'_map.png']
        for fname in fnames:
            if os.path.exists(run_path+'outputs/'+fname):
                shutil.copyfile(run_path+'outputs/'+fname, 'plots/'+fname.split('.')[0]+'.png')
        
        #post_plot.IMGtoVideo(os.getcwd()+'/plots/', run_path+'outputs/tmp_plots_for_animation/', output_name='hydrology_' + catchment_ID)
        
        # Plot performance
        post_plot.plot_performance(run_path+'outputs/', '/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/obs/', current_path+'/plots/', catchment_ID, chainID=0)

elif mode == 'test_forward':


    catchment_ID = 1345871


    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # Set env
    run_path = '/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/'
    if os.path.exists(run_path):
        shutil.rmtree(run_path)
    shutil.copytree('/data/scratch/wusongj/paper4/forward_all/run/'+str(catchment_ID), run_path)
    os.remove(run_path+'run/gEcoHydro')
    os.symlink(Path.model_path+Path.path_EXEC, '/data/scratch/wusongj/paper4/test/'+str(catchment_ID)+'/run/gEcoHydro')

    run_path += 'run/'
    param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param.bin')

    # Model run
    os.chdir(run_path)           
    os.system('./gEcoHydro')
    os.chdir(current_path)



elif mode == 'forward_cali':
    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # set the env
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)
   
    nchains = 20

    # Get parameter
    # Which parameter set to use?
    param_N = GEM_tools.get_param_N(Info, Param)

    param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param.bin')

    """"""
    for gg in range(13):  # Catchment ID

        catchment_ID = Output.Catchment_ID[gg]
        run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'

        if os.path.exists(Path.work_path + mode +'/outputs/cali/' + catchment_ID):
            shutil.rmtree(Path.work_path + mode +'/outputs/cali/' + catchment_ID)

        
        GEM_tools.gen_param(run_path, Info, Param, param)
        GEM_tools.gen_no3_addtion(run_path, Info)
        
        # Model run
        os.chdir(run_path)           
        os.system('./gEcoHydro')
        os.chdir(current_path)

        # Save outputs for each catchment
        GEM_tools.save_outputs(run_path+'outputs/', Path.work_path + mode +'/outputs/cali/' + catchment_ID + '/')

        # Plot spatial maps and Ts results
        post_plot.plot_hydrology(run_path+'outputs/', 'hydro_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/', catchment_ID=catchment_ID, if_average=False)
        post_plot.plot_tracking(run_path+'outputs/', 'WQ_'+str(catchment_ID), spatial_path='/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/', catchment_ID=catchment_ID, if_average=False)

        fnames = ['hydro_'+str(catchment_ID)+'_Ts.png', 'hydro_'+str(catchment_ID)+'_map.png',
                    'WQ_'+str(catchment_ID)+'_Ts.png', 'WQ_'+str(catchment_ID)+'_map.png']
        for fname in fnames:
            if os.path.exists(run_path+'outputs/'+fname):
                shutil.copyfile(run_path+'outputs/'+fname, Path.work_path + '/plots/'+ mode + '/' + fname.split('.')[0]+'.png')
       
        # Plot performance
        post_plot.plot_performance(run_path+'outputs/', '/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/obs/', Path.work_path + '/plots/'+ mode + '/', catchment_ID, chainID=0)


elif mode == 'forward_all':

    catchment_list = [f for f in os.listdir('/data/scratch/wusongj/paper4/data/catchment_info/forward')]
    nchains = 40
    chainIDs = np.arange(1, 40)
    replace = True
    model_run = True
    model_post = False

    if model_run:
        # Model structure update
        os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
        os.system('python3 develop.py')  # todo
        # set the env
        #GEM_tools.sort_directory(mode, Path, Cali, Output, catchment_list=catchment_list)
        #GEM_tools.set_env(mode, Path, Cali, Output, catchment_list=catchment_list)
        #GEM_tools.set_config(mode, Path, Cali, Output, catchment_list=catchment_list)  
        # Get parameter
        # Which parameter set to use?
        param_N = GEM_tools.get_param_N(Info, Param)
        _param = np.fromfile('/data/scratch/wusongj/paper4/cali/best_param_all.bin').reshape(nchains,-1)
        counter = 0
        for chainID in chainIDs:
            for catchment_ID in catchment_list:
                catchment_ID = str(catchment_ID)
                run_path = Path.work_path + mode + '/run/' + str(catchment_ID) + '/run/'
                save_path = Path.work_path + mode +'/outputs/cali/' + catchment_ID + '/'+str(chainID)+'/'
                
                os.makedirs(save_path, exist_ok=True)
                if os.path.exists(save_path):
                    shutil.rmtree(save_path)
                GEM_tools.gen_param(run_path, Info, Param, param)
                GEM_tools.gen_no3_addtion(run_path, Info)
                # Model run
                os.chdir(run_path)           
                os.system('./gEcoHydro')
                os.chdir(current_path)
                # Save outputs for each catchment
                GEM_tools.save_outputs(run_path+'outputs/', save_path)
                counter += 1
                print(str(counter)+' / '+str(len(catchment_list)) + '  :   ' + str(catchment_ID))

    if model_post:
        Vars = ['canopy_storage', 'snow_depth']
        Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'vadose', 'groundwater_storage'])
        Vars.extend(['snowmelt', 'throufall', 'irrigation_from_GW', 'irrigation_from_river'])
        Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', 'perc_vadose'])
        Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3'])
        Vars.extend(['soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', 'channel_evaporation'])
        Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
        Vars.extend(['overland_flow_toChn', 'interflow_toChn', 'GWflow_toChn', 'discharge'])
        Vars.extend(['d18o_canopy_storage', 'd18o_snow_depth'])
        Vars.extend(['d18o_SMC_layer1', 'd18o_SMC_layer2', 'd18o_SMC_layer3', 'd18o_vadose', 'd18o_groundwater_storage', 'd18o_chanS'])
        Vars.extend(['age_canopy_storage', 'age_snow_depth'])
        Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_groundwater_storage', 'age_chanS'])
        Vars.extend(['no3_canopy_storage', 'no3_snow_depth'])
        Vars.extend(['no3_SMC_layer1', 'no3_SMC_layer2', 'no3_SMC_layer3', 'no3_vadose', 'no3_groundwater_storage', 'no3_chanS'])
        Vars.extend(['nitrogen_addition', 'plant_uptake', 'deni_soil', 'minerl_soil', 'degrad_soil','deni_river'])
        #post_plot.merge_spatial_results_EU(mode, catchment_list, Vars, replace)
        #post_plot.plot_spatial_results_EU(mode, Vars, replace)
        post_plot.merge_performance(mode, catchment_list)
        #post_plot.plot_performance_EU(mode)


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

            completed_nbatches = [f.split('.')[0].split('_')[-1] for f in os.listdir('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/')]
            max_nbatches = np.max(np.array(completed_nbatches).astype(np.int16))

            likeli = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(idx)+'_'+str(max_nbatches)+'.bin')
            best_likeli_loc = np.argwhere(likeli==np.max(likeli))[0][0]
            param = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_sampled_params_chain_'+str(idx)+'_'+str(max_nbatches)+'.bin').reshape(-1, param_N)[best_likeli_loc,:]
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

        #post_plot.plot_performance_all(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/','/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/obs/', Path.work_path+'/plots/', catchment_ID, nchains)
        post_plot.plot_param_all(Path.work_path + mode +'/outputs/cali_sep/' + catchment_ID + '/', Path.work_path+'plots/', nchains, catchment_ID)

elif mode == 'forward_cross':

    nparam_per_catchment = 1

    # Model structure update
    os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
    os.system('python3 develop.py')  # todo

    # set the env
    GEM_tools.sort_directory(mode, Path, Cali, Output)
    GEM_tools.set_env(mode, Path, Cali, Output)
    GEM_tools.set_config(mode, Path, Cali, Output)
    param_N = GEM_tools.get_param_N(Info, Param)

    """
    # Summary the best parameters from each catchment
    nchains = 20
    best_likeli_catchmentID = np.array([])
    best_likeli_chainID = np.array([])
    best_likeli_locs = np.array([])
    for gg in range(8):  # Catchment ID
        catchment_ID = Output.Catchment_ID[gg]
        best_likelis_per_catchment = []
        best_likeli_locs_per_catchment = []
        for chainID in range(nchains):
            # Which parameter set to use?
            
            completed_nbatches = [f.split('.')[0].split('_')[-1] for f in os.listdir('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/')]
            max_nbatches = np.max(np.array(completed_nbatches).astype(np.int16))
            likeli = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(chainID)+'_'+str(max_nbatches)+'.bin')
            best_likeli_loc = np.argwhere(likeli==np.max(likeli))[0][0]
            best_likelis_per_catchment.append(likeli[best_likeli_loc])
            best_likeli_locs_per_catchment.append(best_likeli_loc)
        best_likeli_catchmentID = np.append(best_likeli_catchmentID, np.full(nparam_per_catchment, catchment_ID))
        best_likeli_chainID = np.append(best_likeli_chainID, np.argsort(best_likelis_per_catchment)[-1*nparam_per_catchment:])
        best_likeli_locs = np.append(best_likeli_locs, np.array(best_likeli_locs_per_catchment)[np.argsort(best_likelis_per_catchment)[-1*nparam_per_catchment:]])

    param_all = np.array([])
    for kk in range(len(best_likeli_chainID)):
        catchment_ID = best_likeli_catchmentID[kk]
        chainID = int(best_likeli_chainID[kk])
        best_likeli_loc = int(best_likeli_locs[kk])
        completed_nbatches = [f.split('.')[0].split('_')[-1] for f in os.listdir('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/')]
        max_nbatches = np.max(np.array(completed_nbatches).astype(np.int16))
        likeli = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(chainID)+'_'+str(max_nbatches)+'.bin')[best_likeli_loc]
        param = np.fromfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_sampled_params_chain_'+str(chainID)+'_'+str(max_nbatches)+'.bin').reshape(-1, param_N)[best_likeli_loc,:]
        param_all = np.append(param_all, param)
    param_all.tofile(Path.work_path+mode+'/param_all.bin')
    """

    # Loop the parameters for each catchment
    param_all = np.fromfile(Path.work_path+mode+'/param_all.bin').reshape(-1, param_N)
    for gg in [6]:  # Catchment ID
        catchment_ID = Output.Catchment_ID[gg]
        run_path = Path.work_path + mode + '/' + str(catchment_ID) + '/run/'
        """
        if os.path.exists(Path.work_path + mode +'/outputs/cali_sep_cross/' + catchment_ID):
            shutil.rmtree(Path.work_path + mode +'/outputs/cali_sep_cross/' + catchment_ID)

        for kk in range(param_all.shape[0]):
            param = param_all[kk]
            
            GEM_tools.gen_param(run_path, Info, Param, param)
            GEM_tools.gen_no3_addtion(run_path, Info)

            # Model run
            os.chdir(run_path)           
            os.system('./gEcoHydro')
            os.chdir(current_path)

            # Save outputs for each catchment
            GEM_tools.save_outputs(run_path+'outputs/', Path.work_path + mode +'/outputs/cali_sep_cross/' + catchment_ID + '/')
        """
        post_plot.plot_performance_all(Path.work_path + mode +'/outputs/cali_sep_cross/' + catchment_ID + '/','/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/obs/',
                                       Path.work_path+'/plots/', catchment_ID, param_all.shape[0], plot_each_chain=True)



elif mode == 'check':
    arr = []
    lengths = []
    niterations = []
    n_batch = 0
    param_all = np.array([])
    for i in range(Cali.nchains):
        flag = True
        for niteration in np.arange(0, 2e5, Cali.niterations)[::-1]:
            if flag:
                try:
                    loglikes = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_logps_chain_'+str(i)+'_'+str(int(niteration))+'.bin')
                    param = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_sampled_params_chain_'+str(i)+'_'+str(int(niteration))+'.bin').reshape(len(loglikes), -1)
                    param_all = np.append(param_all, param[np.argwhere(loglikes==np.max(loglikes))[0][0],:])
                    arr.append(np.nanmax(loglikes))
                    lengths.append(len(loglikes))
                    niterations.append(niteration)
                    flag = False
                    n_batch += 1
                except:
                    pass
            else:
                break

    likeli = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_logps_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin')
    param = np.fromfile('/data/scratch/wusongj/paper4/cali/results/DREAM_cali_sampled_params_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin').reshape(len(likeli), -1)
    param[np.argwhere(likeli==np.max(likeli))[0][0], :].tofile('/data/scratch/wusongj/paper4/cali/best_param.bin')
    param_all.tofile('/data/scratch/wusongj/paper4/cali/best_param_all.bin')

    #print(niterations, lengths)
    print('Chains  :  ', n_batch)
    print('Batch   :  ', int(np.mean(niterations)), np.mean(lengths))
    print('Average :  ', np.mean(arr))
    print('Maximum :  ', np.max(arr))
    #print(arr, np.argwhere(arr==np.max(arr)))

elif mode == 'check_sep':
    print('')
    for catchment_ID in os.listdir('/data/scratch/wusongj/paper4/cali_sep'):
        if not os.path.isdir('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID):
            continue
        try:
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
                        except Exception as e:
                            pass
                    else:
                        break

            #print(niterations, lengths)
            if len(niterations)>0:
                print('***** Catchment : ' + catchment_ID + '   Chains : ' + str(n_batch) + '   Batch : ', int(np.mean(niterations)), np.mean(lengths))
                print('Average :  ', np.mean(arr))
                print('Maximum :  ', np.max(arr), ' found in  chain ', np.argwhere(arr==np.max(arr))[0][0])

            shutil.copyfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_logps_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
                            '/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'_sep_cali_logps_chain.bin')
            shutil.copyfile('/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'/results/sep_cali_sampled_params_chain_'+str(np.argwhere(arr==np.max(arr))[0][0])+'_'+str(int(niterations[0]))+'.bin',
                            '/data/scratch/wusongj/paper4/cali_sep/'+catchment_ID+'_sep_cali_sampled_params_chain.bin')
            
            #print(arr, np.argwhere(arr==np.max(arr)))
        except Exception as e:
            print('No results found in catchment ',  catchment_ID)





elif mode == 'bbb':

    catchment_ID = '6_001'
    ref_asc = '/data/scratch/wusongj/paper4/data/catchment_info/cali/'+catchment_ID+'/spatial/dem.asc'
    output_path = '/data/scratch/wusongj/paper4/test/'+catchment_ID+'/run/outputs/'
    output_path = '/data/scratch/wusongj/paper4/forward_cali/'+catchment_ID+'/run/outputs/'
    fnames = [f for f in os.listdir(output_path) if '_map.bin' in f]

    ref_data = np.loadtxt(ref_asc, skiprows=6)
    for fname in fnames:
        print(fname)
        data = np.fromfile(output_path + fname).reshape(-1, ref_data.shape[0], ref_data.shape[1])
        data = np.mean(data[2:,:,:], axis=0)
        print(output_path+fname.split('.')[0]+'.asc')
        GEM_tools.create_asc(data, output_path+fname.split('.')[0]+'.asc', ref_asc)


    pass


