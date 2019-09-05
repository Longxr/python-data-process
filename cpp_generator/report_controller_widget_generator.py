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
        
        cppFilePath = r'generator/%s.cpp' % className
        headFilePath = r'generator/%s.h' % className
        controllerCppFilePath = r'generator/%sController.cpp' % className
        controllerHeadFilePath = r'generator/%sController.h' % className
 
        
        cpp_class_file = open(cppFilePath,'w')
        head_class_file = open(headFilePath,'w')
        controller_cpp_class_file = open(controllerCppFilePath,'w')
        controller_head_class_file = open(controllerHeadFilePath,'w')
 
        cppLines = []
        headLines = []
        controllerCppLines = []
        controllerHeadLines = []


        # 2.模版文件
        template_cpp_file = open(r'controller/report_widget_cpp.template','r')
        cpp_tmpl = Template(template_cpp_file.read())
        
        template_head_file = open(r'controller/report_widget_head.template','r')
        head_tmpl = Template(template_head_file.read())

        template_controller_cpp_file = open(r'controller/report_controller_cpp.template','r')
        controller_cpp_tmpl = Template(template_controller_cpp_file.read())
        
        template_controller_head_file = open(r'controller/report_controller_head.template','r')
        controller_head_tmpl = Template(template_controller_head_file.read())
        
        # 2.模板进行转换
        cppLines.append(cpp_tmpl.substitute(
                    CLASSNAME = className))
 
        headLines.append(head_tmpl.substitute(
                    CLASSNAME = className, CLASSDEFINE = className.upper()))

        controllerCppLines.append(controller_cpp_tmpl.substitute(
                    CLASSNAME = className))
 
        controllerHeadLines.append(controller_head_tmpl.substitute(
                    CLASSNAME = className, CLASSDEFINE = className.upper()))
        
        # 3.将生成的代码写入文件
        cpp_class_file.writelines(cppLines)
        cpp_class_file.close()
 
        head_class_file.writelines(headLines)
        head_class_file.close()

        controller_cpp_class_file.writelines(controllerCppLines)
        controller_cpp_class_file.close()
 
        controller_head_class_file.writelines(controllerHeadLines)
        controller_head_class_file.close()
        
        pass   
