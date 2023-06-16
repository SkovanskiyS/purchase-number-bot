from aiogram import types


#for all
from aiogram.dispatcher.filters import Command

from data.config import admins
from loader import dp


async def set_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
        ]
    )
