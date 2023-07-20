from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Language
from misc.throttling_limit import rate_limit
from services.Payments.payme import PaymePay


@rate_limit(limit=3)
async def start_handler(msg: Message):
    db_api = DB_API()
    db_api.connect()
    if db_api.user_exists(msg.chat.id):
        await msg.answer(_('start'), reply_markup=CreateBtn.MenuBtn())
        await msg.answer(_('faq'))
    else:
        # adding user
        referral = msg.get_args() if len(msg.get_args()) > 0 else None
        last_name = ' ' if msg.from_user.last_name == None else msg.from_user.last_name
        db_api.insert_user(
            telegram_id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name.encode('utf-8',errors='replace'),
            last_name=last_name.encode('utf-8',errors='replace'),
            referral=referral
        )
        await msg.answer(
            "<b>Пожалуйста, выберите язык, на котором вы хотели бы взаимодействовать с ботом.\n\n❗️По умолчанию русский язык</b>",
            reply_markup=CreateInlineBtn.language_register())


@rate_limit(limit=3)
async def help_handler(msg: Message):
    await msg.answer(_('help'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def faq_handler(msg: Message):
    await msg.answer("""
English: https://telegra.ph/How-to-use-the-bot---BAN-Buy-Activation-Number-07-16\n
Russian: https://telegra.ph/Kak-polzovatsya-botom---BAN-Buy-Activation-Number-07-16\n
Uzbek: https://telegra.ph/Botdan-qanday-foydalanish---BAN-Buy-Activation-Number-07-16
    """, reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def contact_handler(msg: Message):
    await msg.answer(_('contact'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=3)
async def about_handler(msg: Message):
    await msg.answer(_('about'), reply_markup=CreateBtn.MenuBtn())


async def cancel(msg: Message, state: FSMContext):
    await msg.answer('Canceled')
    await state.finish()


def register_user(dp: Dispatcher) -> None:
    handlers_ = {
        start_handler: 'start',
        help_handler: 'help',
        faq_handler: 'faq',
        contact_handler: 'contact',
        about_handler: 'about'
    }

    for handler, command in handlers_.items():
        dp.register_message_handler(handler, Command(command))

    dp.register_message_handler(cancel, Command('cancel'), state=Language.change_language)
