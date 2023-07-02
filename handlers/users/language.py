import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.dbApi import DB_API
from keyboards.default.creator import CreateBtn
from lexicon.lexicon_RU import LEXICON_COMMANDS,LEXICON_OTHERS
from misc.states import Language


async def choose_language(call: CallbackQuery, state:FSMContext):
    lang = call.data.split(':')  # lang:ru - output [lang,ru]
    database_api = DB_API()
    try:
        database_api.connect()
        if not database_api.user_exists(call.from_user.id):
            database_api.insert_user(
                telegram_id=call.from_user.id,
                username=call.from_user.username,
                first_name=call.from_user.first_name,
                last_name=call.from_user.last_name,
                language=lang[1]
            )
            await call.message.answer(LEXICON_COMMANDS['start'], reply_markup=CreateBtn.MenuBtn())
        else:
            database_api.change_language(call.from_user.id,lang[1])
            await call.message.answer(LEXICON_OTHERS['language_changed'])

        await call.message.delete()
        await state.finish()
    except Exception as err:
        logging.info(str(err))


def register_language(dp: Dispatcher):
    dp.register_callback_query_handler(choose_language, text_contains='lang',state=Language.choose_lang)
