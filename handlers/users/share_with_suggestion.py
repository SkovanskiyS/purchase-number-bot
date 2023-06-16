from email import message

from aiogram.dispatcher import FSMContext

from data.config import REQUEST_CHAT_ID
from keyboards.inline.leave_request_btn import only_back, leave_request_inline
from loader import dp, bot, db
from aiogram.types import CallbackQuery
from aiogram import types

from states.register_state import GetSuggestion

@dp.callback_query_handler(text='share')
async def set_suggestion(call: CallbackQuery, state=FSMContext):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        await call.message.edit_text("💡Распишите <b>Ваше предложение в подробностях: (Добавьте фотографию, если есть)</b>",
                                     reply_markup=only_back)
        await GetSuggestion.suggestion.set()

@dp.callback_query_handler(text='back',state=GetSuggestion.suggestion)
async def back(call: CallbackQuery,state=FSMContext):
    await call.message.edit_text("📛👇📛<b>Выберите категорию</b>, по которой Вы хотите оставить заявку в УК:",
                                 reply_markup=leave_request_inline)
    await state.finish()
@dp.message_handler(state=GetSuggestion.suggestion)
async def get_suggestion(message: types.Message,state:FSMContext):
    result_information = f"<b>💡Поступила новое предложение:</b>\n<b>Юзернейм</b>: @{message.from_user.username}\n<b>Имя и Фамилия:</b>{db.select_user(message.from_user.id)[2]}"f"" \
                         f"\n<b>Номер телефона:</b> {db.select_user(message.from_user.id)[3]}" \
                         f"\n<b>Содержание:</b>{message.text}"
    try:
        await bot.send_message(chat_id=REQUEST_CHAT_ID, text=result_information)
        await message.answer("✅💡<b>Идея принята и передана администрации.</b> Спасибо за Ваше обращение!")
        await state.finish()
    except Exception as err:
        await message.answer(err)

@dp.message_handler(content_types=['photo'], state=GetSuggestion.suggestion)
async def get_media(message: types.Message,state=FSMContext):
    result_information = f"<b>💡Поступила новое предложение:</b>\n<b>Юзернейм</b>: @{message.from_user.username}\n<b>Имя и Фамилия:</b>{db.select_user(message.from_user.id)[2]}"f"" \
                         f"\n<b>Номер телефона:</b> {db.select_user(message.from_user.id)[3]}" \
                         f"\n<b>Содержание:</b>{message.caption}"
    if message.caption is None:
        await message.answer("📛⛔Предложение должно содержать текст:")
        return
    try:
        await bot.send_photo(chat_id=REQUEST_CHAT_ID, photo=message.photo[-1].file_id, caption=result_information)
        await state.finish()
        await message.answer("✅💡<b>Идея принята и передана администрации.</b> Спасибо за Ваше обращение!")
    except Exception as err:
        await message.answer(err)
    # try:
    #     await bot.send_photo(chat_id=CHAT_ID, photo=data.get("photo"), caption=result_information)
    # except Exception as err:
    #     await bot.send_message(chat_id=CHAT_ID, text=result_information)
