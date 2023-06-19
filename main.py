import requests

country = 'usa'
operator = 'any'

headers = {
    'Accept': 'application/json',
}

response = requests.get('https://5sim.net/v1/guest/products/' + country + '/' + operator, headers=headers)
req_result = response.json()
print(req_result['openai']['Price'])
print('smth')
