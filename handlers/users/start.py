import sqlite3

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from loader import dp, db
from aiogram.dispatcher import FSMContext
from states.register_state import SignUp
from aiogram.dispatcher.filters import Command

from keyboards.default.menu_btn import menuR_btns


@dp.message_handler(Command("start"))
async def welcome_message(message: types.Message):
    user_id = message.from_user.id
    result = db.get_white_list(message.from_user.id)

    if result is None or result[0]==0:
        try:
            if db.user_is_exist(user_id)[0] == user_id:
                await message.answer('✈<b>Добро пожаловать</b> в главное меню чат-бота Управляющей компании "УЭР-ЮГ". '
                                     'Здесь вы можете остановить заявку для управляющей компании или направить свое предложение по управлению домом. '
                                     'Просто воспользуйтесь кнопками <b>меню</b>, чтобы взаимодействовать с функциями бота:',
                                     reply_markup=menuR_btns)
        except:
            await message.answer(
                "🌼<b>Доброго времени суток</b>, бот создан, чтобы обрабатывать заявки и обращения пользователей. Чтобы воспользоваться этим, пришлите для начала Ваше <b>Имя</b> и <b>Фамилия</b>",
                reply_markup=ReplyKeyboardRemove())
            await SignUp.name.set()
    else:
        await message.answer(
            "🛑<b>Вы были заблокированы🚫</b>\nЧтобы разблокировать обратитесь к администратору: @o101xd")

@dp.message_handler(state=SignUp.name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    from handlers.others.check_unicode import is_kiril
    name_and_surname = answer.split(' ')
    if ' ' in answer and is_kiril(answer) and name_and_surname[0].istitle() and name_and_surname[1].istitle():
        async with state.proxy() as data:
            data['full_name'] = answer
        from keyboards.default import signUp_btn
        await message.answer(
            "📞Теперь отправьте Ваш <b>номер телефона</b> через <b>+7</b> или <b>+998</b> следующим сообщением:",
            reply_markup=signUp_btn.phone_number_btn)

        await SignUp.next()
    else:
        await message.answer(
            "⛔📛<b>Имя</b> и <b>Фамилия</b> должны быть введены через один пробел, и должны быть написаны через кириллицу. Также должны быть заглавные буквы. <b>Учтите формат и попробуйте снова:</b>")
        # await SignUp.name.set()
    # phone_number_btn = types.ReplyKeyboardRemove()


@dp.message_handler(content_types=['contact', 'text'], state=SignUp.phone_number)
async def get_name(message: types.Message, state: FSMContext):
    warn_text = "⛔❌⛔<b>Номер телефона</b> должен содержать 11 или 13 цифр и должен обязательно содержать в начале <b>+7 или +998. Учтите формат и попробуйте снова:</b>"
    phone_number = ""
    if message.text == None:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    phone_number = phone_number.replace(' ', '')

    if phone_number.startswith("+7") or phone_number.startswith("998") and len(phone_number) == 12 or len(phone_number)==13:
        async with state.proxy() as data:
            data['phone_number'] = phone_number
        data = await state.get_data()
        try:
            db.add_user(id=message.from_user.id, fullname=data.get('full_name'), phone=data.get('phone_number'),username=message.from_user.username)
            await message.answer(
                '✅<b>Вы успешно прошли регистрацию</b>\n\n✈<b>Добро пожаловать</b> в главное меню чат-бота Управляющей компании "УЭР-ЮГ". '
                'Здесь вы можете остановить заявку для управляющей компании или направить свое предложение по управлению домом. '
                'Просто воспользуйтесь кнопками <b>меню</b>, чтобы взаимодействовать с функциями бота:',
                reply_markup=menuR_btns)
        except sqlite3.IntegrityError as err:
            await message.answer(str(err))

        await state.reset_state()
    else:
        print(len(phone_number))
        await message.answer(warn_text)
