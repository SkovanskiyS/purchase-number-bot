from aiogram.dispatcher.filters.state import State, StatesGroup


class Purchase(StatesGroup):
    service = State()
    country_choose = State()
    country = State()
    operator = State()
    confirm = State()
    bonus = State()
    payment = State()
    pay = State()
    purchase = State()
    top = State()


class Language(StatesGroup):
    change_language = State()


class AdminState(StatesGroup):
    user_id_search = State()
    user_id_block = State()
    user_id_unblock = State()
    bonus = State()
    referral = State()
    delete_user = State()
    with_pic = State()
    without_pic = State()
    balance = State()

class Balance(StatesGroup):
    balance_add = State()
    balance_count = State()
    payment = State()
    bill = State()
