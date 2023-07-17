from keyboards.default.constructor import Constructor
from i18n import _


class CreateBtn(Constructor):
    @staticmethod
    def MenuBtn():
        return Constructor.create_btn([[_('buy_number')], [_('my_profile'), _('change_lang')]])

    @staticmethod
    def CancelBtn():
        return Constructor.create_btn([[_('cancel')]])

    @staticmethod
    def AdminMenuBtns():
        return Constructor.create_btn(
            [['👤 Все пользователи', "🔎 Найти пользователя"], ['❌ Заблокировать', '✅ Разблокировать'],
             ['🌟 Изменить баллы','🔗 Получить все рефералы'],['🗑 Удалить пользователя']])
