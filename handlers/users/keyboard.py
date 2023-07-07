from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from database.pages import current_page
from i18n import _

from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn, Pagination
from misc.states import Purchase, Language
from misc.throttling_limit import rate_limit


async def buy_handler(msg: Message) -> None:
    await msg.answer(_('notification'), reply_markup=CreateBtn.CancelBtn())
    await msg.answer(_('choose_service'), reply_markup=CreateInlineBtn.services())
    await Purchase.first()


@rate_limit(limit=3)
async def cancel_purchase(msg: Message, state: FSMContext) -> None:
    await state.reset_state()
    current_page['page'] = 0
    await msg.answer(_('canceled'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def change_language(msg: Message):
    await msg.answer(_('Choose language:') + '\n\nCancel: /cancel', reply_markup=CreateInlineBtn.language())
    await Language.first()


def register_buy_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_purchase, lambda message: message.text == _('cancel'),
                                state=Purchase.all_states_names)
    dp.register_message_handler(buy_handler, lambda message: message.text == _('buy_number'))
    dp.register_message_handler(change_language, lambda message: message.text == _('change_lang'))
