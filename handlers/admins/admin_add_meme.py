import os
import json
import logging

from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.default import main_menu, admin_cancel_add_meme
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from data.config import admins
from states.main_states import AdminNewMeme
from utils.db_api.models import DBCommands

db = DBCommands()


async def confirm_or_change(data, mes):
    kb_confirm = InlineKeyboardMarkup(row_width=4)
    for key in data.keys():
        if key == 'is_meme_in_db':
            break
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


@dp.message_handler(chat_id=admins, commands=['cancel_meme'], state=AdminNewMeme)
async def cancel_add_meme(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}, info: Отмена добавления нового мема.')
    await message.answer('Отмена добавления нового мема.', reply_markup=main_menu)
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=['add_meme'])
async def add_meme(message: Message, state: FSMContext):
    logging.info(f'from: {message.chat.full_name}, text: {message.text}')
    await message.answer('Введите название нового мема или мема, который уже существует в БД, '
                         'но его данные необходимо обновить. '
                         'Введите /cancel_meme для отмены.',
                         reply_markup=admin_cancel_add_meme)
    await AdminNewMeme.Name.set()
    await state.update_data(
        {'name': '',
         'pic_href': '',
         'describe': '',
         'meme_href': '',
         'is_meme_in_db': ''}
    )


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Name)
async def enter_meme_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('name'):
        name = message.text.strip()
        data['name'] = name
        data['is_meme_in_db'] = 'Мем уже существует в БД.' if await db.is_this_meme_in_db(name) \
            else 'Такого мема нет в БД.'
        is_meme_in_db = data.get('is_meme_in_db')
        await state.update_data(data)
        await message.answer(f'Название: "{name}". '
                             f'\n{is_meme_in_db}'
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
        await message.answer(f'Название: "{data.get("name")}". '
                             f'\n{data.get("is_meme_in_db")}'
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
        await message.answer(f'Название: "{data.get("name")}". '
                             f'\n{data.get("is_meme_in_db")}'
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
    # with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
    #         as data_r:
    #     meme_data = json.load(data_r)
    # meme_data.update({data_from_state.get('name'): {
    #     'pic_href': data_from_state.get('pic_href'),
    #     'describe': data_from_state.get('describe'),
    #     'meme_href': data_from_state.get('meme_href')
    # }})
    # with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'w', encoding='utf-8') \
    #         as data_w:
    #     json.dump(meme_data, data_w, indent=4, ensure_ascii=False)
    await db.add_meme(
        meme_name=data_from_state.get('name'),
        meme_href=data_from_state.get('meme_href'),
        meme_describe=data_from_state.get('describe'),
        meme_photo_href=data_from_state.get('pic_href')
    )
    await call.message.answer('Мем добавлен.', reply_markup=main_menu)
    await state.finish()
