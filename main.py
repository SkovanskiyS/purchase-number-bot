import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import load_config


async def main() -> None:
    config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.BOT_TOKEN)
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot,storage=storage)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())