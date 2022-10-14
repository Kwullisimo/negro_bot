import asyncio
from utils.dispatcher import dp
from utils.anti_flood import anti_flood
from aiogram import types
import database
from keyboards.keyboards import add_back_button
from utils.dispatcher import bot
from PIL import Image
from time import sleep

@dp.throttled(anti_flood, rate=1)
async def get_my_profile(message: types.Message):
    user = message.from_user
    chat = message.chat

    if await database.select_user_in_bot_db(user.id) is None:
        delete_msg = await message.reply('Быстро в ЛС регаться негрилла ты такая!')
        await asyncio.sleep(15)
        await delete_msg.delete()
        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass

    else:
        await database.create_skins_table()

        table_user = await database.return_user_from_bot_db(user.id)

        table_user = table_user[0]

        #Image
        skin_color = table_user[3]
        img = Image.open(f'images/skins_color/rendered/background_{skin_color}.png')
        path_to_photo = f'images/skins_color/rendered/users/background_{skin_color}.png'

        img.crop((0, 0, 1080, 600)).save(path_to_photo)

        if await database.check_user_in_rep(user.id, chat.id) is None:
            rep = 0
            unrep = 0
            
        else:
            returned_user = await database.select_reputation(user.id, chat.id)
            returned_user = returned_user[0]
            rep = returned_user[2]
            unrep = returned_user[3]
        
        returned_skin = await database.select_skin(skin_color)
        returned_skin = returned_skin[0]

        returned_name_job = await database.select_name_from_jobs(user.id)
        no_job = False

        if returned_name_job is None:
            no_job = True

        else:
            returned_name_job = returned_name_job[0]

        if no_job == True:
            user_job = "Безработный"

        else:
            user_job = returned_name_job

        #await message.reply(f'*ОТЧИМ {user.mention}*:\n\n*НИК:* {table_user[1]}\n\n*БАЛАНС:* {table_user[2]}\n\n*ЦВЕТ ОТЧИМА:* {table_user[3]}', parse_mode='Markdown')
        delete_msg = await bot.send_photo(chat.id, types.InputFile(path_to_photo), caption=f'*ОТЧИМ {user.mention}*:\n\n*НИК:* {table_user[1]}\n\n*БАЛАНС:* {table_user[2]} рублей\n\n*ЦВЕТ ОТЧИМА:* {returned_skin}\n\n*РАБОТА*: {user_job}\n\n*Репутация в чате*: +{rep}/-{unrep}', parse_mode='Markdown')
        if chat.type != 'private':
            await asyncio.sleep(15)
            await delete_msg.delete()

            try:
                await bot.delete_message(chat.id, message.message_id)
            except:
                pass
