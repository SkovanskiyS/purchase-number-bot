import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import load_config
from handlers.register import register_all_handlers
from middleware.throttling import ThrottlingMiddleware
from middleware.on_process import HandleProcessData
from services.commands import set_main_menu
from database.dbApi import DB_API


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logging.info('BOT STARTED')

    config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.BOT_TOKEN, parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot, storage=storage)
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(HandleProcessData())
    register_all_handlers(dp)

    await set_main_menu(bot)

    # notify admins
    await bot.send_message(config.tg_bot.ADMINS[0], 'BOT HAS BEEN STARTED')

    # create a table
    database_api = DB_API()
    database_api.connect()
    database_api.create_table()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.skip_updates()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
