from aiogram import types
from handlers.process_start import process_start
from utils import anti_flood, dispatcher
import database
import asyncio
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from keyboards.keyboards import add_back_button, add_start_keyboard
from states.insert_promo import insert_promo
from aiogram.dispatcher import FSMContext
import json

dp = dispatcher.dp
bot = dispatcher.bot
flood = anti_flood.anti_flood

@dp.throttled(flood, rate=1)
async def input_promo(message: types.Message):
    user = message.from_user.id
    chat = message.chat

    await database.create_promo_table()
    await database.create_inventory_table()

    if chat.type != 'private':
        del_msg1 = await message.reply('Че гений чтоле? Промики в ЛС вводить надо.')
        await asyncio.sleep(5)
        await del_msg1.delete()

        try:
            await bot.delete_message(chat.id, message.message_id)
        except:
            pass

    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
        await add_back_button(keyboard)
        await message.reply('Вводи промокод: ', reply_markup=keyboard)
        await insert_promo.STATE_1.set()

async def second_state(message: types.Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    if await database.select_promo_user(message.text) is None:
        replys_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        await add_start_keyboard(replys_keyboard)
        await message.reply('Либо ты непраильно ввел промокод, либо ты негр (скорее всего второе), кстати есть еще и третье код использованный)) 😁', reply_markup=replys_keyboard)
        await state.finish()
        await asyncio.sleep(2)
        
    
    else:
        returned_all = await database.select_all_promo(message.text)
        returned_all = returned_all[0]
        uses = returned_all[3]
        type = returned_all[1]
        gift_id = returned_all[2]

        returned_inventory = await database.select_inventory_user(user.id)

        if returned_inventory is not None:
            inv = json.loads(returned_inventory[0])
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            await add_start_keyboard(keyboard)
            if gift_id in inv:
                await message.reply('Ты че, овосч, заскамить меня хочишь? У тебя есть этот скин, негр.', reply_markup=keyboard)
                await state.finish()
                return False

        if uses == 0:
            reerwe_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            await add_start_keyboard(reerwe_keyboard)
            await message.reply('Истек срок действия промокода.', reply_markup=reerwe_keyboard)
            await state.finish()

        else:
            if type == 'skin':

                user_is_first = False
                
                if returned_inventory is None:
                    inventory = []
                    user_is_first = True

                else:
                    inventory = json.loads(returned_inventory[0])

                inventory.append(returned_all[2])
                inventory = json.dumps(inventory)

                skin = await database.select_skin(gift_id)
                skin = skin[0]

                uses -= 1
                await database.update_promo(message.text, uses)

                if user_is_first == True:
                    await database.insert_into_inventory(user.id, inventory)
                    await state.finish()
                    
                    abema_board = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
                    await add_start_keyboard(abema_board)

                    await message.reply(f'Прмокод применен, *выдан скин: {skin}*. Зайди в инвентарь и чекни его, если хочешь применить, это в настройки.', parse_mode='Markdown', reply_markup=abema_board)

                else:
                    await database.update_inventory(user.id, inventory)
                    await state.finish()

                    abema_board = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
                    await add_start_keyboard(abema_board)

                    await message.reply(f'Прмокод применен, *выдан скин: {skin}*. Зайди в инвентарь и чекни его, если хочешь применить, это в настройки.', parse_mode='Markdown', reply_markup=abema_board)