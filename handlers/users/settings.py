from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from handlers.others.check_unicode import is_kiril
from keyboards.default.menu_btn import menuR_btns
from keyboards.inline.settings_inline import setting_inline_btn
from loader import dp,db
from aiogram import types

from states.register_state import NewName


@dp.message_handler(Text(equals="⚙Настройки"))
async def settings(message:types.Message):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
        await message.answer(f"""Тут Вы сможете поменять <b>Имя</b> и
<b>Фамилию</b> в Базе данных нашего бота
или же можете поменять Ваш <b>номер телефона</b>, если Вы изначально вводили что-то неверно. Выберите, что хотите поменять или вернитесь назад в главное меню:\n\n<b>Ваш профиль:</b>\n<i>Имя и Фамилия:</i> <b>{db.select_user(message.from_user.id)[2]}</b>\n<i>Номер Вашего телефона:</i> <b>{db.select_user(message.from_user.id)[3]}</b>""",reply_markup=setting_inline_btn)

@dp.message_handler(state="*",commands='cancel')
@dp.message_handler(Text(equals='cancel',ignore_case=True),state="*")
async def cancel_handler(message:types.Message,state=FSMContext):
    result = db.get_white_list(message.from_user.id)
    if result[0]==0:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Отменено",reply_markup=menuR_btns)

@dp.callback_query_handler(text="change_name")
async def set_new_name(call:CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        result = db.get_white_list(call.from_user.id)
        if result[0]==0:
            await call.message.delete()
            await call.message.answer('🛠Отправьте свое<b> Имя</b> и<b> Фамилию</b>, чтобы поменять настройки:\nОтмена: /cancel')
            await NewName.new_name.set()

@dp.callback_query_handler(text="change_number")
async def set_new_name(call:CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        if result[0]==0:
            await call.message.delete()
            await call.message.answer('🛠Отправьте свой <b>номер телефона</b>, чтобы поменять настройки:\nОтмена: /cancel')
            await NewName.new_phone.set()
        else:
            await call.message.answer(
                "🛑<b>Вы были заблокированы🚫</b>\nЧтобы разблокировать обратитесь к администратору: @o101xd")

@dp.message_handler(state=NewName.new_phone)
async def get_new_phone(message:types.Message,state=FSMContext):
    phone_number = message.text

    if phone_number.startswith("+7") and len(phone_number) == 12 or phone_number.startswith("+998") and len(
            phone_number) == 13:
        db.update_phone(phone_number,message.from_user.id)
        await state.finish()
        await message.answer("✅🛠✅Настройки <b>имени</b> успешно применены!")
    else:
        await message.answer("⛔❌⛔<b>Номер телефона</b> должен содержать 11 или 13 цифр и должен обязательно содержать в начале <b>+7 или +998. Учтите формат и попробуйте снова:</b>\nОтмена: /cancel")

@dp.message_handler(state=NewName.new_name)
async def get_new_name(message:types.Message,state=FSMContext):
    answer = message.text
    name_and_surname = answer.split(' ')
    if ' ' in answer and is_kiril(answer) and name_and_surname[0].istitle() and name_and_surname[1].istitle():
        db.update_name(answer,message.from_user.id)
        await state.finish()
        await message.answer("✅🛠✅Настройки <b>имени</b> успешно применены!")
    else:
        await message.answer(
            "⛔📛<b>Имя</b> и <b>Фамилия</b> должны быть введены через один пробел, и должны быть написаны через кириллицу. Также должны быть заглавные буквы. <b>Учтите формат и попробуйте снова:</b>\nОтмена: /cancel")

