import base64
import requests

# Данные для формирования URL
merchant_id = "%?6Vu4bjJOR#sKd2cNR4GubRarFZBqqXz9v9"
order_id = "197"
amount = "500"

# Формирование параметров и кодирование в base64
params = f"m={merchant_id};ac.order_id={order_id};a={amount}"
encoded_params = base64.b64encode(params.encode()).decode()

# Формирование URL
checkout_url = "https://checkout.paycom.uz"
url = f"{checkout_url}/base64({encoded_params})"

# Отправка GET-запроса
response = requests.get(url)

# Обработка ответа
if response.status_code == 200:
    print("GET-запрос успешно отправлен")
    print(response.text)
    # Дальнейшая обработка полученных данных, если необходимо
else:
    print("Ошибка при отправке GET-запроса")