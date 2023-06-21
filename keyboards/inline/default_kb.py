from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.constant import Constructor


class CreateInlineBtn(Constructor):
    @staticmethod
    def payments():
        return Constructor.create_inline_btn([[{'Payme':'pay:payme:1'},{'Click':'pay:click:1'}]])

    @staticmethod
    def paymeUrl():
        return Constructor.create_inline_btn([[{'Pay':'pay:payme:2'}]],url='https://youtube.com/')

