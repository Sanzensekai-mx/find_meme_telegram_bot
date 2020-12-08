import os
import json
from keyboards.default import search, canсel
from keyboards.inline import result_kb
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from states.search_states import Search
from loader import dp
from aiogram.dispatcher import FSMContext
import logging


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
        result_message = ''
        for num, res in enumerate(result, 1):
            result_message += f'''
{num}. {res}\n'''
        await message.answer(result_message, reply_markup=result_kb)  # Должна будет выводиться inline клавиатура


@dp.callback_query_handler(lambda callback_query: True) # не работает нихуя
async def process_callback_next_button(callback_query: CallbackQuery):
    # await callback_query.answer(callback_query.id)
    # await callback_query.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
    await callback_query.answer('Следующая страница...')
    # callback_data = callback_query.data
    # logging.info(f"{callback_data=}")
    # await callback_query.message.answer("Следующая страница...")
