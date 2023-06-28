import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.creator import Pagination, Operator, CreateInlineBtn
from lexicon.lexicon_RU import LEXICON_BUY, LEXICON_OTHERS, LEXICON_CONFIRMATION, LEXICON_OPERATOR_INFO, LEXICON_ERRORS, \
    LEXICON_PAYMENT
from misc.cost_modification import change_price
from misc.states import Purchase
from services.API_5sim.fetch_operator import GetPrice


async def service_handler(call: CallbackQuery, state: FSMContext) -> None:
    try:
        if call.data == 'telegram':
            async with state.proxy() as data:
                data['service'] = call.data
        elif call.data == 'openai':
            async with state.proxy() as data:
                data['service'] = call.data
    except Exception as ex:
        await call.message.answer(ex)
    finally:
        await call.message.delete()
        pagination_obj = Pagination(current_page=0)
        await call.message.answer(LEXICON_BUY['choose_country'], reply_markup=pagination_obj())
        await Purchase.next()


async def country_handler(call: CallbackQuery, state: FSMContext):
    from database.pages import current_page
    pagination_obj = Pagination(current_page=0)
    try:
        match call.data:
            case 'next':
                current_page['page'] += 1
            case 'previous':
                current_page['page'] -= 1
            case 'page':
                current_page['page'] += 5
            case _:
                async with state.proxy() as data:
                    data['country'] = call.data
                await call.message.delete()
                operator_obj = Operator(country=data['country'], product=data['service'])
                inline_keyboard = operator_obj()
                await call.message.answer(LEXICON_BUY['choose_operator'] + '\n' + operator_obj.description,
                                          reply_markup=inline_keyboard, disable_web_page_preview=True)
                await Purchase.next()

        pagination_obj.page = current_page['page']
        await call.message.edit_reply_markup(reply_markup=pagination_obj())
    except Exception as ex:
        logging.info(str(ex))


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
            await call.answer(LEXICON_ERRORS['empty'], show_alert=True)
            await call.message.answer(LEXICON_ERRORS['empty'])
            await Purchase.country.set()
            pagination_obj = Pagination(current_page=0)
            await call.message.answer(LEXICON_BUY['choose_country'], reply_markup=pagination_obj())

        else:
            cost = change_price(d_dict['cost'])
            text = f"<b>{LEXICON_OTHERS['confirm']}\n\n{LEXICON_CONFIRMATION['service']}: <i>{service.title()}</i>\n" \
                   f"\n{LEXICON_CONFIRMATION['country']}: <i>{country.title()}</i>\n\n" \
                   f"{LEXICON_CONFIRMATION['operator']}: <i>{operator.title()}</i>\n\n{LEXICON_OPERATOR_INFO['cost']}: {cost} </b>"
            await call.message.answer(text, reply_markup=CreateInlineBtn.confirmation())
            await Purchase.next()
    except Exception as ex:
        logging.info(str(ex))


async def confirm_data(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    text = f'{LEXICON_PAYMENT["choose"]}'
    await call.message.answer(text, reply_markup=CreateInlineBtn.payment())


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(service_handler, state=Purchase.service)
    dp.register_callback_query_handler(country_handler, state=Purchase.country)
    dp.register_callback_query_handler(operator_handler, state=Purchase.operator)
    dp.register_callback_query_handler(confirm_data, state=Purchase.confirm)
