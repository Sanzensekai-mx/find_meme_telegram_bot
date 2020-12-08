import os
import json
from keyboards.default import search, canсel
from keyboards.inline import result_kb, inline_kb1
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from states.search_states import Search
from loader import dp, bot
from aiogram.dispatcher import FSMContext


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
    await message.answer(result_message, reply_markup=result_kb)


