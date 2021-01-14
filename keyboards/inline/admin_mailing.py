from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Медиа (Фото/Видео)', callback_data='send_media')
    ],
    # [
    #     InlineKeyboardButton(text='Аудио', callback_data='send_audio')
    # ],
    # [
    #     InlineKeyboardButton(text='Документ', callback_data='send_doc')
    # ],
    [
        InlineKeyboardButton(text='Документы, аудиозаписи, гифки', callback_data='send_another')
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
