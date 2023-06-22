from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.constant import Constructor
from keyboards.inline.callback_data import pay_callback


class CreateInlineBtn(Constructor):
    @staticmethod
    def payments():
        callback_data = pay_callback.new(name="payme")
        return Constructor.create_inline_btn(
            [[{'Payme': f'{callback_data}'}, {'Click': f'{callback_data}'}], [{'Отмена': 'cancel'}]])

    @staticmethod
    def paymeUrl():
        return Constructor.create_inline_btn([[{'Pay': 'pay:payme:1'}]], url='https://payme.uz')

    @staticmethod
    def clickUrl():
        return Constructor.create_inline_btn([[{'Click': 'click:click:1'}]], url='https://click.uz')
