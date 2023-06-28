from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

from database.pages import current_page
from keyboards.inline.constructor import Constructor
from lexicon.lexicon_RU import LEXICON_INLINE_BUTTONS, LEXICON_OPERATOR_INFO, LEXICON_CONFIRMATION, LEXICON_PAYMENT
from misc.cost_modification import change_price
from services.API_5sim.fetch_countries import FilterData
from services.API_5sim.fetch_operator import GetPrice


class CreateInlineBtn(Constructor):
    @staticmethod
    def services():
        return Constructor.create_inline_btn([[{'telegram': LEXICON_INLINE_BUTTONS['telegram']}
                                                  , {'openai': LEXICON_INLINE_BUTTONS['chatgpt']}]])

    @staticmethod
    def confirmation():
        return Constructor.create_inline_btn([[{'confirm_callback': LEXICON_CONFIRMATION['confirm']}]])

    @staticmethod
    def payment():
        return Constructor.create_inline_btn([[{'payme': LEXICON_PAYMENT['payme']},
                                               {'click': LEXICON_PAYMENT['click']}],
                                              [{'qiwi': LEXICON_PAYMENT['qiwi']}]])


class Pagination:
    def __init__(self, current_page):
        self.page: int = current_page

    def __call__(self, *args, **kwargs) -> InlineKeyboardMarkup:
        filtered_data = FilterData()
        all_data = [{k: v} for k, v in filtered_data().items()]
        count_of_pages = len(all_data) // 10
        sorted_data = [[] for _ in range(count_of_pages + 1)]
        offset_start = 0
        offset_end = 10

        for i in sorted_data:
            i.extend(all_data[offset_start:offset_end])
            offset_start = offset_end
            offset_end += 10

        if current_page['page'] < 0:
            current_page['page'] = 17
        elif current_page['page'] > 17:
            current_page['page'] = 0

        self.page = current_page['page']
        bottom_btn = [{'previous': '<<'}, {'page': f'{self.page}/{count_of_pages}'}, {'next': '>>'}]
        countries_btn = [{key: value for d in sorted_data[self.page] for key, value in d.items()}]
        btn = Constructor.create_inline_btn([countries_btn, bottom_btn])
        return btn

    """
    old version
    and should be optimized
    """
    # filtered_data = FilterData()
    # all_data: list[dict[str:str]] = list({k: v} for k, v in filtered_data().items())
    # sorted_data = []
    # count_of_pages: int = len(all_data) // 10
    # offset_start: int = 0
    # offset_end: int = 10
    # # create page indexes
    # for i in range(count_of_pages + 1):
    #     sorted_data.insert(i, [])
    # for i in sorted_data:
    #     for j in all_data[offset_start:offset_end]:
    #         i.append(j)
    #     offset_start = offset_end
    #     offset_end += 10
    # if 0 <= self.page <= count_of_pages:
    #     bottom_btn = [{'previous': '<<'}, {'page': f'{self.page}/{count_of_pages}'}, {'next': '>>'}]
    #     countries_btn = [{key: value for d in sorted_data[self.page] for key, value in d.items()}]
    #     btn = Constructor.create_inline_btn([countries_btn, bottom_btn])
    #     return btn
    # else:
    #     from database.pages import current_page
    #     current_page['page'] = 0
    #     self.page = 0
    #     bottom_btn = [{'previous': '<<'}, {'page': f'{self.page}/{count_of_pages}'}, {'next': '>>'}]
    #     countries_btn = [{key: value for d in sorted_data[self.page] for key, value in d.items()}]
    #     btn = Constructor.create_inline_btn([countries_btn, bottom_btn])
    #     return btn


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
<i>{LEXICON_OPERATOR_INFO['cost']}: {cost} </i>
<i>{LEXICON_OPERATOR_INFO['quantity']}: {quantity} </i>
<i>{LEXICON_OPERATOR_INFO['rate']}: {rate} </i>

            """
        return Constructor.create_inline_btn([[operators_dict]])
