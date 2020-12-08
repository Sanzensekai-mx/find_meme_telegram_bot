from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):  # Определение состояний
    start_search = State()
    search_input_key_words = State()
