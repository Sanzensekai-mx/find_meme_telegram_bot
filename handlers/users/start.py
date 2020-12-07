from aiogram import types
from keyboards.default import search
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'''
Привет, {message.from_user.full_name}!
Этот бот поможет тебе найти пояснение к мему!
''')
    await message.answer('Нажми кнопку ниже для того, чтобы начать!', reply_markup=search)