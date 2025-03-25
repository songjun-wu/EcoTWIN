def group_text(datas):
    grouped_data = {}
    keys = []
    for data in datas:
        if data[1][0]['key'] is None:
            key = None
        else: 
            if len(data[1]) == 1:
                key = 'ctrl.' + data[1][0]['key'] + ' == ' + str(data[1][0]['value'])
            else:
                tmp = []
                for kk in range(len(data[1])):

                    tmp.append('ctrl.' + data[1][kk]['key'] + ' == ' + str(data[1][kk]['value']))
                key = (' or ').join(tmp)
        if key in grouped_data:
            grouped_data[key].append(data)
        else:
            grouped_data[key] = [data]
            keys.append(key)
    return keys, grouped_data

def locate_text(lines, start_sign, end_sign):
    start = -9999
    end = -9999
    for i in range(len(lines)):
        if start_sign in lines[i]:
            start = i + 1
        if end_sign in lines[i]:
            end = i
    if start < 0:
        raise Exception("Did not find  " + start_sign)
    if end < 0:
        raise Exception("Did not find  " + end_sign)
    return start, end

def if_condition_build(key, lines):

    if not (key is None):
        num_blank = lines[0].find(lines[0].lstrip()[0])
        new_lines = lines[0][:num_blank] + 'if ('+key+'){\n'
        for line in lines:
            new_lines += '  ' + line
        new_lines += lines[0][:num_blank] + '}\n'
    else:
        new_lines = ''
        for line in lines:
            new_lines += line

    return new_lines