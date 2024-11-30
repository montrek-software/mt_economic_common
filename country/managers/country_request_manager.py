from api_upload.managers.request_manager import RequestJsonManager


class RestCountriesRequestManager(RequestJsonManager):
    base_url = "https://restcountries.com/v3.1/"
    request_kwargs = {
        "fields": ",".join(
            [
                "name",
                "latlng",
                "continents",
                "capital",
                "postalCode",
                "maps",
                "flags",
                "cca3",
                "cca2",
                "unMember",
                "region",
                "subregion",
                "area",
                "population",
                "currencies",
            ]
        )
    }
