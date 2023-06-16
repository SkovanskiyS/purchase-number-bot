from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from handlers.users.settings import cancel_handler
from keyboards.default.menu_btn import menuR_btns
from keyboards.inline.communication_inline import chatting_btn, recall_btns
from loader import dp, db, bot
from data.config import admins
from states.register_state import NewName, ActualNumber


@dp.message_handler(Text(equals="📞Связаться"))
async def communication_handler(message: types.Message):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
        await message.answer("👇Выберите способ из нижеперечисленного списка:", reply_markup=chatting_btn)
    else:
        await message.answer(
            "🛑<b>Вы были заблокированы🚫</b>\nЧтобы разблокировать обратитесь к администратору: @o101xd")


@dp.callback_query_handler(text='recall')
async def recall_inline(call: CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        await call.message.delete()
        await call.message.answer(f"<b>Это Ваш верный номер телефона</b> "
                                  f"{db.select_user(call.from_user.id)[3]}? Если да, нажмите соответствующую кнопку, "
                                  f"если нет, впишите свой актуальный номер телефона здесь", reply_markup=recall_btns)


@dp.callback_query_handler(text='yes')
async def send_phone(call: CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        await call.message.delete()
        await call.message.answer('✅<b>Отлично!</b> наш диспетчер перезвонит Вам в ближайшее время.')

        await call.bot.send_message(admins[0], f"📩<b>Заявка для перезвона</b>\nОт: {db.select_user(call.from_user.id)[2]}"
                                           f"\nЮзернейм: @{call.from_user.username}\nНомер телефона: +{db.select_user(call.from_user.id)[3]}")


@dp.callback_query_handler(text='leave_phone')
async def leave_phone(call: CallbackQuery, state=FSMContext):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        await call.message.delete()
        await call.message.answer("Введите свой актуальный номер телефона:\nОтмена: /cancel",
                                  reply_markup=ReplyKeyboardRemove())
        await ActualNumber.actual_number.set()


@dp.message_handler(state=ActualNumber.actual_number)
async def new_phone(message: types.Message, state=FSMContext):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
    # db.update_phone(message.text,message.from_user.id)
        await message.answer('✅<b>Отлично!</b> наш диспетчер перезвонит Вам в ближайшее время.', reply_markup=menuR_btns)
        await bot.send_message(admins[0], f"📩<b>Заявка для перезвона</b>\nОт: {db.select_user(message.from_user.id)[2]}"
                                          f"\nЮзернейм: @{message.from_user.username}\nНомер телефона: +{message.text}")
        await state.finish()


@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state=FSMContext):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Отменено", reply_markup=menuR_btns)
