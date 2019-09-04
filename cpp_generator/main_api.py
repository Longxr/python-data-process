#coding=utf-8

from report_api_generator import ReportCppGenerator
 
if __name__ == '__main__':
    
    
    
    # 初始化报表创建类
    report_gen = ReportCppGenerator()
    
    # 配置文件加载所需创建的类名称
    configFilePath = 'className.xml'
    cpp_class_file = open(configFilePath,'r')
    
    lines = []
    
    while 1: 
        line = cpp_class_file.readline() 
        if not line: 
            break
        else:
            line = line.strip('\n')
            print (line)
            report_gen.generate(line)
            lines.append(line)   
    pass # do something 
 
    
    pass
