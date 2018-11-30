import json
import os
import pymongo
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from multiprocessing import Pool
from hashlib import md5
from  json.decoder import JSONDecodeError
from config import *

client pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'autoload':'true',
        'count':20,
        'cur_tab':3,
        'format':'json',
        'keyword':keyword,
        'offset':offset

    }
    params = urlencode(data)
    base = 'http://www.toutiao.com/search_content/'
    url = base + '?' +params
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None

def download_image(url):
    print('Downloading...... ', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def parse_page_index(text):
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('title')
    title = result[0].get_text if result else ''
    images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }
