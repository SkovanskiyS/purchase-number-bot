from aiogram.dispatcher import FSMContext

from keyboards.inline.leave_request_btn import leave_request_inline
from loader import dp,db
from aiogram import types

from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals="📛Оставить заявку"))
async def bot_leave_request(message:types.Message,state:FSMContext):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
        await message.answer("📛👇📛<b>Выберите категорию</b>, по которой Вы хотите оставить заявку в УК:",reply_markup=leave_request_inline)
        await state.finish()

