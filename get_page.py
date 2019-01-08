# Author : ZhangTong
import requests
import math

def download():
    url = 'https://36kr.com/api/search-column/mainsite?per_page=20&page=2&_=1546955215494'
    headers = {
        'Host': '36kr.com',
        'Referer': 'https://36kr.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'UTF-8'
            return response.json()
    except Exception as e:
        print(e)

def parse(js):
    total_count = js['data']['total_count']
    page = math.ceil(total_count / 20)
    return page

page = parse(download())