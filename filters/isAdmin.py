from abc import ABC

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, User
from data.config import load_config


class AdminFilter(BoundFilter, ABC):
    async def check(self, *args):
        # Implement your logic to check if the user is an admin
        msg = Message.get_current()
        config = load_config('../.env')
        user_id = User.get_current().id
        ADMINS = config.tg_bot.ADMINS
        if user_id in ADMINS:
            return True
        return False

    async def __call__(self, *args):
        return await self.check(*args)

