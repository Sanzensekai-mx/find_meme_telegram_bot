import json
import operator
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from math import ceil
import numpy as np
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default import main_menu, cancel_search
from loader import dp
from states.search_states import Search

keyboards = {}
result_mem_search_by_page = {}
all_result_messages = {}


class PageCounter:

    def __init__(self):
        self._value = 1

    def next_page(self):
        self._value += 1
        return self._value

    def previous_page(self):
        self._value -= 1
        return self._value

    def set_first(self):
        self._value = 1

    @property
    def value(self):
        return self._value


global_page = PageCounter()

stop_word_list = ['в', 'до', 'без', 'безо', 'во', 'за', 'из', 'из-за', 'к', 'ко', 'на', 'о', 'об', 'от', 'по', 'при',
                  'про', 'у', 'at', 'in', 'of', 'to', 'as', 'со', 'с', 'и']


def search(msg, dataset):
    # number_of_words = len(msg.text.split())
    # result_match_one_word = set()
    data_list = list(dataset.keys())
    process_msg = msg.text.split()
    # Одинаковый код в условиях засунуть в функцию
    if len(process_msg) == 1:
        process_msg = ''.join(process_msg)
        result_process = process.extract(process_msg, data_list, limit=len(data_list))
        print([res for res in result_process if res[1] >= 70])
        result_match_one_word = [res[0] for res in result_process if res[1] >= 70]
        return result_match_one_word
    else:
        result_process = process.extract(''.join(process_msg), data_list, limit=len(data_list))
        print([res for res in result_process if res[1] >= 70])
        result_match_one_word = [res[0] for res in result_process if res[1] >= 70]
        return result_match_one_word



    # STAROE
    # for word in str(msg.text).split():
    #     result_match_one_word.update(set(list(filter(
    #         lambda mem: word.lower() in mem, dataset.keys()))))
    #     result_match_one_word.update(set(list(filter(
    #         lambda mem: word.title() in mem, dataset.keys()))))
    # result_match_one_word.update(set([res[0] for res in result_process if res[1] >= 70]))


@dp.message_handler(Text(equals=['Начать поиск мема']))
async def wait_for_mem_request(message: Message):
    await Search.search_input_key_words.set()
    await message.answer('Введите ключевые слова для поиска мема в базе',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text, state=Search.search_input_key_words)
async def search_and_show_results(message: Message, state: FSMContext):
    # global_page.set_first()
    if message.text == 'Показать результаты поиска':
        await message.answer(all_result_messages[global_page.value],
                             reply_markup=keyboards[global_page.value])
    elif message.text == 'Отмена':
        await state.finish()
        await message.answer('Отменено', reply_markup=main_menu)
    else:
        global_page.set_first()
        with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
                as dataset:
            mem_data = json.load(dataset)
            # result_search = set()
            # Все это дело поисковое, засунуть в отдельную функцию
            # for word in str(message.text).split():
            #     result_match_one_word = set()
            #     result_match_one_word.update(set(list(filter(
            #         lambda mem: word.lower() in mem, mem_data.keys()))))
            #     result_match_one_word.update(set(list(filter(
            #         lambda mem: word.title() in mem, mem_data.keys()))))
            #     result_search.update(result_match_one_word)
            result_search = search(msg=message, dataset=mem_data)
            if len(result_search) == 0:
                await message.answer('Ничего не найдено по запросу. '
                                     'Попробуй написать еще раз свой запрос, но другими словами.',
                                     reply_markup=cancel_search)
            elif len(result_search) <= 10:
                # keyboards.clear()
                result_mem_search_by_page.clear()
                # keyboards = {}
                result_kb = InlineKeyboardMarkup(row_width=5)
                result_message = ''
                result_mem_search_by_page.update({1: {}})
                for num, res in enumerate(result_search, 1):
                    res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
                    result_mem_search_by_page[1].update({str(num): res})
                    result_kb.insert(res_button)
                    result_message += f'{num}. {res}\n\n'
                keyboards.update({1: result_kb})
                all_result_messages.update({1: result_message})
                await message.answer('Результат поиска:', reply_markup=cancel_search)
                await message.answer(all_result_messages[global_page.value],
                                     reply_markup=keyboards[global_page.value])
            elif len(result_search) > 10:
                result_mem_search_by_page.clear()
                number_of_pages = ceil(len(result_search) / 10)
                rule_np_list = []
                for i in range(number_of_pages):
                    if i == 0:
                        rule_np_list.append(10)
                        continue
                    rule_np_list.append(rule_np_list[i - 1] + 10)
                search_results_by_pages = np.array_split(result_search, rule_np_list)
                # Клавиатура для каждой страницы
                keyboards_inside = {}
                for page_num in range(number_of_pages):
                    if page_num == 0:
                        keyboards_inside.update(
                            {page_num + 1: InlineKeyboardMarkup(row_width=5, inline_keyboard=[
                                [InlineKeyboardButton('➡️', callback_data='next_page')]]
                                                                )})
                        continue
                    if page_num == list(range(number_of_pages))[-1]:
                        keyboards_inside.update(
                            {page_num + 1: InlineKeyboardMarkup(row_width=5, inline_keyboard=[
                                [InlineKeyboardButton('⬅️', callback_data='previous_page')]]
                                                                )})
                        continue
                    keyboards_inside.update({page_num + 1: InlineKeyboardMarkup(row_width=5, inline_keyboard=[
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
                await message.answer('Результат поиска:', reply_markup=cancel_search)
                await message.answer(all_result_messages[global_page.value],
                                     reply_markup=keyboards[global_page.value])  # С первой страницы
