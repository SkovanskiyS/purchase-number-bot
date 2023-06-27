from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command
from keyboards.inline.default_kb import CreateInlineBtn
from lexicon.lexicon_RU import LEXICON_BUY, LEXICON_BUTTONS
from misc.throttling_limit import rate_limit
from misc.states import Purchase


@rate_limit(limit=5)
async def buy_handler(msg: Message) -> None:
    await msg.answer(LEXICON_BUY['choose_service'], reply_markup=CreateInlineBtn.services())
    await Purchase.first()


def register_buy_handler(dp: Dispatcher):
    dp.register_message_handler(buy_handler, Text(equals=LEXICON_BUTTONS['buy_number']))
