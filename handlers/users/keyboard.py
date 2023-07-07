import datetime
import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.dbApi import DB_API
from database.pages import current_page
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Purchase, Language
from misc.throttling_limit import rate_limit
from datetime import datetime

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


@rate_limit(limit=3)
async def my_profile(msg: Message):
    db_api = DB_API()
    db_api.connect()
    all_data = db_api.get_all_info(msg.from_user.id)
    ref_count = len(db_api.check_referral(msg.from_user.id))
    user_id = db_api.get_user_id(msg.from_user.id)
    ref_link = f'https://t.me/dadadbaabybot?start={user_id[0]}'
    dateTime: datetime = all_data[6]

    caption_text = f"""
         <b>{_("my_profile")}</b>\n
<i>ID:</i> <b>{all_data[0]}</b>
<i>Telegram ID: </i> <b>{all_data[1]}</b>
<i>Username: </i> <b>@{all_data[2]}</b>\n
{_('your_name')}: <b>{all_data[3]}</b>
{_('your_lastname')}: <b>{all_data[4]}</b>
{_('your_language')}: <b>{all_data[5]}</b>\n
{_('reg_date')}: <b>{dateTime.strftime("%Y-%m-%d %H:%m")}</b>
{_('bonus')}: <b>{all_data[7]}</b>
{_('referrals')}: <b>{ref_count}</b>
{_('blocked')}: <b>{False if all_data[9] == 0 else True}</b>\n
{_('referral_link')}: <b>{ref_link}</b>
    """
    from pathlib import Path

    current_directory = str(Path(__file__).resolve().parent.parent.parent)+'/logo.jpg'
    with open(current_directory, 'rb') as photo:
        await msg.bot.send_photo(msg.from_user.id, photo=photo, caption=caption_text)
    # await msg.answer(caption_text)


def register_buy_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_purchase, lambda message: message.text == _('cancel'),
                                state=Purchase.all_states_names)
    dp.register_message_handler(buy_handler, lambda message: message.text == _('buy_number'))
    dp.register_message_handler(change_language, lambda message: message.text == _('change_lang'))
    dp.register_message_handler(my_profile, lambda message: message.text == _('my_profile'))
