import requests
from lxml import html


def spider(sn):
    # 爬取京东网图书数据
    url = 'https://search.jd.com/Search?keyword={0}'.format(sn)

    # 获取html内容
    respon = requests.get(url)
    respon.encoding = 'utf-8'
    html_data = respon.text

    # xpath查询对象
    selector = html.fromstring(html_data)

    # 获取图书列表
    ul_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')
    for li in ul_list:
        title = li.xpath('div/div[@class="p-name"]/a/@title')
        print(title[0])

        link = li.xpath('div/div[@class="p-name"]/a/@href')
        print(link[0])

        price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
        print(price[0])

        store = li.xpath('div//a[@class="curr-shop"]/@title')
        # store = '京东自营' if len(store) == 0 else store[0]
        print(store)

        ziying = li.xpath('div//i[@class="goods-icons J-picon-tips J-picon-fix"]/text()')
        if len(ziying) > 0:
            print(ziying)

if __name__ == '__main__':
    sn = '9787115428028'
    spider(sn)
