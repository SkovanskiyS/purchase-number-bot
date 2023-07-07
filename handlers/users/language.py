from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from misc.states import Language


async def choose_language(call: CallbackQuery):
    await call.message.answer(_('start'), reply_markup=CreateBtn.MenuBtn())


async def change_language(call: CallbackQuery, state: FSMContext):
    database_api = DB_API()
    database_api.connect()
    lang = call.data.split(':')  # lang:ru - output [lang,ru]
    database_api.change_language(call.from_user.id, lang[1])
    await call.message.answer(_('language_changed'), reply_markup=CreateBtn.MenuBtn())
    await state.finish()


def register_language(dp: Dispatcher):
    dp.register_callback_query_handler(choose_language, text_contains='lang')
    dp.register_callback_query_handler(change_language, state=Language.change_language)
