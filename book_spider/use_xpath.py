from  lxml import html

def parse_html():
    f = open('./static/index.html', 'r', encoding='utf-8')
    s= f.read()

    selector = html.fromstring(s)
    h2 = selector.xpath('/html/body/h2/text()')
    print(h2[0])

    img = selector.xpath('/html/body/img/@src')
    print(img[0])

    f.close()

if __name__ == '__main__':
    parse_html()