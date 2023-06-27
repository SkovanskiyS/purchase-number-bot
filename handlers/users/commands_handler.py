from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from misc.throttling_limit import rate_limit
from lexicon.lexicon_RU import commands_text


@rate_limit(limit=5)
async def start_handler(msg: Message):
    await msg.answer(commands_text['start'])


@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(commands_text['help'])


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(commands_text['faq'])


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'))
    dp.register_message_handler(help_handler, Command('help'))
    dp.register_message_handler(faq_handler, Command('faq'))









