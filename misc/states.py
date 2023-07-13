from aiogram.dispatcher.filters.state import State, StatesGroup


class Purchase(StatesGroup):
    service = State()
    country = State()
    operator = State()
    confirm = State()
    bonus = State()
    payment = State()
    pay = State()
    purchase = State()


class Language(StatesGroup):
    change_language = State()
