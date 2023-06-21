from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from keyboards.default.default_kb import CreateBtn
from keyboards.inline.default_kb import CreateInlineBtn


@dp.message_handler(Command('start'))
async def start_handler(msg: Message):
    create_btn = CreateBtn()
    await msg.answer('Welcome to Purchase Number BOT', reply_markup=create_btn.mainMenuBtn())


@dp.message_handler(Text(equals='Купить номер'))
async def but_number(msg: Message):
    await msg.answer('Выберите тип платежа: ', reply_markup=CreateInlineBtn.mainMenuBtn())


@dp.callback_query_handler(text_contains='payme')
async def payme_handler(call: CallbackQuery):
    await call.message.answer('You choosed payme')

