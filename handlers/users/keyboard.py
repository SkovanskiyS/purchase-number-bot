import datetime
from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Purchase, Language
from misc.throttling_limit import rate_limit


async def buy_handler(msg: Message) -> None:
    await msg.answer(_('notification'), reply_markup=CreateBtn.CancelBtn())
    await msg.answer(_('choose_service'), reply_markup=CreateInlineBtn.services())
    await Purchase.first()


@rate_limit(limit=3)
async def cancel_purchase(msg: Message, state: FSMContext) -> None:
    await state.reset_state()
    await msg.answer(_('canceled'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def change_language(msg: Message):
    await msg.answer(_('Choose language:'), reply_markup=CreateInlineBtn.language())


@rate_limit(limit=3)
async def my_profile(msg: Message):
    userId = msg.from_user.id
    db_api = DB_API()
    db_api.connect()
    all_data = db_api.get_all_info(userId)
    referrals = db_api.check_referral(userId)
    ref_count = len(referrals) if referrals is not None else 0
    user_id = db_api.get_user_id(userId)
    bot_username = await msg.bot.get_me()
    ref_link = f'https://t.me/{bot_username.username}?start={user_id[0]}'
    dateTime: datetime = all_data[6]

    caption_text = f"""
         <b>{_("my_profile")}</b>\n
<i>ID:</i> <b>{all_data[0]}</b>
<i>Telegram ID: </i><b>{all_data[1]}</b>
<i>Username: </i><b>@{all_data[2]}</b>\n
{_('your_name')}: <b>{all_data[3]}</b>
{_('your_lastname')}: <b>{all_data[4]}</b>
{_('your_language')}: <b>{all_data[5]}</b>\n
{_('reg_date')}: <b>{dateTime.strftime("%Y-%m-%d %H:%M:%S")}</b>
{_('bonus')}: <b>{all_data[7]}</b>
{_('referrals')}: <b>{ref_count}</b>
{_('blocked')}: <b>{False if all_data[9] == 0 else True}</b>\n
{_('referral_link')}: <b>{ref_link}</b>
    """
    from pathlib import Path

    current_directory = str(Path(__file__).resolve().parent.parent.parent) + '/logo.jpg'
    with open(current_directory, 'rb') as photo:
        await msg.bot.send_photo(msg.from_user.id, photo=photo, caption=caption_text,
                                 reply_markup=CreateInlineBtn.get_bonus_for_referrals())


def register_buy_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_purchase, lambda message: message.text == _('cancel'),
                                state=Purchase.all_states_names)
    dp.register_message_handler(buy_handler, lambda message: message.text == _('buy_number'))
    dp.register_message_handler(change_language, lambda message: message.text == _('change_lang'))
    dp.register_message_handler(my_profile, lambda message: message.text == _('my_profile'))
