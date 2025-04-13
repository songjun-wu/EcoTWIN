from develop_tools import *
import numpy as np

def read_configs(fname, options, signs, datas, reports):
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Options */', '/* end of Options */')

        content = []
        opt_list = []
        for key in options.keys():
            item = options.get(key)
            if item['key'] is None:
                continue
            if not item['key'] in opt_list:
                opt_list.append(item['key'])
                content.append('  readInto('+item['key']+', "'+item['key']+'", lines);\n')

        content = lines[:start] + content + lines[end:]
    if(('').join(content) != ('').join(lines)):
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
            if sign == 'GIS':
                content.append('  readInto(fn__fdir, "flow_direction", lines);\n')
                content.append('  readInto(fn__Gauge_to_Report, "Gauge_mask", lines);\n')
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):    
            with open(fname, 'w') as f:
                f.writelines(content)

    with open(fname, 'r') as f:
        lines = f.readlines()
        
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')

        content = []     
        content.append('  // 1: report time series at gauging stations; 2: report maps\n')  
        for i in range(len(reports)):
            if reports[i][5] is not None:
                content.append('  readInto('+'report_'+reports[i][0]+', "report_'+reports[i][5]+'", lines);\n')
        content = lines[:start] + content + lines[end:]
    if(('').join(content) != ('').join(lines)):    
        with open(fname, 'w') as f:
            f.writelines(content)


def read_param(fname, parameters):
    content = []
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Parameters */', '/* end of Parameters */')
        for i in range(len(parameters)):
            content.append('  readIntoParam(' + parameters[i][0][1:] + ', "' + parameters[i][0][1:] + '", lines);\n')
        content = lines[:start] + content + lines[end:]
    if(('').join(content) != ('').join(lines)):        
        with open(fname, 'w') as f:
            f.writelines(content)


def gen_config_template(path, options, signs, datas, reports, parameters, max_category):
    text = []
    text.append('#############################################\n')
    text.append('# Generic Ecohydrological model\n')
    text.append('# Configuration file\n')
    text.append('###########################################\n\n\n')

    text.append('# Paths\n')
    text.append('Maps_Folder = ./spatial/\n')
    text.append('Clim_Maps_Folder = ./climate/\n')
    text.append('Output_Folder = ./outputs/\n\n')
    text.append('# Model configuration\n')
    text.append('Simul_start = 0 # always 0\n')
    text.append('Simul_end = 946857600 # in second\n')
    text.append('Simul_tstep = 86400 # seconds (daily)\n')
    text.append('Clim_input_tstep = 86400 # seconds (daily)\n')
    text.append('Report_interval = 86400 # seconds (daily)\n')
    text.append('Update_interval = 43200000 # seconds (every 100 days); the interval for land use / soil type update \n\n')

    text.append('# Options \n')
    opt_list = []
    for key in options.keys():
        item = options.get(key)
        if item['key'] is None:
            continue
        if not item['key'] in opt_list:
            opt_list.append(item['key'])
            text.append('# ' + item['general_description'] + '\n')
            text.append(item['key'] + ' = '+str(item['value'])+ '\n')
        
    
    

    for i in range(len(datas)):
        counter = 0
        for j in range(len(datas[i])):
            data = datas[i][j]
            if 'spatial' in data[4]:
                if counter == 0:
                    text.append('\n### '+signs[i]+'\n')
                    if signs[i] == 'Parameters':
                        text.append('num_category = 9 # The number of categories for parameterisation ...\n' + \
                                    '#The categories should include the land use types, soil types, or any other types for parameterisation ...\n' + \
                                    '#The distribution of each category (in decimal proportion) should be specified in cat_id.asc ...\n' + \
                                    '#The first category (column) represents global parameter (i.e., cat_0.asc should be 1)\n' )
                        text.append('parameter_file = param.ini # The file contains all parameter name, values, and descriptio. Each column =  a category\n')
                    elif signs[i] == 'Climate':
                        text.append('num_cliamte_zones = 1 # The number of climate zones for parameterisation.\n' )
                        text.append('climate_zones = climate_zones.asc # Needed if opt_climate_input_format = 2; Zone ID should start from 0!\n')
                    elif signs[i] == 'GIS':
                        text.append('flow_direction  =  fdir.asc   # Flow direction [int; d8 method]\n')
                        text.append('Gauge_mask  =  Gauge_to_Report.asc   # Gauges that require outputs [int; start from 0]\n')
                        text.append('# The sequence of reports follows the row-col order\n#For instance, [row 1, col 1] ->  [row 1, col 2] -> [row 2, col 1]\n')
                if data[0][0] == '_':
                    var_name = data[0][1:]
                else:
                    var_name = data[0]
                #var_name = ('').join(data[0].split('_'))
                if 'spatial_TS' in data[4]:
                    text.append(data[5]+'  =  '+ var_name + '.bin   # '+data[2] + '\n')
                elif 'spatial_param' in data[4]:
                    text.append(data[5]+'  =  '+ var_name + '   # '+data[2] + '\n')
                else:
                    text.append(data[5]+'  =  '+ var_name + '.asc   # '+data[2] + '\n')
                counter += 1
            

    text.append('\n\n### Reports\n')
    text.append('# 1: report maps; 2: report time series at gauging stations\n')
    for i in range(len(reports)):
        data = reports[i]
        if data[5] != None:
            text.append('report_'+data[5]+'  =  0   # '+data[2] + '\n')

    with open(path + 'config.ini', 'r') as f:
            lines = f.readlines()
            
    if(('').join(text) != ('').join(lines)):
        with open(path + 'config.ini', 'w') as f:
            f.writelines(text)




def report_build(fname, reports):
    with open(fname, 'r') as f:
        lines = f.readlines()
        
        start, end = locate_text(lines, '/* Init Report */', '/* end of Init Report */')

        content = []     
        content.append('  // Create files for report\n')  
        for i in range(len(reports)):
            data = reports[i]
            if data[5] is not None:
                content.append('  if (ctrl.report_'+data[0]+'>0)  report_create("'+data[5]+'", ctrl.path_ResultsFolder, ctrl.report_'+data[0]+');\n')
        content = lines[:start] + content + lines[end:]
    
    if(('').join(content) != ('').join(lines)):
        with open(fname, 'w') as f:
            f.writelines(content)

    with open(fname, 'r') as f:
        lines = f.readlines()
        
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')

        content = []     
        content.append('  // 1: report time series at gauging stations; 2: report maps\n')  
        for i in range(len(reports)):
            data = reports[i]
            if data[5] is not None:
                content.append('  if (ctrl.report_'+data[0]+'==1) {reportTS(ctrl, Bsn.'+data[0]+', "'+data[5]+'", ctrl.path_ResultsFolder);}\n')
                content.append('  else if (ctrl.report_'+data[0]+'==2) {reportMap(ctrl, Bsn.'+data[0]+', ctrl._sortedGrid, "'+data[5]+'", ctrl.path_ResultsFolder);}\n\n')

        content = lines[:start] + content + lines[end:]
    
    if(('').join(content) != ('').join(lines)):
        with open(fname, 'w') as f:
            f.writelines(content)
