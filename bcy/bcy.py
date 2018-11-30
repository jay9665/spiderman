
import requests
import re
import json
import os
from urllib.parse import urlencode
from multiprocessing import Pool

def get_page_index(count):
    data = {
      'p':count,
      'type':'week',
      'data':20181130
    }
    params = urlencode.(data)
    base_url = 'https://bcy.net/coser/index/ajaxloadtoppost?'
    url = base_url + params

def get_issue_url(response):
    title_url = response.xpath("//div[@id='content-box']//ul//li/a[@class='db posr ovf']/@href").extract()
    return title_url

def get_image_url(html):
    partten = re.compile('window.__ssr_data = JSON.parse\("(.*)"\);', re.S)
    result = re.search(partten, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'post_data' in data.keys():
            post_data = data.get('post_data')
            images = [item.get('original_path') for item in post_data]
            return images

def save_image(url):
    content = requests.get(url)
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
    with open(file_path, 'wb') as f:
        f.write(content)
        f.close()


def main(count):
    firt_floor_url = get_page_index(count)
    response = requests.get(firt_floor_url)
    title_url = get_issue_url(response)
    for url in title_url:
        print(url+'\n')
        html = requests.get(url).text
        images = get_image_url(html)
        for url in images:
            save_image(url)

if __name__ == '__main__':
    pool = Pool()
    groups = ([x for x in range(1, 7)])
    pool.map(main, ())
    pool.close()
    pool.join()
