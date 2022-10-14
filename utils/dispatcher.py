from operator import imod
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config import TOKEN

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

database_path = "databases/users.db"