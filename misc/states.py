from aiogram.dispatcher.filters.state import State, StatesGroup


class Purchase(StatesGroup):
    service: State = State()
    country: State = State()
    operator: State = State()
    confirm: State = State()
    payment: State = State()


class Language(StatesGroup):
    change_language = State()
