import requests
import json

# URL сервера RPC
url = 'https://checkout.paycom.uz/api'

# Параметры запроса
payload = {
    "method": "CheckTransaction",
    "params": {
        "id": "64a57a07a58caefa2d34b97f"
    }
}

# Отправка запроса
response = requests.post(url, json=payload)

# Проверка статуса ответа
if response.status_code == 200:
    # Парсинг ответа
    result = response.json()
    print('successfuly')
    print(result)
else:
    print('Ошибка выполнения запроса:', response.status_code)
