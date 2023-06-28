import requests


class GetPrice:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs) -> requests.models.Response:
        res = requests.get(self.url).json()
        return res
