import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import load_config
from handlers.register import register_all_handlers
from middleware.throttling import ThrottlingMiddleware
from middleware.test import TestMiddleware


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logging.info('BOT STARTED')

    config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.BOT_TOKEN,parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot, storage=storage)
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(TestMiddleware())
    register_all_handlers(dp)

    # notify admins
    await bot.send_message(config.tg_bot.ADMINS[0], 'BOT HAS BEEN STARTED')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
