from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class select_ext_skin_state(StatesGroup):
    STATE_1 = State()