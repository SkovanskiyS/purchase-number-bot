from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, Invoice, LabeledPrice

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Language
from misc.throttling_limit import rate_limit


@rate_limit(limit=5)
async def start_handler(msg: Message):
    # db_api = DB_API()
    # db_api.connect()
    # if db_api.user_exists(msg.chat.id):
    #     await msg.answer(_('start'), reply_markup=CreateBtn.MenuBtn())
    # else:
    #     await msg.answer("<b>❗️ Пожалуйста, выберите язык, на котором вы хотели бы взаимодействовать с ботом.</b>", reply_markup=CreateInlineBtn.language())
    #     # await Language.first()
    #
    price = LabeledPrice(label='Product', amount=1500000)  # amount in cents or smallest currency unit

    invoice = Invoice(
        title='Product Invoice',
        description='This is the invoice for the product.',
        start_parameter='invoice-payment',
        currency='UZS',
        total_amount=[price]
    )

    await msg.bot.send_invoice(msg.from_user.id,

        title=invoice.title,
        description=invoice.description,
        payload=invoice.start_parameter,
        provider_token="387026696:LIVE:649d58ff94aff0d52dbda442",
        currency=invoice.currency,
        prices=invoice.total_amount,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=False)

@rate_limit(limit=5)
async def help_handler(msg: Message):
    await msg.answer(_('help'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def faq_handler(msg: Message):
    await msg.answer(_('faq'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
async def contact_handler(msg: Message):
    await msg.answer(_('contact'), reply_markup=CreateBtn.MenuBtn())


@rate_limit(limit=5)
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
