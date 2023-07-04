from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

from database.dbApi import DB_API
from database.others import countries_btn_
from database.pages import current_page
from keyboards.inline.constructor import Constructor
from lexicon.lexicon_RU import LEXICON_INLINE_BUTTONS, LEXICON_OPERATOR_INFO, LEXICON_CONFIRMATION, LEXICON_PAYMENT
from misc.cost_modification import change_price
from services.API_5sim.fetch_countries import FilterData
from services.API_5sim.fetch_operator import GetPrice
from i18n import _

class CreateInlineBtn(Constructor):
    @staticmethod
    def services():
        return Constructor.create_inline_btn([[{'telegram': _('telegram')}
                                                  , {'openai': _('chatgpt')}]])

    @staticmethod
    def confirmation():
        return Constructor.create_inline_btn([[{'confirm_callback': _('confirm_btn')}]])

    @staticmethod
    def payment():
        return Constructor.create_inline_btn([[{'payme': _('payme')},
                                               {'click': _('click')}],
                                              [{'qiwi': _('qiwi')}]])

    @staticmethod
    def language():
        return Constructor.create_inline_btn([[{'lang:ru': '🇷🇺'},
                                               {'lang:uzb': '🇺🇿'},
                                               {'lang:eng': '🇺🇸'}]])


class Pagination:
    def __init__(self, current_page):
        self.page: int = current_page
        self.lang: tuple = None

    def get_language(self, user_id):
        db_api = DB_API()
        db_api.connect()
        return db_api.get_current_language(user_id)

    def __call__(self, *args, **kwargs) -> InlineKeyboardMarkup:
        countries_data = countries_btn_[self.lang[0]]
        if current_page['page'] < 0:
            current_page['page'] = 17
        elif current_page['page'] > 17:
            current_page['page'] = 0

        self.page = current_page['page']
        bottom_btn = [{'previous': '<<'}, {'page': f'{self.page}/{17}'}, {'next': '>>'}]
        countries_btn = [{key: value for d in countries_data[self.page] for key, value in d.items()}]
        btn = Constructor.create_inline_btn([countries_btn, bottom_btn])
        return btn

        # all_data = [{k: v} for k, v in countries_data.items()]
        # count_of_pages = len(all_data) // 10
        # sorted_data = [[] for _ in range(count_of_pages + 1)]
        # offset_start = 0
        # offset_end = 10
        #
        # for i in sorted_data:
        #     i.extend(all_data[offset_start:offset_end])
        #     offset_start = offset_end
        #     offset_end += 10
        #


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
        return Constructor.create_inline_btn([[operators_dict]])
