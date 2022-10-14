import asyncio
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram import types
import database
from keyboards.keyboards import add_back_button
import random
from utils.dispatcher import bot

@dp.throttled(anti_flood, rate=1)
async def spenking_sheep(message: types.Message):
    user = message.from_user
    chat = message.chat

    msgs = ["Вас выебал осел", "Бэээ", "Вас изнасиловали тристо козлов", "Вы выебали собаку и съели ее"]
    
    rnd_msg = random.choice(msgs)

    await message.reply(rnd_msg)
