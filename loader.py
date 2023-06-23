import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot,Dispatcher
from data.config import load_config

config = load_config('.env')
bot_token = config.tg_bot.BOT_TOKEN

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=bot_token,parse_mode='HTML')
dp = Dispatcher(bot=bot,storage=storage)




