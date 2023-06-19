from main import dp, bot
from config import ADMIN_ID
from aiogram.types import Message


async def send_to_admin(dp):
    await bot.send_message(ADMIN_ID, 'Bot Has Started')

@dp.message_handler()
async def echo(message:Message):
    await message.answer(message.text)
