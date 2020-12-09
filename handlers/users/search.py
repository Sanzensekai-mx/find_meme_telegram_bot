import os
import json
from math import ceil
import numpy as np
from keyboards.default import search, canсel
from keyboards.inline import result_kb_1_page_less_10, inline_kb1
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from states.search_states import Search
from loader import dp, bot
from aiogram.dispatcher import FSMContext

keyboards = {}


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
        result = set()
        for word in str(message.text).split():  # Примитивнейший механизм поиска даже стыдно немного
            result_match_one_word = set()
            result_match_one_word.update(set(list(filter(lambda mem: word.lower() in mem, mem_data.keys()))))
            result_match_one_word.update(set(list(filter(lambda mem: word.title() in mem, mem_data.keys()))))
            result.update(result_match_one_word)
        # await message.answer(str(len(result)))  # Тест
        dict_of_result_request = {}
        if len(result) < 10:  # Походу придется прямо здесь создавать клавиатуру
            result_kb = InlineKeyboardMarkup()
            result_message = ''
            for num, res in enumerate(result, 1):
                res_button = InlineKeyboardButton(str(f'{num}'), callback_data=f'res_{num}')
                result_kb.insert(res_button)
                result_message += f'{num}. {res}\n\n'
            await message.answer(result_message, reply_markup=result_kb)
        elif len(result) > 10:
            # result_kb = InlineKeyboardMarkup()
            number_of_pages = ceil(len(result) / 10)
            result_message = ''
            rule_np_list = []
            for el in range(number_of_pages):
                if el == 0:
                    rule_np_list.append(10)
                    continue
                rule_np_list.append(rule_np_list[el - 1] + 10)
            list_of_lists = np.array_split(list(result), rule_np_list)
            # Клавиатура для каждой страницы
            # keyboards = {}
            for page_num in range(number_of_pages):
                if page_num == 0:
                    keyboards.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton('➡️', callback_data='next_page')]])})
                    continue
                if page_num == list(range(number_of_pages))[-1]:
                    keyboards.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton('⬅️', callback_data='previous_page')]])})
                    continue
                keyboards.update({page_num + 1: InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton('⬅️', callback_data='previous_page')],
                    [InlineKeyboardButton('➡️', callback_data='next_page')]])})
            # Наверное стоит это как то в функцию захуярить, я валяюсь
            for num, res in enumerate(list_of_lists[0], 1):   # Индивидуально для каждой страницы должно быть
                res_button = InlineKeyboardButton(str(f'{num}'), callback_data=f'res_{num}')
                if num == 1:
                    keyboards[1].add(res_button)
                    result_message += f'{num}. {res}\n\n'
                    continue
                keyboards[1].insert(res_button)
                result_message += f'{num}. {res}\n\n'
            await message.answer(result_message, reply_markup=keyboards[1])
