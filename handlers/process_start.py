from utils.dispatcher import dp, bot
from utils.anti_flood import anti_flood
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import database
import asyncio
from keyboards.keyboards import add_start_keyboard

@dp.throttled(anti_flood, rate=0.5)
async def process_start(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type != 'private':
        del1 = await message.reply(f'{user.mention}, сначала советую разобраться с ботом в ЛС.')
        
        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass

        await asyncio.sleep(15)
        await del1.delete()
    
    else:
        await database.create_default_table()
        await database.create_bot_table()
        
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = KeyboardButton('Создать отчима')

        if await database.select_user_in_bot_db(user.id) is None:
            keyboard.add(btn1)

        else:
            await add_start_keyboard(keyboard)

        await message.reply(f"*Главное меню {user.mention}*", reply_markup=keyboard, parse_mode='Markdown')