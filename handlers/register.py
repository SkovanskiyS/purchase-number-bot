from aiogram import Dispatcher
from handlers.users.commands import register_user
from handlers.users.keyboard import register_buy_handler
from handlers.users.purchase import register_callbacks
from handlers.users.language import register_language


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_language,
        register_user,
        register_buy_handler,
        register_callbacks
    )
    for handler in handlers:
        handler(dp)
