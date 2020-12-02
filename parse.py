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


memes = {mem.text: mem['href']
         for mem in soup.find_all('a', attrs={'href': re.compile(r'https://memepedia.ru/[a-zA-Z-_]+/')})}
print(memes)

if __name__ == '__main__':
    while True:
        print('Запрос')
        user_input = input('--> ')
        if user_input == '':
            sys.exit()
        # regex = r"[\w\d\n#'\"]+{word}[\w\d\n#'\"]+" оказалось ненужным
        for word in user_input.split():
            print(dict(filter(lambda mem: word in mem, memes.keys())))
            # Норм спарсились мемы с другими ссылками со страницами, надо будет отфильтровать словарь с мемами
