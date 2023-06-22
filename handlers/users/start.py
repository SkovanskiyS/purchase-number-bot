import logging, pprint

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.default.default_kb import CreateBtn
from keyboards.inline.default_kb import CreateInlineBtn
from keyboards.inline.callback_data import pay_callback


async def start_handler(msg: Message):
    create_btn = CreateBtn()
    await msg.answer('Welcome to Purchase Number BOT', reply_markup=create_btn.mainMenuBtn())


async def buy_number(msg: Message):
    await msg.answer('Выберите тип платежа: ', reply_markup=CreateInlineBtn.payments())


async def payme_handler(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    logging.info(callback_data)
    await call.message.answer('Here is the link to make payment', reply_markup=CreateInlineBtn.paymeUrl())


async def click_hander(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Here is the link to make payment:', reply_markup=CreateInlineBtn.clickUrl())


async def cancel(call: CallbackQuery):
    await call.answer('Вы отменили заказ!', show_alert=True)
    await call.message.edit_reply_markup()


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'))
    dp.register_message_handler(start_handler, Text(equals='Назад'))
    dp.register_message_handler(buy_number, Text(equals='Купить номер'))
    dp.register_callback_query_handler(payme_handler, pay_callback.filter(name='payme'))
    dp.register_callback_query_handler(click_hander, text_contains='click')
    dp.register_callback_query_handler(cancel, text='cancel')
