from keyboards.inline import inline_kb1
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from states.search_states import Search
from loader import dp, bot

import os
import json
from .search import result_mem_search_by_page, keyboards, all_result_messages


class PageCounter:

    def __init__(self):
        self._value = 1

    def next_value(self):
        self._value += 1
        return self._value

    def previous_value(self):
        self._value -= 1
        return self._value

    @property
    def value(self):
        return self._value


current_page = PageCounter()


# Заработало, надо было добавить state
# @dp.callback_query_handler(lambda c: c.data == 'next page', state=Search.search_input_key_words)
@dp.callback_query_handler(text_contains='res', state=Search.search_input_key_words) # Прописать алгоритм для номерных кнопок
async def process_callback_res_num_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    # await call.message.answer('Номерная кнопка')
    # await call.message.answer(call.data)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') as dataset:
        mem_data = json.load(dataset)
        mem_id = call.data.split(':')[1]
        # await call.message.answer(mem_name)
        await bot.send_photo(chat_id=call.from_user.id, photo=mem_data[result_mem_search_by_page[current_page.value][mem_id]]['pic_href'])
        # await SendPhoto(call.id, mem_data[mem_name]['pic_href'])
        # await call.message.answer(mem_data[mem_name]['pic_href'])   # Тут должен присылать картинку, а не тупо ссылку
        await call.message.answer(mem_data[result_mem_search_by_page[current_page.value][mem_id]]['describe'])
        # last_result_message = ''
        # for num, res in enumerate(list(result_search), 1):
        #     last_result_message += f'{num}. {res}\n\n'
        # await call.message.answer(last_result_message)
        # await call.message.answer(last_result_message, reply_markup=keyboards[1])   # 0 - временно


# Этот хэндлер должен как то еще выводить результат поиска
@dp.callback_query_handler(text_contains='page', state=Search.search_input_key_words)
async def process_callback_page_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    # await call.message.answer('Кнопка смены страницы')
    if call.data == 'next_page':
        # await call.message.answer('Не лезь, не работает пока')
        await call.message.answer(all_result_messages[current_page.value + 1], reply_markup=keyboards[current_page.value + 1])
        current_page.next_value()
    elif call.data == 'previous_page':
        await call.message.answer(all_result_messages[current_page.value - 1], reply_markup=keyboards[current_page.value - 1])
        current_page.previous_value()


# Test
@dp.message_handler(commands=['1'])
async def process_command_1(message: Message):
    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
