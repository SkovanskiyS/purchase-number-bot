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

url = 'https://payme.uz/checkout/64e1ff8c9b78846e951daaf7?back=null&timeout=15000&lang=ru'
print(url)
print(url.split('?')[0].split('/')[-1])