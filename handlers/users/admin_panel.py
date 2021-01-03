import os
import json
from asyncio import sleep

from loader import dp, bot
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from data.config import admins
from states.main_states import AdminNewMeme, AdminMailing


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


@dp.message_handler(chat_id=admins, commands=['cancel'], state=AdminNewMeme)
async def cancel_add_meme(message: Message, state: FSMContext):
    await message.answer('Отмена добавления нового мема.')
    await state.reset_state()


@dp.message_handler(chat_id=admins, commands=['add_meme'])
async def add_meme(message: Message, state: FSMContext):
    await message.answer('Введите название нового мема или введите /cancel для отмены.')
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
                             '\nПришлите мне ССЫЛКУ на фото мема (не картинку и не документ) или введите /cancel для '
                             'отмены')

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
                             '\nПришлите мне описание мема, которое будет показываться в боте или введите /cancel для '
                             'отмены')
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
                             '\nПришлите мне ссылку на страницу мема на сайте или введите /cancel для отмены')
        await AdminNewMeme.Link.set()
    else:
        describe = message.text
        data['describe'] = describe
        await state.update_data(data)
        await confirm_or_change(data, message)


@dp.message_handler(chat_id=admins, state=AdminNewMeme.Link)
async def enter_meme_link(message: Message, state: FSMContext):
    data = await state.get_data()
    # if not data.get('meme_href'):
    link = message.text
    data['meme_href'] = link
    await state.update_data(data)
    await confirm_or_change(data, message)

# @dp.message_handler(chat_id=admins, state=AdminNewMeme.Confirm)
# async def confirm(message: Message, state: FSMContext):
#     data = await state.get_data()


@dp.callback_query_handler(text_contains='change', chat_id=admins, state=AdminNewMeme.Confirm)
async def change_some_data(call: CallbackQuery):
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


@dp.callback_query_handler(text_contains='сonfirm', chat_id=admins, state=AdminNewMeme.Confirm)
async def confirm_new_meme(call: CallbackQuery, state: FSMContext):
    data_from_state = await state.get_data()
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'w+', encoding='utf-8') \
            as data:
        meme_data = json.load(data)
        meme_data.update({data_from_state.get('name'): {
            'pic_href': data_from_state.get('pic_href'),
            'describe': data_from_state.get('describe'),
            'meme_href': data_from_state.get('meme_href')
        }})
        json.dump(meme_data, data, indent=4, ensure_ascii=False)
    await call.message.answer('Мем добавлен.')
    await state.finish()


@dp.message_handler(chat_id=admins, commands=["mail"])
async def mailing(message: Message):
    await message.answer("Пришлите текст рассылки")
    await AdminMailing.Text.set()


@dp.message_handler(chat_id=admins, state=AdminMailing.Text)
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
        except Exception:
            pass
    await message.answer("Рассылка выполнена.")
    await state.finish()
