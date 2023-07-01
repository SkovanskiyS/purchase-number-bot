from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from misc.states import Language
from keyboards.inline.creator import CreateInlineBtn
from aiogram.dispatcher.filters import Command


async def choose_language(call: CallbackQuery):
    data = call.data.split(':')
    await call.message.answer(data[1])


def register_language(dp: Dispatcher):
    dp.register_callback_query_handler(choose_language, text_contains='lang')
