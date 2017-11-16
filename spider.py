import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool

def get_page(url):
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        responce = requests.get(url,headers=headers)
        # responce.encoding = 'gbk'
        return responce.text
    except RequestException:
        return None

def html_parse(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:#生成字典
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'scocre':item[5]+item[6]
        }

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    # print(html)
    for item in html_parse(html):
        print(item)

if __name__ == '__main__':
    # for i in range(10):
    #   main(i*10)
    pool = Pool() #进程池 多进程
    pool.map(main,[i*10 for i in range(10)])