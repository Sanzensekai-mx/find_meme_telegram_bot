import os
import json
from aiogram.utils.exceptions import BadRequest
from .ten_random_memes import process_random_memes
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.users.search import result_mem_search_by_page, keyboards, all_result_messages, global_page
from states.search_states import Search
from loader import dp, bot


async def open_choice_meme(current_call, meme_data, meme_id):
    try:
        detailed_inline_kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Подробнее',
                                 url=meme_data[result_mem_search_by_page[global_page.value][meme_id]]
                                 ['meme_href']
                                 ))
    except BadRequest:
        await current_call.message.answer('Страница мема в интернете не найдена.')
        # detailed_inline_kb = InlineKeyboardMarkup().add(
        #     InlineKeyboardButton('Страница мема не найдена'))
    try:
        await bot.send_photo(
            chat_id=current_call.from_user.id,
            photo=meme_data[result_mem_search_by_page[global_page.value][meme_id]]
            ['pic_href'])
    except BadRequest:
        await current_call.message.answer('Картинка не найдена.')
    try:
        await current_call.message.answer(
            meme_data[result_mem_search_by_page[global_page.value][meme_id]]
            ['describe'])
    except BadRequest:
        await current_call.message.answer('Описание мема не найдено.')
    try:
        # Добавить вывод названия сайта по записи в json?
        await current_call.message.answer('Нажми кнопку, чтобы открыть странцу мема в источнике на memepedia.ru', reply_markup=detailed_inline_kb)
    except Exception as e:
        print(e)
        await current_call.message.answer('Мем не имеет страницы в интернете')


async def action_process_callback(call):
    await call.answer(cache_time=60)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        data = json.load(dataset)
        cur_id = call.data.split(':')[1]
        await open_choice_meme(current_call=call, meme_data=data, meme_id=cur_id)


# search
@dp.callback_query_handler(text_contains='res',
                           state=Search.search_input_key_words)
async def process_callback_res_num_button(callback: CallbackQuery):
    await action_process_callback(callback)


# ten random memes
@dp.callback_query_handler(text_contains='res', state=Search.ten_random_memes)
async def process_callback_res_num_button(callback: CallbackQuery):
    await action_process_callback(callback)


# search
# Этот хэндлер должен как то еще выводить результат поиска
@dp.callback_query_handler(text_contains='page', state=Search.search_input_key_words)
async def process_callback_page_button(callback: CallbackQuery):
    await callback.answer(cache_time=60)
    if callback.data == 'next_page':
        global_page.next_page()
        await callback.message.answer(all_result_messages[global_page.value],
                                      reply_markup=keyboards[global_page.value])
    elif callback.data == 'previous_page':
        global_page.previous_page()
        await callback.message.answer(all_result_messages[global_page.value],
                                      reply_markup=keyboards[global_page.value])


# ten random memes
@dp.callback_query_handler(text_contains='new_random', state=Search.ten_random_memes)
async def process_callback_new_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=60)
    await state.finish()
    await process_random_memes(call=callback)
