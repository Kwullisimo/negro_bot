from ast import Delete
from aiogram import types
from utils.dispatcher import dp, bot
from utils.anti_flood import anti_flood
from database import (create_reputation_table,
                        create_last_time_table,
                        select_user_in_bot_db,
                        select_last_time,
                        insert_into_last_time,
                        update_last_time,
                        select_reputation,
                        update_reputation_table,
                        insert_reputation_table,
                        check_user_in_rep)

from datetime import datetime, timedelta
import asyncio

@dp.throttled(anti_flood, rate=1)
async def add_reputation(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type == 'private':
        await message.reply('Ты реально думаешь что в приватном чате будут столь хорошие команды? 😶')
    
    else:
        try:
            user_who_adding_rep = message.reply_to_message.from_user

        except:
            del_msg1 = await message.reply('Вам нужно ответить на сообщение негра, которого хотите похвалить за сбор хлопка! 😁')

            await asyncio.sleep(5)
            await del_msg1.delete()

            try:
                await bot.delete_message(chat.id, message.message_id)
            except:
                pass

            return False

        await create_reputation_table()
        await create_last_time_table()

        if await select_user_in_bot_db(user_who_adding_rep.id) is None:
            del_msg2 = await message.reply('Негр должey быть зарегейстрирован! 👳🏿‍♂️')

            await asyncio.sleep(5)
            await del_msg2.delete()

            try:
                await bot.delete_message(chat.id, message.message_id)
            except:
                pass

        else:
            now = datetime.now()
            before = await select_last_time(user.id, chat.id)
            negr = False

            try:
                before = datetime.fromisoformat(before[0])

            except:
                await insert_into_last_time(user.id, chat.id, now.isoformat())

            try:
                delta = now - before

            except:
                negr = True

            if negr == True or delta > timedelta(hours=24):
                await update_last_time(user.id, chat.id, now.isoformat())

                returnedd_user = await check_user_in_rep(user_who_adding_rep.id, chat.id)
                if returnedd_user is None:
                    rep = 1
                    unrep = 0
                    await insert_reputation_table(user_who_adding_rep.id, chat.id, rep, unrep)
                    del_msg3 = await message.reply(f'*Текущая репутация {user_who_adding_rep.mention}*:\n\n*Положительные оценки*: {rep}\n\n*Ортицательные оценки*: {unrep}', parse_mode='Markdown')

                    await asyncio.sleep(15)
                    await del_msg3.delete()

                    try:
                        await bot.delete_message(chat.id, message.message_id)
                    except:
                        pass

                else:
                    returned_user = await select_reputation(user_who_adding_rep.id, chat.id)
                    returned_user = returned_user[0]
                    rep = returned_user[2]
                    unrep = returned_user[3]
                    rep += 1
                    await update_reputation_table(user_who_adding_rep.id, chat.id, rep, unrep)
                    del_msg4 = await message.reply(f'*Текущая репутация {user_who_adding_rep.mention}*:\n\n*Положительные оценки*: {rep}\n\n*Ортицательные оценки*: {unrep}', parse_mode='Markdown')

                    await asyncio.sleep(5)
                    await del_msg4.delete()

                    try:
                        await bot.delete_message(chat.id, message.message_id)

                    except:
                        pass

            else:
                del_msg5 = await message.reply(f'Хвалить негронатов за работу можно раз в 24 часа, так придумал очень хороший человек 😁')

                await asyncio.sleep(5)
                await del_msg5.delete()

                try:
                    await bot.delete_message(chat.id, message.message_id)

                except:
                    pass

@dp.throttled(anti_flood, rate=1)
async def rm_reputation(message: types.Message):
    user = message.from_user
    chat = message.chat

    if chat.type == 'private':
        await message.reply('Ты реально думаешь что в приватном чате будут столь хорошие команды? 😶')
    
    else:
        try:
            user_who_adding_rep = message.reply_to_message.from_user

        except:
            del_msg1 = await message.reply('Вам нужно ответить на сообщение негра, которого хотите избить за плохой сбор хлопка! 😁')

            await asyncio.sleep(5)
            await del_msg1.delete()

            try:
                await bot.delete_message(chat.id, message.message_id)
            except:
                pass

            return False

        await create_reputation_table()
        await create_last_time_table()

        if await select_user_in_bot_db(user_who_adding_rep.id) is None:
            del_msg2 = await message.reply('Негр должey быть зарегейстрирован! 👳🏿‍♂️')

            await asyncio.sleep(5)
            await del_msg2.delete()

            try:
                await bot.delete_message(chat.id, message.message_id)
            except:
                pass

        else:
            now = datetime.now()
            before = await select_last_time(user.id, chat.id)
            negr = False

            try:
                before = datetime.fromisoformat(before[0])

            except:
                await insert_into_last_time(user.id, chat.id, now.isoformat())

            try:
                delta = now - before

            except:
                negr = True

            if negr == True or delta > timedelta(hours=24):
                await update_last_time(user.id, chat.id, now.isoformat())

                returnedd_user = await check_user_in_rep(user_who_adding_rep.id, chat.id)
                if returnedd_user is None:
                    rep = 0
                    unrep = 1
                    await insert_reputation_table(user_who_adding_rep.id, chat.id, rep, unrep)
                    del_msg3 = await message.reply(f'*Текущая репутация {user_who_adding_rep.mention}*:\n\n*Положительные оценки*: {rep}\n\n*Ортицательные оценки*: {unrep}', parse_mode='Markdown')

                    await asyncio.sleep(15)
                    await del_msg3.delete()

                    try:
                        await bot.delete_message(chat.id, message.message_id)
                    except:
                        pass

                else:
                    returned_user = await select_reputation(user_who_adding_rep.id, chat.id)
                    returned_user = returned_user[0]
                    rep = returned_user[2]
                    unrep = returned_user[3]
                    unrep += 1
                    await update_reputation_table(user_who_adding_rep.id, chat.id, rep, unrep)
                    del_msg4 = await message.reply(f'*Текущая репутация {user_who_adding_rep.mention}*:\n\n*Положительные оценки*: {rep}\n\n*Ортицательные оценки*: {unrep}', parse_mode='Markdown')

                    await asyncio.sleep(5)
                    await del_msg4.delete()

                    try:
                        await bot.delete_message(chat.id, message.message_id)

                    except:
                        pass

            else:
                del_msg5 = await message.reply(f'Бить негронатов за работу можно раз в 24 часа, так придумал очень хороший человек 😁')

                await asyncio.sleep(5)
                await del_msg5.delete()

                try:
                    await bot.delete_message(chat.id, message.message_id)

                except:
                    pass
