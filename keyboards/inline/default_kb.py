from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.constant import Constructor


class CreateInlineBtn(Constructor):
    @staticmethod
    def mainMenuBtn():
        return Constructor.create_inline_btn([[{'Payme':'pay:payme:1'},{'Click':'pay:click:1'}]])





