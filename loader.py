import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN,parse_mode='HTML')
dp = Dispatcher(bot=bot,storage=storage)




