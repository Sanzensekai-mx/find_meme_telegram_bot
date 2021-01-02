from loader import dp
from states.main_states import UserStates
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import main_menu, cancel_cooperation


@dp.message_handler(Text(equals=['Сотрудничество/Предложения']))
async def ask_offers_and_cooperation(message: Message):
    # LOG you
    print(f'from: {message.chat.first_name}, text: {message.text}')
    # LOG you
    await UserStates.cooperation.set()
    await message.answer('Можете написать свое предложение. ', reply_markup=cancel_cooperation)
    await message.answer('Раздел в разработке, можете нажмите кнопку Отмена, чтобы вернуться в главное меню')


@dp.message_handler(Text, state=UserStates.cooperation)
async def process_offers_and_cooperation(message: Message, state: FSMContext):
    # LOG you
    print(f'from: {message.chat.first_name}, text: {message.text}')
    # LOG you
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отменено', reply_markup=main_menu)
