from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins
from handlers.users.back_to_menu import backMenu
from keyboards.default.admin_btns.admin_panel_menu import main_admin_panel
from keyboards.default.admin_btns.fini_start_states import start_dialog

from keyboards.default.menu_btn import menuR_btns
from loader import db, dp, bot
from aiogram.types import CallbackQuery,ReplyKeyboardMarkup

from states.register_state import Communicate

from keyboards.inline.communication_inline import stop_dialog


@dp.callback_query_handler(text='stop_dialog', state=Communicate.chat_with_admin)
async def stop_dialog_method(call: CallbackQuery, state=FSMContext):
    await call.message.answer('<b>⛔📞Диалог с администратором завершён...</b>')
    await state.finish()
    await backMenu(call)


@dp.message_handler(state=Communicate.chat_with_admin)
async def chatting(message: types.Message, state=FSMContext):
    message_from_user = f"<b>Диалог</b>\n<i>Юзернейм</i>: @{message.from_user.username}\n" \
                        f"<i>Имя и Фамилия:</i> {db.select_user(message.from_user.id)[2]}"f"" \
                        f"\n<i>Номер телефона:</i> {db.select_user(message.from_user.id)[3]}" \
                        f"\n<b>Содержание: {message.text}</b>"
    global user_id
    user_id = message.from_user.id
    await bot.send_message(admins[0], message_from_user,reply_markup=start_dialog)

@dp.message_handler(text='❌Завершить', state=Communicate.admin_state, chat_id=admins)
async def stop_dialog_admin(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer("Диалог завершен.",reply_markup=main_admin_panel)

@dp.message_handler(text='▶Начать', chat_id=admins)
async def st(message: types.Message):
    await Communicate.admin_state.set()
    await message.answer('Диалог начат:')

@dp.message_handler(state=Communicate.admin_state)
async def talk_with_user(message: types.Message, state=FSMContext):
    await bot.send_message(message.from_user.id, '✅Отправлено✅')
    await bot.send_message(user_id, message.text)


@dp.callback_query_handler(text='chat_with_me')
async def dialog(call: CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    if result[0] == 0:
        await call.message.edit_text(
            '✅📞✅Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ", готов помочь Вам. Напишите, пожалуйста интересующий Вас вопрос и ожидайте',
            reply_markup=stop_dialog)
        await Communicate.chat_with_admin.set()

# @dp.callback_query_handler(text='start_dialog_admin',state=Communicate.chat_with_admin)
# async def start_dialog_admin(call:CallbackQuery,state=FSMContext):
#
#     await Communicate.admin_state.set()
