from aiogram import Dispatcher
from handlers.users.commands import register_user
from handlers.users.keyboard import register_buy_handler
from handlers.users.purchase import register_callbacks
from handlers.users.language import register_language
from handlers.users.referral_bonus_add import register_ref_bonus
from handlers.admin.all_commands import register_admin_handler
from handlers.users.topup_balance import register_balance_add


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_admin_handler,
        register_language,
        register_user,
        register_buy_handler,
        register_callbacks,
        register_ref_bonus,
        register_balance_add
    )
    for handler in handlers:
        handler(dp)
