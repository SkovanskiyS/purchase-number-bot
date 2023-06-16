from data.config import admins
from handlers.admin_panel.admin_command import admin_panel
from loader import dp
from aiogram import types

@dp.message_handler(commands=['admin','start'],chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def admin_chat(message:types.Message):
    await admin_panel(message)


