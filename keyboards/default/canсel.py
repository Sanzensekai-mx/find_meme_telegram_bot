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

admin_cancel_or_confirm = ReplyKeyboardMarkup(
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

admin_cancel_add_meme = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel_meme")
        ]
    ],
    resize_keyboard=True
)
