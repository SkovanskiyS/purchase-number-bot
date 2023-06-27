from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.constant import Constructor
from lexicon.lexicon_RU import LEXICON_BUTTONS

class CreateBtn(Constructor):
    @staticmethod
    def MenuBtn():
        return Constructor.create_btn([[LEXICON_BUTTONS['buy_number']],[LEXICON_BUTTONS['contact_with']]])


