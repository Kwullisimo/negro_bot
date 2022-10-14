import asyncio
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram import types
import database
from keyboards.keyboards import add_back_button, add_jobs_button, add_start_keyboard
from utils.dispatcher import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from states.choose_job import choose_your_job
from aiogram.dispatcher import FSMContext
import random
from time import sleep

@dp.throttled(anti_flood, rate=1)
async def show_works(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        del_msg = await message.reply('Только в ЛС 😁')
        await asyncio.sleep(5)
        await del_msg.delete()

    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)

        await database.create_jobs_table()
        await database.create_welder_table()
        await database.create_warning_table()
        await database.create_taxi_table()

        button_leave_job = KeyboardButton('Уволиться с работы')

        await add_jobs_button(keyboard)

        returned_user = await database.select_user_from_jobs(user.id)
        if returned_user is not None:
            keyboard.add(button_leave_job)

        await add_back_button(keyboard)

        await message.reply('*Список всех доступных работ:*', reply_markup=keyboard, parse_mode='MarkdownV2')
        await choose_your_job.STATE_1.set()

async def welder_job(message: types.Message):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)
    dungeon = False
    try:
        returned_user = returned_user[0]

    except:
        dungeon = True

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    btn1 = KeyboardButton('Устроиться негро-варщиком')
    btn2 = KeyboardButton('Работать')

    if returned_user != 'welder' or dungeon == True:
        keyboard.add(btn1)

    else:
        keyboard.add(btn2)

    await add_back_button(keyboard)

    await message.reply('*Работа сварщика:*\n\nКороче берешь сварочный аппарат и варишь трубы, за *45 секунд* дают *от 1 до 20 рублей*.', reply_markup=keyboard, parse_mode='Markdown')
    await choose_your_job.WELDER_CHOOSE.set()

async def enter_the_welder(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)

    create_welder = False
    welder_user = await database.select_welder_user(user.id)
    if welder_user is None:
        create_welder = True

    if returned_user is None:
        job = 'welder'
        job_name = 'Сварщик'
        await database.replace_into_jobs(user.id, job, job_name)
        if create_welder == True:
            uses = 0
            await database.replace_into_welder(user.id, uses)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)

        await message.reply('Теперь ты работаешь негро-сварщиком, для начала работы перейди *работы -> сварщик*.', reply_markup=keyboard, parse_mode='Markdown')
        await state.finish()
    
    else:
        keybard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keybard)
        
        await message.reply(f'Негронат натрия, ты уже работаешь, короче уволься и все.', reply_markup=keybard)
        await state.finish()
        return False

async def welder_start_working(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)

    try:
        returned_user = returned_user[0]

    except:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)
        await message.reply('На работу устройся мудила!', reply_markup=keyboard)
        await state.finish()
        return False

    if returned_user != 'welder':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)

        await message.reply('Советую тибе нафек пойти с такими запросами, устройся сначала на работу, бомжара нищий))', reply_markup=keyboard)
        await state.finish()

    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = ('Варить трубу')
        keyboard.add(btn1)
        await add_back_button(keyboard)
        await message.reply('Начинай варить трубы', reply_markup=keyboard)
        await choose_your_job.WELDER_WORKING.set()

async def welder_working(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    btn1 = ('Варить трубу')
    keyboard.add(btn1)
    await add_back_button(keyboard)

    await message.reply('Жди 45 секунд.')
    await state.finish()
    sost = False
    await database.replace_warning(user.id, sost)
    await asyncio.sleep(45)
    sost = True
    await database.replace_warning(user.id, sost)

    rand_money = random.randint(1, 20)

    welder_uses = await database.select_welder_uses(user.id)
    uses = welder_uses[0] + 1
    returned_user = await database.return_user_from_bot_db(user.id)
    returned_user = returned_user[0]
    balance = returned_user[2] + rand_money

    await database.replace_into_welder(user.id, uses)
    await database.update_balance_bot(user.id, balance)

    await bot.send_message(chat.id, f'Отлично, ты заработал: *{rand_money} руб*. Твой баланс составляет: *{balance} руб*. Работай дальше негрилла!', reply_markup=keyboard, parse_mode='Markdown')
    await choose_your_job.WELDER_WORKING.set()

async def taxi_job(message: types.Message):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)
    dungeon = False
    try:
        returned_user = returned_user[0]

    except:
        dungeon = True

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    btn1 = KeyboardButton('Устроиться негро-таксистом')
    btn2 = KeyboardButton('Работать')

    if returned_user != 'taxi' or dungeon == True:
        keyboard.add(btn1)

    else:
        keyboard.add(btn2)

    await add_back_button(keyboard)

    await message.reply('*Работа таксиста:*\n\nАриндуешь машыну, садишься бип-бип паихали, платят больше чем на сварщике, но клиент может убежать не заплатив! Зарплата: *от 25 до 70 рублей* за заказ.', reply_markup=keyboard, parse_mode='Markdown')
    await choose_your_job.TAXI_CHOOSE.set()

async def enter_the_taxi(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)

    create_taxi = False
    taxi_user = await database.select_taxi_user(user.id)
    if taxi_user is None:
        create_taxi = True

    if returned_user is None:
        job = 'taxi'
        job_name = 'Негро-таксист'
        await database.replace_into_jobs(user.id, job, job_name)
        if create_taxi == True:
            uses = 0
            await database.replace_into_taxi(user.id, uses)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)

        await message.reply('Теперь ты работаешь негро-таксистом, для начала работы перейди *работы -> таксист*.', reply_markup=keyboard, parse_mode='Markdown')
        await state.finish()
    
    else:
        keybard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keybard)
        
        await message.reply(f'Негронат натрия, ты уже работаешь, короче уволься и все.', reply_markup=keybard)
        await state.finish()
        return False

async def taxi_start_working(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    returned_user = await database.select_user_from_jobs(user.id)

    try:
        returned_user = returned_user[0]

    except:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)
        await message.reply('На работу устройся мудила!', reply_markup=keyboard)
        await state.finish()
        return False

    if returned_user != 'taxi':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(keyboard)

        await message.reply('Советую тибе нафек пойти с такими запросами, устройся сначала на работу, бомжара нищий))', reply_markup=keyboard)
        await state.finish()

    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = ('Возить бичей')
        keyboard.add(btn1)
        await add_back_button(keyboard)
        await message.reply('Начинай возить негронатов', reply_markup=keyboard)
        await choose_your_job.TAXI_WORKING.set()

async def taxi_working(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    btn1 = ('Возить бичей')
    keyboard.add(btn1)
    await add_back_button(keyboard)

    random_time = random.randint(20, 150)
    random_l = random.randint(3, 25)
    kidok = random.randint(1, 100)

    if kidok > 60:
        kidok = True

    else:
        kidok = False

    await message.reply(f'Вам ехать: *{random_l} км*. Примерное время: *{random_time} сек*.', parse_mode='Markdown')
    await state.finish()
    sost = False
    await database.replace_warning(user.id, sost)
    await asyncio.sleep(random_time)
    sost = True
    await database.replace_warning(user.id, sost)

    if kidok == True:
        await bot.send_message(chat.id, '*Вас кинули, вы ничего не заработали! 🤬*', reply_markup=keyboard, parse_mode='Markdown')
        await choose_your_job.TAXI_WORKING.set()

    else:    

        rand_money = random.randint(25, 70)

        taxi_uses = await database.select_taxi_uses(user.id)
        uses = taxi_uses[0] + 1
        returned_user = await database.return_user_from_bot_db(user.id)
        returned_user = returned_user[0]
        balance = returned_user[2] + rand_money

        await database.replace_into_taxi(user.id, uses)
        await database.update_balance_bot(user.id, balance)

        await bot.send_message(chat.id, f'Отлично, ты заработал: *{rand_money} руб*. Твой баланс составляет: *{balance} руб*. Работай дальше негрилла!', reply_markup=keyboard, parse_mode='Markdown')
        await choose_your_job.TAXI_WORKING.set()

async def leave_from_job(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    await add_start_keyboard(keyboard)

    returned_user = await database.select_user_from_jobs(user.id)
    if returned_user is None:
        await message.reply('Ты че, негрилла такая, устройся сначала на нее! 🤡', reply_markup=keyboard)
        await state.finish()
    
    else:
        await state.finish()
        await database.delete_user_from_jobs(user.id)
        await message.reply('*Вы были уволены с работы!* 💼', reply_markup=keyboard, parse_mode='Markdown')