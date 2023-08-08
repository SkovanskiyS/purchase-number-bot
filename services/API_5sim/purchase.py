import asyncio

import requests
from data.config import load_config


class Buy:
    config = load_config('../../.env')

    def __init__(self, country=None, operator=None, product=None):
        self.country = country
        self.operator = operator
        self.product = product
        self.token = self.config.api.API_KEY
        self.header = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json',
        }

    async def purchase_number(self):
        buy_url = f'https://5sim.net/v1/user/buy/activation/{self.country}/{self.operator}/{self.product}?reuse=1'
        response = requests.get(buy_url, headers=self.header)
        i = 0
        while response.text == 'no free phones':
            await asyncio.sleep(.5)
            buy_url = f'https://5sim.net/v1/user/buy/activation/{self.country}/{self.operator}/{self.product}?reuse=1'
            response = requests.get(buy_url, headers=self.header)
            if i > 20:
                self.operator = 'any'
            if i > 30:
                self.country = 'usa'
                self.operator = 'any'
            if i > 50:
                self.country = 'any'
            if i > 100:
                return 'failed'
            i += 1
        try:
            return response.json()
        except Exception as err:
            return 'empty'

    async def get_sms(self, product_id):
        check_url = f'https://5sim.net/v1/user/check/{product_id}'
        response = requests.get(check_url, headers=self.header).json()
        return response

    async def finish_order(self, product_id):
        finish_url = f'https://5sim.net/v1/user/finish/{product_id}'
        response = requests.get(finish_url, headers=self.header)
        try:
            return response.json()
        except Exception as err:
            return 'empty'

    async def cancel_order(self, product_id):
        cancel_url = f'https://5sim.net/v1/user/cancel/{product_id}'
        response = requests.get(cancel_url, headers=self.header)
        try:
            return response.json()
        except Exception as err:
            return 'cancel error'

    def banned(self, product_id):
        banned_url = f'https://5sim.net/v1/user/ban/{product_id}'
        response = requests.get(banned_url, headers=self.header).json()
        return response

    def re_buy(self, product, number):
        re_buy_url = f'https://5sim.net/v1/user/reuse/{product}/{number}'
        response = requests.get(re_buy_url, headers=self.header)
        i = 0
        while response.text == 'no free phones':
            i += 1
            response = requests.get(re_buy_url, headers=self.header)
            if i > 100:
                self.operator = 'any'
            elif i > 200:
                self.country = 'germany'
        try:
            return response.json()
        except Exception as err:
            return 'empty'
