from email import message_from_binary_file
from itertools import chain
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram.dispatcher import FSMContext
from aiogram import types
import database
from states.create_profile_states import create_bot_profile
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from keyboards.keyboards import add_back_button
from utils.dispatcher import bot
from time import sleep as sl
import asyncio

@dp.throttled(anti_flood, rate=0.5)
async def create_profile_in_bot_function(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        delete_msg = await message.reply('Это в ЛС делается, нигер!')
        try:
            await bot.delete_message(chat.id, message.message_id)

        except:
            pass
        await asyncio.sleep(15)
        await delete_msg.delete()

    else:
        if await database.select_user_in_bot_db(user.id) is None:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            await add_back_button(keyboard)
            await message.reply('Отлично, выбирай себе ник <не больше 20 симв.>:', reply_markup=keyboard)
            await create_bot_profile.CHOOSE_NICK.set()
        else:
            await message.reply('MQ, у тебя есть профиль, негр!')

async def choose_nickname_state(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat
    if len(message.text) > 20:
        await message.reply('Я че-то неясно сказал? 20 символов максимум, негрилла ты такая.')
        await create_bot_profile.CHOOSE_NICK.set()
    else:
        async with state.proxy() as data:
            data['nick'] = message.text

        await message.reply('Ага, скин выбери себе негр: ')
        #**************************************************
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = KeyboardButton(text='Нигерс с района')
        btn2 = KeyboardButton(text='Азиат с рисом')
        btn3 = KeyboardButton(text='Белая элита')
        keyboard.add(btn1, btn2, btn3)
        await add_back_button(keyboard)

        media = types.MediaGroup()

        media.attach_photo(types.InputFile('images/skins_color/rendered/background_nigga.png'), 'Нигерс с района')
        media.attach_photo(types.InputFile('images/skins_color/rendered/background_aziat.png'), 'Азиат с рисом')
        media.attach_photo(types.InputFile('images/skins_color/rendered/background_white.png'), 'Белая элита')

        await bot.send_media_group(chat.id, media)
        await bot.send_message(chat.id, 'Выбирай себе цвет отчима: ', reply_markup=keyboard)
        #**************************************************
        await create_bot_profile.CHOOSE_SKIN_COLOR.set()

async def choose_skin_color_state(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat
    skins = ['Нигерс с района', 'Азиат с рисом', 'Белая элита']
    balance = 0

    if message.text not in skins:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = KeyboardButton(text='Нигерс с района')
        btn2 = KeyboardButton(text='Азиат с рисом')
        btn3 = KeyboardButton(text='Белая элита')
        keyboard.add(btn1, btn2, btn3)
        await add_back_button(keyboard)
        await message.reply('Советую выбрать на клавиатуре себе отчима))', reply_markup=keyboard)
        await create_bot_profile.CHOOSE_SKIN_COLOR.set()
    else:
        async with state.proxy() as data:
            nick = data['nick']
        
        if message.text == 'Нигерс с района':
            skin_colorss = 'nigga'

        elif message.text == 'Азиат с рисом':
            skin_colorss = 'aziat'

        elif message.text == 'Белая элита':
            skin_colorss = 'white'

        await database.insert_into_bot_db(user.id, nick, skin_colorss, chat.id)
        await message.reply('Отлично, твой отчим создан! Вот он: ')
        await bot.send_message(chat.id, f'Ник: {nick}\n\nБаланс: {balance}\n\nСкин отчима: {message.text}\n\nТеперь мы возьмём на тебя кредит 😁')
        await state.finish()
