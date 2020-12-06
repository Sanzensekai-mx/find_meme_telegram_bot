import requests
from bs4 import BeautifulSoup
import sys
import re
import json
import os
from datetime import timedelta
import time

start_time = time.monotonic()
page_link = 'https://memepedia.ru/all-memes/#.'
response = requests.get(page_link)
# print(response)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
memes_not_clear = {mem.text: mem['href']
                   for mem in soup.find_all('a', attrs={'href': re.compile(r'https://memepedia.ru/[a-zA-Z-_]+/')})}
memes = {}
clear_mem_list = [item[0] for item in list(memes_not_clear.items())[11:-2]]
for k in memes_not_clear.copy().keys():  # Цикл по итогу отфильтрует словарь мемов и создаст новый чистый словарь мемов
    if k not in clear_mem_list:
        continue
    memes[k] = memes_not_clear[k]


# print(memes)


def parse_one_mem(url):  # делаем парс парс по странице конкретного мема
    parse_result = {}
    response_mem = requests.get(url)
    html_mem = response_mem.content
    soup_mem = BeautifulSoup(html_mem, 'html.parser')
    obj_mem_picture = soup_mem.find('figure', attrs={
        'class': 's-post-media-img post-thumbnail post-media-b'})
    obj_mem_title = soup_mem.find('h1', attrs={'class': 'entry-title s-post-title bb-mb-el'})
    obj_mem_describe = soup_mem.find('div', attrs={'class':
                                                       'js-mediator-article s-post-content s-post-small-el bb-mb-el',
                                                   'itemprop':
                                                       'articleBody'})
    try:
        parse_result.update({obj_mem_title.text: {'pic_href': obj_mem_picture.img['src'],
                                                  'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                                                  if '\xa0' in obj_mem_describe.p.text
                                                  else obj_mem_describe.p.text}})
    except AttributeError:
        obj_mem_picture = soup_mem.find('div', attrs={'class': 'bb-media-placeholder'})
        parse_result.update({obj_mem_title.text: {'pic_href': obj_mem_picture.img['src'],
                                                  'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                                                  if '\xa0' in obj_mem_describe.p.text
                                                  else obj_mem_describe.p.text}})
    return parse_result


with open('mem_dataset.json', 'w', encoding='utf-8') as mem_data:
    add_to_file = {}
    for one_mem, mem_href in memes.items():
        print(f'Парсится мем: {one_mem}')
        result_parse = parse_one_mem(mem_href)
        add_to_file.update(result_parse)
    json.dump(add_to_file, mem_data, indent=4, ensure_ascii=False)
end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))