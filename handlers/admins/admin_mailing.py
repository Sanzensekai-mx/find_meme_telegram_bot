import os
import json
import logging
from asyncio import sleep

from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.default import main_menu, admin_cancel_or_confirm
from keyboards.inline import admin_mailing_kb
from aiogram.types import Message, CallbackQuery, ContentType, \
    ReplyKeyboardRemove, InputMediaPhoto, InputMediaVideo
from data.config import admins
from states.main_states import AdminMailing

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


@dp.message_handler(chat_id=admins, commands=['cancel_mail'], state=AdminMailing)
async def cancel_mail(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}, info: Отмена рассылки.')
    await message.answer('Отмена рассылки.', reply_markup=main_menu)
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=["mail"])
async def mailing(message: Message):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    await message.answer("Выберите тип рассылки из меню. /cancel_mail для отмены", reply_markup=ReplyKeyboardRemove())
    await message.answer("Отправить:", reply_markup=admin_mailing_kb)
    await AdminMailing.MailingMenu.set()


@dp.callback_query_handler(text_contains='send', chat_id=admins, state=AdminMailing.MailingMenu)
async def process_callback_data_mailing(call: CallbackQuery):
    await call.answer(cache_time=60)
    what_to_send = call.data.split('_')[1]
    if what_to_send == 'media':
        await AdminMailing.Media.set()
        await call.message.answer('Пришлите нужное количество фото/видео по одной штуке для отправки пользователям '
                                  'группы. Нужную подпись можно будет добавить к одному присланному медиа. Если к '
                                  'нескольким файлам добавить надпись, то её вообще не будет.',
                                  reply_markup=admin_cancel_or_confirm)
    elif what_to_send == 'another':
        await AdminMailing.AnotherMedia.set()
        await call.message.answer('Пришлите документ, аудио или анимацию. За раз можно отправить только один объект.')
    elif what_to_send == 'text':
        await AdminMailing.Text.set()
        await call.message.answer('Напишите текст для отправки.')


async def process_media_send(msg, state):
    data_from_state = await state.get_data()
    if msg.photo:
        data_from_state.get('media_file_id').append(InputMediaPhoto(msg.photo[-1].file_id, caption=msg.caption))
    elif msg.video:
        # print(mes.video)
        data_from_state.get('media_file_id').append(InputMediaVideo(msg.video.file_id, caption=msg.caption))
    await state.update_data(data_from_state)
    await state.reset_state(with_data=False)
    await AdminMailing.Media.set()


@dp.message_handler(chat_id=admins, state=AdminMailing.Media, content_types=[ContentType.PHOTO,
                                                                             ContentType.VIDEO,
                                                                             ContentType.TEXT])
async def send_group_photo(message: Message, state: FSMContext):
    logging.info(message.text)
    data_from_state = await state.get_data()
    if data_from_state.get('media_file_id') is None:
        await state.update_data({'media_file_id': []})
    else:
        print(data_from_state.get('media_file_id'))
    if message.photo or message.video:
        await process_media_send(message, state)
    # elif message.text == 'Отмена':
    #       await message.answer('Отменено.', reply_markup=main_menu)
    #       await state.reset_state()
    elif message.text == 'Подтвердить':
        with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
            users_data = json.load(user_r)
            users_chat_id = [user.get('chat_id') for user in users_data.values()]
            for user_chat_id in users_chat_id:
                try:
                    await bot.send_media_group(chat_id=user_chat_id, media=data_from_state.get('media_file_id'))
                    await sleep(0.3)
                except Exception as e:
                    print(e)
        await message.answer("Рассылка выполнена.", reply_markup=main_menu)
        await state.finish()


@dp.message_handler(chat_id=admins, state=AdminMailing.AnotherMedia, content_types=[ContentType.DOCUMENT,
                                                                                    ContentType.AUDIO,
                                                                                    ContentType.ANIMATION])
async def send_another(message: Message, state: FSMContext):
    type_dict = ['audio', 'document', 'animation']
    type_from_msg = [k for k in message.values.keys() if k in type_dict][0]
    with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
        users_data = json.load(user_r)
        users_chat_id = [user.get('chat_id') for user in users_data.values()]
    type_msg_dict = {}
    if type_from_msg == 'document':
        type_msg_dict['document'] = bot.send_document
        type_msg_dict['file_id'] = message.document.file_id
    elif type_from_msg == 'audio':
        type_msg_dict['audio'] = bot.send_audio
        type_msg_dict['file_id'] = message.audio.file_id
    elif type_from_msg == 'animation':
        type_msg_dict['animation'] = bot.send_animation
        type_msg_dict['file_id'] = message.animation.file_id
    for user_chat_id in users_chat_id:
        try:
            await type_msg_dict[type_from_msg](user_chat_id, type_msg_dict['file_id'], caption=message.caption)
            await sleep(0.3)
        except Exception as e:
            print(e)
    await message.answer("Рассылка выполнена.", reply_markup=main_menu)
    await state.finish()


@dp.message_handler(chat_id=admins, state=AdminMailing.Text, content_types=ContentType.TEXT)
async def send_everyone(message: Message, state: FSMContext):
    text = message.text
    with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
        users_data = json.load(user_r)
        users_chat_id = [user.get('chat_id') for user in users_data.values()]
    for user_chat_id in users_chat_id:
        try:
            await bot.send_message(chat_id=user_chat_id,
                                   text=text)
            await sleep(0.3)
        except Exception as e:
            print(e)
    await message.answer("Рассылка выполнена.", reply_markup=main_menu)
    await state.finish()