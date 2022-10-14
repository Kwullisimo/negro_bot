from aiogram import types
from handlers.process_start import process_start
import keyboards
from utils import anti_flood, dispatcher
from keyboards.keyboards import add_back_button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import states.select_skin
import database
import asyncio
import json


dp = dispatcher.dp
bot = dispatcher.bot
flood = anti_flood.anti_flood

@dp.throttled(flood, rate=1)
async def get_inventory(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        del_msg1 = await message.reply('Эта настройка производиться в лс бота.')
        await asyncio.sleep(5)
        await del_msg1.delete()
        try:
            await bot.delete_message(chat.id, message.message_id)

        except:
            pass

    else:
        await database.create_inventory_table()

        returned_inventory = await database.select_inventory_user(user.id)

        if returned_inventory is None:
            await message.reply('Ну ты ботяра конечно, ни одного скина.')
        
        else:
            inventory = json.loads(returned_inventory[0])

            str = ''

            for x in inventory:
                skin = await database.select_skin(x)
                skin = skin[0]
                str = str + skin + ' *[ ' + x + ' ]*\n\n'

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
            btn1 = KeyboardButton('Выбрать скин')
            keyboard.add(btn1)
            await add_back_button(keyboard)

            await message.reply(f'*Все твои скины* (значения в скобках его ID):\n\n{str}', parse_mode='Markdown', reply_markup=keyboard)

@dp.throttled(flood, rate=1)
async def choose_ext_skin(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        del_msg1 = await message.reply('Эта настройка производиться в лс бота.')
        await asyncio.sleep(5)
        await del_msg1.delete()
        try:
            await bot.delete_message(chat.id, message.message_id)

        except:
            pass

    else:
        await database.create_inventory_table()

        returned_inventory = await database.select_inventory_user(user.id)

        if returned_inventory is None:
            await message.reply('Какой выбирать, у тебя ни одного скина, ахах 😁')

        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
            await add_back_button(keyboard)
            await message.reply('Введи ID скина который хочешь поставить: ', reply_markup=keyboard)
            await states.select_skin.select_ext_skin_state.STATE_1.set()

async def ext_skin_set(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    returned_inventory = await database.select_inventory_user(user.id)
    inventory = json.loads(returned_inventory[0])

    if message.text not in inventory:
        await message.reply('Этого скина нет у вас в инвентаре, либо вы неправильно набрали его ID, негрилла ты такая вроде ботом пользуешься, а писать так и не научился))')
        await state.finish()
        await asyncio.sleep(2)
        await process_start(message)

    else:
        await database.update_skin_color_bot_db(user.id, message.text)
        await message.reply(f'Отлично, текущий отчим: *{message.text}*', parse_mode='Markdown')
        await state.finish()
        await asyncio.sleep(2)
        await process_start(message)