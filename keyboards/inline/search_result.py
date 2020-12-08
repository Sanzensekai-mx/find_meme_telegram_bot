from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import result_callback


result_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Сл. Страница', callback_data=result_callback.new(item_name="next", quantity=1))
    ]
])
