import logging

from loader import dp
from aiogram.types import Message
from data.config import admins


@dp.message_handler(chat_id=admins, commands=['help_admin'])
async def admin_help(message: Message):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    text = [
        'Список команд: ',
        '/add_meme - добавление нового мема в датасет',
        '/cancel_meme - отмена добавления нового мема (можно импользовать на любом шаге добавления)',
        '/mail - текстовая рассылка всем пользователям',
        '/cancel_mail - отмена рассылки'
    ]
    await message.answer('\n'.join(text))
