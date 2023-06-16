from time import sleep

from aiogram.dispatcher import FSMContext

from data.config import admins, ADMIN_CHAT_ID
from loader import dp, db, bot
from aiogram import types

from states.register_state import MailingText


@dp.message_handler(text="📤Рассылка",chat_id=admins)
async def mailing(message: types.Message):
    await message.answer('Пришлите текст рассылки: \nОтмена: /cancel')
    await MailingText.mailing_text.set()


@dp.message_handler(state=MailingText.mailing_text, user_id=admins)
async def enter_text(message: types.Message,state=FSMContext):
    if message.text=='/cancel':
        await message.answer("Отменено")
        await state.finish()
    else:
        text = message.text
        usersId = db.select_user_id()
        for value in usersId:
            try:
                await message.answer(f"Успешно отправлено пользователю:\n<b>@{db.select_user(value[0])[1]}</b>")
                sleep(0.3)
            except Exception as err:
                print(err)
    await state.finish()

