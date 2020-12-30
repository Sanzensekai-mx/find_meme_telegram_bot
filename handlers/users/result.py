import os
import json
from aiogram.utils.exceptions import BadRequest
from .ten_random_memes import process_random_memes
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from handlers.users.search import result_mem_search_by_page, keyboards, all_result_messages, global_page
from states.search_states import Search
from loader import dp, bot


async def open_choice_meme(current_call, meme_data, meme_id, state):
    state_data = await state.get_data()
    try:
        detailed_inline_kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Подробнее',
                                 url=meme_data[state_data.get('result_mem_search_by_page')[state_data.get('page')]
                                 [meme_id]]
                                 ['meme_href']
                                 ))
    # Придумать другую заглушку?
    except BadRequest:
        await current_call.message.answer('Ссылки на страницу мема нет в базе.')
        # detailed_inline_kb = InlineKeyboardMarkup().add(
        # InlineKeyboardButton('Недоступно'))
    try:
        await bot.send_photo(
            chat_id=current_call.from_user.id,
            photo=meme_data[state_data.get('result_mem_search_by_page')[state_data.get('page')][meme_id]]
            ['pic_href'])
    except BadRequest:
        await current_call.message.answer('Картинка не найдена.')
    try:
        await current_call.message.answer(
            meme_data[state_data.get('result_mem_search_by_page')[state_data.get('page')][meme_id]]
            ['describe'])
    except BadRequest:
        await current_call.message.answer('Описание мема не найдено.')
    try:
        # Добавить вывод названия сайта по записи в json?
        await current_call.message.answer('Нажми кнопку, чтобы открыть странцу мема в источнике на memepedia.ru',
                                          reply_markup=detailed_inline_kb)
    except Exception as e:
        print(e)
        await current_call.message.answer('Ссылки на страницу мема нет в базе.')


async def action_process_callback(call, state):
    await call.answer(cache_time=60)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        data = json.load(dataset)
        cur_id = call.data.split(':')[1]
        await open_choice_meme(current_call=call, meme_data=data, meme_id=cur_id, state=state)


# search
@dp.callback_query_handler(text_contains='res',
                           state=Search.search_input_key_words)
async def process_callback_res_num_button(callback: CallbackQuery, state: FSMContext):
    await action_process_callback(call=callback, state=state)


# ten random memes
@dp.callback_query_handler(text_contains='res', state=Search.ten_random_memes)
async def process_callback_res_num_button(callback: CallbackQuery, state: FSMContext):
    await action_process_callback(call=callback, state=state)


# search
# Этот хэндлер должен как то еще выводить результат поиска
@dp.callback_query_handler(text_contains='page', state=Search.search_input_key_words)
async def process_callback_page_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=60)
    if callback.data == 'next_page':
        async with state.proxy() as data_from_state:
            data_from_state['page'] += 1
        data_from_state = await state.get_data()
        await callback.message.answer(data_from_state.get('all_result_messages')[data_from_state.get('page')],
                                      reply_markup=data_from_state.get('keyboards')[data_from_state.get('page')])
    elif callback.data == 'previous_page':
        async with state.proxy() as data_from_state:
            data_from_state['page'] -= 1
        data_from_state = await state.get_data()
        await callback.message.answer(data_from_state.get('all_result_messages')[data_from_state.get('page')],
                                      reply_markup=data_from_state.get('keyboards')[data_from_state.get('page')])


# ten random memes
@dp.callback_query_handler(text_contains='new_random', state=Search.ten_random_memes)
async def process_callback_new_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=60)
    await process_random_memes(call=callback, state=state)
