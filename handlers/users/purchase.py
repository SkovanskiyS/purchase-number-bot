from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.dbApi import DB_API
from handlers.users.keyboard import cancel_purchase, buy_handler
from i18n import _
from keyboards.inline.creator import Bonuses
from keyboards.inline.creator import Pagination, Operator, CreateInlineBtn
from misc.bonuses import Bonus
from misc.cost_modification import change_price, percent_from_bonus
from misc.states import Purchase
from services.API_5sim.fetch_operator import GetPrice
from services.Payments.payme import PaymePay
from services.API_5sim.purchase import Buy
from dateutil.parser import parse
from keyboards.default.creator import CreateBtn
from data.config import load_config


async def back_btn(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    current_state = current_state.split(':')[1]
    data = await state.get_data()
    if current_state == 'service':
        await cancel_purchase(call.message, state)
    elif current_state == 'country':
        await call.message.delete()
        await buy_handler(call.message)
    elif current_state == 'operator':
        pagination_obj = Pagination()
        await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
        await Purchase.country.set()
        await call.message.delete()
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
            await state.update_data(bonus_count=None)
        print(data)
        await generate_confirmation_message(call, state)


async def service_handler(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['service'] = call.data
    await call.message.delete()
    pagination_obj = Pagination()
    await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
    await Purchase.next()


async def country_handler(call: CallbackQuery, state: FSMContext):
    pagination_obj = Pagination()
    match call.data:
        case 'next':
            pagination_obj.page += 1
        case 'previous':
            pagination_obj.page -= 1
        case 'page':
            pagination_obj.page += 5
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
        pagination_obj = Pagination()
        await call.message.delete()
        await call.answer(_('empty'), show_alert=True)
        await call.message.answer(_('empty'))
        await Purchase.country.set()
        await call.message.answer(_('choose_country'), reply_markup=pagination_obj())
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
    data = await state.get_data()
    await call.message.delete()
    text = f'{_("choose")}'
    print(data)
    await call.message.answer(text, reply_markup=CreateInlineBtn.payment())
    await Purchase.payment.set()


async def use_bonuses(call: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    print(all_data)
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
        use_bonuses_count -= 30
    elif call_data == 'minus_one' and use_bonuses_count > 0:
        use_bonuses_count -= 1
    elif call_data == 'plus_one' and use_bonuses_count < all_bonuses:
        use_bonuses_count += 1
    elif call_data == 'plus_ten' and use_bonuses_count < all_bonuses:
        use_bonuses_count += 30
    elif call_data == 'use_all':
        use_bonuses_count = all_bonuses

    if use_bonuses_count < 0 or use_bonuses_count > all_bonuses:
        await call.answer(_('limit'), show_alert=True)
    else:
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


async def payme_callback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cost_data: str = data['cost'] if 'new_cost' not in data or data['new_cost'] is None else data['new_cost']
    await state.update_data(last_price=cost_data)
    formatting = cost_data.replace('сум', '').replace(',', '')
    formatted_output = f'{float(formatting) * 100:.2f}'
    if formatted_output == '0.00':
        await state.update_data(paid=True)
        await call.message.delete()
        await call.message.answer(_('paid_check'), reply_markup=CreateInlineBtn.confirm_btn())
    else:
        payme_obj = PaymePay(formatted_output, data['service'] + ' ' + data['country'])
        url_to_pay = await payme_obj.bill()
        # url_to_pay = 'https://payme.uz/checkout/64b03107bb51fe5bee562bd5?back=null&timeout=15000&lang=ru'
        await state.update_data(url_for_payment=url_to_pay)
        await call.message.delete()
        await call.message.answer(_('check_payment'), reply_markup=CreateInlineBtn.pay(url_to_pay))


async def check_payment(call: CallbackQuery, state: FSMContext):
    await call.message.answer(_('checking'))
    data = await state.get_data()
    print(data)
    paid = None
    config = load_config('../../.env')
    if 'paid' not in data:
        url_to_check = data['url_for_payment']
        payme_obj = PaymePay(0, '')
        paid = await payme_obj.check_status_of_payment(url_to_check)
    else:
        paid = True
    if paid or call.from_user.id in config.tg_bot.ADMINS:
        await call.answer(_('paid'), show_alert=True)
        await call.message.delete()
        await call.message.answer(_('trying_to_get_number'))

        data = await state.get_data()
        buy = Buy(data['country'], data['operator'], data['service'])
        res = await buy.purchase_number()
        if res != 'empty':
            bonus = Bonus()
            await bonus.remove_bonus(data['bonus_count'])
            text = await normalize_response(res['id'], res['created_at'], res['phone'],
                                            res['product'], res['status'], res['expires'],
                                            res['sms'], res['country'], res['operator'], data['last_price'])
            await call.message.answer(text, reply_markup=CreateInlineBtn.purchase_number(), parse_mode='MarkDown')
            await state.update_data(product_id=res['id'])
            await state.update_data(phone=res['phone'])
            await Purchase.purchase.set()
    else:
        await call.answer(_('not_paid'), show_alert=True)
        await payme_callback(call, state)


async def get_sms_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    buy = Buy()
    res = None
    match call.data:
        case 'getsms':
            res = await buy.get_sms(data['product_id'])
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
    if res != 'empty':
        await call.message.delete()
        text = await normalize_response(res['id'], res['created_at'], res['phone'],
                                        res['product'], res['status'], res['expires'],
                                        res['sms'], res['country'], res['operator'], data['last_price'])
        await call.message.answer(text, reply_markup=CreateInlineBtn.purchase_number(), parse_mode='MarkDown')


async def normalize_response(product_id, created_at, phone, product, status, expires, sms, country, operator,
                             last_price):
    parsed_output_expires = parse(expires)
    formatted_output_expires = parsed_output_expires.strftime("%Y-%m-%d %H:%M:%S")

    parsed_output_created = parse(created_at)
    formatted_output_created_at = parsed_output_created.strftime("%Y-%m-%d %H:%M:%S")

    code_list = []
    sms = sms if sms is not None else []
    for i in sms:
        code_list.append(i['code'])
    text = f'''
🆔: {product_id}

{_('phone')}: *{phone}*
{_('sms')}: `{code_list}`

{_('created_at')}: *{formatted_output_created_at}*
{_('expires')}: *{formatted_output_expires}*

{_('price')}: *{last_price}*
{_('status')}: *{status}*

{_('service_text')}: {product}
{_('country_text')}: {country}
{_('operator_text')}: {operator}


            '''
    return text


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(back_btn, text='back', state=Purchase.all_states_names)
    dp.register_callback_query_handler(service_handler, state=Purchase.service)
    dp.register_callback_query_handler(country_handler, state=Purchase.country)
    dp.register_callback_query_handler(operator_handler, state=Purchase.operator)
    dp.register_callback_query_handler(confirm_data, state=Purchase.confirm, text='confirm_callback')
    dp.register_callback_query_handler(use_bonuses, state=Purchase.confirm, text='bonus')
    dp.register_callback_query_handler(handle_bonuses_change, state=Purchase.bonus, text_contains='change')
    dp.register_callback_query_handler(confirm_bonus, state=Purchase.bonus, text='confirm_bonus')
    dp.register_callback_query_handler(payme_callback, state=Purchase.payment, text='payme')
    dp.register_callback_query_handler(check_payment, state=Purchase.payment, text='confirm_payment')
    dp.register_callback_query_handler(get_sms_handler, state=Purchase.purchase)
