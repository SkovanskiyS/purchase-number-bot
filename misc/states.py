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


class AdminState(StatesGroup):
    user_id_search = State()
    user_id_block = State()
    user_id_unblock = State()
    bonus = State()
    referral = State()
    delete_user = State()
