from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from keyboards.default import main_menu, cancel_search, cancel_ten_random
from states.search_states import Search
from loader import dp


@dp.message_handler(Text(equals=['10 рандомных мемов']))
async def start_ten_random_memes(message: Message):
    await Search.ten_random_memes.set()
    await message.answer('Скоро заработает)', reply_markup=cancel_ten_random)


@dp.message_handler(state=Search.ten_random_memes)
async def show_ten_random_memes(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Отмена.', reply_markup=main_menu)
        await state.finish()
