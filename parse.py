import requests
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup
import sys
import re

# Если возвращается 403 error
# from fake_useragent import UserAgent
#     UserAgent().chrome
# response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})

page_link = 'https://memepedia.ru/all-memes/#.'
response = requests.get(page_link)

print(response)
# for key, value in response.request.headers.items():
#     print(key+": "+value)

html = response.content
# print(html[:1000])

soup = BeautifulSoup(html, 'html.parser')

# print(soup.html.head.title.text)
alphabet = [letter.text for letter in soup.find_all('a', attrs={'class': 'letter-nav'})
            if letter.text.isdigit() is True or letter.text.isalpha() is True]
# print(alphabet)
# команда должна найти элемент, который лежит внутри тега 'a' и имеет класс photo
# obj = soup.find('a', attrs={'class': 'photo'})
# obj = soup.find(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# obj = soup.find('li', attrs={'id': 'А'})
# print(obj)


memes_not_clear = {mem.text: mem['href']
                   for mem in soup.find_all('a', attrs={'href': re.compile(r'https://memepedia.ru/[a-zA-Z-_]+/')})}
memes = {}
clear_mem_list = [item[0] for item in list(memes_not_clear.items())[11:-2]]
for k in memes_not_clear.copy().keys():  # Цикл по итогу отфильтрует словарь мемов и создаст новый чистый словарь мемов
    if k not in clear_mem_list:
        continue
    memes[k] = memes_not_clear[k]
# print(memes)


def parse_one_mem(url):     # делаем парс парс по странице конкретного мема
    parse_result = {}
    response_mem = requests.get(url)
    html_mem = response_mem.content
    soup_mem = BeautifulSoup(html_mem, 'html.parser')
    obj_mem_picture = soup_mem.find('figure', attrs={'class': 's-post-media-img post-thumbnail post-media-b'})
    obj_mem_title = soup_mem.find('h1', attrs={'class': 'entry-title s-post-title bb-mb-el'})
    obj_mem_describe = soup_mem.find('div', attrs={'class':
                                                       'js-mediator-article s-post-content s-post-small-el bb-mb-el',
                                                   'itemprop':
                                                       'articleBody'})
    try:
        parse_result.update({obj_mem_title.text: {'picture_sourse': obj_mem_picture.img['src'],
                                                    'mem_describe': obj_mem_describe.p.text}})
    except AttributeError:
        parse_result.update({obj_mem_title.text: {'picture_sourse': None,
                                                  'mem_describe': obj_mem_describe.p.text}})
    return parse_result


if __name__ == '__main__':
    while True:
        print('Запрос')
        user_input = input('--> ')
        if user_input == '':
            sys.exit()
        # regex = r"[\w\d\n#'\"]+{word}[\w\d\n#'\"]+" оказалось ненужным
        print('Результаты запроса: ')
        result = set()
        for word in user_input.split():
            result_match_one_word = set()
            result_match_one_word.update(set(list(filter(lambda mem: word.lower() in mem, memes))))
            result_match_one_word.update(set(list(filter(lambda mem: word.title() in mem, memes))))
            result.update(result_match_one_word)
            # Норм спарсились мемы с другими ссылками со страницами, надо будет отфильтровать словарь с мемами
        if result:
            dict_of_result_request = {}
            while True:
                for num, res in enumerate(result, 1):
                    print(f'{num}. {res} - {memes[res]}')
                    dict_of_result_request.update({num: [res, memes[res]]})
                print('')
                user_choise = input('--> ')
                if user_choise == '':
                    sys.exit()
                try:
                    print(dict_of_result_request[int(user_choise)][1])
                except KeyError:
                    print('Выбери цифру из результатов!!!!!!!!!!!!!!!!!')
                    continue
                break
            print(parse_one_mem(dict_of_result_request[int(user_choise)][1]))

