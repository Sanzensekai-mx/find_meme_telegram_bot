import logging

from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.default import main_menu, admin_cancel_del_meme
from aiogram.types import Message
from data.config import admins
from states.main_states import AdminDelMeme
from utils.db_api.models import DBCommands

db = DBCommands()


@dp.message_handler(chat_id=admins, commands=['cancel_del_meme'], state=AdminDelMeme)
async def cancel_del_meme(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}, info: Отмена добавления нового мема.')
    await message.answer('Отмена удаления мема.', reply_markup=main_menu)
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=['del_meme'])
async def start_del_meme(message: Message):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    await message.answer('Введите точное имя мема для удаления из БД.'
                         '\nИли /cancel_del_meme для отмены удаления.', reply_markup=admin_cancel_del_meme)
    await AdminDelMeme.Del.set()


@dp.message_handler(chat_id=admins, state=AdminDelMeme.Del)
async def enter_del_meme_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if await db.get_meme(name):
        await db.del_meme(name)
        await message.answer(f'Мем "{name}" был удален.', reply_markup=main_menu)
        await state.finish()
    else:
        await message.answer(f'Мема "{name}" нет в БД.'
                             '\nПопробуйте ввести еще раз.'
                             '\nИли /cancel_del_meme для отмены удаления.', reply_markup=main_menu)
