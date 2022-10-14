from email.message import Message
from aiogram import types
from aiogram.utils.exceptions import Throttled
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram.dispatcher import FSMContext
from handlers.process_start import process_start
from database import select_warning_table, create_warning_table

@dp.throttled(anti_flood, rate=0.5)
async def cancel_button(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    await create_warning_table()

    returned_warning = await select_warning_table(user.id)
    dungeon = False
    try:
        returned_warning = returned_warning[0]

    except:
        dungeon = True

    if returned_warning == False:
        await message.reply('Жди негр!')

    else:
        await state.finish()
        await process_start(message)