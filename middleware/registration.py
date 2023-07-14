from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update,Message

from database.dbApi import DB_API
from i18n import _


class Registration(BaseMiddleware):

    async def on_process_message(self,message:Message,data:dict):
        database_api = DB_API()
        await database_api.connect()
        banned_users = await database_api.get_all_banned_users()
        user_id = message.from_user.id
        if (user_id,) in banned_users:
            await message.answer('<b>❗️Ваш аккаунт был заблокирован администратором. Пожалуйста, обратитесь к администратору, чтобы снять это ограничение.</b>')
            raise CancelHandler()

    async def on_process_update(self, update: Update, data: dict):
        database_api = DB_API()
        await database_api.connect()

        if update.callback_query:
            lang = update.callback_query.data.split(':')  # lang:ru - output [lang,ru]
            if 'register' in update.callback_query.data or 'lang' in update.callback_query.data:
                await database_api.change_language(update.callback_query.from_user.id, lang[1])
