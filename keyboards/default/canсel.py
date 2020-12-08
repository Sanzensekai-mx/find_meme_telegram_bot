from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

canсel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ],
    ],
    resize_keyboard=True)
