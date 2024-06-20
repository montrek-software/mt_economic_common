from api_upload.managers.request_manager import RequestJsonManager


class RestCountriesRequestManager(RequestJsonManager):
    base_url = "https://restcountries.com/v3.1/"
