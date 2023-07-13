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

    def purchase_number(self):
        print(self.country)
        buy_url = f'https://5sim.net/v1/user/buy/activation/{self.country}/{self.operator}/{self.product}'
        response = requests.get(buy_url, headers=self.header)
        i = 0
        while response.text == 'no free phones':
            i += 1
            response = requests.get(buy_url, headers=self.header)
            if i > 100:
                self.operator = 'any'
            print(i)
        try:
            print(response.json())
            return response.json()
        except Exception as err:
            return 'empty'

    def get_sms(self, product_id):
        check_url = f'https://5sim.net/v1/user/check/{product_id}'
        response = requests.get(check_url, headers=self.header).json()
        return response

    def finish_order(self, product_id):
        finish_url = f'https://5sim.net/v1/user/finish/{product_id}'
        response = requests.get(finish_url, headers=self.header).json()
        return response

    def cancel_order(self, product_id):
        cancel_url = f'https://5sim.net/v1/user/cancel/{product_id}'
        response = requests.get(cancel_url, headers=self.header).json()
        return response

    def banned(self, product_id):
        banned_url = f'https://5sim.net/v1/user/ban/{product_id}'
        response = requests.get(banned_url, headers=self.header).json()
        return response
