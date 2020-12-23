from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ],
        [
            KeyboardButton(text="Результаты последнего поиска")
        ],
    ],
    resize_keyboard=True)
