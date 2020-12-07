from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'''
Привет, {message.from_user.full_name}!
Этот бот поможет тебе найти пояснение к мему!
''')
    await message.answer()

# @dp.message_handler(Text)
