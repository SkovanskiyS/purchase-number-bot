from aiogram.dispatcher.filters.state import State,StatesGroup

class SignUp(StatesGroup):
    name = State()
    phone_number = State()

class LeaveRequest(StatesGroup):
    address = State()
    photo = State()
    reason = State()

class NewName(StatesGroup):
    new_name = State()
    new_phone = State()

class ActualNumber(StatesGroup):
    actual_number = State()

class GetSuggestion(StatesGroup):
    suggestion = State()

class Communicate(StatesGroup):
    chat_with_admin = State()
    admin_state = State()


class MailingText(StatesGroup):
    mailing_text = State()

class BlockDialog(StatesGroup):
    black_list = State()
    white_list = State()
