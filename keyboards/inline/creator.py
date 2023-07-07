from aiogram.types import InlineKeyboardMarkup, User

from database.dbApi import DB_API
from database.others import countries_btn_
from i18n import _
from keyboards.inline.constructor import Constructor
from misc.cost_modification import change_price
from services.API_5sim.fetch_operator import GetPrice


class CreateInlineBtn(Constructor):
    @staticmethod
    def services():
        return Constructor.create_inline_btn([[{'telegram': _('telegram')}
                                                  , {'openai': _('chatgpt')}]])

    @staticmethod
    def confirmation():
        return Constructor.create_inline_btn([[{'confirm_callback': _('confirm_btn')}],[{'back':_('back')}]])

    @staticmethod
    def payment():
        return Constructor.create_inline_btn([[{'payme': _('payme')},
                                               {'click': _('click')}],
                                              [{'qiwi': _('qiwi')}]])

    @staticmethod
    def language():
        return Constructor.create_inline_btn([[{'lang:ru': '🇷🇺 RU'},
                                               {'lang:uzb': '🇺🇿 UZB'},
                                               {'lang:eng': '🇺🇸 ENG'}]])


class Pagination:
    def __init__(self):
        self.user_id = User.get_current().id
        self.db_api = DB_API()
        self.db_api.connect()
        self.page = self.db_api.get_current_page(self.user_id)[0]
        self.lang = self.db_api.get_current_language(self.user_id)[0]

    def __call__(self, *args, **kwargs) -> InlineKeyboardMarkup:
        if self.page < 0:
            self.page = 17
        elif self.page > 17:
            self.page = 0
        self.db_api.update_page(self.user_id, self.page)
        countries_data = countries_btn_[self.lang]
        bottom_btn = [{'previous': '<<'}, {'page': f'{self.page}/{17}'}, {'next': '>>'}]
        countries_btn = [{key: value for d in countries_data[self.page] for key, value in d.items()}]
        back_btn = [{'back':_('back')}]
        btn = Constructor.create_inline_btn([countries_btn, bottom_btn, back_btn])

        return btn


class Operator:
    def __init__(self, country, product):
        self.country = country
        self.product = product
        self.description = ''

    def __call__(self):
        url = f'https://5sim.net/v1/guest/prices?country={self.country}&product={self.product}'
        getPrice = GetPrice(url)
        response_dict: dict = getPrice()
        operators_dict: dict = dict()
        if response_dict:
            for item in response_dict[self.country][self.product]:
                cost: str = response_dict[self.country][self.product][item]['cost']
                # cost modification
                cost = change_price(cost)
                quantity: str = response_dict[self.country][self.product][item]['count']
                rate: str = ''
                if 'rate' not in response_dict[self.country][self.product][item]:
                    response_dict[self.country][self.product][item]['rate'] = 'None'
                    rate += response_dict[self.country][self.product][item]['rate']
                else:
                    rate += str(response_dict[self.country][self.product][item]['rate']) + '/100 %'

                operators_dict[item] = item

                self.description += f"""\n\t<b>{str(item).upper()}</b>:\n
    <i>{_('cost')}: {cost} </i>
    <i>{_('quantity')}: {quantity} </i>
    <i>{_('rate')}: {rate} </i>
    
                """
            return Constructor.create_inline_btn([[operators_dict],[{'back':_('back')}]])

