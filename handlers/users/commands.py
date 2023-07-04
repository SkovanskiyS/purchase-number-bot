from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from database.dbApi import DB_API
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
# from lexicon.lexicon_RU import LEXICON_COMMANDS
from lexicon.lexicon_RU import LEXICON_COMMANDS
from misc.states import Language
from misc.throttling_limit import rate_limit
from i18n import _


@rate_limit(limit=5)
async def start_handler(msg: Message, **data):
    db_api = DB_API()
    db_api.connect()

    if db_api.user_exists(msg.from_user.id):
        await msg.answer(_('start'), reply_markup=CreateBtn.MenuBtn())
    else:
        await msg.answer(_('Choose language:'), reply_markup=CreateInlineBtn.language())
        await Language.first()


@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(_('help'))


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(_('faq'))


@rate_limit(limit=5)
async def contact_handler(msg: Message):
    await msg.answer(_('contact'))


@rate_limit(limit=5)
async def about_handler(msg: Message):
    await msg.answer(_('about'))


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

    dp.register_message_handler(cancel, Command('cancel'), state=Language.choose_lang)
