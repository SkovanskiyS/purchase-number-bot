import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import load_config
from handlers.register import register_all_handlers
from middleware.throttling import ThrottlingMiddleware


async def main() -> None:
    config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.BOT_TOKEN)
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot, storage=storage)
    dp.middleware.setup(ThrottlingMiddleware())
    register_all_handlers(dp)

    # notify admins
    await bot.send_message(config.tg_bot.ADMINS[0], 'BOT HAS BEEN STARTED')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
