import json
import re

import requests
from lxml import html
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 具体介绍参考：https://blog.csdn.net/kelanmomo/article/details/82886718
from selenium.webdriver.support.wait import WebDriverWait

# browser = webdriver.Chrome()
# wait = WebDriverWait(browser,10)

#这是个人登录淘宝网址时，保留的cookie文件，可用浏览器插件EditThisCookie把登录时的cookie保存下来
def add_cookies():
    with open('./static/taobao_cookie.json','rb') as f:
        cookies = json.load(f)
        for item in cookies:
            browser.add_cookie(item)

def get_products_pyquery(html_data):
    #使用pyquery获取商品信息
    doc = pq(html_data)
    items = doc('#mainsrp-itemlist .items .item').items()#关于css选择器，可以模糊匹配

    for item in items:
        product = {
            'image':item.find('.pic-link .img').attr('data-src'),#商品缩略图
            'price':item.find('.price').text().strip().replace('\n',''),#价格
            'deal':item.find('.deal-cnt').text(),#销售量
            'title':item.find('.title').text().strip().replace('\n',','),#简介
            'shop':item.find('.shop').text(),#商家
            'location':item.find('.location').text()#商家地址
        }
        print(product)

def get_products_xpath(html_data):
    #使用xpath获取商品信息
    selector = html.fromstring(html_data)
    items = selector.xpath('//div[@class="item J_MouserOnverReq  "]')
    print(len(items))

    for item in items:
        product = {
            'goods':item.xpath('div/div/div/a/img/@alt')[0],#商品名称
            'price':item.xpath('div[2]/div/div/strong/text()')[0],#价格
            'shop':item.xpath('div[2]/div[3]/div/a/span[2]/text()')[0],#店铺
            'address':item.xpath('div[2]/div[3]/div[@class="location"]/text()')[0],#地址
        }
        print(product)

def get_products_json(html_data):
    #使用json解析获取商品信息

    content = re.findall(r'g_page_config = (.*?)g_srp_loadCss',html_data,re.S)[0] # 正则表达式处理的结果是一个列表，取第一个元素（字典）
 
    # 格式化，将json格式的字符串切片，去掉首尾空格还有最后一个分号
    content = content.strip()[:-1]
    # 将json转为dict
    content = json.loads(content)
 
    # 借助json在线解析分析，取dict里的具体data
    data_list = content['mods']['itemlist']['data']['auctions']
 
 
    # 提取数据
    for item in data_list:
        temp = {
            'title' : item['raw_title'],
            'view_price' : item['view_price'],
            'view_sales' : item['view_sales'],
            'view_fee' : '否' if float(item['view_fee']) else '是' ,
            'isTmall' : '是' if item['shopcard']['isTmall'] else '否',
            'area' : item['item_loc'],
            'store' : item['nick'],
            'link' : item['detail_url'],
        }
        print(temp)

def index_page(page):
    print('正在爬取第',page,'页')
    try:
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))#找到页面底部页数跳转输入框
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))#输入页数后，点击确定进行跳转
            input.clear()
            input.send_keys(page)
            submit.click()
        #判断当前高亮的页码数是当前的页码数即可，所以这里使用了另一个等待条件text_to_be_present_in_element，它会等待指定的文本出现在某一个节点里面时即返回成功。
        # 这里我们将高亮的页码节点对应的CSS选择器和当前要跳转的页码通过参数传递给这个等待条件，这样它就会检测当前高亮的页码节点是不是我们传过来的页码数，
        # 如果是，就证明页面成功跳转到了这一页，页面跳转成功。
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager .items .item.active .num'), str(page)))
        #我们最终要等待商品信息加载出来，就指定了presence_of_element_located这个条件，然后传入了.m-itemlist .items .item这个选择器，而这个选择器对应的页面内容就是每个商品的信息块，
        # 可以到网页里面查看一下。如果加载成功，就会执行后续的get_products()方法，提取商品信息。
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        
        html_data = browser.page_source
        # print(html_data,file=open('./static/source.html','w',encoding='utf-8'))

        # get_products_pyquery(html_data)
        get_products_xpath(html_data)


    except TimeoutException:
        index_page(page)



def spider(sn):
    # 爬取淘宝网图书数据
    browser.get('https://www.taobao.com')
    add_cookies()
    input = browser.find_element_by_id('q')
    input.send_keys(sn)
    button = browser.find_element_by_class_name('btn-search')
    button.click()
    print('淘宝模拟登录成功，现在开始爬取内容')
    # for i in range(1,3):
        # index_page(i)
    index_page(1)
    browser.close()

if __name__ == '__main__':
    sn = '9787115428028'
    # spider(sn)
    f = open('./static/source.html', 'r', encoding='utf-8')
    html_data = f.read()
    # get_products_pyquery(html_data)
    # get_products_xpath(html_data)
    get_products_json(html_data)
