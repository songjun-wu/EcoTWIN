from develop_tools import *

def parameterisation_build(fname, parameters):

    content = []
    keys, grouped_data = group_text(parameters)
    for key in keys:
        text = []
        for i in range(len(grouped_data[key])):
            
            text.append('  ' + grouped_data[key][i][0] + '->reset();\n')
            text.append('  for (int k=0; k<param_category->n_category; k++){\n')
            text.append('    for (int i=0; i<param_category->nrow; i++){\n')
            text.append('      for (int j=0; j<param_category->ncol; j++){\n')
            text.append('        ' + grouped_data[key][i][0] + '->matrix[i][j] += param_category->matrix[k][i][j] * ' + grouped_data[key][i][0][1:] + '[k];\n')
            text.append('  }' + '}' +'}\n')
        content.append(if_condition_build(key, text))
    
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Parameters */', '/* end of Parameters */')
        
            

        content = lines[:start] + content + lines[end:]
            
    with open(fname, 'w') as f:
        f.writelines(content)