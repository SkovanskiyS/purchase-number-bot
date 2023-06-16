from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from data.config import admins, ADMIN_CHAT_ID
from states.register_state import BlockDialog

@dp.message_handler(text='🚫Заблокировать',chat_id=admins)
async def ban_user_text(message: types.Message):
    await message.answer('🆔Введите <b>ID</b> пользователя, которого нужно заблокировать.\nОтмена: /cancel_ban')
    await BlockDialog.black_list.set()

@dp.message_handler(state=BlockDialog.black_list,chat_id = admins)
async def ban_user(message:types.Message,state=FSMContext):
    for i in admins:
        if i==message.text:
            await message.answer("<b>Нельзя блокировать админа!</b>")
            await state.finish()
            return
    if message.text == "/cancel_ban":
        await message.answer('<b>Отмена!</b> Возвращаю назад.')
        await state.finish()
    else:
        if message.text.isdigit():
         # db = Database()
          #cur = db.execute()
          cur = db.execute(sql=f"SELECT blocked FROM Users WHERE id = {message.text}",fetchall=True)
          if len(cur) == 0:
            await message.answer('❗Такой пользователь не найден в базе данных.')
            await state.finish()
          else:
            for i in cur:
              if i[0] == 0 or i[0] is None:
                db.execute(sql=f"UPDATE Users SET blocked = 1 WHERE id = {message.text}",commit=True)
                await message.answer('✅Пользователь успешно добавлен в ЧС.')
                await state.finish()
                await bot.send_message(message.text, '⚠Вы были забанены Администрацией')
              else:
                await message.answer('🚫Данный пользователь уже получил бан')
                await state.finish()
        else:
          await message.answer('🆔Введите ID')


