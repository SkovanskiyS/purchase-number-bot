from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from database.pages import current_page
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from lexicon.lexicon_RU import LEXICON_BUY, LEXICON_BUTTONS, LEXICON_OTHERS
from misc.states import Purchase
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def buy_handler(msg: Message) -> None:
    await msg.answer(LEXICON_OTHERS['notification'], reply_markup=CreateBtn.CancelBtn())
    await msg.answer(LEXICON_BUY['choose_service'], reply_markup=CreateInlineBtn.services())
    await Purchase.first()


@rate_limit(limit=5)
async def cancel_purchase(msg: Message, state: FSMContext) -> None:
    await state.reset_state()
    current_page['page'] = 0
    await msg.answer(LEXICON_OTHERS['canceled'], reply_markup=CreateBtn.MenuBtn())


def register_buy_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_purchase, Text(equals=LEXICON_BUTTONS['cancel']),
                                state=Purchase.all_states_names)
    dp.register_message_handler(buy_handler, Text(equals=LEXICON_BUTTONS['buy_number']))
