from aiogram.dispatcher.filters.state import State, StatesGroup


class Purchase(StatesGroup):
    service: State = State()
    country: State = State()
    operator: State = State()


