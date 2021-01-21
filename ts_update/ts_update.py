import json
import os
import re
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dic_translate = {}
    with open(root_dir + '/111.json', "r", encoding='utf-8') as fin:
        dic_translate = json.load(fin)

    # for key, value in dic_translate.items():
        # print("key--：%s value--: %s" % (key, value))

    update_tree = ET.parse(root_dir + '/i18n_zh_cn.ts')
    element_root = update_tree.getroot()  # 使用getroot()获取根节点，得到的是一个Element对象
    print('ts file version: {}, language: {}'.format(element_root.attrib['version'], element_root.attrib['language']))

    for element_context in element_root.findall('context'):
        for element_message in element_context.findall('message'):
            source_element = element_message.find('source')
            translation_element = element_message.find('translation')
            print('source: {}, translation: {}'.format(source_element.text, translation_element.text))

            # 删除源码中已经没有的key，或者在生成ts时命令改为: lupdate xxx.pro -no-obsolete
            translate_type = translation_element.attrib.get('type')
            if translate_type == 'vanished':
                element_context.remove(element_message)
                continue

            # 修改翻译内容
            if source_element.text in dic_translate:
                translate_value = dic_translate[source_element.text]
                # 没有对应的翻译则跳过
                if len(translate_value) == 0:
                    continue

                translation_element.text = translate_value
                # 删除属性type，没翻译时为unfinished，表示没翻译完成
                if 'type' in translation_element.attrib:
                    del translation_element.attrib['type']

    update_tree.write(root_dir + '/result.ts', encoding='utf-8', xml_declaration=True)
