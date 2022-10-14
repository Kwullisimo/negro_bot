from aiogram.dispatcher.filters.state import StatesGroup, State

class choose_your_job(StatesGroup):
    STATE_1 = State()
    WELDER_CHOOSE = State()
    WELDER_WORKING = State()
    TAXI_CHOOSE = State()
    TAXI_WORKING = State()