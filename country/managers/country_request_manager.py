from api_upload.managers.request_manager import RequestManager


class CountryRequestManager(RequestManager):
    def get_countries_as_json(self) -> list:
        return []


class RestCountriesRequestManager(CountryRequestManager):
    base_url = "https://restcountries.com/v3.1/"

    def get_countries_as_json(self) -> list:
        return self.get_json("all")
