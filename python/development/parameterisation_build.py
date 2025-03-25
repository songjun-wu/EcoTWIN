from develop_tools import *

def parameterisation_build(fname, parameters):

    content = []
    content.append('  int nodata = ctrl._nodata;\n\n')
    keys, grouped_data = group_text(parameters)
    for key in keys:
        text = []
        for i in range(len(grouped_data[key])):
            text.append('\n  ' + grouped_data[key][i][0] + '->reset();\n')

            text.append('  for (int k=0; k<param_category->n_category; k++){\n')

            text.append('    if ('+grouped_data[key][i][0][1:]+'[k]!=nodata) {\n')
            
            text.append('      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {\n')
            text.append('      '+grouped_data[key][i][0]+'->val[j] += param_category->val[k][j] * '+grouped_data[key][i][0][1:]+'[k];\n')
            text.append('   }}}\n')

        content.append(if_condition_build(key, text))
    
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Parameters */', '/* end of Parameters */')
        
            

        content = lines[:start] + content + lines[end:]

    if(('').join(content) != ('').join(lines)):     
        with open(fname, 'w') as f:
            f.writelines(content)