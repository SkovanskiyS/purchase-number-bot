from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from misc.bonuses import Bonus
from i18n import _


async def add_ref_bonuses(call: CallbackQuery):
    bonus = Bonus()
    result = await bonus.referral_bonus()
    match result:
        case 'empty':
            await call.message.answer(_('not_enough'))
        case _:
            await call.message.answer(_('bonus_changed'))


def register_ref_bonus(dp: Dispatcher):
    dp.register_callback_query_handler(add_ref_bonuses, text='ref_bonus')
