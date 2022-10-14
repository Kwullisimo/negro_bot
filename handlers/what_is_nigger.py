from ast import arg
from email.message import Message
from sys import exec_prefix
from utils.dispatcher import dp, bot
from aiogram import types
from utils.anti_flood import anti_flood
from database import select_user_in_bot_db
from database import return_user_from_bot_db
from database import check_user_in_rep
from database import select_reputation
from database import select_skin, select_name_from_jobs
from PIL import Image
import asyncio

@dp.throttled(anti_flood, rate=1)
async def what_is_this_nigger(message: types.Message):
    user = message.from_user
    chat = message.chat

    try:
        replied_message = message.reply_to_message.from_user

    except:
        del_msg66 = await message.reply('Ответь на сообщение негра, что бы посмотреть его статистику.')
        await asyncio.sleep(5)
        await del_msg66.delete()
        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass
        return False

    if await select_user_in_bot_db(replied_message.id) is None:
        del_msg55 = await message.reply('Заставь этого абэмуса зарегестрироваться сначала и дизлайк ему поставь потом!')
        await asyncio.sleep(5)
        await del_msg55.delete()

        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass

    else:
        table_user = await return_user_from_bot_db(replied_message.id)
        table_user = table_user[0]

        #Image
        skin_color = table_user[3]
        img = Image.open(f'images/skins_color/rendered/background_{skin_color}.png')
        path_to_photo = f'images/skins_color/rendered/users/background_{skin_color}.png'

        img.crop((0, 0, 1080, 600)).save(path_to_photo)

        if await check_user_in_rep(replied_message.id, chat.id) is None:
            rep = 0
            unrep = 0
            
        else:
            returned_user = await select_reputation(replied_message.id, chat.id)
            returned_user = returned_user[0]
            rep = returned_user[2]
            unrep = returned_user[3]

        returned_skin = await select_skin(skin_color)
        returned_skin = returned_skin[0]

        returned_name_job = await select_name_from_jobs(replied_message.id)
        no_job = False

        if returned_name_job is None:
            no_job = True

        else:
            returned_name_job = returned_name_job[0]

        if no_job == True:
            user_job = "Безработный"

        else:
            user_job = returned_name_job

        delete_msg = await bot.send_photo(chat.id, types.InputFile(path_to_photo), caption=f'*ОТЧИМ {replied_message.mention}*:\n\n*НИК:* {table_user[1]}\n\n*БАЛАНС:* {table_user[2]}\n\n*ЦВЕТ ОТЧИМА:* {returned_skin}\n\n*РАБОТА*: {user_job}\n\n*Репутация в чате*: +{rep}/-{unrep}', parse_mode='Markdown')
        await asyncio.sleep(15)
        await delete_msg.delete()
        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass
