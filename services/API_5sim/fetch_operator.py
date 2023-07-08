import requests


class GetPrice:
    def __init__(self, country, service):
        self.url = f'https://5sim.net/v1/guest/prices?country={country}&product={service}'

    def __call__(self, *args, **kwargs) -> requests.models.Response:
        try:
            res = requests.get(self.url).json()
            return res
        except Exception as err:
            print(err)