from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database.dbApi import DB_API


class HandleProcessData(BaseMiddleware):
    current_lang = ''
    current_id = 0
    db_api = DB_API()

    def get_language(self):
        self.db_api.connect()
        language = self.db_api.get_current_language(self.current_id)
        self.current_lang = language

    async def on_process_message(self, message: Message, data: dict):
        self.current_id = message.from_user.id


        print('hi')

middleware_on_process = HandleProcessData()
middleware_on_process.get_language()
print(middleware_on_process.current_lang)
match middleware_on_process.current_lang:
    case 'ru':
        from lexicon.lexicon_RU import *
    case 'eng':
        from lexicon.lexicon_ENG import *
    case 'uz':
        from lexicon.lexicon_UZB import *
