import os
import json
from math import ceil
import numpy as np
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from keyboards.default import search, cancel
from states.search_states import Search
from loader import dp

keyboards = {}
result_mem_search_by_page = {}
all_result_messages = {}


@dp.message_handler(Text(equals=['Начать поиск мема', 'Искать новый мем']))
async def wait_for_mem_request(message: Message):
    await Search.search_input_key_words.set()
    await message.answer('Введите ключевые слова для поиска мема в базе',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text, state=Search.search_input_key_words)
async def search_and_show_results(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отмена.', reply_markup=search)
    else:
        await message.answer('Результат поиска:', reply_markup=cancel)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        mem_data = json.load(dataset)
        result_search = set()
        # Все это дело поисковое, засунуть в отдельную функцию
        for word in str(message.text).split():  # Примитивнейший механизм поиска даже стыдно немного
            result_match_one_word = set()
            result_match_one_word.update(set(list(filter(
                lambda mem: word.lower() in mem, mem_data.keys()))))
            result_match_one_word.update(set(list(filter(
                lambda mem: word.title() in mem, mem_data.keys()))))
            result_search.update(result_match_one_word)
        if len(result_search) < 9:
            result_mem_search_by_page.clear()
            # keyboards = {}
            result_kb = InlineKeyboardMarkup(row_width=3)
            result_message = ''
            # result_kb.update({1: InlineKeyboardMarkup()})
            result_mem_search_by_page.update({1: {}})
            for num, res in enumerate(list(result_search), 1):
                res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
                result_mem_search_by_page[1].update({str(num): res})
                result_kb.insert(res_button)
                result_message += f'{num}. {res}\n\n'
            await message.answer(result_message, reply_markup=result_kb)
        elif len(result_search) > 9:
            result_mem_search_by_page.clear()
            number_of_pages = ceil(len(result_search) / 9)
            rule_np_list = []
            for i in range(number_of_pages):
                if i == 0:
                    rule_np_list.append(9)
                    continue
                rule_np_list.append(rule_np_list[i - 1] + 9)
            search_results_by_pages = np.array_split(list(result_search), rule_np_list)
            # Клавиатура для каждой страницы
            keyboards_inside = {}
            for page_num in range(number_of_pages):
                if page_num == 0:
                    keyboards_inside.update(
                        {page_num + 1: InlineKeyboardMarkup(row_width=3, inline_keyboard=[
                                    [InlineKeyboardButton('➡️', callback_data='next_page')]]
                                                            )})
                    continue
                if page_num == list(range(number_of_pages))[-1]:
                    keyboards_inside.update(
                        {page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('⬅️', callback_data='previous_page')]]
                        )})
                    continue
                keyboards_inside.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton('⬅️', callback_data='previous_page')],
                    [InlineKeyboardButton('➡️', callback_data='next_page')]])})
            # Наверное стоит это как то в функцию захуярить, я валяюсь
            for page_num, page in enumerate(range(number_of_pages), 1):
                result_mem_search_by_page.update({page_num: {}})
                # Индивидуально для каждой страницы должно быть
                result_message = ''
                for num, res in enumerate(list(search_results_by_pages)[page], 1):
                    res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
                    result_mem_search_by_page[page_num].update({str(num): res})
                    if num == 1:
                        keyboards_inside[page_num].add(res_button)
                        result_message += f'{num}. {res}\n\n'
                        continue
                    keyboards_inside[page_num].insert(res_button)
                    result_message += f'{num}. {res}\n\n'
                result_message += f'Страница {page_num} из {number_of_pages}'  # current_page
                all_result_messages.update({page_num: result_message})
            keyboards.update(keyboards_inside)
            await message.answer(all_result_messages[1],
                                 reply_markup=keyboards[1])  # С первой страницы
