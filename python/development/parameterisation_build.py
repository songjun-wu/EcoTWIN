from develop_tools import *

def parameterisation_build(fname, parameters):

    content = []
    content.append('  int r;\n  int c;\nint nodata = ctrl._nodata;\n\n')
    keys, grouped_data = group_text(parameters)
    for key in keys:
        text = []
        for i in range(len(grouped_data[key])):
            text.append('\n  ' + grouped_data[key][i][0] + '->reset();\n')

            text.append('  for (int k=0; k<param_category->n_category; k++){\n')

            text.append('    if ('+grouped_data[key][i][0][1:]+'[k]!=nodata) {\n')
            
            text.append('\n      for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {\n')
            text.append('      r = _sortedGrid.row[j];\n')
            text.append('      c = _sortedGrid.col[j];\n')
            text.append('      '+grouped_data[key][i][0]+'->matrix[r][c] += param_category->matrix[k][r][c] * '+grouped_data[key][i][0][1:]+'[k];\n')
            text.append('   }\n')
            text.append('   }\n')
            text.append('   }\n\n')

        print(text)
        content.append(if_condition_build(key, text))
    
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Parameters */', '/* end of Parameters */')
        
            

        content = lines[:start] + content + lines[end:]
            
    with open(fname, 'w') as f:
        f.writelines(content)