import os
import json
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.users.search import result_mem_search_by_page, keyboards, all_result_messages, global_page
from states.search_states import Search
from loader import dp, bot


async def open_choice_meme(current_call, meme_data, meme_id):
    detailed_inline_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Подробнее',
                             url=meme_data[result_mem_search_by_page[global_page.value][meme_id]]
                             ['meme_href']
                             ))
    await bot.send_photo(
        chat_id=current_call.from_user.id,
        photo=meme_data[result_mem_search_by_page[global_page.value][meme_id]]
        ['pic_href'])
    await current_call.message.answer(
        meme_data[result_mem_search_by_page[global_page.value][meme_id]]
        ['describe'], reply_markup=detailed_inline_kb)


@dp.callback_query_handler(text_contains='res',
                           state=Search.search_input_key_words)
async def process_callback_res_num_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        data = json.load(dataset)
        cur_id = call.data.split(':')[1]
        # try:
        await open_choice_meme(current_call=call, meme_data=data, meme_id=cur_id)
        # except KeyError:
        #     page.set_first()
        #     await open_choice_meme(current_call=call, meme_data=data, meme_id=cur_id)


# Этот хэндлер должен как то еще выводить результат поиска
@dp.callback_query_handler(text_contains='page', state=Search.search_input_key_words)
async def process_callback_page_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    if call.data == 'next_page':
        global_page.next_page()
        await call.message.answer(all_result_messages[global_page.value],
                                  reply_markup=keyboards[global_page.value])
    elif call.data == 'previous_page':
        global_page.previous_page()
        await call.message.answer(all_result_messages[global_page.value],
                                  reply_markup=keyboards[global_page.value])
