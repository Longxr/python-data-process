import requests

def get_book(sn):
    url = 'http://search.dangdang.com/'
    rest = requests.get(url, params={
        'key': sn,
        'act': 'input'
    })
    print(rest.text)
    print(rest.encoding)

if __name__ == '__main__':
    get_book('9787115428028')