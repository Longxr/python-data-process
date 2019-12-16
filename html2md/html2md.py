import requests
from tomd import Tomd


def html2md(url):
    # 获取html内容
    html_data = requests.get(url).text

    text = Tomd(html_data).markdown
    # print(text)

    with open("html.md", "w", encoding='utf-8') as text_file:
        text_file.write(text)


if __name__ == '__main__':
    url = 'https://www.runoob.com/w3cnote/linux-common-command-2.html'
    html2md(url)
    print('Convert success')
