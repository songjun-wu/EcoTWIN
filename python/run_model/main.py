import os
import GEM_tools
from def_GEM import *
import numpy as np

""""""
# set the env for model runs

current_path = os.getcwd()

""""""
#os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/release_linux')
#os.system('make clean')

# Model structure update
os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
os.system('python3 develop.py')

# 
#os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/preprocessing')
#os.system('python3 test_run.py')

# Model preprocessing
GEM_tools.set_env(Path)
GEM_tools.set_config(Path)
GEM_tools.gen_param(Path, Info, Param, np.full(19+5*20, 0.5))

# Model run
os.chdir(Path.run_path)
os.system('./gEcoHydro')

os.chdir(current_path)
os.system('python3 posterior_anlalysis.py')

#tmp = np.fromfile('/home/wusongj/GEM/test/run/outputs/canopy_storage_map.bin').reshape(-1, 9, 9)
#tmp = np.mean(tmp, axis=0)
#print(tmp, np.max(tmp))
