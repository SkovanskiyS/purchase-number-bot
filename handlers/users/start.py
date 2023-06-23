from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from misc.states import Registration
from keyboards.default.default_kb import CreateBtn


async def start_handler(msg: Message):
    await msg.answer('Welcome to Purchase Number BOT\nPlease enter your name: ', reply_markup=ReplyKeyboardRemove())
    await Registration.NAME.set()
    # or Registration.NAME.first() | next() | last()


async def acquire_name(msg: Message, state: FSMContext):
    answer_name = msg.text
    # 1 example
    # async with state.proxy() as data:
    #     data['name'] = answer_name

    # 2 example
    # await state.update_data(name=answer_name)

    # 3 example
    await state.update_data(
        {'name': answer_name}
    )

    await msg.answer('Great job, %s!\nNow, enter your surname: ' % answer_name)
    await Registration.next()


async def acquire_surname(msg: Message, state: FSMContext):
    answer_surname = msg.text
    await state.update_data(
        {'surname': answer_surname}
    )

    await msg.answer('You are very very close, last one step left:\nPlease enter your phone number: ',
                     reply_markup=CreateBtn.request_phone_number())
    await Registration.next()


async def acquire_phone_number(msg: Message, state: FSMContext):
    answer_phone_number = ''
    if msg.text is None:
        answer_phone_number = msg.contact.phone_number
    else:
        answer_phone_number = msg.text
    await state.update_data(
        {'phone_number': answer_phone_number}
    )
    await msg.answer('<b>Congratulations!</b>\nYou have finished the registration form.',reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    all_data = f'Your name: {data["name"]}\nYour surname: {data["surname"]}\nYour cell number: {data["phone_number"]}'
    await msg.answer(all_data)
    await state.finish()

#
#
# async def buy_number(msg: Message):
#     await msg.answer('Выберите тип платежа: ', reply_markup=CreateInlineBtn.payments())
#
#
# async def payme_handler(call: CallbackQuery, callback_data: dict):
#     await call.message.delete()
#     logging.info(callback_data)
#     await call.message.answer('Here is the link to make payment', reply_markup=CreateInlineBtn.paymeUrl())
#
#
# async def click_hander(call: CallbackQuery):
#     await call.message.delete()
#     await call.message.answer('Here is the link to make payment:', reply_markup=CreateInlineBtn.clickUrl())
#
#
# async def cancel(call: CallbackQuery):
#     await call.answer('Вы отменили заказ!', show_alert=True)
#     await call.message.edit_reply_markup()


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'), state=None)
    dp.register_message_handler(acquire_name, state=Registration.NAME)
    dp.register_message_handler(acquire_surname, state=Registration.SURNAME)
    dp.register_message_handler(acquire_phone_number, content_types=['contact','text'],
                                state=Registration.PHONE_NUMBER)

    # dp.register_message_handler(start_handler, Text(equals='Назад'))
    # dp.register_message_handler(buy_number, Text(equals='Купить номер'))
    # dp.register_callback_query_handler(payme_handler, pay_callback.filter(name='payme'))
    # dp.register_callback_query_handler(click_hander, text_contains='click')
    # dp.register_callback_query_handler(cancel, text='cancel')
