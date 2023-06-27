from aiogram import Dispatcher
from handlers.users.commands_handler import register_user


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_user,
    )
    for handler in handlers:
        handler(dp)





