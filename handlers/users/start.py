import os
import json
import logging
from aiogram import types
from keyboards.default import main_menu
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove
from states.main_states import UserStates
from loader import dp
from aiogram.dispatcher import FSMContext
from utils.db_api.models import DBCommands
from data.config import admins

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

db = DBCommands()

# async def log_user(mes):
    # with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
    #     user_data = {} if os.stat(os.path.join(os.getcwd(), 'data', 'user_info.json')).st_size == 0 \
    #         else json.load(user_r)
    # logging.info(f'Новый пользователь: {mes.chat.full_name}') if mes.chat.full_name not in user_data.keys() \
    #     else logging.info(f'Команда /start была написана пользователем {mes.chat.full_name}')
    # user_data.update({f'{mes.chat.full_name}': {
    #     'chat_id': mes.chat.id,
    #     'username': mes.chat.username,
    # }})
    # with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'w', encoding='utf-8') as user_w:
    #     json.dump(user_data, user_w, indent=4, ensure_ascii=False)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.get_user(message.chat.id)
    if user is None:    # Если пользователя нет в БД
        logging.info(f'Новый пользователь (/start): Name: {message.chat.full_name}, '
                     f'chat_id: {message.chat.id}')
        user = await db.add_new_user()
    else:
        id_user = user.id
        logging.info(f'Зарегистрированный пользователь (/start): id: {id_user}, Name: {message.chat.full_name}, '
                     f'chat_id: {message.chat.id}')
    chat_id = user.user_id
    name_user = user.full_name
    count_users = await db.count_users()
    count_memes = await db.count_memes()
    if str(chat_id) in admins:
        await message.answer(f'''
Привет, {name_user}!
У тебя права администратора! Введи /help_admin
Пользователей в БД: {count_users} юзер(а).
Мемов в БД: {count_memes} мем(а).
        ''')
    else:
        await message.answer(f'''
Привет, {name_user}!
Этот бот поможет тебе найти пояснение к мему!
Сейчас в боте {count_memes} мем(а).
''')
    await message.answer('Нажми кнопку ниже для того, чтобы начать!', reply_markup=main_menu)
