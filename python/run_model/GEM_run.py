import os
import GEM_tools
from def_GEM import *

""""""
# set the env for model runs
GEM_tools.set_env(Path)
GEM_tools.set_config(Path)

os.chdir('/home/wusongj/GEM/python/development')
os.system('python3 develop.py')
os.chdir(Path.run_path)
os.system('./gEcoHydro')


