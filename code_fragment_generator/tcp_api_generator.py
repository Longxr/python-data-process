# coding=utf-8

import os
import re
import string
from string import Template


def fun_replace(str):
    str1 = re.sub(r'[^\w\s]','', str)
    return str1.strip()

def fun_get_attri(line):
    line_list = line.split('//')
    comment = ''
    if len(line_list) > 1:
        comment = '//' + line_list[1]

    line_list = line_list[0].split(':')
    line_list = list(map(fun_replace, line_list))

    attri_name = line_list[0]
    attri_up_name = attri_name[0].upper() + attri_name[1:]
    attri_type = 'QString'

    if len(line_list) > 1:
        attri_type = line_list[1]

        if attri_type == 'string':
            attri_type = 'QString'
            

    return attri_name, attri_up_name, attri_type, comment

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = open(os.path.join(root_dir, 'input.cpp'), 'r', encoding='gb18030', errors='ignore')
    out_file = open(os.path.join(root_dir, 'output.cpp'), 'w', encoding='gb18030')
    template_http_api_file = open(
        os.path.join(root_dir, os.path.join('template', 'tcp_api.template')), 'r')

    attri_tmpl = Template('JY_PROPERTY_READWRITE($type_name, $var_up_name) \t\t')
    request_param_tmpl = Template('params.insert("$var_name", _$var_up_name);\n')
    response_replace_tmpl = Template('map.insert("$var_up_name","$var_name");\n')
    constructor_tmpl = Template('this->_$var_up_name\t\t\t= obj._$var_up_name;\n')
    http_api_tmpl = Template(template_http_api_file.read())

    line_first = input_file.readline().split()
    class_name = line_first[0]
    request_type = line_first[1]
    module_id = line_first[2]
    print(class_name, request_type, module_id)

    input_file.readline() #空行

    request_attri = ''
    request_param = ''
    response_attri = ''
    response_replace = ''
    data_constructor = ''

    table = str.maketrans({key: None for key in string.punctuation})
    # new_s = s.translate(table)

    while 1:
        line = input_file.readline()
        line = line.strip()
        if not line:
            break

        attri_name, attri_up_name, attri_type, comment = fun_get_attri(line)

        attri_item = attri_tmpl.safe_substitute(type_name=attri_type, var_up_name=attri_up_name)
        request_attri += '    ' + attri_item + comment + '\n'

        param_item = request_param_tmpl.safe_substitute(var_name=attri_name, var_up_name=attri_up_name)
        request_param += '    ' + param_item
        
    while 1:
        line = input_file.readline()
        line = line.strip()
        if not line:
            break

        attri_name, attri_up_name, attri_type, comment = fun_get_attri(line)

        attri_item = attri_tmpl.safe_substitute(type_name=attri_type, var_up_name=attri_up_name)
        response_attri += '    ' + attri_item + comment + '\n'

        replace_item = response_replace_tmpl.safe_substitute(var_name=attri_name, var_up_name=attri_up_name)
        response_replace += '    ' + replace_item

        constructor_item = constructor_tmpl.safe_substitute(var_up_name=attri_up_name)
        data_constructor += '    ' + constructor_item
        
    
    str_out = http_api_tmpl.safe_substitute(str_api_class=class_name, str_request_type=request_type, str_module_id=module_id, 
    str_request_atti=request_attri, str_request_params=request_param, str_response_atti=response_attri, str_response_replace=response_replace, str_data_constructor=data_constructor)
    out_file.write(str_out)

    print(request_attri)
    print(request_param)
    print(response_attri)
    print(response_replace)

    input_file.close()
    out_file.close()
