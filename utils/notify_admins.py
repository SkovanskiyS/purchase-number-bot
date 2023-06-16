import logging

from loader import dp,bot
from data.config import admins

from aiogram import types,Dispatcher

async def notify_on_startup(dp:Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin,"Бот запущен")
        except Exception as err:
            logging.exception(err)
