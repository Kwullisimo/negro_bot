from email.message import Message
from aiogram import types
from aiogram.utils.exceptions import Throttled
from utils.dispatcher import dp
from handlers.process_start import process_start
from utils.anti_flood import anti_flood

@dp.throttled(anti_flood, rate=0.5)
async def back_button(message: types.Message):
    user = message.from_user
    chat = message.chat
    await process_start(message)