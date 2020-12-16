import os
import json
from math import ceil
import numpy as np
from keyboards.default import search, canсel
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from states.search_states import Search
from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.inline.callback_datas import mem_callback

keyboards = {}
result_mem_search_by_page = {}
all_result_messages = {}


@dp.message_handler(Text(equals=['Начать поиск мема']))
async def wait_for_mem_request(message: Message):
    await Search.search_input_key_words.set()
    await message.answer('Введите ключевые слова для поиска мема в базе', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text, state=Search.search_input_key_words)
async def search_and_show_results(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отмена.', reply_markup=search)
    else:  # Else тут полюбому нужен, иначе 'Результат поиска' выводится и после отмены
        await message.answer('Результат поиска:', reply_markup=canсel)
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') as dataset:
        mem_data = json.load(dataset)
        # for mem, data in mem_data.items():
        result_search = set()
        for word in str(message.text).split():  # Примитивнейший механизм поиска даже стыдно немного
            result_match_one_word = set()
            result_match_one_word.update(set(list(filter(lambda mem: word.lower() in mem, mem_data.keys()))))
            result_match_one_word.update(set(list(filter(lambda mem: word.title() in mem, mem_data.keys()))))
            result_search.update(result_match_one_word)
        # for w in result_search:
        #     await message.answer(w)
        # await message.answer(str(len(result_search)))  # Тест
        if len(result_search) < 9:
            result_mem_search_by_page.clear()
            # keyboards = {}
            result_kb = InlineKeyboardMarkup(row_width=3)
            result_message = ''
            # result_kb.update({1: InlineKeyboardMarkup()})
            for num, res in enumerate(list(result_search), 1):
                res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
                result_mem_search_by_page.update({str(num): res})
                result_kb.insert(res_button)
                result_message += f'{num}. {res}\n\n'
            # await message.answer(result_kb[0])
            await message.answer(result_message, reply_markup=result_kb)     # 1 - временно
        elif len(result_search) > 9:
            result_mem_search_by_page.clear()
            # keyboards.clear()
            # result_kb = InlineKeyboardMarkup()
            number_of_pages = ceil(len(result_search) / 9)
            rule_np_list = []
            for el in range(number_of_pages):
                if el == 0:
                    rule_np_list.append(9)
                    continue
                rule_np_list.append(rule_np_list[el - 1] + 9)
            search_results_by_pages = np.array_split(list(result_search), rule_np_list)
            # Клавиатура для каждой страницы
            keyboards_inside = {}
            for page_num in range(number_of_pages):
                if page_num == 0:
                    keyboards_inside.update({page_num + 1: InlineKeyboardMarkup(row_width=3, inline_keyboard=[
                        [InlineKeyboardButton('➡️', callback_data='next_page')]])})
                    continue
                if page_num == list(range(number_of_pages))[-1]:
                    keyboards_inside.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton('⬅️', callback_data='previous_page')]])})
                    continue
                keyboards_inside.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton('⬅️', callback_data='previous_page')],
                    [InlineKeyboardButton('➡️', callback_data='next_page')]])})
            # Наверное стоит это как то в функцию захуярить, я валяюсь
            for page_num, page in enumerate(range(number_of_pages), 1):
                # Индивидуально для каждой страницы должно быть
                result_message = ''
                for num, res in enumerate(list(search_results_by_pages)[page], 1):
                    res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
                    result_mem_search_by_page.update({str(num): res})
                    if num == 1:
                        keyboards_inside[page_num].add(res_button)
                        result_message += f'{num}. {res}\n\n'
                        continue
                    keyboards_inside[page_num].insert(res_button)
                    result_message += f'{num}. {res}\n\n'
                result_message += f'Страница {page_num} из {number_of_pages}'  # current_page
                all_result_messages.update({page_num: result_message})
            keyboards.update(keyboards_inside)
            # await message.answer(all_result_messages[2])
            # await message.answer('1')
            # await message.answer(all_result_messages[2], reply_markup=keyboards[2])
            await message.answer(all_result_messages[1], reply_markup=keyboards[1])     # С первой страницы
