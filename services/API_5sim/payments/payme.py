import requests
from bs4 import BeautifulSoup
from pathlib import Path

from fake_useragent import FakeUserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#выставляние счета

# url = "https://checkout.paycom.uz"
# data = {
#     'merchant': '',
#     'amount': '1500',
#     'account[user_id]': 'kovanskiy_test'
# }
# response = requests.post(url, data=data)
#
# soup = BeautifulSoup(response.content, 'html.parser')
# response_url = soup.find('meta', property='og:url')['content']
# print(response_url)

#проверка на оплату

userAgent = FakeUserAgent()
options = webdriver.ChromeOptions()
url = 'https://checkout.paycom.uz/64a6f7fbfe92c07aacd1aa1b'
options.add_argument('--headless')
service = Service(executable_path='/home/kovanskiy/PycharmProjects/learningWebScraping/chromedriver/chromedriver')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get(url)
    print(driver.find_element(By.CLASS_NAME,'mb-2').text)
except Exception as err:
    print(err)
finally:
    driver.close()