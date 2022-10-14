from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class create_bot_profile(StatesGroup):
    CHOOSE_NICK = State()
    CHOOSE_SKIN_COLOR = State()