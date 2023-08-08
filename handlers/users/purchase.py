from datetime import timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from dateutil.parser import parse

from database.dbApi import DB_API
from handlers.users.keyboard import cancel_purchase, buy_handler, back_buy_handler
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import Bonuses, TopCountries_Btn
from keyboards.inline.creator import Pagination, Operator, CreateInlineBtn
from misc.bonuses import Bonus
from misc.cost_modification import change_price, percent_from_bonus
from misc.states import Purchase
from services.API_5sim.fetch_operator import GetPrice
from services.API_5sim.purchase import Buy
from database.countries import telegram_top_countries
from database.countries import chatgpt_top_countries


async def back_btn(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    current_state = current_state.split(':')[1]
    data = await state.get_data()
    if current_state == 'service':
        await cancel_purchase(call.message, state)
    elif current_state == 'country' or current_state == 'top':
        await call.message.delete()
        await call.message.answer(_('choose_type_country'), reply_markup=CreateInlineBtn.choose_type_country())
        await Purchase.country_choose.set()
    elif current_state == 'country_choose':
        await call.message.delete()
        await back_buy_handler(call.message)
    elif current_state == 'operator':
        await call.message.delete()
        if 'type' in data and data['type'] == 'top':
            countries_btn = TopCountries_Btn(data['count_obj'])
            await call.message.answer(_('choose_top10'), reply_markup=countries_btn())
            await Purchase.top.set()
        else:
            pagination_obj = Pagination()
            await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
            await Purchase.country.set()
    elif current_state == 'confirm':
        operator_obj = Operator(country=data['country'], product=data['service'])
        inline_keyboard = operator_obj()
        await call.message.delete()
        await call.message.answer(_('choose_operator') + '\n' + operator_obj.description,
                                  reply_markup=inline_keyboard)
        await Purchase.operator.set()
    elif current_state == 'bonus':
        if 'new_cost' in data and 'bonus_count' in data:
            await state.update_data(new_cost=None)
        await state.update_data(bonus_count=0)
        await generate_confirmation_message(call, state)


async def service_handler(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['service'] = call.data
    await call.message.delete()
    await call.message.answer(_('choose_type_country'), reply_markup=CreateInlineBtn.choose_type_country())
    await Purchase.country_choose.set()


async def country_choose_handler(call: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    if call.data == 'all':
        await call.message.delete()
        pagination_obj = Pagination()
        await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
        await Purchase.country.set()
    elif call.data == 'top':
        service = all_data.get('service')
        countries_obj = telegram_top_countries if service == 'telegram' else chatgpt_top_countries if service == 'openai' else None
        if countries_obj:
            await call.message.delete()
            pagination = Pagination()
            pagination.type = 'top'
            pagination.countries_obj = countries_obj
            countries_btn = TopCountries_Btn(countries_obj)
            await call.message.answer(_('choose_top10'), reply_markup=countries_btn())
            await state.update_data(count_obj=countries_obj)
            await state.update_data(type='top')
            await Purchase.top.set()
        else:
            await call.answer(_('top10_not_available'), show_alert=True)


async def top10_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    async with state.proxy() as data:
        data['country'] = call.data
    await call.message.delete()
    operator_obj = Operator(country=data['country'], product=data['service'])
    inline_keyboard = operator_obj()
    if inline_keyboard:
        await call.message.answer(_('choose_operator') + '\n' + operator_obj.description,
                                  reply_markup=inline_keyboard, disable_web_page_preview=True)
        await Purchase.operator.set()
    else:
        await call.answer(_('no_operator'), show_alert=True)
        if data['type'] == 'top':
            countries_btn = TopCountries_Btn(data['count_obj'])
            await call.message.answer(_('choose_top10'), reply_markup=countries_btn())
            await Purchase.top.set()
        else:
            pagination_obj = Pagination()
            await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
            await Purchase.country.set()


async def country_handler(call: CallbackQuery, state: FSMContext):
    pagination_obj = Pagination()
    match call.data:
        case 'next':
            pagination_obj.page += 1
        case 'previous':
            pagination_obj.page -= 1
        case 'page':
            pagination_obj.page += 3
        case _:
            async with state.proxy() as data:
                data['country'] = call.data
            await call.message.delete()
            operator_obj = Operator(country=data['country'], product=data['service'])
            inline_keyboard = operator_obj()
            if inline_keyboard:
                await call.message.answer(_('choose_operator') + '\n' + operator_obj.description,
                                          reply_markup=inline_keyboard, disable_web_page_preview=True)
                await Purchase.next()
            else:
                await call.answer(_('no_operator'), show_alert=True)
                await call.message.answer(_('no_operator'))
                await Purchase.country.set()
                await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
            return
    await call.message.edit_reply_markup(reply_markup=pagination_obj())


async def operator_handler(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['operator'] = call.data
    all_data = await state.get_data()
    service: str = all_data.get('service')
    country: str = all_data.get('country')
    operator: str = all_data.get('operator')
    operator_info = GetPrice(country, service)
    d_dict = operator_info()[country][service][operator]
    if not d_dict['count']:
        await call.message.delete()
        await call.answer(_('empty'), show_alert=True)
        if data['type'] == 'top':
            countries_btn = TopCountries_Btn(data['count_obj'])
            await call.message.answer(_('choose_top10'), reply_markup=countries_btn())
            await Purchase.top.set()
        else:
            pagination_obj = Pagination()
            await call.message.answer(_('choose_type_country'), reply_markup=pagination_obj())
            await Purchase.country.set()
    else:
        await generate_confirmation_message(call, state)


async def generate_confirmation_message(call, state):
    await call.message.delete()
    all_data = await state.get_data()
    service: str = all_data.get('service')
    country: str = all_data.get('country')
    operator: str = all_data.get('operator')
    operator_info = GetPrice(country, service)
    d_dict = operator_info()[country][service][operator]
    cost = change_price(d_dict['cost'])
    await state.update_data(cost=cost)
    text = f"<b>{_('confirm_text')}\n\n{_('service')}: <i>{service.title()}</i>\n" \
           f"\n{_('country')}: <i>{country.title()}</i>\n\n" \
           f"{_('operator')}: <i>{operator.title()}</i>\n\n{_('cost')}: {cost} </b>"
    await call.message.answer(text, reply_markup=CreateInlineBtn.confirmation())
    await Purchase.confirm.set()


async def confirm_data(call: CallbackQuery, state: FSMContext):
    db = DB_API()
    db.connect()
    data = await state.get_data()
    current_balance = int(db.get_balance(call.from_user.id)[0])
    cost_data: str = data['cost'] if 'new_cost' not in data or data['new_cost'] is None else data['new_cost']
    await state.update_data(last_price=cost_data)
    number_formatted_cost = int(cost_data.replace(',', '').replace('сум', '').split('.')[0])
    if current_balance >= number_formatted_cost:
        await call.message.delete()
        await Purchase.purchase.set()
        await purchase_phone_number(call, state)
    else:
        await call.answer(_('not_enough_money'), show_alert=True)


async def use_bonuses(call: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    await call.message.delete()  # top_btn = [{'minus_ten': '-10'},{'minus_one':'-'}, {'plus_one':'+'}, {'plus_ten': '+10'}]
    db_api = DB_API()
    db_api.connect()
    all_bonuses = db_api.get_bonus(call.from_user.id)[0]
    use_bonuses_count = all_data['bonus_count'] if 'bonus_count' in all_data else 0
    description = f"""
    <b>{_('your_bonuses')}: {all_bonuses}</b> 🌟\n
<b>{_('use_bonuses')}: {use_bonuses_count}</b> 🌟
    """
    bonuses_btn = Bonuses()
    await call.message.answer(description, reply_markup=bonuses_btn())
    await Purchase.bonus.set()


async def handle_bonuses_change(call: CallbackQuery, state: FSMContext):
    db_api = DB_API()
    db_api.connect()
    all_bonuses = db_api.get_bonus(call.from_user.id)[0]
    use_bonuses_count = 0
    all_data = await state.get_data()
    if 'bonus_count' in all_data:
        use_bonuses_count = all_data['bonus_count']
    call_data = call.data.split(':')[0]
    if call_data == 'minus_ten' and use_bonuses_count > 0:
        use_bonuses_count -= 25
    elif call_data == 'minus_one' and use_bonuses_count > 0:
        use_bonuses_count -= 5
    elif call_data == 'plus_one' and use_bonuses_count < all_bonuses:
        use_bonuses_count += 5
    elif call_data == 'plus_ten' and use_bonuses_count < all_bonuses:
        use_bonuses_count += 25
    elif call_data == 'use_all':
        use_bonuses_count = all_bonuses
    if use_bonuses_count < 0 or use_bonuses_count > all_bonuses:
        await call.answer(_('limit'), show_alert=True)
    else:
        if use_bonuses_count >= 1000:
            use_bonuses_count = 1000
        await state.update_data(bonus_count=use_bonuses_count)
        description = f"""
<b>{_('your_bonuses')}: {all_bonuses}</b> 🌟\n
<b>{_('use_bonuses')}: {use_bonuses_count}</b> 🌟
        """
    try:
        bonuses_btn = Bonuses()
        await call.message.edit_text(description, reply_markup=bonuses_btn())
    except Exception:
        await call.answer(_('limit'), show_alert=True)


async def confirm_bonus(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'bonus_count' in data:
        new_cost = await percent_from_bonus(data['bonus_count'])
        percent_bonus = float('{:.1f}'.format(new_cost))
        if percent_bonus > 100:
            percent_bonus = 100
        await call.message.delete()
        all_data = await state.get_data()
        service: str = all_data.get('service')
        country: str = all_data.get('country')
        operator: str = all_data.get('operator')
        old_cost: str = all_data.get('cost')
        old_cost_float = float(old_cost.replace(',', '').replace('сум', ''))
        new_cost = '{:,.2f} сум'.format(old_cost_float - ((percent_bonus / 100) * old_cost_float))
        text = f"<b>{_('confirm_text')}\n\n{_('service')}: <i>{service.title()}</i>\n" \
               f"\n{_('country')}: <i>{country.title()}</i>\n\n" \
               f"{_('operator')}: <i>{operator.title()}</i>\n\n{_('cost')}: <s>{old_cost}</s> - {percent_bonus}% = {new_cost}</b>"
        await call.message.answer(text, reply_markup=CreateInlineBtn.confirmation())
        await state.update_data(new_cost=new_cost)
        await Purchase.confirm.set()
    else:
        await call.answer(_('choose_bonus'), show_alert=True)


async def purchase_phone_number(call: CallbackQuery, state: FSMContext):
    await call.message.answer(_('trying_to_get_number'), reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    buy = Buy(data['country'], data['operator'], data['service'])
    import asyncio
    res = await asyncio.create_task(buy.purchase_number())
    if res != 'empty':
        text = await normalize_response(res['id'], res['created_at'], res['phone'],
                                        res['product'], res['status'], res['expires'],
                                        res['sms'], res['country'], res['operator'], data['last_price'])
        await call.message.answer(text, reply_markup=CreateInlineBtn.purchase_number(), parse_mode='MarkDown')
        await state.update_data(product_id=res['id'])
        await state.update_data(phone=res['phone'])
        await Purchase.purchase.set()
    if res == 'failed':
        await state.finish()
        await call.message.answer(_('smth_wrong'))


async def get_sms_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = DB_API()
    db.connect()
    buy = Buy()
    res = None
    match call.data:
        case 'getsms':
            res = await buy.get_sms(data['product_id'])
            sms_code: list = res['sms']
            if len(sms_code) > 0:
                last_price: str = data['last_price']
                formatted_price = int(last_price.replace(',', '').replace('сум', '').split('.')[0])
                balance = db.get_balance(call.from_user.id)[0]
                left_price = balance - formatted_price
                db.update_balance(call.from_user.id, left_price)
                if 'bonus_count' in data:
                    bonus = Bonus()
                    await bonus.remove_bonus(data['bonus_count'])
        # case 're_buy':
        #     formatted_phone = data['phone'].replace('+','')
        #     res = buy.re_buy(data['service'],formatted_phone)
        case 'cancel_order':
            res = await buy.cancel_order(data['product_id'])
            await call.message.answer(_('canceled'), reply_markup=CreateBtn.MenuBtn())
            await state.finish()
        # case 'banned':
        #     res = buy.banned(data['product_id'])
        #     await call.message.answer(_('blocked'))
        #     await state.finish()
        case 'finish_order':
            res = await buy.finish_order(data['product_id'])
            if res == 'empty':
                await call.answer(_('not_finished'), show_alert=True)
            else:
                await state.finish()
                await call.message.answer(_('finished'), reply_markup=CreateBtn.MenuBtn())
    if res != 'empty' and res is not None:
        await call.message.delete()
        text = await normalize_response(res['id'], res['created_at'], res['phone'],
                                        res['product'], res['status'], res['expires'],
                                        res['sms'], res['country'], res['operator'], data['last_price'])
        await call.message.answer(text, reply_markup=CreateInlineBtn.purchase_number(), parse_mode='MarkDown')

    if call.data == 'no_sms':
        await call.answer(_('sms_notification'), show_alert=True)


async def normalize_response(product_id, created_at, phone, product, status, expires, sms, country, operator,
                             last_price):
    parsed_output_expires = parse(expires)
    modified_datetime_expires = parsed_output_expires + timedelta(hours=5)

    formatted_output_expires = modified_datetime_expires.strftime("%Y-%m-%d %H:%M:%S")

    parsed_output_created = parse(created_at)
    modified_datetime_created = parsed_output_created + timedelta(hours=5)

    formatted_output_created_at = modified_datetime_created.strftime("%Y-%m-%d %H:%M:%S")

    code_list = []
    sms = sms if sms is not None else []
    for i in sms:
        code_list.append(i['code'])
    text = f'''
🆔: {product_id}

{_('phone')}: `{phone}`
{_('sms')}: `{code_list}`

{_('created_at')}: *{formatted_output_created_at}*
{_('expires')}: *{formatted_output_expires}*

{_('price')}: *{last_price}*
{_('status')}: *{status}*

{_('service_text')}: *{str(product).upper()}*
{_('country_text')}: *{str(country).upper()}*
{_('operator_text')}: *{str(operator).upper()}*


            '''
    return text


async def cancel(msg: Message, state: FSMContext):
    await msg.answer('❌', reply_markup=CreateBtn.MenuBtn())
    await state.finish()


def register_callbacks(dp: Dispatcher):
    dp.register_message_handler(cancel, lambda message: message.text == _("cancel_balance"), state='*')
    dp.register_callback_query_handler(back_btn, text='back', state=Purchase.all_states_names)
    dp.register_callback_query_handler(service_handler, state=Purchase.service)
    dp.register_callback_query_handler(country_choose_handler, state=Purchase.country_choose)
    dp.register_callback_query_handler(top10_handler, state=Purchase.top)
    dp.register_callback_query_handler(country_handler, state=Purchase.country)
    dp.register_callback_query_handler(operator_handler, state=Purchase.operator)
    dp.register_callback_query_handler(confirm_data, state=Purchase.confirm, text='confirm_callback')
    dp.register_callback_query_handler(use_bonuses, state=Purchase.confirm, text='bonus')
    dp.register_callback_query_handler(handle_bonuses_change, state=Purchase.bonus, text_contains='change')
    dp.register_callback_query_handler(confirm_bonus, state=Purchase.bonus, text='confirm_bonus')
    # dp.register_callback_query_handler(other_payments, state=Purchase.payment, text='click')
    # dp.register_callback_query_handler(other_payments, state=Purchase.payment, text='qiwi')
    # dp.register_callback_query_handler(payme_callback, state=Purchase.payment, text='payme')
    # dp.register_callback_query_handler(check_payment, state=Purchase.payment, text='confirm_payment')
    dp.register_callback_query_handler(get_sms_handler, state=Purchase.purchase)
