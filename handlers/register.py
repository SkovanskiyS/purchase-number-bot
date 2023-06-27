from aiogram import Dispatcher
from handlers.users.commands import register_user
from handlers.users.keyboard_handlers import register_buy_handler
from handlers.users.purchase import register_callbacks


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_user,
        register_buy_handler,
        register_callbacks
    )
    for handler in handlers:
        handler(dp)
