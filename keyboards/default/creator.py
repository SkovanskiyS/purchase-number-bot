from keyboards.default.constructor import Constructor
from i18n import _


class CreateBtn(Constructor):
    @staticmethod
    def MenuBtn():
        return Constructor.create_btn([[_('buy_number')], [_('contact_with'),_('change_lang')],[_('my_profile')]])

    @staticmethod
    def CancelBtn():
        return Constructor.create_btn([[_('cancel')]])
