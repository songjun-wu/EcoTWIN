from develop_tools import *
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/scripts_v2/')
import def_GEM_v2

def parameterisation_build(fname, parameters):

    content = []
    content.append('  int nodata = ctrl._nodata;\n\n')
    keys, grouped_data = group_text(parameters)

    param_list = def_GEM_v2.Param.ref



    for key in keys:
        text = []
        for i in range(len(grouped_data[key])):
            param_name = grouped_data[key][i][0]
            if param_name[1:] in param_list.keys():
                log_flag = param_list[param_name[1:]]['log']
            else:
                log_flag = 0


            if log_flag == 1:
                text.append('\n  ' + param_name + '->reset();\n')
                text.append('  for (int k=0; k<param_category->n_category; k++){\n')
                text.append('    if ('+param_name[1:]+'[k]!=nodata) {\n')
                text.append('      double logp = log('+param_name[1:]+'[k]);\n')
                text.append('      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {\n')
                text.append('        '+param_name+'->val[j] += param_category->val[k][j] * logp;\n')
                text.append('   }}}\n')
                text.append('  for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {\n')
                text.append('    '+param_name+'->val[j] = exp('+param_name+'->val[j]);\n')
                text.append('   }\n')
            else:
                text.append('\n  ' + param_name + '->reset();\n')
                text.append('  for (int k=0; k<param_category->n_category; k++){\n')
                text.append('    if ('+param_name[1:]+'[k]!=nodata) {\n')
                text.append('      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {\n')
                text.append('        '+param_name+'->val[j] += param_category->val[k][j] * '+param_name[1:]+'[k];\n')
                text.append('   }}}\n')

                

        content.append(if_condition_build(key, text))
    
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Parameters */', '/* end of Parameters */')
        
            

        content = lines[:start] + content + lines[end:]

    if(('').join(content) != ('').join(lines)):     
        with open(fname, 'w') as f:
            f.writelines(content)