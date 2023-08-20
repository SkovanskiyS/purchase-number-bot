from datetime import datetime

import pandas as pd
import asyncio
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, InputFile
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.utils.exceptions import BotBlocked


from database.admin_panel import DB_API_ADMIN
from filters.isAdmin import AdminFilter
from keyboards.default.creator import CreateBtn
from misc.states import AdminState


async def start_command(msg: Message):
    await msg.answer('<b>Добро пожаловать в админ панель!</b>', reply_markup=CreateBtn.AdminMenuBtns())


async def all_users(msg: Message):
    db = DB_API_ADMIN()
    db.connect()
    all_users_data = db.get_all_users()
    user_length = len(all_users_data)
    text = f"📢 В данный момент: {user_length} пользователей"
    await convert_to_excel(all_users_data)
    with open('botusers.xlsx', 'rb') as file:
        await msg.bot.send_document(chat_id=msg.chat.id, document=InputFile(file), caption=text)


async def find_user(msg: Message):
    await msg.answer('Введите Telegram ID пользователя: ')
    await AdminState.user_id_search.set()


async def search(msg: Message, state: FSMContext):
    try:
        user_id = msg.text
        db = DB_API_ADMIN()
        db.connect()
        user_info = db.get_user(user_id)
        bot_username = await msg.bot.get_me()
        ref_link = f'https://t.me/{bot_username.username}?start={user_id[0]}'
        dateTime: datetime = user_info[6]
        referrals = db.check_referral(user_id)
        ref_count = len(referrals) if referrals is not None else 0
        caption_text = f"""
<i>ID:</i> <b>{user_info[0]}</b>
<i>Telegram ID: </i><b>{user_info[1]}</b>
<i>Username: </i><b>@{user_info[2]}</b>\n
Имя: <b>{user_info[3]}</b>
Фамилия: <b>{user_info[4]}</b>
Язык: <b>{user_info[5]}</b>\n
Дата регистрации: <b>{dateTime.strftime("%Y-%m-%d %H:%M:%S")}</b>
Бонусы: <b>{user_info[7]}</b>
Рефералы: <b>{ref_count}</b>
Заблокирован: <b>{False if user_info[9] == 0 else True}</b>\n
Рефералы: <b>{ref_link}</b>
            """
        await msg.answer(caption_text)
    except Exception as err:
        await msg.answer('Неверный ID либо такого пользователя не существует!')
    await state.finish()


async def block_user(msg: Message):
    await msg.answer('Введите Telegram ID пользователя: ')
    await AdminState.user_id_block.set()


async def block_user_state(msg: Message, state: FSMContext):
    try:
        db = DB_API_ADMIN()
        db.connect()
        db.block_user(msg.text)
        await msg.answer('Успешно заблокирован!')
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


async def unblock_user(msg: Message):
    await msg.answer('Введите Telegram ID пользователя: ')
    await AdminState.user_id_unblock.set()


async def unblock_user_state(msg: Message, state: FSMContext):
    try:
        db = DB_API_ADMIN()
        db.connect()
        db.unblock_user(msg.text)
        await msg.answer('Успешно разблокирован!')
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


async def change_bonus(msg: Message):
    await msg.answer('Введите Telegram ID пользователя и бонус в виде: ID|КОЛ-ВО БОНУСОВ ')
    await AdminState.bonus.set()


async def change_bonus_state(msg: Message, state: FSMContext):
    try:
        data = msg.text.split('|')
        db = DB_API_ADMIN()
        db.connect()
        if 1000 >= int(data[1]) >= 0:
            db.change_bonus(data[1], data[0])
            await msg.answer('Успешно добавлен!')
        else:
            raise Exception
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


async def referral_check(msg: Message):
    await msg.answer('Введите Telegram ID пользователя: ')
    await AdminState.referral.set()


async def referrals_check_state(msg: Message, state: FSMContext):
    try:
        db = DB_API_ADMIN()
        db.connect()
        data = db.check_referral(msg.text)
        await msg.answer(data)
        await msg.answer('Успешно!')
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


async def delete_user(msg: Message):
    await msg.answer('Введите Telegram ID пользователя: ')
    await AdminState.delete_user.set()


async def delete_user_state(msg: Message, state: FSMContext):
    try:
        db = DB_API_ADMIN()
        db.connect()
        db.delete_user(msg.text)
        await msg.answer('Успешно удалено!')
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


async def convert_to_excel(data):
    df = pd.DataFrame(data,
                      columns=['ID', 'User ID', 'Username', 'First Name', 'Language', 'Reg Date',
                               'Bonuses',
                               'Referral', 'Blocked', 'Page', 'Balance'])
    writer = pd.ExcelWriter('botusers.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='users_data', index=False)
    writer.close()


async def mailing_with_photo(msg: Message):
    await msg.answer('Отправьте фото и текст как одно сообщение\nCancel - /cancel')
    await AdminState.with_pic.set()


async def mailing_with_photo_state(msg: Message, state: FSMContext):
    largest_photo = msg.photo[-1].file_id
    db = DB_API_ADMIN()
    db.connect()
    user_id_list = db.get_user_id()
    for i in user_id_list:
       try:
          await msg.bot.send_photo(i[0], photo=largest_photo, caption=msg.caption)
          await msg.answer(f'Успешно отправлено: {i[0]}')
       except:
          await asyncio.sleep(1)
    await state.finish()

async def mailing_text(msg: Message):
    await msg.answer('Отправьте текст как одно сообщение\nCancel - /cancel')
    await AdminState.without_pic.set()

async def mailing_text_state(msg: Message, state: FSMContext):
    try:
        db = DB_API_ADMIN()
        db.connect()
        user_id_list = db.get_user_id()
        for i in user_id_list:
            await msg.bot.send_message(i[0], msg.text)
            await msg.answer(f'Успешно отправлено: {i[0]}')
    except Exception as err:
        await msg.answer(err)
    finally:
        await state.finish()


async def change_balance(msg: Message):
    await msg.answer('Введите Telegram ID пользователя и бонус в виде: ID|СКОЛЬКО НУЖНО ДОБАВИТЬ')
    await AdminState.balance.set()


async def change_balance_state(msg: Message, state: FSMContext):
    try:
        data = msg.text.split('|')
        db = DB_API_ADMIN()
        db.connect()
        chosen_sum = data[1]
        formatted_sum = chosen_sum.replace(' ', '')
        user_balance = db.get_balance(data[0])[0]
        new_balance = int(formatted_sum) + int(user_balance)
        db.update_balance(data[0],new_balance)
        await msg.answer('Успешно добавлен!')
    except Exception as err:
        await msg.answer(f'Некорректные данные\n\n{err}')
    await state.finish()


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, Command('admin'), AdminFilter())
    with_text: dict = {
        all_users: Text(equals='👤 Все пользователи'),
        find_user: Text(equals='🔎 Найти пользователя'),
        block_user: Text(equals='❌ Заблокировать'),
        unblock_user: Text(equals='✅ Разблокировать'),
        change_bonus: Text(equals='🌟 Изменить баллы'),
        referral_check: Text(equals='🔗 Получить все рефералы'),
        delete_user: Text(equals='🗑 Удалить пользователя'),
        mailing_with_photo: Text(equals='🖼 Рассылка с фото'),
        mailing_text: Text(equals='💬 Рассылка без фото'),
        change_balance: Text(equals='💰 Пополнить баланс')
    }
    for key, value in with_text.items():
        dp.register_message_handler(key, value, AdminFilter())
    only_states: dict = {
        search: AdminState.user_id_search,
        block_user_state: AdminState.user_id_block,
        unblock_user_state: AdminState.user_id_unblock,
        change_bonus_state: AdminState.bonus,
        referrals_check_state: AdminState.referral,
        delete_user_state: AdminState.delete_user,
        mailing_text_state: AdminState.without_pic,
        change_balance_state: AdminState.balance
    }
    for key, value in only_states.items():
        dp.register_message_handler(key, state=value)
    dp.register_message_handler(mailing_with_photo_state, content_types=types.ContentType.PHOTO,
                                state=AdminState.with_pic)
