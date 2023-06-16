from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import admins
from keyboards.default.admin_btns.admin_panel_menu import main_admin_panel
from loader import dp

@dp.message_handler(Command("admin"),chat_id = admins)
async def admin_panel(message:types.Message):
    await message.answer('Добро пожаловать в админ панель:',reply_markup=main_admin_panel)
