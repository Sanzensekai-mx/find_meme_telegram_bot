from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Фото (можно с подписью)', callback_data='send_photo')
    ],
    [
        InlineKeyboardButton(text='Обычный текст', callback_data='send_text')
    ]
])

#
# photo_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Добавить подпись', callback_data='add_text_to_photo')
#     ],
#     [
#         InlineKeyboardButton(text='Не добавлять', callback_data='no_text_to_photo')
#     ]
# ])
