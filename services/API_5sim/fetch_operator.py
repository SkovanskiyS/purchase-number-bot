import requests


class GetPrice:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs) -> requests.models.Response:
        try:
            res = requests.get(self.url).json()
            return res
        except Exception as err:
            print(err)