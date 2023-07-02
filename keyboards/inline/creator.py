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

    @staticmethod
    def language():
        return Constructor.create_inline_btn([[{'lang:ru': '🇷🇺'},
                                               {'lang:uzb': '🇺🇿'},
                                               {'lang:eng': '🇺🇸'}]])


class Pagination:
    def __init__(self, current_page):
        self.page: int = current_page

    def __call__(self, *args, **kwargs) -> InlineKeyboardMarkup:
        filtered_data = FilterData()
        data_ct = {'afghanistan': 'Афганистан', 'albania': 'Албания', 'algeria': 'Алжир', 'angola': 'Ангола', 'anguilla': 'Ангилья', 'antiguaandbarbuda': 'Антигуа и Барбуда', 'argentina': 'Аргентина', 'armenia': 'Армения', 'aruba': 'Аруба', 'australia': 'Австралия', 'austria': 'Австрия', 'azerbaijan': 'Азербайджан', 'bahamas': 'Багамы', 'bahrain': 'Бахрейн', 'bangladesh': 'Бангладеш', 'barbados': 'Барбадос', 'belarus': 'Беларусь', 'belgium': 'Бельгия', 'belize': 'Белиз', 'benin': 'Бенин', 'bhutane': 'Бутан', 'bih': 'Босния и Герцеговина', 'bolivia': 'Боливия', 'botswana': 'Ботсвана', 'brazil': 'Бразилия', 'bulgaria': 'Болгария', 'burkinafaso': 'Буркина-Фасо', 'burundi': 'Бурунди', 'cambodia': 'Камбоджи', 'cameroon': 'Камерун', 'canada': 'Канада', 'capeverde': 'Кабо-Верде', 'caymanislands': 'Острова Кайман', 'chad': 'Чад', 'chile': 'Чили', 'china': 'Китай', 'colombia': 'Колумбия', 'comoros': 'Коморы', 'congo': 'Конго', 'costarica': 'Коста-Рика', 'croatia': 'Хорватия', 'cyprus': 'Кипр', 'czech': 'Чехия', 'denmark': 'Дания', 'djibouti': 'Джибути', 'dominica': 'Доминика', 'dominicana': 'Доминиканская Республика', 'easttimor': 'Восточный Тимор', 'ecuador': 'Эквадор', 'egypt': 'Египет', 'england': 'Великобритания', 'equatorialguinea': 'Экваториальная Гвинея', 'eritrea': 'Эритрея', 'estonia': 'Эстония', 'ethiopia': 'Эфиопия', 'finland': 'Финляндия', 'france': 'Франция', 'frenchguiana': 'Французская Гвиана', 'gabon': 'Габон', 'gambia': 'Гамбия', 'georgia': 'Грузия', 'germany': 'Германия', 'ghana': 'Гана', 'greece': 'Греция', 'grenada': 'Гренада', 'guadeloupe': 'Гваделупа', 'guatemala': 'Гватемала', 'guinea': 'Гвинея', 'guineabissau': 'Гвинея-Бисау', 'guyana': 'Гайана', 'haiti': 'Гаити', 'honduras': 'Гондурас', 'hongkong': 'Гонконг', 'hungary': 'Венгрия', 'india': 'Индия', 'indonesia': 'Индонезия', 'ireland': 'Ирландия', 'israel': 'Израиль', 'italy': 'Италия', 'ivorycoast': "Кот-д'Ивуар", 'jamaica': 'Ямайка', 'japan': 'Япония', 'jordan': 'Иордания', 'kazakhstan': 'Казахстан', 'kenya': 'Кения', 'kuwait': 'Кувейт', 'kyrgyzstan': 'Кыргызстан', 'laos': 'Лаос', 'latvia': 'Латвия', 'lesotho': 'Лесото', 'liberia': 'Либерия', 'lithuania': 'Литва', 'luxembourg': 'Люксембург', 'macau': 'Макао', 'madagascar': 'Мадагаскар', 'malawi': 'Малави', 'malaysia': 'Малайзия', 'maldives': 'Мальдивы', 'mauritania': 'Мавритания', 'mauritius': 'Маврикий', 'mexico': 'Мексика', 'moldova': 'Молдавия', 'mongolia': 'Монголия', 'montenegro': 'Черногория', 'montserrat': 'Монтсеррат', 'morocco': 'Марокко', 'mozambique': 'Мозамбик', 'myanmar': 'Мьянма', 'namibia': 'Намибия', 'nepal': 'Непал', 'netherlands': 'Нидерланды', 'newcaledonia': 'Новая Каледония', 'newzealand': 'Новая Зеландия', 'nicaragua': 'Никарагуа', 'niger': 'Нигер', 'nigeria': 'Нигерия', 'northmacedonia': 'Северная Македония', 'norway': 'Норвегия', 'oman': 'Оман', 'pakistan': 'Пакистан', 'panama': 'Панама', 'papuanewguinea': 'Папуа-Новая Гвинея', 'paraguay': 'Парагвай', 'peru': 'Перу', 'philippines': 'Филиппины', 'poland': 'Польша', 'portugal': 'Португалия', 'puertorico': 'Пуэрто-Рико', 'reunion': 'Реюньон', 'romania': 'Румыния', 'russia': 'Россия', 'rwanda': 'Руанда', 'saintkittsandnevis': 'Сент-Китс и Невис', 'saintlucia': 'Сент-Люсия', 'saintvincentandgrenadines': 'Сент-Винсент и Гренадины', 'salvador': 'Сальвадор', 'samoa': 'Самоа', 'saotomeandprincipe': 'Сан-Томе и Принсипи', 'saudiarabia': 'Саудовская Аравия', 'senegal': 'Сенегал', 'serbia': 'Сербия', 'seychelles': 'Сейшелы', 'sierraleone': 'Сьерра-Леоне', 'singapore': 'Сингапур', 'slovakia': 'Словакия', 'slovenia': 'Словения', 'solomonislands': 'Соломоновы острова', 'southafrica': 'Южная Африка', 'southkorea': 'Южная Корея', 'spain': 'Испания', 'srilanka': 'Шри-Ланка', 'suriname': 'Суринам', 'swaziland': 'Эсватини', 'sweden': 'Швеция', 'switzerland': 'Швейцария', 'taiwan': 'Тайвань', 'tajikistan': 'Таджикистан', 'tanzania': 'Танзания', 'thailand': 'Таиланд', 'tit': 'Тринидад и Тобаго', 'togo': 'Того', 'tonga': 'Тонга', 'tunisia': 'Тунис', 'turkey': 'Турция', 'turkmenistan': 'Туркменистан', 'turksandcaicos': 'Теркс и Кайкос', 'uganda': 'Уганда', 'ukraine': 'Украина', 'uruguay': 'Уругвай', 'usa': 'США', 'uzbekistan': 'Узбекистан', 'venezuela': 'Венесуэла', 'vietnam': 'Вьетнам', 'virginislands': 'Виргинские острова', 'zambia': 'Замбия', 'zimbabwe': 'Зимбабве'}
        all_data = [{k: v} for k, v in data_ct.items()]
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
