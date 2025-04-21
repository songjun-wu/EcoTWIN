import os
import shutil
import numpy as np

def linux_make(release_path):
    path = os.getcwd()
    os.chdir(release_path)
    #os.system('make clean')
    os.system('make all')
    os.chdir(path)


def release_linux(path, release_path):
    header = ['################################################################################\n' + \
                '# Automatically-generated file. Do not edit!\n' + \
                '################################################################################\n\n' + \
                '# Add inputs and outputs from these tool invocations to the build variables\n']

    fnames_0 = os.listdir(path)
    folders = []
    for fname_0 in fnames_0:
        text = []
        if os.path.isdir(path + fname_0):  # for each folder
            
            fnames_1 = np.array(os.listdir(path + fname_0))
            cppfiles = fnames_1[[kk.split('.')[-1]=='cpp' for kk in fnames_1]]
            if len(cppfiles) > 0:
                folders.append(fname_0)
                if not os.path.exists(release_path + fname_0):
                    os.mkdir(release_path + fname_0)

                text.extend(header)
                cpp_text = ['CPP_SRCS += ' + '\\'+ '\n']
                objs_text = ['OBJS += ' + '\\'+ '\n']
                DEPS_text = ['CPP_DEPS += ' + '\\'+ '\n']
                for gg in range(len(cppfiles)):
                    cpp_text.append('../codes/'+fname_0+'/'+cppfiles[gg]+' \\\n')
                    objs_text.append('./'+fname_0+'/'+cppfiles[gg].split('.')[0]+'.o \\\n')
                    DEPS_text.append('./'+fname_0+'/'+cppfiles[gg].split('.')[0]+'.d \\\n')
                
                text.extend(cpp_text + ['\n\n'])  
                text.extend(objs_text + ['\n\n']) 
                text.extend(DEPS_text + ['\n\n'])                
                text.extend(['# Each subdirectory must supply rules for building sources it contributes\n'])
                text.extend([fname_0+'/%.o: ../codes/'+fname_0+'/%.cpp\n'])
                text.extend(["	@echo 'Building file: $<'\n"])
                text.extend(["	@echo 'Invoking: GCC C++ Compiler'\n"])
                text.extend(['	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"\n'])
                text.extend(["	@echo 'Finished building: $<'\n"])
                text.extend(["	@echo ' '\n"])

                with open(release_path + fname_0 + '/subdir.mk', 'r') as f:
                    lines = f.readlines()
                if(('').join(text) != ('').join(lines)):
                    with open(release_path + fname_0 + '/subdir.mk', 'w') as f:
                        f.writelines(text)   

    with open(release_path + 'sources.mk', 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if 'SUBDIRS :=' in lines[i]: 
            start = i
    text = lines[:start+1]
    for folder in folders:

        text.extend(folder + ' \\\n')
    text.extend('. \\')

    if(('').join(text) != ('').join(lines)):
        with open(release_path + 'sources.mk', 'w') as f:
            f.writelines(text)
    

    with open(release_path + 'makefile', 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if '-include sources.mk' in lines[i]:
            start = i
        elif '-include subdir.mk' in lines[i]:
            end = i
    content = []
    for folder in folders:
        content.append('-include '+folder+'/subdir.mk\n')

    text = lines[:start+1]
    text.extend(content)
    text.extend(lines[end:])
    if(('').join(text) != ('').join(lines)):
        with open(release_path + 'makefile', 'w') as f:
            f.writelines(text)
    