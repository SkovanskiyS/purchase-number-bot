from aiogram import Dispatcher
from aiogram.types import Message
from lexicon.lexicon_RU import all_text
from misc.throttling_limit import rate_limit
from aiogram.dispatcher.filters import Text, Command


@rate_limit(limit=5)
async def start_handler(msg: Message):
    await msg.send_copy(msg.from_user.id)


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'))
