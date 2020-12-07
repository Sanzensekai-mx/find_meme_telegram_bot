from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

search = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начать поиск мема"),
        ],
    ],
    resize_keyboard=True)
