# Author : ZhangTong
import requests
import json
import re
import time
from urllib.parse import urlencode
from lxml import etree
from multiprocessing.pool import Pool
from config import *
from get_page import page

def structure_url1():
    '''
    构造第一层的URL：包含每个新闻信息的URL
    :return:
    '''
    urls = []
    base_url = 'https://36kr.com/api/search-column/mainsite?'
    for i in range(1, page+1):
        params = {
            'per_page': 20,
            'page': i,
        }
        urls.append(base_url + urlencode(params))
    return urls

def structure_url2(id):
    '''
    构造第二层的URL：包含新闻详情的URL
    :param id: 每个新闻对应的id
    :return:
    '''
    base_url = 'https://36kr.com/p/'
    url = '%s.html' % (base_url + str(id))
    return url

def download(url):
    '''
    发送请求，返回响应内容
    :param url:
    :return:
    '''
    headers = {
        'Host': '36kr.com',
        'Referer': 'https://36kr.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'UTF-8'
            return response.text
    except Exception as e:
        print(e)

def parse_first(text):
    '''
    获取新闻id，从而构造新闻详情URL
    :param text:
    :return:
    '''
    js = json.loads(text)
    items = js['data']['items']
    for item in items:
        id = item['id']
        yield id

def parse_second(text):
    '''
    解析新闻详情页，获得新闻id, title, summary, content
    :param text:
    :return:
    '''
    item = {}
    text = re.search(
        '<script>var props={".*?{"id":"(.*?)",.*?"title":"(.*?)",.*?"summary":"(.*?)","content":"(.*?)","cover"',
        text, re.S)
    content = text.group(4)
    html = etree.HTML(content)
    content = ''.join(html.xpath('//text()'))
    item['id'] = text.group(1)
    item['title'] = text.group(2)
    item['summary'] = text.group(3)
    item['content'] = content
    return item

def save(content):
    '''
    将数据保存在MongoDB
    :param content:
    :return:
    '''
    try:
        News.insert_one(content)
        # print('插入成功')
    except Exception as e:
        print(e)

def first_step(url):
    text = download(url)
    ids = parse_first(text)
    for id in ids:
        News_url = structure_url2(id)
        yield News_url

def main(url):
    News_urls = first_step(url)
    for News_url in News_urls:
        text = download(News_url)
        if text != None:
            print(News_url)
            item = parse_second(text)
            save(item)

if __name__ == '__main__':
    start = time.time()
    urls = structure_url1()
    pool = Pool()
    pool.map(main, urls)
    pool.close()
    pool.join()
    end = time.time()
    print('Total Spend Time: %s' % (end - start))