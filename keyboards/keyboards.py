from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

async def add_cancel_button(name_keyboard):
    cancel_button = KeyboardButton('Назад в меню')
    name_keyboard.add(cancel_button)

async def add_back_button(name_keyboard):
    back_button = KeyboardButton('Вернуться в главное меню')
    name_keyboard.add(back_button)

async def add_jobs_button(name_keyboard):
    jobs_btn1 = KeyboardButton('Таксист')
    jobs_btn2 = KeyboardButton('Сварщик')

    name_keyboard.add(jobs_btn1, jobs_btn2)

async def add_start_keyboard(name_keyboard):
    btn5 = KeyboardButton('Работы')
    btn2 = KeyboardButton('Настроить отчима')
    btn3 = KeyboardButton('Доп. Скины')
    btn4 = KeyboardButton('Ввести промокод')

    name_keyboard.add(btn2)
    name_keyboard.add(btn5)
    name_keyboard.add(btn3)
    name_keyboard.add(btn4)