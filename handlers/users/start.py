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
    # await log_user(message)
    user = await db.add_new_user()
    chat_id = user.user_id
    id_user = user.id
    name_user = user.full_name
    count_users = await db.count_users()
    logging.info(f'Пользователь прописал команду /start: Name: {name_user}, id: {id_user}, chat_id: {chat_id}')
    if str(chat_id) in admins:
        await message.answer(f'''
Привет, {name_user}!
У тебя права администратора! Введи /help_admin
В боте {count_users} юзера.
        ''')
    else:
        await message.answer(f'''
Привет, {name_user}!
Этот бот поможет тебе найти пояснение к мему!
''')
    await message.answer('Нажми кнопку ниже для того, чтобы начать!', reply_markup=main_menu)
