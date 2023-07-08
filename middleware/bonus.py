from aiogram.dispatcher.middlewares import BaseMiddleware
from misc.bonuses import Bonus

from database.dbApi import DB_API
from aiogram.types import Message


class BonusModification(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        bonus = Bonus()
        bonus.referral_bonus()
        bonus.add_bonus(10)
