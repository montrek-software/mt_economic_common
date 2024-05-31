from api_upload.managers.request_manager import RequestManager


class RestCountriesRequestManager(RequestManager):
    base_url = "https://restcountries.com/v3.1/"
