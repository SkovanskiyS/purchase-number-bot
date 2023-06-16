from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.admin_btns.admin_panel_menu import main_admin_panel
from loader import dp, bot, db
from data.config import admins, ADMIN_CHAT_ID
from states.register_state import BlockDialog

from utils.dp_api.sqlite import Database

@dp.message_handler(text='✅Разблокировать',chat_id=admins)
async def unban_user_text(message: types.Message, state: FSMContext):
  await message.answer('🆔Введите <b>ID</b> пользователя, которого нужно разаблокировать.\nОтмена: /cancel_ban')
  await BlockDialog.white_list.set()

@dp.message_handler(state=BlockDialog.white_list,chat_id=admins)
async def unban_user(message:types.Message,state=FSMContext):
    if message.text == "/cancel_ban":
        await message.answer('<b>Отмена!</b> Возвращаю назад.')
        await state.finish()
    else:
        if message.text.isdigit():
          cur = db.execute(sql=f"SELECT blocked FROM Users WHERE id = {message.text}",fetchall=True)
          if len(cur) == 0:
            await message.answer('❗Такой пользователь не найден в базе данных.')
            await state.finish()
          else:
            for i in cur:
              if i[0] == 1:
                db.execute(sql=f"UPDATE Users SET blocked = 0 WHERE id = {message.text}",commit=True)
                await message.answer('✅Пользователь успешно разбанен.')
                await state.finish()
                await bot.send_message(message.text, '✅Вы были разблокированы Администрацией')
              else:
                await message.answer('🔅Данный пользователь не получал бан.')
                await state.finish()
        else:
          await message.answer('❕Ты вводишь буквы...\n\nВведи ID')


