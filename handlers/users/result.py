import re
import logging
from aiogram.utils.exceptions import BadRequest
from .ten_random_memes import process_random_memes
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from states.main_states import UserStates
from loader import dp, bot
from utils.db_api.models import DBCommands

db = DBCommands()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def open_choice_meme(current_call, meme_list, meme_id, state):
    state_data = await state.get_data()
    current_meme_db_object = [meme_object for meme_object in meme_list
                              if meme_object.meme_name == state_data.get('result_mem_search_by_page')
                              [state_data.get('page')][meme_id]][0]
    try:
        detailed_inline_kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Подробнее',
                                 url=current_meme_db_object.meme_href
                                 ))
    # Придумать другую заглушку?
    except BadRequest:
        await current_call.message.answer('Ссылки на страницу мема нет в базе.')
        # detailed_inline_kb = InlineKeyboardMarkup().add(
        # InlineKeyboardButton('Недоступно'))
    try:
        await bot.send_photo(
            chat_id=current_call.from_user.id,
            photo=current_meme_db_object.pic_href)
    except BadRequest:
        await current_call.message.answer('Картинка не найдена.')
    try:
        await current_call.message.answer(current_meme_db_object.describe)
    except BadRequest:
        await current_call.message.answer('Описание мема не найдено.')
    try:
        pattern = re.compile(r'https?:\/\/\.?([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]'
                             r'{1,6})\b[-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*')
        url = current_meme_db_object.meme_href
        search_process = pattern.search(url)
        site_name = search_process.group(1)
        await current_call.message.answer(f'Нажми кнопку, чтобы открыть страницу мема в источнике на {site_name}',
                                          reply_markup=detailed_inline_kb)
    except Exception as e:
        logging.info(e)
        await current_call.message.answer('Ссылки на страницу мема нет в базе.')


async def action_process_callback(call, state):
    await call.answer(cache_time=60)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        # data = json.load(dataset)
        data_meme_list = await db.all_meme()
        cur_id = call.data.split(':')[1]
        await open_choice_meme(current_call=call, meme_list=data_meme_list, meme_id=cur_id, state=state)


# search
@dp.callback_query_handler(text_contains='res',
                           state=UserStates.search_input_key_words)
async def process_callback_res_num_button(callback: CallbackQuery, state: FSMContext):
    await action_process_callback(call=callback, state=state)


# ten random memes
@dp.callback_query_handler(text_contains='res', state=UserStates.ten_random_memes)
async def process_callback_res_num_button(callback: CallbackQuery, state: FSMContext):
    await action_process_callback(call=callback, state=state)


# search
@dp.callback_query_handler(text_contains='page', state=UserStates.search_input_key_words)
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
@dp.callback_query_handler(text_contains='new_random', state=UserStates.ten_random_memes)
async def process_callback_new_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=60)
    await process_random_memes(call=callback, state=state)
