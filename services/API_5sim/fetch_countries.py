import requests


class ApiRequest:
    url: str = "https://5sim.net/v1/guest/countries"
    header: dict[str:str] = {
        'Accept': 'application/json'
    }
    params = None

    def get_data(self) -> requests.models.Response:
        return requests.get(self.url, headers=self.header, params=self.params)


class FilterData(ApiRequest):

    def __init__(self):
        self.__filtered_data = dict()

    def __call__(self, *args, **kwargs):
        json_data: dict = self.get_data().json()
        for key, value in json_data.items():
            self.__filtered_data[key] = value['text_en']
        return self.__filtered_data
