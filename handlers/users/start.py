import os
import json
from aiogram import types
from keyboards.default import main_menu
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove
from states.main_states import UserStates
from loader import dp
from aiogram.dispatcher import FSMContext


async def log_user(mes):
    with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
        user_data = {} if os.stat(os.path.join(os.getcwd(), 'data', 'user_info.json')).st_size == 0 \
            else json.load(user_r)
    print(f'Новый пользователь: {mes.chat.full_name}') if mes.chat.full_name in user_data.keys() \
        else print(f'Команда /start была написана пользователем {mes.chat.full_name}')
    user_data.update({f'{mes.chat.full_name}': {
        'chat_id': mes.chat.id,
        'username': mes.chat.username,
    }})
    with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'w', encoding='utf-8') as user_w:
        json.dump(user_data, user_w, indent=4, ensure_ascii=False)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await log_user(message)
    await message.answer(f'''
Привет, {message.from_user.full_name}!
Этот бот поможет тебе найти пояснение к мему!
''')
    await message.answer('Нажми кнопку ниже для того, чтобы начать!', reply_markup=main_menu)
