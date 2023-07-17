import asyncio

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from data.config import Config, load_config


class PaymePay:
    config: Config = load_config('../../.env')
    endpoint_url = 'https://checkout.paycom.uz'

    def __init__(self, amount, description):
        self.amount = amount
        self.merchant_id = self.config.payme.merchant_id
        self.account_value = 'Payment for virtual number'
        self.description = description

    async def bill(self):
        data = {
            'merchant': self.merchant_id,
            'amount': self.amount,
            'account[user_id]': self.account_value,
            f'description': self.description
        }
        response = requests.post(url=self.endpoint_url, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')
        response_url = soup.find('meta', property='og:url')['content']
        return response_url

    def check_status_of_payment(self, url, loop):
        options = webdriver.ChromeOptions()
        url_to_check = url
        #options.add_argument('--headless')
        service = Service(executable_path='../../chromedriver/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        try:
            driver.get(url_to_check)
            output = driver.find_element(By.CLASS_NAME, 'mb-2').text
            if output.lower() == 'успешно':
                return True
            return False
        except Exception as err:
            return err
        finally:
            driver.close()
            driver.quit()
