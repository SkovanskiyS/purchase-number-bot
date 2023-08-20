from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from database.dbApi import DB_API
from i18n import _
from keyboards.default.creator import CreateBtn
from keyboards.inline.creator import CreateInlineBtn
from misc.states import Balance
from services.Payments.payme import PaymePay
from services.Payments.payme import check_status_of_payment


async def balance_handler(call: CallbackQuery, state: FSMContext):
    # Выберите сумму для пополнения:\nИмейте ввиду, после пополния вы не сможете вывести деньги из виртуального кошелька'
    await call.message.answer(_('notification'), reply_markup=CreateBtn.BalanceCancel())
    await call.message.answer(_('balance_add_info'), reply_markup=CreateInlineBtn.count_of_money())
    await Balance.balance_add.set()


async def balance_add(call: CallbackQuery, state: FSMContext):
    if call.data == 'other_sum':
        await Balance.balance_count.set()
        await balance_add_other(call, state)
    else:
        await call.message.delete()
        await state.update_data(sum=call.data)
        await Balance.payment.set()
        await call.message.answer(f'{_("choose")}', reply_markup=CreateInlineBtn.payment())


async def balance_add_other(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(_('write_sum'))


async def balance_other_sum(msg: Message, state: FSMContext):
    # проверка на сумму
    chosen_sum = msg.text
    formatted_sum = chosen_sum.replace(' ', '')
    if formatted_sum.isdigit() and 1000 <= int(formatted_sum) <= 1000000:
        await state.update_data(sum=chosen_sum)
        await Balance.payment.set()
        await msg.answer(f'{_("choose")}', reply_markup=CreateInlineBtn.payment())
    else:
        await msg.answer(_('write_sum'))


async def payme_bill(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    amount = data['sum'] + '00'
    amount = amount.replace(' ', '')
    payme_obj = PaymePay(amount, str(msg.from_user.id))
    url_to_pay = await payme_obj.bill()
    #url_to_pay = 'https://payme.uz/checkout/64e251ae3df64755957e78f2?back=null&timeout=15000&lang=ru'
    await state.update_data(url=url_to_pay)
    await msg.answer(_('check_payment'), reply_markup=CreateInlineBtn.pay(url_to_pay))


async def payment_choose(call: CallbackQuery, state: FSMContext):
    await state.update_data(payment=call.data)
    await Balance.bill.set()
    if call.data == 'payme':
        await payme_bill(call.message, state)


async def check_payment(call: CallbackQuery, state: FSMContext):
    try:
        db_api = DB_API()
        db_api.connect()
        #await call.message.answer(_('checking'))
        #await call.answer(_('checking'),show_alert=True)
        #await call.message.delete()
        data = await state.get_data()
        url_to_check = data['url']
        paid = await check_status_of_payment(url_to_check)
        if paid is True:
            await call.message.answer(_('paid'), reply_markup=CreateBtn.MenuBtn())

            amount = int(data['sum'])
            db_amount = int(db_api.get_balance(call.from_user.id)[0])
            amount_to_add = amount + db_amount
            db_api.update_balance(call.from_user.id, amount_to_add)
            await state.finish()
        elif paid is False:
            await call.answer(_('not_paid'), show_alert=True)
            #await call.message.answer(_('check_payment'), reply_markup=CreateInlineBtn.pay(data['url']))
        else:
            await call.message.bot.send_message(996346575, f'{call.from_user.id} has a problem with payment:\n{paid}')
    except Exception as err:
        await call.message.bot.send_message(996346575, f'{call.from_user.id} has a problem with payment:\n{err}')


def register_balance_add(dp: Dispatcher):
    dp.register_callback_query_handler(balance_handler, text='replenish')
    dp.register_callback_query_handler(balance_add, state=Balance.balance_add)
    dp.register_callback_query_handler(balance_add_other, state=Balance.balance_count)
    dp.register_message_handler(balance_other_sum, state=Balance.balance_count)
    dp.register_callback_query_handler(payment_choose, state=Balance.payment)
    dp.register_message_handler(payme_bill, text='payme', state=Balance.bill)
    dp.register_callback_query_handler(check_payment, text='confirm_payment', state=Balance.bill)
