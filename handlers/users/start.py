import logging, pprint

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.default.default_kb import CreateBtn
from keyboards.inline.default_kb import CreateInlineBtn


async def start_handler(msg: Message):
    create_btn = CreateBtn()
    await msg.answer('Welcome to Purchase Number BOT', reply_markup=create_btn.mainMenuBtn())


async def buy_number(msg: Message):
    await msg.answer('Выберите тип платежа: ', reply_markup=CreateInlineBtn.payments())


async def payme_handler(call: CallbackQuery):
    logging.info(f'Call Data: {call.data}')
    await call.message.answer('Here is the link to make payment', reply_markup=CreateInlineBtn.paymeUrl())
    print(call.data.split(':')[1])


def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command('start'))
    dp.register_message_handler(start_handler, Text(equals='Назад'))
    dp.register_message_handler(buy_number, Text(equals='Купить номер'))
    dp.register_callback_query_handler(payme_handler, text_contains='payme')
