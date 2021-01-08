import os
import json
import logging
from asyncio import sleep

from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.default import main_menu, cancel_or_confirm
from keyboards.inline import admin_mailing_kb
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType, \
    ReplyKeyboardRemove, InputMediaPhoto, InputMediaVideo
from data.config import admins
from states.main_states import AdminNewMeme, AdminMailing

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def confirm_or_change(data, mes):
    kb_confirm = InlineKeyboardMarkup(row_width=4)
    for key in data.keys():
        change_button = InlineKeyboardButton(f'Изменить {key}', callback_data=f'change:{key}')
        kb_confirm.add(change_button)
    kb_confirm.add(InlineKeyboardButton('Подтвердить', callback_data='сonfirm'))
    await mes.answer(f'''
Проверьте введенные данные.\n
Название - {data.get("name")}\n
Ссылка на картинку - {data.get("pic_href")}\n
Описание - {data.get("describe")}\n
Ссылка - {data.get("meme_href")}\n''', reply_markup=kb_confirm)
    await AdminNewMeme.Confirm.set()


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


@dp.message_handler(chat_id=admins, commands=['cancel_meme'], state=AdminNewMeme)
async def cancel_add_meme(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}, info: Отмена добавления нового мема.')
    await message.answer('Отмена добавления нового мема.', reply_markup=main_menu)
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=['cancel_mail'], state=AdminMailing)
async def cancel_mail(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}, info: Отмена рассылки.')
    await message.answer('Отмена рассылки.', reply_markup=main_menu)
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=['add_meme'])
async def add_meme(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    await message.answer('Введите название нового мема или введите /cancel_meme для отмены.',
                         reply_markup=ReplyKeyboardRemove())
    await AdminNewMeme.Name.set()
    await state.update_data(
        {'name': '',
         'pic_href': '',
         'describe': '',
         'meme_href': ''}
    )


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Name)
async def enter_meme_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('name'):
        name = message.text
        data['name'] = name
        await state.update_data(data)
        await message.answer(f'Название: {name}'
                             '\nПришлите мне ССЫЛКУ на фото мема (не картинку и не документ) или введите /cancel_meme '
                             'для отмены')

        await AdminNewMeme.Pic.set()
    else:
        name = message.text
        data['name'] = name
        await state.update_data(data)
        await confirm_or_change(data, message)


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Pic)
async def enter_meme_pic_link(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('pic_href'):
        pic = message.text
        data['pic_href'] = pic
        await state.update_data(data)
        await message.answer(f'Название: {data.get("name")}'
                             '\nПришлите мне описание мема, которое будет показываться в боте или введите /cancel_meme '
                             'для отмены')
        await AdminNewMeme.Describe.set()
    else:
        pic = message.text
        data['pic_href'] = pic
        await state.update_data(data)
        await confirm_or_change(data, message)


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Describe)
async def enter_meme_describe(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('describe'):
        describe = message.text
        data['describe'] = describe
        await state.update_data(data)
        await message.answer(f'Название: {data.get("name")}'
                             '\n(Опционально) Пришлите мне ссылку на страницу мема на сайте или введите /cancel_meme '
                             'для отмены')
        await AdminNewMeme.Link.set()
    else:
        describe = message.text
        data['describe'] = describe
        await state.update_data(data)
        await confirm_or_change(data, message)


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Link)
async def enter_meme_link(message: Message, state: FSMContext):
    data = await state.get_data()
    link = message.text
    data['meme_href'] = link
    await state.update_data(data)
    await confirm_or_change(data, message)


@dp.callback_query_handler(text_contains='change', chat_id=admins, state=AdminNewMeme.Confirm)
async def change_some_data(call: CallbackQuery):
    await call.answer(cache_time=60)
    what_to_change = call.data.split(':')[1]
    if what_to_change == 'name':
        await call.message.answer('Введите новое имя мема')
        await AdminNewMeme.Name.set()
    elif what_to_change == 'pic_href':
        await call.message.answer('Пришлите новую ссылку на картинку')
        await AdminNewMeme.Pic.set()
    elif what_to_change == 'describe':
        await call.message.answer('Пришлите новое описание мема')
        await AdminNewMeme.Describe.set()
    elif what_to_change == 'meme_href':
        await call.message.answer('Пришлите ссылку на страницу мема')
        await AdminNewMeme.Link.set()


@dp.callback_query_handler(text_contains='сonfirm', chat_id=admins, state=AdminNewMeme.Confirm)
async def confirm_new_meme(call: CallbackQuery, state: FSMContext):
    data_from_state = await state.get_data()
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as data_r:
        meme_data = json.load(data_r)
    meme_data.update({data_from_state.get('name'): {
        'pic_href': data_from_state.get('pic_href'),
        'describe': data_from_state.get('describe'),
        'meme_href': data_from_state.get('meme_href')
    }})
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'w', encoding='utf-8') \
            as data_w:
        json.dump(meme_data, data_w, indent=4, ensure_ascii=False)
    await call.message.answer('Мем добавлен.', reply_markup=main_menu)
    await state.finish()


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
                                  reply_markup=cancel_or_confirm)
    # elif what_to_send == 'audio':
    #     await AdminMailing.Audio.set()
    #     await call.message.answer('Пришлите аудиозапись. За раз можно отправить только одну.')
    # elif what_to_send == 'doc':
    #     await AdminMailing.Documents.set()
    #     await call.message.answer('Пришлите документ. За раз можно отправить только один.')
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


@dp.message_handler(chat_id=admins, state=AdminMailing.Media, content_types=[ContentType.PHOTO, ContentType.VIDEO,
                                                                             ContentType.VIDEO_NOTE])
async def send_group_photo(message: Message, state: FSMContext):
    data_from_state = await state.get_data()
    if data_from_state.get('media_file_id') is None:
        await state.update_data({'media_file_id': []})
    else:
        print(data_from_state.get('media_file_id'))
    if message.photo or message.video:
        await process_media_send(message, state)
    elif message.text == 'Отмена':
        await state.finish()
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


# @dp.message_handler(chat_id=admins, state=AdminMailing.Audio, content_types=[ContentType.AUDIO])
# async def send_audio(message: Message, state: FSMContext):
#     with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
#         users_data = json.load(user_r)
#         users_chat_id = [user.get('chat_id') for user in users_data.values()]
#     for user_chat_id in users_chat_id:
#         try:
#             await bot.send_audio(chat_id=user_chat_id, audio=message.audio.file_id, caption=message.caption)
#             await sleep(0.3)
#         except Exception as e:
#             print(e)
#     await message.answer("Рассылка выполнена.", reply_markup=main_menu)
#     await state.finish()


# @dp.message_handler(chat_id=admins, state=AdminMailing.Documents, content_types=[ContentType.DOCUMENT])
# async def send_doc(message: Message, state: FSMContext):
#     # print(message.as_json())
#     with open(os.path.join(os.getcwd(), 'data', 'user_info.json'), 'r', encoding='utf-8') as user_r:
#         users_data = json.load(user_r)
#         users_chat_id = [user.get('chat_id') for user in users_data.values()]
#     for user_chat_id in users_chat_id:
#         try:
#             await bot.send_document(chat_id=user_chat_id, document=message.document.file_id, caption=message.caption)
#             await sleep(0.3)
#         except Exception as e:
#             print(e)
#     await message.answer("Рассылка выполнена.", reply_markup=main_menu)
#     await state.finish()


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
