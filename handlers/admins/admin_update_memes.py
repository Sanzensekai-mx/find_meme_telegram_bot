import re
import time
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from aiogram.types import Message
from loader import dp
from data.config import admins
from utils.db_api.models import DBCommands

db = DBCommands()


async def parse_one_mem(url):  # делаем парс парс по странице конкретного мема
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
        parse_result.update({'meme_name': obj_mem_title.text,
                             'pic_href': obj_mem_picture.img['src'],
                             'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                             if '\xa0' in obj_mem_describe.p.text
                             else obj_mem_describe.p.text,
                             'meme_href': url})
    except AttributeError:
        obj_mem_picture = soup_mem.find('div', attrs={'class': 'bb-media-placeholder'})
        parse_result.update({'meme_name': obj_mem_title.text,
                             'pic_href': obj_mem_picture.img['src'],
                             'describe': obj_mem_describe.p.text.replace('\xa0', ' ')
                             if '\xa0' in obj_mem_describe.p.text
                             else obj_mem_describe.p.text,
                             'meme_href': url})
    return parse_result


@dp.message_handler(chat_id=admins, commands=['update_memes'])
async def start_update(message: Message):
    await message.answer('Начинается обновление базы данных мемов...')
    start_time = time.monotonic()
    page_link = 'https://memepedia.ru/all-memes/#.'
    response = requests.get(page_link)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    memes_not_clear = {meme.text: meme['href']
                       for meme in soup.find_all('a',
                                                 attrs={'href': re.compile(r'https://memepedia.ru/[a-zA-Z-_]+/'
                                                                           )})
                       }
    change_db_1, change_db_2, change_db_3, change_db_4 = re.compile(r'“|”'), re.compile(r'–'), \
                                                         re.compile(r'‘|’'), re.compile(r'…')
    # Преобразование clear_mem_list
    clear_mem_list = [change_db_1.sub('\"', item[0])
                      for item in list(memes_not_clear.items())[11:-2]]
    clear_mem_list = [change_db_2.sub('\'', item) for item in clear_mem_list]
    clear_mem_list = [change_db_3.sub('\'', item) for item in clear_mem_list]
    clear_mem_list = [change_db_4.sub('\'', item) for item in clear_mem_list]
    # Преобразование memes_from_db
    memes_from_db = [change_db_1.sub('\"', meme.meme_name) for meme in await db.all_meme()]
    memes_from_db = [change_db_2.sub('-', meme) for meme in memes_from_db]
    memes_from_db = [change_db_3.sub('\'', meme) for meme in memes_from_db]
    memes_from_db = [change_db_4.sub('...', meme) for meme in memes_from_db]
    memes_to_add = {}
    for meme in clear_mem_list:
        if meme in memes_from_db:
            continue
        print(meme)
        memes_to_add[meme] = memes_not_clear[meme]
    await message.answer(f'Мемов для добавления {len(memes_to_add)}.')
    if len(memes_to_add) == 0:
        await message.answer('На сайте нет мемов для обновления.')
    else:
        for meme_name, meme_href in memes_to_add.items():
            one_meme = await parse_one_mem(meme_href)
            await db.add_meme(meme_name=one_meme.get('meme_name'),
                              meme_href=one_meme.get('meme_href'),
                              meme_describe=one_meme.get('describe'),
                              meme_photo_href=one_meme.get('pic_href'))
        end_time = time.monotonic()
        await message.answer('Обновление базы данных мемов завершено.')
        await message.answer(f'Времени прошло: {str(timedelta(seconds=end_time - start_time))}.')
