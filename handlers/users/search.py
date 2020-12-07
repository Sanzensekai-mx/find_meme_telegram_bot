from keyboards.default import search
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from aiogram.dispatcher import FSMContext


@dp.message_handler(Text('Начать поиск мема'))
async def wait_for_mem_request(message: Message):
    await message.answer('Введите ключевые слова для поиска мема в базе', reply_markup=ReplyKeyboardRemove())

# @dp.message_handler(Text())
# async def search_and_show(message: Message):
