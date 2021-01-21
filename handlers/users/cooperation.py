import logging
from loader import dp, bot
from states.main_states import UserStates
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from keyboards.default import main_menu, cancel_cooperation
from data.config import admins

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


@dp.message_handler(Text(equals=['Сотрудничество/Предложения ✉']))
async def ask_offers_and_cooperation(message: Message):
    # LOG you
    logging.info(f'from: {message.chat.first_name}, text: {message.text}')
    # LOG you
    await UserStates.cooperation.set()
    await message.answer('Можете написать свое предложение. ', reply_markup=cancel_cooperation)


@dp.message_handler(Text, state=UserStates.cooperation, content_types=ContentType.all())
async def process_offers_and_cooperation(message: Message, state: FSMContext):
    # LOG you
    logging.info(f'from: {message.chat.first_name}, text: {message.text}')
    # LOG you
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отменено', reply_markup=main_menu)
    else:
        for admin in admins:
            await bot.forward_message(chat_id=admin, from_chat_id=message.chat.id, message_id=message.message_id)
        await message.answer('Ваше сообщение отправлено.', reply_markup=main_menu)
        await state.finish()
