from aiogram import executor

from handlers.register import register_all_handlers
from loader import dp
from handlers.users.start import register_user
import logging


def on_startup():
    print('registered')
    register_all_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
