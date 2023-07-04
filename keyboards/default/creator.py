from keyboards.default.constructor import Constructor
from lexicon.lexicon_RU import LEXICON_BUTTONS
from i18n import _

class CreateBtn(Constructor):
    @staticmethod
    def MenuBtn():
        return Constructor.create_btn([[_('buy_number')], [_('contact_with'),_('change_lang')]])

    @staticmethod
    def CancelBtn():
        return Constructor.create_btn([[_('cancel')]])







