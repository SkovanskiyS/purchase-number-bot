from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, LabeledPrice, Invoice

from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from lexicon.lexicon_RU import LEXICON_COMMANDS
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def start_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['start'], reply_markup=CreateBtn.MenuBtn())
    #await msg.answer('Choose language:', reply_markup=CreateInlineBtn.language())


@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['help'])


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['faq'])


@rate_limit(limit=5)
async def contact_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['contact'])


@rate_limit(limit=5)
async def about_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['about'])


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
