from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_search = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ],
        [
            KeyboardButton(text="Показать результаты поиска")
        ],
    ],
    resize_keyboard=True)

cancel_ten_random = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ],
        [
            KeyboardButton(text="Показать результаты рандома")
        ]
    ],
    resize_keyboard=True)

cancel_cooperation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)

admin_cancel_mail_or_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel_mail")
        ],
        [
            KeyboardButton(text='Подтвердить')
        ]
    ],
    resize_keyboard=True
)
admin_cancel_mail = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel_mail")
        ]
    ],
    resize_keyboard=True
)

admin_cancel_add_meme = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel_meme")
        ]
    ],
    resize_keyboard=True
)

admin_cancel_del_meme = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel_del_meme")
        ]
    ],
    resize_keyboard=True
)
