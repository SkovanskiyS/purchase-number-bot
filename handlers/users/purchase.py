import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from i18n import _
from keyboards.inline.creator import Pagination, Operator, CreateInlineBtn
from misc.cost_modification import change_price
from misc.states import Purchase
from services.API_5sim.fetch_operator import GetPrice
from database.dbApi import DB_API

async def service_handler(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['service'] = call.data
    await call.message.delete()
    pagination_obj = Pagination(current_page=0)
    db_api = DB_API()
    db_api.connect()
    pagination_obj.lang = pagination_obj.get_language(call.from_user.id)
    db_api.update_page(call.from_user.id, 0)
    await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
    await Purchase.next()


async def country_handler(call: CallbackQuery, state: FSMContext):
    pagination_obj = Pagination(current_page=0)
    db_api = DB_API()
    db_api.connect()
    pagination_obj.lang = pagination_obj.get_language(call.from_user.id)
    curr_page = db_api.get_current_page(call.from_user.id)[0]

    match call.data:
        case 'next':
            curr_page += 1
        case 'previous':
            curr_page -= 1
        case 'page':
            curr_page += 5
        case _:
            async with state.proxy() as data:
                data['country'] = call.data
            await call.message.delete()
            operator_obj = Operator(country=data['country'], product=data['service'])
            inline_keyboard = operator_obj()
            await call.message.answer(_('choose_operator') + '\n' + operator_obj.description,
                                      reply_markup=inline_keyboard, disable_web_page_preview=True)
            await Purchase.next()
    if curr_page < 0:
        curr_page = 17
    elif curr_page > 17:
        curr_page = 0

    db_api.update_page(call.from_user.id, curr_page)
    pagination_obj.page = curr_page
    await call.message.edit_reply_markup(reply_markup=pagination_obj())


async def operator_handler(call: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['operator'] = call.data
        all_data = await state.get_data()
        service: str = all_data.get('service')
        country: str = all_data.get('country')
        operator: str = all_data.get('operator')
        await call.message.delete()

        url = f'https://5sim.net/v1/guest/prices?country={country}&product={service}'
        operator_info = GetPrice(url)
        d_dict = operator_info()[country][service][operator]
        if d_dict['count'] == 0:
            await call.answer(_('empty'), show_alert=True)
            await call.message.answer(_('empty'))
            await Purchase.country.set()
            pagination_obj = Pagination(current_page=0)
            print(pagination_obj)
            await call.message.answer(_('choose_country'), reply_markup=pagination_obj())

        else:
            cost = change_price(d_dict['cost'])
            text = f"<b>{_('confirm_text')}\n\n{_('service')}: <i>{service.title()}</i>\n" \
                   f"\n{_('country')}: <i>{country.title()}</i>\n\n" \
                   f"{_('operator')}: <i>{operator.title()}</i>\n\n{_('cost')}: {cost} </b>"
            await call.message.answer(text, reply_markup=CreateInlineBtn.confirmation())
            await Purchase.next()
    except Exception as ex:
        logging.info(str(ex))


async def confirm_data(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    text = f'{_("choose")}'
    await call.message.answer(text, reply_markup=CreateInlineBtn.payment())
    await Purchase.next()


async def payment_handler(call: CallbackQuery, state: FSMContext):
    pass

    """
    Handle a payment process
    """


def register_callbacks(dp: Dispatcher):
    handlers = {
        service_handler: Purchase.service,
        country_handler: Purchase.country,
        operator_handler: Purchase.operator,
        confirm_data: Purchase.confirm,
        payment_handler: Purchase.payment,
    }

    for key, value in handlers.items():
        dp.register_callback_query_handler(key, state=value)
