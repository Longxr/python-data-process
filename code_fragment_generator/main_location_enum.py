#coding=utf-8
import os
from string import Template

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = open(os.path.join(root_dir, 'input.cpp'),'r')
    output_file = open(os.path.join(root_dir, 'output.cpp'),'w')
    
    s = Template('if ($enum_name\t== str) return tr("$key_name");\n')
    
    while 1: 
        line = input_file.readline()
        if not line: 
            break
            
        line = line.strip()
        line = line.strip(',')
        
        if not len(line) or line.startswith('//'):
            output_file.write(line + '\n')
        else:
            output_line = s.safe_substitute(enum_name=line.upper(), key_name=line.replace('STR_', '').lower())
            output_file.write(output_line)  
    pass # do something 
 
    input_file.close()
    output_file.close()
