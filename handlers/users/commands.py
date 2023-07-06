from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Language
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def start_handler(msg: Message):
    db_api = DB_API()
    db_api.connect()
    if db_api.user_exists(msg.chat.id):
        await msg.answer(_('start'), reply_markup=CreateBtn.MenuBtn())
    else:
        await msg.answer("<b>❗️ Пожалуйста, выберите язык, на котором вы хотели бы взаимодействовать с ботом.</b>", reply_markup=CreateInlineBtn.language())
        await Language.first()

@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(_('help'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(_('faq'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def contact_handler(msg: Message):
    await msg.answer(_('contact'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def about_handler(msg: Message):
    await msg.answer(_('about'), reply_markup=CreateBtn.MenuBtn())


async def cancel(msg: Message, state: FSMContext):
    await msg.answer('Canceled')
    await state.finish()


def register_user(dp: Dispatcher) -> None:
    handlers_ = {
        start_handler: 'start',
        help_handler: 'help',
        faq_handler: 'faq',
        contact_handler: 'contact',
        about_handler: 'about'
    }

    for handler, command in handlers_.items():
        dp.register_message_handler(handler, Command(command))

    dp.register_message_handler(cancel, Command('cancel'), state=Language.change_language)
