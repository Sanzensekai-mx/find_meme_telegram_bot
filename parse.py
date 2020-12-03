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
# команда должна найти элемент, который лежит внутри тега a и имеет класс photo
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
print(memes)

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
            result_match_one_word.update(set(list(filter(lambda mem: word in mem, memes))))
            result_match_one_word.update(set(list(filter(lambda mem: word.title() in mem, memes))))
            result.update(result_match_one_word)
            # Норм спарсились мемы с другими ссылками со страницами, надо будет отфильтровать словарь с мемами
        for num, res in enumerate(result, 1):
            print(f'{num}. {res} - {memes[res]}')
