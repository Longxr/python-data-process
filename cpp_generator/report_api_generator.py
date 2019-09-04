#coding=utf-8

from string import Template
 
class ReportCppGenerator(object):
    '''
    classdocs
    '''
 
    def __init__(self):
        '''
        Constructor
        '''
    
    def generate(self, cppName):
        
        print ("Generate Start")
        
        #1 将传入的class的名称创建对应的head 和 cpp文件
        className = cppName
        
        cppFilePath = r'generator/%sManager.cpp' % className
        headFilePath = r'generator/%sManager.h' % className
 
        
        cpp_class_file = open(cppFilePath,'w')
        head_class_file = open(headFilePath,'w')
 
        cppLines = []
        headLines = []
 
 
        # 2.模版文件
        template_cpp_file = open(r'api/report_cpp.template','r')
        cpp_tmpl = Template(template_cpp_file.read())
        
        template_head_file = open(r'api/report_head.template','r')
        head_tmpl = Template(template_head_file.read())
        
        # 2.模板进行转换
        cppLines.append(cpp_tmpl.substitute(
                    CLASSNAME = className))
 
        headLines.append(head_tmpl.substitute(
                    CLASSNAME = className, CLASSDEFINE = className.upper()))
        
        # 3.将生成的代码写入文件
        cpp_class_file.writelines(cppLines)
        cpp_class_file.close()
 
        head_class_file.writelines(headLines)
        head_class_file.close()
        
        pass   
