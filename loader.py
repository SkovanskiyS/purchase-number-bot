import logging

from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)




