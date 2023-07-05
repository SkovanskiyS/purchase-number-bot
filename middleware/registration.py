from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, CallbackQuery

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn


class Registration(BaseMiddleware):
    async def on_process_update(self, update: Update, data: dict):
        database_api = DB_API()
        database_api.connect()
        if update.callback_query:
            lang = update.callback_query.data.split(':')  # lang:ru - output [lang,ru]
            if 'lang' in update.callback_query.data:
                if not database_api.user_exists(update.callback_query.from_user.id):
                    database_api.insert_user(
                        telegram_id=update.callback_query.from_user.id,
                        username=update.callback_query.from_user.username,
                        first_name=update.callback_query.from_user.first_name,
                        last_name=update.callback_query.from_user.last_name,
                        language=lang[1]
                    )
                    await update.callback_query.message.delete()
        elif update.message.text != '/start' and not database_api.user_exists(update.message.from_user.id): #lock of using other commands whule registering
            raise CancelHandler()
