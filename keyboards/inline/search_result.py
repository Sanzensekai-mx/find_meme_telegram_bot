from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# result_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Сл. Страница', callback_data=result_callback.new(item_name="next"))
#     ]
# ])
next_page_button = InlineKeyboardButton('➡️', callback_data='next page')
previous_page_button = InlineKeyboardButton('⬅️', callback_data='previous page')

result_kb_1_page = InlineKeyboardMarkup().add(next_page_button)
result_kb_1_page_less_10 = InlineKeyboardMarkup().add(next_page_button)

# test
inline_btn_12 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_12)
result_kb = InlineKeyboardMarkup()