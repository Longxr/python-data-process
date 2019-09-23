#coding=utf-8

import os
from string import Template


def fun_replace(str):
    str1 =  str.strip('*')
    return str1.replace('m_p', '')

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = open(os.path.join(root_dir, 'input.cpp'),'r')
    out_h_file = open(os.path.join(root_dir, 'output.h'),'w')
    out_cpp_file = open(os.path.join(root_dir, 'output.cpp'),'w')
    template_ui_getter_file = open(os.path.join(root_dir, 'ui_getter.template'),'r')
    template_layout_getter_file = open(os.path.join(root_dir, 'layout_getter.template'),'r')
    
    h_tmpl = Template('$class_name*\tGet$var_name();\n')
    ui_getter_tmpl = Template(template_ui_getter_file.read())
    layout_getter_tmpl = Template(template_layout_getter_file.read())

    parent_widget = input_file.readline().strip()

    var_nulls = list()

    while 1: 
        line = input_file.readline()
        if not line: 
            break
            
        line = line.strip()
        line = line.strip(';')
        name_list = list(map(fun_replace, line.split()))

        out_h = h_tmpl.safe_substitute(class_name=name_list[0], var_name=name_list[1], parent_name=parent_widget)
        out_h_file.write(out_h)

        out_cpp = "";
        if "Layout" in name_list[0]:
            out_cpp = layout_getter_tmpl.safe_substitute(class_name=name_list[0], var_name=name_list[1], parent_name=parent_widget)
        else:
            out_cpp = ui_getter_tmpl.safe_substitute(class_name=name_list[0], var_name=name_list[1], parent_name=parent_widget)
        out_cpp_file.write(out_cpp + '\n')

        var_nulls.append('m_p%s = nullptr;\n'%name_list[1])

    out_cpp_file.write('\n')
    for i in var_nulls:
        out_cpp_file.write(i)
 
    input_file.close()
    out_h_file.close()
    out_cpp_file.close()
