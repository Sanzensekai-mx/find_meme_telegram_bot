import logging

from loader import dp
from aiogram.types import Message
from data.config import admins


@dp.message_handler(chat_id=admins, commands=['help_admin'])
async def admin_help(message: Message):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    text = [
        'Список команд администратора: ',
        '/add_meme - добавление нового мема в БД',
        '/cancel_meme - отмена добавления нового мема '
        '\n(можно импользовать на любом шаге добавления)',
        '/del_meme - удаление мема из БД.',
        '/cancel_del_meme - отмена удаления мема.',
        '/mail - рассылка всем пользователям бота.',
        '/cancel_mail - отмена рассылки.',
        '/update_memes - обновление мемов с сайта memepedia.ru'
    ]
    await message.answer('\n'.join(text))
