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
        if line_list[1] == 'int':
            attri_type = 'int'
        elif line_list[1] == 'long':
            attri_type = 'qint64'

    return attri_name, attri_up_name, attri_type, comment

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    tmpl_dir = os.path.join(root_dir, 'template')
    output_dir = os.path.join(root_dir, 'generator')
    input_file = open(os.path.join(root_dir, 'className.xml'), 'r', encoding='gb18030', errors='ignore')

    template_cpp_file = open(os.path.join(tmpl_dir, 'model_cpp.tmpl'), 'r')
    cpp_tmpl = Template(template_cpp_file.read())
    
    template_h_file = open(os.path.join(tmpl_dir, 'model_head.tmpl'), 'r')
    h_tmpl = Template(template_h_file.read())

    attri_tmpl = Template('JY_PROPERTY_READWRITE($type_name, $var_up_name) \t\t')
    model_replace_tmpl = Template('map.insert("$var_up_name","$var_name");\n')
    constructor_tmpl = Template('this->_$var_up_name\t\t\t= obj._$var_up_name;\n')
    equal_tmpl = Template(' (obj._$var_up_name == this->_$var_up_name) &&')
    zero_tmpl = Template('this->_$var_up_name = 0;\n')

    class_name = input_file.readline().strip()
    h_class_file = open(os.path.join(output_dir, r'%s.h' % class_name), 'w', encoding='gb18030')
    cpp_class_file = open(os.path.join(output_dir, r'%s.cpp' % class_name), 'w')

    input_file.readline() #空行

    model_attri = ''
    model_replace = ''
    model_constructor = ''
    model_zero = ''

    table = str.maketrans({key: None for key in string.punctuation})
        
    line_count = 0
    while 1:
        line = input_file.readline()
        line = line.strip()
        if not line:
            break

        line_count +=1

        attri_name, attri_up_name, attri_type, comment = fun_get_attri(line)

        attri_item = attri_tmpl.safe_substitute(type_name=attri_type, var_up_name=attri_up_name)
        model_attri += '    ' + attri_item + comment + '\n'

        replace_item = model_replace_tmpl.safe_substitute(var_name=attri_name, var_up_name=attri_up_name)
        model_replace += '    ' + replace_item

        constructor_item = constructor_tmpl.safe_substitute(var_up_name=attri_up_name)
        model_constructor += '    ' + constructor_item

        if attri_type == 'int' or attri_type == 'qint64':
            zero_item = zero_tmpl.safe_substitute(var_up_name=attri_up_name)
            model_zero += '    ' + zero_item

    str_h_out = h_tmpl.safe_substitute(str_class_name = class_name, str_class_define = class_name.upper(), str_model_atti=model_attri)
    str_cpp_out = cpp_tmpl.safe_substitute(str_class_name = class_name, str_model_replace=model_replace, str_model_constructor=model_constructor,
                                            str_model_zero = model_zero)

    h_class_file.write(str_h_out)
    cpp_class_file.write(str_cpp_out)

    input_file.close()
    h_class_file.close()
    cpp_class_file.close()
