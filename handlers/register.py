from aiogram import Dispatcher
from handlers.users.start import register_user


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_user,
    )
    for handler in handlers:
        handler(dp)