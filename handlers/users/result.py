import os
import json
from aiogram.types import CallbackQuery
from handlers.users.search import result_mem_search_by_page, keyboards, all_result_messages
from states.search_states import Search
from loader import dp, bot


class PageCounter:

    def __init__(self):
        self._value = 1

    def next_value(self):
        self._value += 1
        return self._value

    def previous_value(self):
        self._value -= 1
        return self._value

    def set_first(self):
        self._value = 1

    @property
    def value(self):
        return self._value


current_page = PageCounter()


# Заработало, надо было добавить state
# @dp.callback_query_handler(lambda c: c.data == 'next page', state=Search.search_input_key_words)
@dp.callback_query_handler(text_contains='res',
                           state=Search.search_input_key_words)
async def process_callback_res_num_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        mem_data = json.load(dataset)
        mem_id = call.data.split(':')[1]
        try:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=mem_data[result_mem_search_by_page[current_page.value][mem_id]]
                ['pic_href'])
            await call.message.answer(
                mem_data[result_mem_search_by_page[current_page.value][mem_id]]
                ['describe'])
        except KeyError:
            current_page.set_first()
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=mem_data[result_mem_search_by_page[current_page.value][mem_id]]
                ['pic_href'])
            await call.message.answer(
                mem_data[result_mem_search_by_page[current_page.value][mem_id]]
                ['describe'])


# Этот хэндлер должен как то еще выводить результат поиска
@dp.callback_query_handler(text_contains='page', state=Search.search_input_key_words)
async def process_callback_page_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    if call.data == 'next_page':
        current_page.next_value()
        await call.message.answer(all_result_messages[current_page.value],
                                  reply_markup=keyboards[current_page.value])
    elif call.data == 'previous_page':
        current_page.previous_value()
        await call.message.answer(all_result_messages[current_page.value],
                                  reply_markup=keyboards[current_page.value])
