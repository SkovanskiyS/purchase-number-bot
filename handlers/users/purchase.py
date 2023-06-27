from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from misc.states import Purchase
from services.API_5sim.fetch_countries import FilterData
from lexicon.lexicon_RU import LEXICON_BUY


async def service_handler(call: CallbackQuery, state: FSMContext) -> None:
    try:
        if call.data == 'telegram':
            async with state.proxy() as data:
                data['service'] = call.data
        elif call.data == 'openai':
            async with state.proxy() as data:
                data['service'] = call.data
    except Exception as ex:
        await call.message.answer(ex)
    finally:
        await call.message.answer(LEXICON_BUY['choose_country'])
        await Purchase.next()


async def country_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(f'You chose {data}')


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(service_handler, state=Purchase.service)
    dp.register_message_handler(country_handler, state=Purchase.country)
