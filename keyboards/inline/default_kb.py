from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.constant import Constructor
from lexicon.lexicon_RU import LEXICON_INLINE_BUTTONS


class CreateInlineBtn(Constructor):
    @staticmethod
    def paymeUrl():
        return Constructor.create_inline_btn([[{'Pay': 'pay:payme:1'}]], url='https://payme.uz')

    @staticmethod
    def clickUrl():
        return Constructor.create_inline_btn([[{'Click': 'click:click:1'}]], url='https://click.uz')

    @staticmethod
    def services():
        return Constructor.create_inline_btn([[{LEXICON_INLINE_BUTTONS['telegram']: 'telegram'}
                                                  , {LEXICON_INLINE_BUTTONS['chatgpt']: 'openai'}]])
