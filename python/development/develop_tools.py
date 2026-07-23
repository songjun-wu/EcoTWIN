def get_class(lines, name):
    """Find and extract a class by name using indentation analysis."""
    for i, line in enumerate(lines):
        if line.strip().startswith(f"class {name}"):
            indent = len(line) - len(line.lstrip())
            res = [line]
            # Collect lines until indentation returns to or goes below the class definition
            for l in lines[i + 1:]:
                stripped = l.strip()
                if stripped and not stripped.startswith('#') and (len(l) - len(l.lstrip())) <= indent:
                    break
                res.append(l)
            return res
    return []

def extract_multiple_classes(src, dest, class_list):
    """Extract multiple classes in class_list from source and save them to destination."""
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    extracted_blocks = ['import numpy as np\n']
    for name in class_list:
        cls_content = get_class(lines, name)
        if cls_content:
            # Join lines of a single class into one block of text
            extracted_blocks.append("".join(cls_content))
    print(extracted_blocks)  # todo
    with open(dest, 'w', encoding='utf-8') as f:
        # Join all extracted classes with PEP 8 standard double blank lines
        f.write("\n\n".join(extracted_blocks) + "\n")


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



def if_condition_build_reverse(key, lines):

    key = key.replace('ctrl.', '')

    if not (key is None):
        num_blank = lines[0].find(lines[0].lstrip()[0])
        new_lines = lines[0][:num_blank] + 'if (!('+key+')){\n'
        for line in lines:
            new_lines += '  ' + line
        new_lines += lines[0][:num_blank] + '}\n'
    else:
        new_lines = ''
        for line in lines:
            new_lines += line

    return new_lines