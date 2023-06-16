from loader import dp
from aiogram.types import CallbackQuery

@dp.callback_query_handler(text='back_to_menu')
async def backMenu(call:CallbackQuery):
    await call.message.delete()
    await call.message.answer('Главное меню: ')