import os
import json
from random import choice
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from handlers.users.search import result_mem_search_by_page, keyboards, all_result_messages, global_page
from keyboards.default import main_menu, cancel_ten_random
from loader import dp
from states.search_states import Search


# функция используется в разных хэндлерах, поэтому предлагается такое решение
# Если функция выполняется в message_handler --> руками задаем агумент mes, call не трогаем
# Если функция выполняется в callback_handler --> прописываем наоборот call, mes не трогаем
async def process_random_memes(state_data, mes=None, call=None):
    await Search.ten_random_memes.set()
    await mes.answer('Ваши рандомные мемы, сэр', reply_markup=cancel_ten_random) if mes is not None \
        else await call.message.answer('Ваши рандомные мемы, сэр', reply_markup=cancel_ten_random)
    async with state_data.proxy() as data_from_state:
        data_from_state['page'] = 1
    with open(os.path.join(os.getcwd(), 'parse', 'mem_dataset.json'), 'r', encoding='utf-8') \
            as dataset:
        state_data.get('result_mem_search_by_page')
        mem_data = json.load(dataset)
        result_random = set()
        state_data.get('result_mem_search_by_page').update({1: {}})
        while len(result_random) < 10:
            result_random.add(choice(list(mem_data.keys())))
        result_kb = InlineKeyboardMarkup(row_width=5)
        result_message = ''
        for num, res in enumerate(result_random, 1):
            res_button = InlineKeyboardButton(str(num), callback_data=f"res_{num}:{num}")
            state_data.get('result_mem_search_by_page')[1].update({str(num): res})
            result_kb.insert(res_button)
            result_message += f'{num}. {res}\n\n'
        result_kb.add(InlineKeyboardButton('Еще 10 мемов', callback_data='new_random'))
        state_data.get('keyboards').update({1: result_kb})
        state_data.get('all_result_messages').update({1: result_message})
        await mes.answer(text=result_message, reply_markup=result_kb) if mes is not None \
            else await call.message.answer(text=result_message, reply_markup=result_kb)


@dp.message_handler(Text(equals=['10 рандомных мемов']), state=Search.ten_random_memes)
async def start_ten_random_memes(message: Message, state: FSMContext):
    # LOG you!!!!!!!
    print({'from': message.chat.first_name, 'text': message.text})
    # LOG you!!!!!!!
    data_from_state = await state.get_data()
    await process_random_memes(state_data=data_from_state, mes=message)


@dp.message_handler(Text(equals=['Отмена', 'Показать результаты рандома']), state=Search.ten_random_memes)
async def process_random_menu(message: Message, state: FSMContext):
    data_from_state = await state.get_data()
    # LOG you!!!!!!!
    print({'from': message.chat.first_name, 'text': message.text})
    # LOG you!!!!!!!
    if message.text == 'Показать результаты рандома':
        await message.answer(data_from_state.get('all_result_messages')[data_from_state.get('page')],
                             reply_markup=data_from_state.get('keyboards')[data_from_state.get('page')])
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отменено', reply_markup=main_menu)

