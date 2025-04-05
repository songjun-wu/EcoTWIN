import os
import GEM_tools
from def_GEM_test import *

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



