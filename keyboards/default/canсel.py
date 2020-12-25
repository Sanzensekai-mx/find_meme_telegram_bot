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
