from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def start_handler(msg: Message):
    await msg.answer('Welcome!')


async def message_handler(msg: Message):
    await msg.send_copy(msg.from_user.id)


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'))
    dp.register_message_handler(message_handler, content_types='text')
