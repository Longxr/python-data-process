import requests
from lxml import html


def spider(sn, book_list):
    # 爬取一号店图书数据
    url = 'https://search.yhd.com/c0-0/k{0}/'.format(sn)

    # 获取html内容
    html_data = requests.get(url).text

    # xpath查询对象
    selector = html.fromstring(html_data)

    # 获取图书列表
    ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
    for li in ul_list:
        title = li.xpath('div//p[@class="proName clearfix"]/a/@title')
        print(title[0])

        link = li.xpath('div//p[@class="proName clearfix"]/a/@href')
        print(link[0])

        price = li.xpath('div//p[@class="proPrice"]/em/@yhdprice')
        print(price[0])

        store = li.xpath('div//p[@class="searh_shop_storeName storeName limit_width"]/a/@title')
        print(store[0])

        book_list.append({
            'price': price[0],
            'title': title[0],
            'link': link[0],
            'store': store[0]
        })


if __name__ == '__main__':
    sn = '9787115428028'
    spider(sn)
