from baseclasses.managers.request_manager import RequestManager


class CountryRequestManager(RequestManager):
    pass


class RestCountriesRequestManager(CountryRequestManager):
    base_url = "https://restcountries.com/v3.1/"

    def get_countries_as_json(self):
        return self.get_json("all")
