from aiogram import Dispatcher,Bot
from environs import Env
from data.config import Config


async def main():
    tg = Config()
    bot: Bot = Bot(token = tg.TgBot.API_TOKEN)
    dp : Dispatcher = Dispatcher()