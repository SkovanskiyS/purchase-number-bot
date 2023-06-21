from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.constant import Constructor


class CreateBtn(Constructor):
    @staticmethod
    def mainMenuBtn():
        return Constructor.create_btn([['Купить номер','Назад']])




