from aiogram.dispatcher.filters.state import StatesGroup, State

class FirstURL(StatesGroup):
    sending_URL = State()