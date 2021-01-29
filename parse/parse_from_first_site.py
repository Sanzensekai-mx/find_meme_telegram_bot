import requests
from bs4 import BeautifulSoup
import sys
import re
import json
import os
from datetime import timedelta
import time
from utils.db_api.models import DBCommands

db = DBCommands()

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
    mem_name = list(obj_mem_title.text)
    for c in mem_name.copy():
        if c in '“”':
            mem_name.remove(c)
    mem_name = "".join(mem_name)
    try:
        parse_result.update({mem_name: {'pic_href': obj_mem_picture.img['src'],
                                        'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                                        if '\xa0' in obj_mem_describe.p.text
                                        else obj_mem_describe.p.text,
                                        'meme_href': url}})
    except AttributeError:
        obj_mem_picture = soup_mem.find('div', attrs={'class': 'bb-media-placeholder'})
        parse_result.update({mem_name: {'pic_href': obj_mem_picture.img['src'],
                                        'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                                        if '\xa0' in obj_mem_describe.p.text
                                        else obj_mem_describe.p.text,
                                        'meme_href': url}})
    return parse_result


with open('old_mem_dataset.json', 'w', encoding='utf-8') as old_meme, \
        open('mem_dataset.json', 'r', encoding='utf-8') as now_old_meme:
    current_old_memes = json.load(now_old_meme)
    json.dump(current_old_memes, old_meme, indent=4, ensure_ascii=False)

with open('mem_dataset.json', 'w', encoding='utf-8') as mem_data, \
        open('old_mem_dataset.json', 'r', encoding='utf-8') as old_mem_data:
    add_to_file = {}
    old_mem = json.load(old_mem_data)
    # i = 0
    for one_mem, mem_href in memes.items():
        # if i == 5:
        #     break
        one_mem = one_mem.replace('"', '')
        if one_mem in old_mem.keys():
            add_to_file.update({one_mem:
                                    {'pic_href': old_mem[one_mem]['pic_href'],
                                     'describe': old_mem[one_mem]['describe'],
                                     'meme_href': old_mem[one_mem]['meme_href']}})
            continue
        print(f'Парсится мем: {one_mem}')
        result_parse = parse_one_mem(mem_href)
        add_to_file.update(result_parse)
        # i += 1
    json.dump(add_to_file, mem_data, indent=4, ensure_ascii=False)
end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))
