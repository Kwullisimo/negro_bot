from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class settings_bot_new(StatesGroup):
    CHOOSE_NEW_NICKNAME = State()
    CHOOSE_NEW_SKIN_COLOR = State()