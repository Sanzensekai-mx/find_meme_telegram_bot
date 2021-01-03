from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):  # Определение состояний
    search_input_key_words = State()
    ten_random_memes = State()
    cooperation = State()


class AdminNewMeme(StatesGroup):
    Name = State()
    Describe = State()
    Pic = State()
    Link = State()
    Confirm = State()


class AdminMailing(StatesGroup):
    Text = State()
