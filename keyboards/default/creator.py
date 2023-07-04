from keyboards.default.constructor import Constructor
from lexicon.lexicon_RU import LEXICON_BUTTONS


class CreateBtn(Constructor):
    @staticmethod
    def MenuBtn():
        return Constructor.create_btn([[LEXICON_BUTTONS['buy_number']], [LEXICON_BUTTONS['contact_with'],LEXICON_BUTTONS['change_lang']]])

    @staticmethod
    def CancelBtn():
        return Constructor.create_btn([[LEXICON_BUTTONS['cancel']]])







