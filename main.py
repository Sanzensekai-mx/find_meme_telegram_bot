import requests
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup

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
print(soup.html.head.title.text)
# команда должна найти элемент, который лежит внутри тега a и имеет класс photo
# obj = soup.find('a', attrs={'class': 'photo'})
# obj = soup.find(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
obj = soup.find('li', attrs={'id': 'А'})
print(obj)
