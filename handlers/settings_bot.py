import asyncio
from audioop import add
import imp
from modulefinder import ReplacePackage
from os import stat
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram import types
from handlers.process_start import process_start
import database
from keyboards.keyboards import add_back_button
from utils.dispatcher import bot
from time import sleep as sl
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from states.setting_bot import settings_bot_new
from aiogram.dispatcher import FSMContext

@dp.throttled(anti_flood, rate=1)
async def settings_bot(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        delete_msg = await message.reply('Негр, это в ЛС моем делается, если что-то не рботает, пропиши /start.')
        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass
        await asyncio.sleep(15)
        await delete_msg.delete()

    else:
        if await database.select_user_in_bot_db(user.id) is None:
            await message.reply('Быстро в ЛС регаться негрилла ты такая!')

        else:
            table_user = await database.return_user_from_bot_db(user.id)
            table_user = table_user[0]

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            btn1 = KeyboardButton('Изменить ник')
            btn2 = KeyboardButton('Изменить цвет отчима')
            keyboard.add(btn1, btn2)
            await add_back_button(keyboard)

            await message.reply('Выбирай что хочешь изменить: ', reply_markup=keyboard)

@dp.throttled(anti_flood, rate=1)
async def choose_new_nickname(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        delete_msg = await message.reply('Негр, это в ЛС моем делается, если что-то не рботает, пропиши /start.')
        await asyncio.sleep(15)
        await delete_msg.delete()

    else:
        if await database.select_user_in_bot_db(user.id) is None:
            await message.reply('Быстро в ЛС регаться негрилла ты такая!')

        else:
            table_user = await database.return_user_from_bot_db(user.id)
            table_user = table_user[0]

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
            await add_back_button(keyboard)

            await message.reply(f'*Текущий ник*: {table_user[1]}\n\nПиши свой новый ник, меньше чем 20 символов: ', parse_mode='Markdown', reply_markup=keyboard)
            await settings_bot_new.CHOOSE_NEW_NICKNAME.set()

@dp.throttled(anti_flood, rate=1)
async def choose_new_skin_color(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        delete_msg = await message.reply('Негр, это в ЛС моем делается, если что-то не рботает, пропиши /start.')
        await asyncio.sleep(15)
        await delete_msg.delete()

    else:
        if await database.select_user_in_bot_db(user.id) is None:
            await message.reply('Быстро в регайся негрилла ты такая!')

        else:
            table_user = await database.return_user_from_bot_db(user.id)
            table_user = table_user[0]

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
            btn1 = KeyboardButton(text='Нигерс с района')
            btn2 = KeyboardButton(text='Азиат с рисом')
            btn3 = KeyboardButton(text='Белая элита')

            keyboard.add(btn1, btn2, btn3)

            await add_back_button(keyboard)

            await message.reply(f'<b>Текущий цвет отчима</b>: {table_user[3]}\n\nВыбирай нового отчима: ', parse_mode='HTML', reply_markup=keyboard)
            await settings_bot_new.CHOOSE_NEW_SKIN_COLOR.set()

async def set_new_nickname(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    if len(message.text) > 20:
        await message.reply('Сказал же, меньше 20 символов! Попробуй еще раз: ')
        await settings_bot_new.CHOOSE_NEW_NICKNAME.set()

    else:
        table_user = await database.return_user_from_bot_db(user.id)
        table_user = table_user[0]

        await database.update_nickname_bot_db(user.id, message.text)
        await message.reply(f'Отлично, ник изменен! Текущий ник: *{message.text}*', parse_mode='Markdown')
        await state.finish()
        await asyncio.sleep(2)
        await process_start(message)

async def set_new_skin_color(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    skins = ['Нигерс с района', 'Азиат с рисом', 'Белая элита']

    if message.text not in skins:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = KeyboardButton(text='Нигерс с района')
        btn2 = KeyboardButton(text='Азиат с рисом')
        btn3 = KeyboardButton(text='Белая элита')
        keyboard.add(btn1, btn2, btn3)
        await add_back_button(keyboard)
        await message.reply('Советую выбрать на клавиатуре себе отчима. Скины будут в отдельной кнопке))', reply_markup=keyboard)
        await settings_bot_new.CHOOSE_NEW_SKIN_COLOR.set()

    else:
        if message.text == 'Нигерс с района':
            skin_colorss = 'nigga'

        elif message.text == 'Азиат с рисом':
            skin_colorss = 'aziat'

        elif message.text == 'Белая элита':
            skin_colorss = 'white'

        await database.update_skin_color_bot_db(user.id, skin_colorss)
        await message.reply(f'Отлично, текущий цвет: *{message.text}*', parse_mode='Markdown')
        await state.finish()
        await asyncio.sleep(2)
        await process_start(message)