import aiohttp
import requests
from bs4 import BeautifulSoup

from data.config import Config, load_config


async def check_status_of_payment(url):
    m_id = url.split('?')[0].split('/')[-1]
    url_to_req = "https://payme.uz/api/cheque.get"
    payload = {
        "method": "cheque.get",
        "params": {
            "id": m_id
        }
    }
    async with (aiohttp.ClientSession() as session):
        async with session.post(url_to_req, json=payload) as res:
            res = await res.json()
            if 'fiscal' in res['result']['cheque']:
                return True
            return False

    # print('i am here')
    # options = webdriver.ChromeOptions()
    # url_to_check = url
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # service = Service(executable_path='/home/ban_new_update/purchase-number-bot/chromedriver')
    # driver = webdriver.Chrome(service=service, options=options)
    # driver.implicitly_wait(20)
    #
    # try:
    #     driver.get(url_to_check)
    #     output = driver.find_element(By.CLASS_NAME, 'mb-2').text
    #     print(output)
    #     if output.lower() == 'успешно':
    #         return True
    #     return False
    # except Exception as err:
    #     return err
    # finally:
    #     driver.close()
    #     driver.quit()


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
