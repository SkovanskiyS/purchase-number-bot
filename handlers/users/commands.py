from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.default.creator import CreateBtn
from lexicon.lexicon_RU import LEXICON_COMMANDS
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def start_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['start'],reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['help'])


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['faq'])


@rate_limit(limit=5)
async def contact_handler(msg: Message):
    await msg.answer(LEXICON_COMMANDS['contact'])


def register_user(dp: Dispatcher) -> None:
    handlers_ = {
        start_handler: 'start',
        help_handler: 'help',
        faq_handler: 'faq',
        contact_handler: 'contact'
    }

    for handler, command in handlers_.items():
        dp.register_message_handler(handler, Command(command))

