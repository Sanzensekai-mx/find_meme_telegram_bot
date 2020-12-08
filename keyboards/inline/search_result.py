from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# result_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Сл. Страница', callback_data=result_callback.new(item_name="next"))
#     ]
# ])
inline_btn_1 = InlineKeyboardButton('Сл. Страница', callback_data='next page')
result_kb = InlineKeyboardMarkup().add(inline_btn_1)

# test
inline_btn_12 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_12)
