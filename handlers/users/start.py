from aiogram.dispatcher.filters import Command
from aiogram import types
from loader import dp, bot

@dp.message_handler(Command('start'))
async def start_handler(msg: types.Message):
    await msg.answer('Welcome to Los Pollos Hermanos Family')






