from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

import utils.dp_api.sqlite
from data.config import REQUEST_CHAT_ID
from keyboards.default.menu_btn import menuR_btns
from keyboards.inline.leave_request_btn import step_btns, only_back
from loader import bot, db
from handlers.users import dp
from states.register_state import LeaveRequest



@dp.callback_query_handler(text_contains="request", state=None)
async def call_leave_request(call: CallbackQuery):
    result = db.get_white_list(call.from_user.id)
    if result[0]==0:
        await call.message.delete()
        # await call.message.edit_reply_markup(reply_markup=step_btns)
        await call.message.answer("📛Вы выбрали вкладку: Оставить заявку",reply_markup=ReplyKeyboardRemove())
        await call.message.answer(
            '<b>Шаг 1/3</b>. 📓Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру)'
            ' или пропустите этот пункт:\nОтмена: /cancel', reply_markup=step_btns)
        await LeaveRequest.address.set()

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

@dp.message_handler(state=LeaveRequest.address)
async def leave_photo(message: types.Message, state: FSMContext):
    address_text = message.text
    async with state.proxy() as data:
        data["address"] = address_text

    await message.answer(
        '<b>Шаг 2/3</b>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:\nОтмена: /cancel',
        reply_markup=step_btns)
    await LeaveRequest.next()


@dp.message_handler(content_types=['photo', 'text'], state=LeaveRequest.photo)
async def message_photo_handler(message: types.Message, state=FSMContext):
    if message.text == None:
        file_id = message.photo[-1].file_id
        async with state.proxy() as data:
            data['photo'] = file_id
        await message.answer('<b>Шаг 3/3</b>. 📛Напишите причину обращения в подробностях:\nОтмена: /cancel', reply_markup=only_back)
        await LeaveRequest.next()
    else:
        await message.answer(
            '📛В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> в виде медиа-сообщения. <b>Попробуйте еще раз</b>: \nОтмена: /cancel')


@dp.message_handler(content_types=['video'], state=LeaveRequest.photo)
async def message_video_handler(message: types.Message, state=FSMContext):
    video_id = message.video.file_id
    async with state.proxy() as data:
        data['photo'] = video_id
    await LeaveRequest.next()
    await message.answer('<b>Шаг 3/3</b>. 📛Напишите причину обращения в подробностях:\nОтмена: /cancel', reply_markup=only_back)


@dp.message_handler(content_types='text', state=LeaveRequest.reason)
async def message_reason_handler(message: types.Message, state=FSMContext):
    reason = message.text
    async with state.proxy() as data:
        data["reason"] = reason
    data = await state.get_data()
    database = db.select_user(message.chat.id)
    print(str(database))
    result_information = f"<b>⛔Поступила новая жалоба</b>\n<b>Юзернейм</b>: @{message.from_user.username}\n<b>Имя и Фамилия:</b>{database[2]}"f"" \
                         f"\n<b>Номер телефона:</b> {database[3]}" \
                         f"\n<b>Адрес</b>: {data.get('address')}" \
                         f"\n<b>Содержание:</b>{data.get('reason')}"
    try:
        await bot.send_photo(chat_id=REQUEST_CHAT_ID, photo=data.get("photo"), caption=result_information)
    except Exception as err:
        await bot.send_message(chat_id=REQUEST_CHAT_ID, text=result_information)
    await message.answer("✅<b>Жалоба отправлена адмнистрации. Спасибо за Ваше обращение!</b>",reply_markup=menuR_btns)

    await state.finish()
