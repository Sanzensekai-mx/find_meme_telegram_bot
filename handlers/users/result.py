from keyboards.default import search, canсel
from keyboards.inline import result_kb, inline_kb1
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from states.search_states import Search
from loader import dp, bot
from aiogram.dispatcher import FSMContext
import logging


# Заработало, надо было добавить state
@dp.callback_query_handler(lambda c: c.data == 'next page', state=Search.search_input_key_words)
async def process_callback_next_button(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('Следующая страница')
    # await bot.answer_callback_query(call.id)
    # await bot.send_message(call.from_user.id, 'Следующая страница!')


# Test
@dp.message_handler(commands=['1'])
async def process_command_1(message: Message):
    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
