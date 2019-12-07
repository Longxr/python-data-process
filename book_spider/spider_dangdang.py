import requests
from lxml import html

def spider(sn):
    # 爬取当当网图书数据
    url = 'http://search.dangdang.com/?key={sn}&act=input'.format(sn = sn)

    # 获取html内容
    html_data = requests.get(url).text

    # xpath查询对象
    selector = html.fromstring(html_data)

    # 获取图书列表
    ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
    for li in ul_list:
        title = li.xpath('a/@title')
        print(title[0])

        link = li.xpath('a/@href')
        print(link[0])

        price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
        print(price[0].replace('¥', ''))

        store = li.xpath('p[@class="search_shangjia"]/a/text()')
        store = '当当自营' if len(store) == 0 else store[0]
        print(store)

if __name__ == '__main__':
    sn = '9787115428028'
    spider(sn)