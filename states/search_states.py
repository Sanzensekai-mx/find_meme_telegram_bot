from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):  # Определение состояний
    search_input_key_words = State()
    ten_random_memes = State()
