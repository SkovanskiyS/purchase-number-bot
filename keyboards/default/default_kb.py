from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.constant import Constructor


class CreateBtn(Constructor):
    @staticmethod
    def mainMenuBtn():
        return Constructor.create_btn([['Купить номер','Назад']])

    @staticmethod
    def request_phone_number():
        return Constructor.create_btn([['Send phone number']],request_contact=True)


