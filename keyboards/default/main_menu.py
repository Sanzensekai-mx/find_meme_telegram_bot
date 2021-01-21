from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton(text="Поиск мема 🗿"))
main_menu.insert(KeyboardButton(text="10 рандомных мемов ✨"))
main_menu.add(KeyboardButton(text='Сотрудничество/Предложения ✉'))
    # keyboard=[
    #     [
    #         KeyboardButton(text="Поиск мема"),
    #     ],
    #     [
    #         KeyboardButton(text="10 рандомных мемов")
    #     ],
    #     [
    #         KeyboardButton(text='Сотрудничество/Предложения')
    #     ]
    # ],
    # resize_keyboard=True)
