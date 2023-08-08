import datetime
from dateutil.parser import parse
from datetime import datetime, timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Purchase, Language
from misc.throttling_limit import rate_limit
from pathlib import Path


async def my_balance(msg: Message):
    db = DB_API()
    db.connect()
    user_balance = float(db.get_balance(msg.from_user.id)[0])
    formatted = "{:,.2f}".format(user_balance)
    text = f"""
         <b>{_("balance_btn")}</b>\n
<b>{_('your_balance')}:</b> \n<i>{formatted} сум</i>
"""
    current_directory = str(Path(__file__).resolve().parent.parent.parent) + '/logo.jpg'
    with open(current_directory, 'rb') as photo:
        await msg.bot.send_photo(msg.from_user.id, photo=photo, caption=text,
                                 reply_markup=CreateInlineBtn.my_balance_btn())


async def buy_handler(msg: Message) -> None:
    await msg.answer(_('notification'), reply_markup=CreateBtn.CancelBtn())
    await msg.answer(_('choose_service'), reply_markup=CreateInlineBtn.services())
    await Purchase.first()


async def back_buy_handler(msg: Message):
    await msg.answer(_('choose_service'), reply_markup=CreateInlineBtn.services())
    await Purchase.first()


async def cancel_purchase(msg: Message, state: FSMContext) -> None:
    await state.reset_state()
    await msg.answer(_('canceled'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def change_language(msg: Message):
    await msg.answer(_('Choose language:'), reply_markup=CreateInlineBtn.language())


@rate_limit(limit=10)
async def how_touse(msg: Message):
    await msg.answer('Video')


@rate_limit(limit=5)
async def support(msg: Message):
    await msg.answer(_('contact'), reply_markup=CreateBtn.MenuBtn())


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
    dateTime: datetime = all_data[5]
    parsed_output_expires = parse(str(dateTime))
    modified_datetime_expires = parsed_output_expires + timedelta(hours=2)

    formatted_output_expires = modified_datetime_expires.strftime("%Y-%m-%d %H:%M:%S")

    caption_text = f"""
         <b>{_("my_profile")}</b>\n
<i>ID:</i> <b>{all_data[0]}</b>
<i>Telegram ID: </i><b>{all_data[1]}</b>
<i>Username: </i><b>@{all_data[2]}</b>\n
{_('your_language')}: <b>{all_data[4]}</b>\n
{_('reg_date')}: <b>{formatted_output_expires}</b>
{_('bonus')}: <b>{all_data[6]}</b>
{_('referrals')}: <b>{ref_count}</b>
{_('blocked')}: <b>{False if all_data[8] == 0 else True}</b>\n
{_('referral_link')}: <b>{ref_link}</b>
    """

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
    dp.register_message_handler(my_balance, lambda message: message.text == _('balance_btn'))
    dp.register_message_handler(how_touse, lambda message: message.text == _('how_use'))
    dp.register_message_handler(support, lambda message: message.text == _('support'))