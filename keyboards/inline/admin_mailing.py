from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_items = {'Фото': 'send_photo', 'Обычный текст': 'send_text'}
admin_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Фото', callback_data='send_photo')
    ],
    [
        InlineKeyboardButton(text='Обычный текст', callback_data='send_text')
    ]
])


photo_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Добавить подпись', callback_data='add_text_to_photo')
    ],
    [
        InlineKeyboardButton(text='Не добавлять', callback_data='no_text_to_photo')
    ]
])
