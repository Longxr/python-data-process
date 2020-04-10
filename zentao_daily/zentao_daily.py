import json
import os

import requests
from lxml import html

# from requests.cookies import RequestsCookieJar


# 读取本地文件的cookies
def getcookies_decode_to_dict():
    cookies_dict = {}
    root_dir = os.path.dirname(os.path.abspath(__file__))
    with open(root_dir + '/static/cookie.json', 'rb') as f:
        cookies = json.load(f)
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict


# def getcookies_decode_to_cookiejar():
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#     cookiejar = RequestsCookieJar()
#     with open(root_dir + '/static/cookie.json', 'rb') as f:
#         cookies = json.loads(f.read())
#         for cookie in cookies:
#             cookiejar.set(cookie['name'], cookie['value'])
#     return cookiejar

def spider():
    # 读取本地文件的cookies
    cookies = getcookies_decode_to_dict()

    # 爬取禅道今日动态
    url = 'http://www.mythware.net:9080/zentao/index.php?m=my&f=dynamic'

    # 获取html内容
    html_data = requests.get(url, cookies=cookies).text
    # print(html_data)

    # xpath查询对象
    selector = html.fromstring(html_data)

    # 获取动态列表
    tr_list = selector.xpath('//*[@id= "wrap"]/div[1]/table/tbody/tr')
    bug_dict = {}
    for tr in tr_list:
        tr_type = tr.xpath('td[4]/text()')
        # print(tr_type[0])
        if (tr_type[0] != 'Bug'):
            continue

        tr_id = tr.xpath('td[5]/text()')
        tr_description = tr.xpath('td[6]/a/text()')
        # print(tr_id[0], tr_description[0])

        bug_dict[tr_id[0]] = tr_description[0]

    # key是bug id, value是bug描述
    for k in bug_dict.keys():
        print('Bug', k, '\t', bug_dict[k])


if __name__ == '__main__':
    spider()
