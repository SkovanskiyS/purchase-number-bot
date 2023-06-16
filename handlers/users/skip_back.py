from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.leave_request_states import call_leave_request, leave_photo, message_photo_handler, \
    message_video_handler
from handlers.users.menu_call_markup import bot_leave_request
from keyboards.inline.leave_request_btn import step_btns,only_back
from loader import dp
from states.register_state import LeaveRequest
from handlers.users import leave_request_states



@dp.callback_query_handler(text="skip", state=LeaveRequest.address)
async def skip_state(call: CallbackQuery, state: FSMContext):
   # message_id = await call.message.edit_text("<b>Шаг 2/3</b>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:\nОтмена: /cancel",reply_markup=step_btns)
    await call.message.delete()
    #await leave_photo(call.message,state=state)
    await call.message.answer(
        '<b>Шаг 2/3</b>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:',
        reply_markup=step_btns)
    await LeaveRequest.photo.set()
   # print(message_id.message_id)

@dp.callback_query_handler(text="skip", state=LeaveRequest.photo)
async def skip_state(call: CallbackQuery, state: FSMContext):

    await call.message.delete()
    await call.message.answer('<b>Шаг 3/3</b>. 📛Напишите причину обращения в подробностях:', reply_markup=only_back)
    # message_id = await call.message.edit_text("<b>Шаг 3/3</b>. 📛Напишите причину обращения в подробностях:\nОтмена: /cancel",reply_markup=only_back)
    # print(message_id.message_id)
    await LeaveRequest.reason.set()

@dp.callback_query_handler(text="back", state=LeaveRequest.address)
async def skip_state(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot_leave_request(call.message,state)

@dp.callback_query_handler(text="back", state=LeaveRequest.photo)
async def skip_state(call: CallbackQuery, state: FSMContext):
     await call.message.delete()
     # await call.message.edit_text(
     #    '<b>Шаг 1/3</b>. 📓Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру)'
     #    ' или пропустите этот пункт:\nОтмена: /cancel', reply_markup=step_btns)
     await call.message.answer('<b>Шаг 1/3</b>. 📓Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру)'
     ' или пропустите этот пункт:\nОтмена: /cancel', reply_markup=step_btns)
     await LeaveRequest.address.set()

@dp.callback_query_handler(text="back", state=LeaveRequest.reason)
async def skip_state(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    # message_id = await call.message.edit_text(
    #     '<b>Шаг 2/3</b>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:\nОтмена: /cancel', reply_markup=step_btns)
    await call.message.answer('<b>Шаг 2/3</b>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:\nОтмена: /cancel', reply_markup=step_btns)
    await LeaveRequest.photo.set()

