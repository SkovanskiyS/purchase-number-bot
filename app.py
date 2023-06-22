import logging
from aiogram import executor
from handlers.register import register_all_handlers
from loader import dp


def on_startup():
    try:
        register_all_handlers(dp)
    except Exception as ex:
        logging.info(ex)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
