import requests


class ApiRequest:
    def __init__(self, url, header, params):
        self.url = url
        self.header = header
        self.params = params

    def get_data(self) -> requests.models.Response:
        return requests.get(self.url, headers=self.header, params=self.params)


class FilterData(ApiRequest):
    def __init__(self, url, header, params):
        super().__init__(url, header, params)
        self.__filtered_data = dict()

    def __call__(self, *args, **kwargs):
        json_data: dict = self.get_data().json()
        for key, value in json_data.items():
            self.__filtered_data[key] = value['text_ru']
        return self.__filtered_data


