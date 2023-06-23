from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    NAME = State()
    SURNAME = State()
    PHONE_NUMBER = State()
