from aiogram.dispatcher.filters import Command
from aiogram import types
from loader import dp, bot
from keyboards.default.default_kb import rep,CreateBtn


@dp.message_handler(Command('start'))
async def start_handler(msg: types.Message):
    create_btn = CreateBtn()
    await msg.answer('Welcome to Los Pollos Hermanos Family',reply_markup=create_btn.mainMenuBtn())






