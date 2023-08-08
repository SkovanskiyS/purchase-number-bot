from bs4 import BeautifulSoup as beauty
# import cloudscraper
#
# url = 'https://5sim.net'
# scraper = cloudscraper.create_scraper()
# info = scraper.get(url).text
#
# with open('index.html','w') as file:
#     file.write(info)
# import cfscrape
#
# scraper = cfscrape.create_scraper()
# scraped_data = scraper.get('https://5sim.net').text

# import requests
# scraped_data = requests.get('https://opensea.io/rankings').text

# import cloudscraper
#
# url = 'https://opensea.io/rankings'
# scraper = cloudscraper.create_scraper()
# scraped_data = scraper.get(url).text

import requests

token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNTQzMDYsImlhdCI6MTY4NjgxODMwNiwicmF5IjoiYWU3OWE0MWY2ZTdmYjc4YTc4Nzc2NGI0YTJjYTkxYzEiLCJzdWIiOjE2OTcwMTJ9.m1kzSqtwFUf7SAQbfWDio2RTf9E8J3GKrH3JUqGcPjBF1euv0ihMwkPOLE7Mr02frMpSrEz3OezBgD0ZDyrrcuhTohi2d9vmYrT7_3jKlA7zjonsb5nHANspkBrs6LkeStnp0Mz5BFHVDMSZ8uGVk-HK7b2oCTZQhFVjmk_edvOJqJaNoLowhpBa2DHqw_pJqoGe9B8a67pJqQ8qxCYD3r1qVvwN9FuLEITZFkW-G0ibXza4fuQjT6-PjtzeGlcU2YVKWmTWcJ-Xe-4ru_V8pc8DSWJwUfrtr0Mo7F4kiZBJJh0tuvzUrL7s6oDUyBLxk-PCPdG171ljwKWVvLDNNQ'

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-type': 'application/json',
}

data = '{"receiver":"123456","method":"qiwi","amount":"10","fee":"unitpay"}'

response = requests.post('https://5sim.net/v1/vendor/withdraw', headers=headers, data=data).text
print(response)