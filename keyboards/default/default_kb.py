from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.constant import Constructor

rep = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='Wassap'),
        KeyboardButton(text='Nigga')
    ]
], resize_keyboard=True)

print(rep)


class CreateBtn(Constructor):
    @staticmethod
    def mainMenuBtn():
        return Constructor.create_btn([['Назад'], ['Вперед', 'Стоять']], request_contact=True)
