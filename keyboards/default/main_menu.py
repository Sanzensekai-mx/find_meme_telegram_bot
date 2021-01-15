from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск мема"),
        ],
        [
            KeyboardButton(text="10 рандомных мемов")
        ],
        [
            KeyboardButton(text='Сотрудничество/Предложения')
        ]
    ],
    resize_keyboard=True)
