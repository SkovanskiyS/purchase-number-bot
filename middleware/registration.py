from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update

from database.dbApi import DB_API


class Registration(BaseMiddleware):
    async def on_process_update(self, update: Update, data: dict):
        database_api = DB_API()
        database_api.connect()
        if update.callback_query:
            lang = update.callback_query.data.split(':')  # lang:ru - output [lang,ru]
            if 'lang' in update.callback_query.data:
                database_api.change_language(update.callback_query.from_user.id, lang[1])
                await update.callback_query.message.delete()
        # elif update.message.text != '/start' and not database_api.user_exists(update.message.from_user.id): #lock of using other commands whule registering
        #     raise CancelHandler()
