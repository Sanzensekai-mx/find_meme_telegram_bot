import logging
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from loader import dp
from keyboards.default import main_menu
from utils.db_api.models import DBCommands
from data.config import admins

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] '
                           u'#%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.get_user(message.chat.id)
    if user is None:    # Если пользователя нет в БД
        logging.info(f'Новый пользователь (/start): Name: {message.chat.full_name}, '
                     f'chat_id: {message.chat.id}')
        user = await db.add_new_user()
    else:
        id_user = user.id
        logging.info(f'Зарегистрированный пользователь (/start): id: {id_user}, '
                     f'Name: {message.chat.full_name}, '
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
