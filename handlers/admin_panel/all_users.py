from time import sleep

import telegram as telegram
from aiogram import types
from aiogram.types import ParseMode

from data.config import admins, ADMIN_CHAT_ID
from loader import dp,db


@dp.message_handler(text="📜Все пользователи🔎", chat_id=admins)
async def search(message:types.Message):
    all_users = db.select_all_users()
    for i in all_users:
        if i[4]==0:
            status = "<b>Имеет доступ</b>"
        else:
            status = "<b>Не имеет доступ</b>"
        await message.answer(f"<i>ID:</i> <b>{i[0]}</b>\n<i>Юзернейм</i>: <b>@{i[1]}</b>\n<i>Имя</i>: <b>{i[2]}</b>\n<i>Номер телефона</i>: <b>+{i[3]}</b>\n<i>Статус:</i> {status}")
        sleep(0.3)
