import requests
from tomd import Tomd


def html2md(url):
    # 获取html内容
    html_data = requests.get(url).text

    text = Tomd(html_data).markdown
    # print(text)

    with open("html.md", "w", encoding='utf-8') as text_file:
        text_file.write(text)

def html2mdtest():
    html_data = """<pre>ls -a 列出目录所有文件，包含以.开始的隐藏文件
    ls -A 列出除.及..的其它文件
    ls -r 反序排列
    ls -t 以文件修改时间排序
    ls -S 以文件大小排序
    ls -h 以易读大小显示
    ls -l 除了文件名之外，还将文件的权限、所有者、文件大小等信息详细列出来</pre>"""

    text = Tomd(html_data).markdown
    print(text)

if __name__ == '__main__':
    url = 'https://www.runoob.com/w3cnote/linux-common-command-2.html'
    # html2md(url)
    html2mdtest()
    print('Convert success')
