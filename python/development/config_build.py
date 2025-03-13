from develop_tools import *

def read_configs(fname, options, signs, datas, reports):
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Options */', '/* end of Options */')

        content = []
        for i in range(len(options)):
            content.append('  readInto('+options[i][0]+', "'+options[i][0]+'", lines);\n')
        content = lines[:start] + content + lines[end:]
    with open(fname, 'w') as f:
            f.writelines(content)

    for j in range(len(signs)):
        sign = signs[j]
        Contents = []
        for data in (datas[j]):
            if 'spatial' in data[4]:
                Contents.append(data)

        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')
            content = []          
            for i in range(len(Contents)):
                content.append('  readInto('+'fn_'+Contents[i][0]+', "'+Contents[i][5]+'", lines);\n')
            content = lines[:start] + content + lines[end:]
            
        with open(fname, 'w') as f:
            f.writelines(content)

    with open(fname, 'r') as f:
        lines = f.readlines()
        
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')

        content = []     
        content.append('  // 1: report time series at gauging stations; 2: report maps\n')  
        for i in range(len(reports)):
            content.append('  readInto('+'report_'+reports[i][0]+', "report_'+reports[i][5]+'", lines);\n')
        content = lines[:start] + content + lines[end:]
        
    with open(fname, 'w') as f:
        f.writelines(content)


def gen_config_template(path, options, signs, datas, reports):
    text = []
    text.append('#############################################\n')
    text.append('# Generic Ecohydrological model\n')
    text.append('# Configuration file\n')
    text.append('###########################################\n\n\n')

    text.append('# Paths\n')
    text.append('Maps_Folder = ./spatial/\n')
    text.append('Clim_Maps_Folder = ./climate/\n')
    text.append('Output_Folder = ./outputs/\n\n')
    text.append('# Settings\n')
    text.append('Simul_start = 0 # always 0\n')
    text.append('Simul_end = 157766400 # in second\n')
    text.append('Simul_tstep = 86400 # seconds (daily)\n')
    text.append('Clim_input_tstep = 86400 # seconds (daily)\n')
    text.append('Report_interval = 86400 # seconds (daily)\n\n')

    text.append('# Options \n')
    for i in range(len(options)):
        text.append(options[i][0] + ' = 1  # ' + options[i][1] + '\n')
    
    text.append('climate_zones = climate_zones.asc # Needed if opt_climate_input_format = 1; Zone ID should start from 0!\n')

    for i in range(len(datas)):
        counter = 0
        for j in range(len(datas[i])):
            
            data = datas[i][j]
            if 'spatial' in data[4]:
                if counter == 0:
                    text.append('\n### '+signs[i]+'\n')
                var_name = ('').join(data[0].split('_'))
                if 'spatial_TS' in data[4]:
                    text.append(data[5]+'  =  '+ var_name + '.bin   # '+data[2] + '\n')
                else:
                    text.append(data[5]+'  =  '+ var_name + '.asc   # '+data[2] + '\n')
                counter += 1

    text.append('\n\n### Reports\n')
    text.append('# 1: report maps; 2: report time series at gauging stations\n')
    for i in range(len(reports)):
        data = reports[i]
        text.append('report_'+data[5]+'  =  0   # '+data[2] + '\n')

    with open(path + 'config.ini', 'w') as f:
        f.writelines(text)


def report_build(fname, reports):
    with open(fname, 'r') as f:
        lines = f.readlines()
        
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')

        content = []     
        content.append('  // 1: report time series at gauging stations; 2: report maps\n')  
        for i in range(len(reports)):
            data = reports[i]
            content.append('  if (ctrl.report_'+data[0]+'==1) {reportTS('+data[0]+', "'+data[5]+'", ctrl.path_ResultsFolder);}\n')
            content.append('  else if (ctrl.report_'+data[0]+'==2) {reportMap('+data[0]+', "'+data[5]+'", ctrl.path_ResultsFolder);}\n\n')

        content = lines[:start] + content + lines[end:]
    
    with open(fname, 'w') as f:
        f.writelines(content)
