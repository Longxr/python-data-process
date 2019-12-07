from spider_dangdang import spider as dangdang
from spider_jingdong import spider as jd
from spider_taobao import spider as taobao
from spider_yhd import spider as yhd


def spider_book(sn):
    """图书比价工具"""
    book_list = []

    # 当当网数据
    print('dangdang.com dada crawl complete')
    dangdang(sn, book_list)

    # 京东网数据
    print('jd.com dada crawl complete')
    jd(sn, book_list)

    # 一号店数据
    print('yhd.com dada crawl complete')
    yhd(sn, book_list)

    # 淘宝网数据
    # print('taobao.com dada crawl complete')

    #排序书的数据
    book_list = sorted(book_list, key = lambda item : float(item["price"]), reverse = True)

    print('----------------------排序结果------------------------')

    for book in book_list:
        print(book)








if __name__ == '__main__':
    # sn = input('input book ISBN: ')
    sn = '9787115428028'
    spider_book(sn)
